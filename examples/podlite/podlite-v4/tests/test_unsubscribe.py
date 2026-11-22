import sqlite3
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from podlite import database, feeds, service

URL = "https://example.com/rss"
OTHER_URL = "https://example.com/other"
APP = Path(__file__).resolve().parent.parent / "app.py"


def subscribe_two():
    service.subscribe(URL)
    service.subscribe(OTHER_URL)
    return service.list_subscriptions()


def test_unsubscribe_persists_and_keeps_other_subscriptions(monkeypatch):
    first, second = subscribe_two()
    monkeypatch.setattr(feeds, "urlopen", lambda *a, **k: pytest.fail("RSS fetched"))
    service.unsubscribe(first["id"])
    assert service.list_subscriptions() == [second]
    # A fresh connection reads the committed deletion.
    with sqlite3.connect(database.DB_PATH) as connection:
        assert connection.execute("SELECT id FROM subscriptions").fetchall() == [(second["id"],)]


def test_missing_subscription_is_ignored():
    service.subscribe(URL)
    before = service.list_subscriptions()
    service.unsubscribe(999)
    assert service.list_subscriptions() == before


def test_delete_uses_parameters():
    subscribe_two()
    before = service.list_subscriptions()
    database.unsubscribe("1 OR 1=1")
    assert service.list_subscriptions() == before


@pytest.mark.parametrize("error", [sqlite3.OperationalError("locked"), OSError("disk error")])
def test_storage_errors_keep_subscription(monkeypatch, error):
    service.subscribe(URL)
    before = service.list_subscriptions()
    def fail(podcast_id):
        raise error
    monkeypatch.setattr(database, "unsubscribe", fail)
    with pytest.raises(service.SubscriptionError, match="Could not unsubscribe"):
        service.unsubscribe(before[0]["id"])
    assert service.list_subscriptions() == before


def test_confirmation_cancel_and_last_subscription():
    service.subscribe(URL)
    app = AppTest.from_file(str(APP)).run()
    app.button(key="unsubscribe_1").click().run()
    assert not app.exception
    assert any(item.value == "Unsubscribe from Sample Podcast?" for item in app.markdown)
    assert len(service.list_subscriptions()) == 1
    app.button(key="cancel_1").click().run()
    assert not app.exception
    assert len(service.list_subscriptions()) == 1
    assert not any(button.label == "Confirm" for button in app.button)
    app.button(key="unsubscribe_1").click().run()
    app.button(key="confirm_1").click().run()
    assert not app.exception
    assert service.list_subscriptions() == []
    assert "Add a podcast" in app.info[0].value
    assert "pending_unsubscribe" not in app.session_state
    reloaded = AppTest.from_file(str(APP)).run()
    assert not reloaded.exception
    assert "Add a podcast" in reloaded.info[0].value


def test_only_selected_podcast_is_unsubscribed():
    first, second = subscribe_two()
    app = AppTest.from_file(str(APP)).run()
    app.button(key=f'unsubscribe_{second["id"]}').click().run()
    app.button(key=f'confirm_{second["id"]}').click().run()
    assert not app.exception
    assert service.list_subscriptions() == [first]
    assert len(app.subheader) == 1
    assert app.button(key=f'episodes_{first["id"]}')


def test_subscription_disappears_while_confirmation_is_open():
    service.subscribe(URL)
    app = AppTest.from_file(str(APP)).run()
    app.button(key="unsubscribe_1").click().run()
    database.unsubscribe(1)
    app.button(key="confirm_1").click().run()
    assert not app.exception
    assert "Add a podcast" in app.info[0].value
    assert "pending_unsubscribe" not in app.session_state


def test_failed_delete_keeps_card_and_allows_retry():
    service.subscribe(URL)
    with database._connect() as connection:
        connection.execute("""CREATE TRIGGER block_unsubscribe
            BEFORE DELETE ON subscriptions
            BEGIN SELECT RAISE(ABORT, 'delete failed'); END""")
    app = AppTest.from_file(str(APP)).run()
    app.button(key="unsubscribe_1").click().run()
    app.button(key="confirm_1").click().run()
    assert not app.exception
    assert app.error[0].value == "Could not unsubscribe from this podcast."
    assert app.subheader[0].value == "Sample Podcast"
    assert len(service.list_subscriptions()) == 1
    assert app.session_state.pending_unsubscribe == 1
    with database._connect() as connection:
        connection.execute("DROP TRIGGER block_unsubscribe")
    app.button(key="confirm_1").click().run()
    assert not app.exception
    assert not app.error
    assert service.list_subscriptions() == []

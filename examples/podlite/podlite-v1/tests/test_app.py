from pathlib import Path

from streamlit.testing.v1 import AppTest

from podlite import feeds, service

APP = Path(__file__).resolve().parent.parent / "app.py"


def test_empty_list_and_invalid_input():
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert "Add a podcast" in app.info[0].value
    app.button[0].click().run()
    assert not app.exception
    assert "valid HTTP" in app.error[0].value
    assert not app.success


def test_subscription_form_and_reload():
    app = AppTest.from_file(str(APP)).run()
    app.text_input[0].set_value("https://example.com/rss")
    app.button[0].click().run()
    assert not app.exception
    assert app.success[0].value == "Subscribed to Sample Podcast."
    assert app.subheader[0].value == "Sample Podcast"
    assert app.text[0].value == "Hello listeners & friends."
    assert not app.info
    reloaded = AppTest.from_file(str(APP)).run()
    assert not reloaded.exception
    assert reloaded.subheader[0].value == "Sample Podcast"
    app.button[0].click().run()
    assert "already subscribed" in app.error[0].value
    assert not app.success


def test_missing_metadata_and_broken_image(monkeypatch):
    monkeypatch.setattr(feeds, "fetch_podcast", lambda url: {
        "title": "No metadata", "cover_url": "https://example.com/broken",
        "description": None,
    })
    monkeypatch.setattr(service, "get_cover", lambda url: b"not an image")
    service.subscribe("https://example.com/rss")
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert app.text[0].value == "No description available"
    assert app.get("image")[0].proto.imgs[0].url.startswith(
        "data:image/svg+xml;base64,"
    )


def test_read_failure_is_not_an_empty_state(monkeypatch):
    def fail():
        raise service.SubscriptionError("Could not load subscriptions.")
    monkeypatch.setattr(service, "list_subscriptions", fail)
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert "Could not load" in app.error[0].value
    assert not app.info

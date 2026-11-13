import io
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import URLError

import pytest
from streamlit.testing.v1 import AppTest

from podlite import feeds, service, storage

APP = Path(__file__).resolve().parent.parent / "app.py"
URL = "https://example.com/feed.xml"
OTHER_URL = "https://example.com/other.xml"


def rss(items=""):
    return (
        '<rss version="2.0"><channel><title>Podcast</title>'
        + items + '</channel></rss>'
    ).encode()


def item(title, date="", description=""):
    return (
        f"<item><title>{title}</title><pubDate>{date}</pubDate>"
        f"<description><![CDATA[{description}]]></description></item>"
    )


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "podlite.db"
    monkeypatch.setattr(storage, "DEFAULT_DB_PATH", path)
    return path


@pytest.fixture
def http(monkeypatch):
    responses = {}
    calls = []

    def fetch(request, timeout):
        calls.append(request.full_url)
        result = responses[request.full_url]
        if isinstance(result, Exception):
            raise result
        return io.BytesIO(result)

    monkeypatch.setattr(feeds.urllib.request, "urlopen", fetch)
    return responses, calls


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Mon, 02 Nov 2026 10:00:00 -0300", datetime(2026, 11, 2, 13, tzinfo=UTC)),
        ("02 Nov 2026 10:00:00", datetime(2026, 11, 2, 10, tzinfo=UTC)),
        ("", None),
        ("not a date", None),
        ("32 Nov 2026 10:00:00 GMT", None),
    ],
)
def test_publication_dates(value, expected):
    assert feeds.publication_date(value) == expected


def test_episode_metadata_and_sorting(database, http):
    responses, _ = http
    storage.save_subscription(URL, "Podcast", database)
    responses[URL] = rss(
        item("Undated", "bad")
        + item("Older", "01 Nov 2026 10:00:00 GMT", "<p>News &amp; ideas.</p>")
        + item("First tie", "02 Nov 2026 10:00:00 GMT")
        + item("Second tie", "02 Nov 2026 07:00:00 -0300")
        + "<item/>"
    )
    episodes = service.list_episodes(1, database)
    assert [episode["title"] for episode in episodes] == [
        "First tie", "Second tie", "Older", "Undated", "Untitled episode"
    ]
    assert episodes[2]["description"] == "News & ideas."
    assert episodes[-1]["description"] == "No description available"
    assert episodes[-1]["published_at"] is None


def test_pagination_and_switching(database, http):
    responses, calls = http
    storage.save_subscription(URL, "First", database)
    storage.save_subscription(OTHER_URL, "Second", database)
    responses[URL] = rss("".join(
        item(f"Episode {i}", f"{i:02} Nov 2026 10:00:00 GMT")
        for i in range(1, 24)
    ))
    responses[OTHER_URL] = rss(item("Other episode"))
    app = AppTest.from_file(APP).run()
    assert not calls
    app.button(key="see_episodes_1").click().run()
    assert not app.exception
    assert not app.text_input
    assert not any(button.label == "See Episodes" for button in app.button)
    assert any(heading.value == "First" for heading in app.subheader)
    assert len(app.get("image")) == 11
    assert len(app.caption) == 10
    assert any(text.value == "Episode 23" for text in app.markdown)
    app.button[-1].click().run()
    assert len(app.caption) == 20
    app.button[-1].click().run()
    assert len(app.caption) == 23
    assert not any(button.label == "Load more" for button in app.button)
    assert calls == [URL]

    app.button(key="back_to_podcasts").click().run()
    assert app.text_input
    assert not app.caption
    assert service.list_podcasts(database)[0]["title"] == "First"
    app.button(key="see_episodes_1").click().run()
    assert len(app.caption) == 10
    assert calls == [URL, URL]
    app.button(key="back_to_podcasts").click().run()
    app.button(key="see_episodes_2").click().run()
    assert not app.exception
    assert len(app.caption) == 1
    assert app.caption[0].value == "Date unavailable"
    assert not any(text.value.startswith("Episode ") for text in app.markdown)
    app.button(key="back_to_podcasts").click().run()
    app.button(key="see_episodes_1").click().run()
    assert len(app.caption) == 10
    assert calls == [URL, URL, OTHER_URL, URL]


@pytest.mark.parametrize("response", [b"broken xml", URLError("offline")])
def test_feed_error_clears_previous_list_and_preserves_subscriptions(database, http, response):
    responses, _ = http
    storage.save_subscription(URL, "First", database)
    storage.save_subscription(OTHER_URL, "Second", database)
    responses[URL] = rss(item("Visible episode"))
    responses[OTHER_URL] = response
    before = service.list_podcasts(database)
    app = AppTest.from_file(APP).run()
    app.button(key="see_episodes_1").click().run()
    assert len(app.caption) == 1
    app.button(key="back_to_podcasts").click().run()
    app.button(key="see_episodes_2").click().run()
    assert not app.exception
    assert app.error
    assert not app.caption
    assert not any(text.value == "Visible episode" for text in app.markdown)
    assert not any(button.label == "Load more" for button in app.button)
    assert service.list_podcasts(database) == before
    app.button(key="back_to_podcasts").click().run()
    assert not app.exception
    assert app.text_input
    assert not app.error


def test_empty_feed_and_missing_metadata(database, http):
    responses, _ = http
    storage.save_subscription(URL, "Podcast", database)
    responses[URL] = rss()
    app = AppTest.from_file(APP).run()
    app.button(key="see_episodes_1").click().run()
    assert not app.exception
    assert app.info[0].value == "No episodes available"
    assert "svg" in app.get("image")[0].proto.imgs[0].url
    assert not any(button.label == "Load more" for button in app.button)
    app.button(key="back_to_podcasts").click().run()
    assert app.text_input

    responses[URL] = rss("<item><title> </title><description> </description></item>")
    app = AppTest.from_file(APP).run()
    app.button(key="see_episodes_1").click().run()
    assert not app.exception
    assert any(text.value == "Untitled episode" for text in app.markdown)
    assert app.caption[0].value == "Date unavailable"
    assert any(text.value == "No description available" for text in app.text)


def test_no_subscriptions(database):
    app = AppTest.from_file(APP).run()
    assert not app.exception
    assert "Add one" in app.info[0].value
    assert not app.selectbox


def test_unknown_subscription(database):
    with pytest.raises(service.PodcastError, match="Podcast not found"):
        service.list_episodes(999, database)


@pytest.mark.parametrize(
    "artwork, expected",
    [
        ('<itunes:image xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
         'href="/episode.jpg"/>', "https://example.com/episode.jpg"),
        ('<image><url>https://example.com/rss-cover.jpg</url></image>',
         "https://example.com/rss-cover.jpg"),
        ('<itunes:image xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
         'href="https://["/>', None),
        ("", None),
    ],
)
def test_episode_artwork(artwork, expected, http):
    responses, _ = http
    responses[URL] = rss(f"<item><title>Episode</title>{artwork}</item>")
    assert feeds.fetch_episodes(URL)[0]["image_url"] == expected


@pytest.mark.parametrize("podcast_cover", [None, "https://example.com/podcast.jpg"])
def test_episode_cards_with_descriptions_and_cover_fallback(database, http, podcast_cover):
    responses, _ = http
    storage.save_subscription(URL, "Podcast", database, image_url=podcast_cover)
    responses[URL] = rss(
        '<item><title>Own cover</title>'
        '<itunes:image xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
        'href="https://example.com/episode.jpg"/>'
        '<description><![CDATA[<p>Episode <b>description</b>.</p>]]></description></item>'
        '<item><title>Inherited cover</title></item>'
    )
    app = AppTest.from_file(APP).run()
    app.button(key="see_episodes_1").click().run()
    assert not app.exception
    images = [image.proto.imgs[0].url for image in app.get("image")]
    assert len(images) == 3
    assert images[1] == "https://example.com/episode.jpg"
    if podcast_cover:
        assert images[2] == podcast_cover
    else:
        assert "svg" in images[2]
    assert [text.value for text in app.text] == [
        "Episode description.", "No description available"
    ]

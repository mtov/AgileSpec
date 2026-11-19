import base64
from io import BytesIO

import pytest

from podlite import database, feeds

RSS = b"""<rss version="2.0"
 xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
 <channel><title>Sample Podcast</title>
 <description><![CDATA[<p>Hello <b>listeners</b> &amp; friends.</p>]]></description>
 <itunes:image href="https://example.com/cover.png"/>
 </channel></rss>"""
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII="
)


@pytest.fixture(autouse=True)
def isolated_storage_and_network(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "data" / "podlite.db")

    def open_request(request, timeout):
        assert timeout == 10
        if request.full_url.endswith("cover.png"):
            return BytesIO(PNG)
        return BytesIO(RSS)

    monkeypatch.setattr(feeds, "urlopen", open_request)

"""Fetch and verify same-origin URLs from the published XML sitemap.

This is a discovery allowlist, not proof that a page is indexable or relevant.
"""

from dataclasses import dataclass
from urllib.parse import urlsplit
from urllib.request import urlopen
import xml.etree.ElementTree as ET


class SitemapError(RuntimeError):
    pass


@dataclass(frozen=True)
class URLRegistry:
    origin: str
    urls: frozenset[str]

    def contains(self, url: str) -> bool:
        p = urlsplit(url)
        return p.scheme == "https" and p.netloc.lower() == self.origin and url in self.urls


def fetch_registry(sitemap_url: str, *, max_documents: int = 10,
                   max_urls: int = 10000) -> URLRegistry:
    root_url = urlsplit(sitemap_url)
    if root_url.scheme != "https" or not root_url.hostname:
        raise SitemapError("Sitemap must use HTTPS with a hostname")
    origin = root_url.netloc.lower()
    pending = [sitemap_url]
    seen = set()
    urls = set()
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        if len(seen) >= max_documents:
            raise SitemapError("Sitemap document limit exceeded")
        p = urlsplit(current)
        if p.scheme != "https" or p.netloc.lower() != origin:
            raise SitemapError("Cross-origin sitemap rejected")
        seen.add(current)
        try:
            with urlopen(current, timeout=15) as response:
                if response.geturl() != current:
                    raise SitemapError("Sitemap redirect requires explicit verification")
                xml = response.read(5_000_001)
                if len(xml) > 5_000_000:
                    raise SitemapError("Sitemap too large")
        except OSError as exc:
            raise SitemapError("Could not fetch sitemap") from exc
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as exc:
            raise SitemapError("Invalid sitemap XML") from exc
        tag = root.tag.rsplit("}", 1)[-1]
        if tag not in ("urlset", "sitemapindex"):
            raise SitemapError("Unexpected sitemap root")
        for loc in root.iter():
            if loc.tag.rsplit("}", 1)[-1] != "loc" or not loc.text:
                continue
            url = loc.text.strip()
            parts = urlsplit(url)
            if parts.scheme != "https" or parts.netloc.lower() != origin:
                raise SitemapError("Cross-origin URL in sitemap")
            if tag == "sitemapindex":
                pending.append(url)
            else:
                urls.add(url)
                if len(urls) > max_urls:
                    raise SitemapError("URL limit exceeded")
    if not urls:
        raise SitemapError("No URLs found")
    return URLRegistry(origin, frozenset(urls))

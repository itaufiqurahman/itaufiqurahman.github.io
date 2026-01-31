#!/usr/bin/env python3
"""
build_sitemap.py — generator untuk sitemap.xml dan robots.txt (GitHub Pages)

Cara pakai:
  python tools/build_sitemap.py
Environment:
  SITE_URL (default: https://itaufiqurahman.github.io)
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import os, re

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = os.getenv("SITE_URL", "https://itaufiqurahman.github.io").rstrip("/")

# Halaman statis utama (sesuaikan jika kamu tambah halaman baru)
STATIC_PATHS = [
    "index.html",
    "tentang.html",
    "contact.html",
    "search.html",
    "catatan/index.html",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def to_url(path: str) -> str:
    if path.endswith("index.html"):
        # /catatan/index.html -> /catatan/
        return f"{SITE_URL}/" + path.replace("index.html", "")
    return f"{SITE_URL}/" + path

def find_html_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted([p for p in folder.glob("*.html") if p.is_file()])

def collect_urls() -> list[str]:
    urls: list[str] = []
    for p in STATIC_PATHS:
        if (ROOT / p).exists():
            urls.append(to_url(p))
    # Artikel
    for p in find_html_files(ROOT / "artikel"):
        urls.append(to_url(f"artikel/{p.name}"))
    return sorted(set(urls))

def write_sitemap(urls: list[str]) -> None:
    lastmod = iso_now()
    items = []
    for u in urls:
        items.append(f"""  <url>
    <loc>{u}</loc>
    <lastmod>{lastmod}</lastmod>
  </url>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(items)}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")

def write_robots() -> None:
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")

def main() -> None:
    urls = collect_urls()
    write_sitemap(urls)
    write_robots()
    print(f"Generated sitemap.xml with {len(urls)} URLs and robots.txt")

if __name__ == "__main__":
    main()

## Auto-sync posts.json, search-index, dan sitemap

Setiap kali kamu menambah/mengubah file di `artikel/*.html`, jalankan:

- `python tools/build_posts.py --also-search-index`
- `python tools/build_sitemap.py`

Repo ini juga sudah disiapkan **GitHub Actions** (`.github/workflows/build.yml`) untuk:
- rebuild `assets/posts.json`
- rebuild `assets/search-index.json`
- rebuild `sitemap.xml` dan `robots.txt`

Target URL (untuk sitemap/robots) memakai:
- `https://itaufiqurahman.github.io`

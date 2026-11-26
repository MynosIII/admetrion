# Admetrion website

Static site for admetrion.com (Amazon seller services by Matías Gaglio). Deployed on Vercel from `main`.

- `src/page.html` is the editable source (page body, styles and scripts).
- `src/es_strings.py` holds the Spanish copy as (English, Spanish) pairs applied to `page.html`.
- `python3 src/build.py` regenerates `index.html` (English), `es/index.html` (Spanish), both privacy pages and `sitemap.xml`. If you change English copy, update the matching pair; the build stops and lists any pair whose English text no longer exists.
- The contact form posts to FormSubmit (admetrion@gmail.com).

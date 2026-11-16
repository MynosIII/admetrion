# Admetrion website

Static site for admetrion.com (Amazon seller services by Matías Gaglio). Deployed on Vercel from `main`.

- `src/page.html` is the editable source (page body, styles and scripts).
- `python3 src/build.py` regenerates `index.html` and `privacy.html` from it.
- The contact form posts to FormSubmit (admetrion@gmail.com).

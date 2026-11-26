# Build the deployable site from src/page.html (an HTML fragment, also used for the Artifact preview).
#   index.html          English (default)
#   es/index.html       Spanish, from src/es_strings.py applied to the English page
#   privacy.html, es/privacy.html, sitemap.xml, robots.txt
# Run: python3 src/build.py
import os, re, sys
SRC = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(SRC) + '/'
sys.path.insert(0, SRC)
from es_strings import PAIRS

SITE = 'https://admetrion.com'
ENDPOINT = 'https://formsubmit.co/ajax/admetrion@gmail.com'
page = open(W + 'src/page.html').read()

HREFLANG = ('<link rel="alternate" hreflang="en" href="%s/">\n'
            '<link rel="alternate" hreflang="es" href="%s/es/">\n'
            '<link rel="alternate" hreflang="x-default" href="%s/">\n') % (SITE, SITE, SITE)

def head(lang):
    return ('<!doctype html>\n<html lang="%s" data-theme="dark">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n') % lang

def wrap(s, lang, switch):
    s = s.replace('<link rel="canonical"', HREFLANG + '<meta property="og:locale" content="%s">\n<link rel="canonical"' % ('es_419' if lang == 'es' else 'en_US'), 1)
    # language switch, just before the CTA in the top bar
    s = s.replace('      <a class="cta" href="#contact">', '      ' + switch + '\n      <a class="cta" href="#contact">', 1)
    s = s.replace('data-endpoint=""', 'data-endpoint="%s"' % ENDPOINT)
    i = s.index('<header')
    return head(lang) + s[:i] + '</head>\n<body>\n' + s[i:] + '</body>\n</html>\n'

# ---------- English
en = wrap(page, 'en', '<a class="lang" href="/es/" hreflang="es" lang="es" title="Ver en español">ES</a>')
open(W + 'index.html', 'w').write(en)

# ---------- Spanish
es = page
missing = [a for a, b in PAIRS if a not in es]
if missing:
    sys.exit('es_strings.py is out of date. These English strings are no longer in page.html:\n- ' + '\n- '.join(m[:120] for m in missing))
for a, b in PAIRS:
    es = es.replace(a, b)
# es/ lives one folder down: point shared files at the root
es = es.replace('src="images/', 'src="/images/').replace("'js/three.min.js'", "'/js/three.min.js'").replace('href="privacy.html"', 'href="/es/privacy.html"')
es = wrap(es, 'es', '<a class="lang" href="/" hreflang="en" lang="en" title="View in English">EN</a>')
os.makedirs(W + 'es', exist_ok=True)
open(W + 'es/index.html', 'w').write(es)

# ---------- Privacy pages
style = page[page.index('<style>'):page.index('</style>') + 8]
fav = re.search(r'<link rel="icon"[^>]*>', page).group(0)
fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">\n'
mark = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="6" y="34" width="13" height="24" fill="#86f5a8"/><rect x="25" y="20" width="13" height="38" fill="#86f5a8"/><rect x="44" y="6" width="13" height="52" fill="#86f5a8"/></svg>'

PRIV = {
 'en': dict(home='/', title='Privacy policy', nav=('Home', 'Free mini-audit'), sw=('/es/privacy.html', 'es', 'ES'),
   updated='Last updated: November 26, 2026', foot='Not affiliated with Amazon.', body='''
<p>This site belongs to Admetrion, run by Matías Gaglio (Argentina). Contact: admetrion@gmail.com.</p>
<h2>What I collect</h2>
<p>Only what you type into the mini-audit form: your name, email, ASIN or product link, marketplace and your message. The site has no tracking cookies and no analytics.</p>
<h2>How I use it</h2>
<p>To reply to your request and prepare your mini-audit. I do not sell your data or add you to a mailing list.</p>
<h2>Who processes it</h2>
<p>Form messages are delivered to my inbox through FormSubmit (formsubmit.co) and stored in Gmail (Google). The page fonts load from Google Fonts.</p>
<h2>How long I keep it</h2>
<p>As long as we are in conversation or working together, and up to 12 months after the last contact. Ask me any time and I will delete it.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete your data by writing to admetrion@gmail.com.</p>'''),
 'es': dict(home='/es/', title='Política de privacidad', nav=('Inicio', 'Mini auditoría gratis'), sw=('/privacy.html', 'en', 'EN'),
   updated='Última actualización: 26 de noviembre de 2026', foot='Sin relación con Amazon.', body='''
<p>Este sitio pertenece a Admetrion, a cargo de Matías Gaglio (Argentina). Contacto: admetrion@gmail.com.</p>
<h2>Qué datos recopilo</h2>
<p>Solo lo que escribes en el formulario de mini auditoría: tu nombre, correo, ASIN o link del producto, mercado y tu mensaje. El sitio no usa cookies de seguimiento ni analítica.</p>
<h2>Para qué los uso</h2>
<p>Para responder tu pedido y preparar tu mini auditoría. No vendo tus datos ni te sumo a ninguna lista de correo.</p>
<h2>Quién los procesa</h2>
<p>Los mensajes del formulario llegan a mi correo a través de FormSubmit (formsubmit.co) y se guardan en Gmail (Google). Las fuentes de la página se cargan desde Google Fonts.</p>
<h2>Cuánto tiempo los guardo</h2>
<p>Mientras estemos en contacto o trabajando juntos, y hasta 12 meses después del último contacto. Pídemelo cuando quieras y los borro.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir ver, corregir o borrar tus datos escribiendo a admetrion@gmail.com.</p>'''),
}
for lang, d in PRIV.items():
    path = 'privacy.html' if lang == 'en' else 'es/privacy.html'
    out = (head(lang) + '<title>%s · Admetrion</title>\n' % d['title'] + fav + '\n' + fonts + style + (
      '\n</head>\n<body>\n<header class="bar"><div class="wrap"><a class="brand" href="%s">%sADMETRION</a>'
      '<nav class="nav" aria-label="Main"><a href="%s">%s</a><a class="lang" href="%s" hreflang="%s" lang="%s">%s</a>'
      '<a class="cta" href="%s#contact">%s</a></nav></div></header>\n'
      '<main class="wrap doc">\n<h1 style="font-size:2rem">%s</h1>\n<p class="note">%s</p>%s\n</main>\n'
      '<footer><div class="wrap meta"><span>Admetrion &middot; Matías Gaglio &middot; Argentina</span><span>%s</span></div></footer>\n</body>\n</html>\n'
      ) % (d['home'], mark, d['home'], d['nav'][0], d['sw'][0], d['sw'][1], d['sw'][1], d['sw'][2], d['home'], d['nav'][1],
           d['title'], d['updated'], d['body'], d['foot']))
    open(W + path, 'w').write(out)

# ---------- Sitemap and robots
def url(loc, en_href, es_href):
    return ('<url><loc>%s</loc>'
            '<xhtml:link rel="alternate" hreflang="en" href="%s"/>'
            '<xhtml:link rel="alternate" hreflang="es" href="%s"/>'
            '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/></url>\n') % (loc, en_href, es_href, en_href)
home_en, home_es, pr_en, pr_es = SITE + '/', SITE + '/es/', SITE + '/privacy', SITE + '/es/privacy'
open(W + 'sitemap.xml', 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + url(home_en, home_en, home_es) + url(home_es, home_en, home_es)
    + url(pr_en, pr_en, pr_es) + url(pr_es, pr_en, pr_es) + '</urlset>\n')
open(W + 'robots.txt', 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
print('built: index.html, es/index.html, privacy.html, es/privacy.html, sitemap.xml')

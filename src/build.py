# Build deployable files from src/page.html (artifact fragment) -> index.html, plus privacy.html
import re
import os; W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
s=open(W+'src/page.html').read()
head='<!doctype html>\n<html lang="en" data-theme="dark">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
i=s.index('<header')
full=head+s[:i]+'</head>\n<body>\n'+s[i:]+'</body>\n</html>\n'
full=full.replace('data-endpoint=""','data-endpoint="https://formsubmit.co/ajax/admetrion@gmail.com"')
open(W+'index.html','w').write(full)

style=s[s.index('<style>'):s.index('</style>')+8]
fav=re.search(r'<link rel="icon"[^>]*>',s).group(0)
priv=head+'<title>Privacy policy · Admetrion</title>\n'+fav+'''
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
'''+style+'''
</head>
<body>
<header class="bar"><div class="wrap"><a class="brand" href="index.html"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 48 L24 30 L34 38 L56 14" stroke="#ffb000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="56" cy="14" r="5" fill="#ffb000"/></svg>ADMETRION</a><nav class="nav" aria-label="Main"><a href="index.html">Home</a><a class="cta" href="index.html#contact">Free mini-audit</a></nav></div></header>
<main class="wrap doc">
<p class="label">Privacy</p>
<h1 style="font-size:2rem">Privacy policy</h1>
<p class="note">Last updated: November 17, 2026</p>
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
<p>You can ask to see, correct or delete your data by writing to admetrion@gmail.com.</p>
</main>
<footer><div class="wrap"><span>Admetrion &middot; Matías Gaglio &middot; Argentina</span><span>Not affiliated with Amazon.</span></div></footer>
</body>
</html>
'''
open(W+'privacy.html','w').write(priv)
open(W+'robots.txt','w').write('User-agent: *\nAllow: /\n')
print('built')

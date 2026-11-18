import email, sys, os, re
from email import policy

src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
m = email.message_from_bytes(open(src,'rb').read(), policy=policy.default)
subj = m['subject'] or ''
html = None
for part in m.walk():
    if part.get_content_type() == 'text/html':
        html = part.get_content()
print(f'{os.path.basename(src)}')
print(f'  Konu   : {subj}')
print(f'  Gonderen: {m["from"]}')
print(f'  HTML   : {"var, "+str(len(html))+" karakter" if html else "YOK"}')
if html:
    name = os.path.basename(src).split("-",1)[1].replace(".eml","")
    open(os.path.join(outdir, name + ".html"), "w", encoding="utf-8").write(html)
    print(f'  -> {name}.html')

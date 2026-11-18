import email, sys, os, re
from email import policy

src, outdir = sys.argv[1], sys.argv[2]
name = os.path.basename(src).split('-',1)[1].replace('.eml','')
d = os.path.join(outdir, name); os.makedirs(d, exist_ok=True)
m = email.message_from_bytes(open(src,'rb').read(), policy=policy.default)

html=None; saved={}
for part in m.walk():
    ct = part.get_content_type()
    if ct=='text/html' and html is None:
        html = part.get_content()
    elif part.get_content_maintype()=='image':
        cid = (part.get('Content-ID') or '').strip('<>')
        data = part.get_payload(decode=True)
        if not cid or not data: continue
        ext = ct.split('/')[-1].replace('jpeg','jpg')
        fn = re.sub(r'[^A-Za-z0-9._-]','_',cid)+'.'+ext
        open(os.path.join(d,fn),'wb').write(data)
        saved[cid]=fn

for cid,fn in saved.items():
    html = html.replace('cid:'+cid, fn)
open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(html)
print(f'{name}: {len(saved)} gomulu gorsel -> {d}/index.html')

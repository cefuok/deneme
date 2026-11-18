import re, sys, os, html as H
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
print(os.path.basename(sys.argv[1]))
for m in re.finditer(r'<img\b[^>]*>', s, re.I):
    tag=m.group(0)
    w=re.search(r'width="?(\d+)',tag); h=re.search(r'height="?(\d+)',tag)
    src=re.search(r'src="([^"]+)"',tag); alt=re.search(r'alt="([^"]*)"',tag)
    a=H.unescape(alt.group(1)) if alt else ''
    a=' '.join(a.split())
    kind='GOMULU(cid)' if src and src.group(1).startswith('cid:') else 'URL'
    print(f'  {w.group(1) if w else "?":>4}x{h.group(1) if h else "?":<4} {kind:12s} alt="{a[:70]}"')

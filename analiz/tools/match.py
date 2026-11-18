import re, sys, os, html as H, difflib, glob

def text(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S|re.I)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = H.unescape(s)
    s = re.sub(r'[^0-9A-Za-zÇĞİÖŞÜçğıöşü]+', ' ', s)
    return ' '.join(s.split()).lower()

orig = {os.path.basename(p): text(p) for p in sorted(glob.glob(sys.argv[1]+'/tt-*.html'))}
for p in sorted(glob.glob(sys.argv[2]+'/*.html')):
    t = text(p)
    scores = sorted(((difflib.SequenceMatcher(None, t, o).ratio(), n) for n,o in orig.items()), reverse=True)
    name = os.path.basename(p)
    print(f'{name[:52]:54s}')
    for sc,n in scores[:3]:
        print(f'      {sc*100:5.1f}%  {n}')

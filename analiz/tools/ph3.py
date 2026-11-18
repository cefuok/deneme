import re, sys, os, json, urllib.parse
src, dst, sizes = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
os.makedirs(os.path.dirname(dst), exist_ok=True)
s = open(src, encoding='utf-8', errors='replace').read()
def fix(m):
    t = m.group(0)
    u = re.search(r'src="(https?://[^"]+)"', t)
    if not u: return t
    base = os.path.basename(u.group(1))
    wh = sizes.get(base) or sizes.get(urllib.parse.unquote(base))
    t = re.sub(r'src="https?://[^"]+"', 'src="ph.png"', t)
    if wh:
        w,h = wh
        # her iki olcuyu da acikca yaz, 'height:auto' varsa gercek degeriyle degistir
        t = re.sub(r'\swidth="?\d+"?', f' width="{w}"', t, count=1)
        t = re.sub(r'\sheight="?\d+"?', '', t)
        t = t[:-1] + f' height="{h}">' if t.endswith('>') else t
        t = re.sub(r'height\s*:\s*auto', f'height:{h}px', t)
        t = re.sub(r'width\s*:\s*\d+px', f'width:{w}px', t)
    return t
s = re.sub(r'<img\b[^>]*>', fix, s)
s = re.sub(r'src="https?://[^"]+"', 'src="ph.png"', s)
open(dst,'w',encoding='utf-8').write(s)

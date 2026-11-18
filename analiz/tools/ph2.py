import re, sys, os, json, glob
# 1) Gelen maillerden URL -> gercek (genislik, yukseklik) haritasi cikar
size = {}
for f in glob.glob(sys.argv[1]+'/*.html') + glob.glob(sys.argv[2]+'/*.html'):
    s = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'<img\b[^>]*>', s, re.I):
        t = m.group(0)
        u = re.search(r'src="(https?://[^"]+)"', t)
        w = re.search(r'width="?(\d+)', t); h = re.search(r'height="?(\d+)', t)
        if u and w and h:
            size[os.path.basename(u.group(1))] = (int(w.group(1)), int(h.group(1)))
json.dump(size, open(sys.argv[3],'w'))
print(f'{len(size)} gorselin gercek olcusu bulundu')
for k,v in sorted(size.items()): print('   ',k,v)

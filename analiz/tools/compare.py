import re, sys, os, html as H

NAMED = {'white':'#ffffff','black':'#000000','blue':'#0000ff','red':'#ff0000',
         'purple':'#800080','navy':'#000080','gray':'#808080','grey':'#808080'}

def norm_color(c):
    c = c.strip().lower()
    if c in NAMED: return NAMED[c]
    if re.fullmatch(r'#[0-9a-f]{6}', c): return c
    if re.fullmatch(r'#[0-9a-f]{3}', c): return '#'+''.join(ch*2 for ch in c[1:])
    m = re.fullmatch(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', c)
    if m: return '#%02x%02x%02x' % tuple(int(g) for g in m.groups())
    return c

def plain(frag):
    frag = re.sub(r'<!--.*?-->', ' ', frag, flags=re.S)
    frag = re.sub(r'<[^>]+>', ' ', frag)
    frag = H.unescape(frag)
    frag = re.sub(r'[^0-9A-Za-zÇĞİÖŞÜçğıöşü]+', ' ', frag)
    return ' '.join(frag.split()).lower()

def colored_runs(path):
    """{normalize edilmis metin: renk} -- renk tasiyan her elemanin ic metni"""
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S|re.I)
    out = {}
    # renk tasiyan acilis etiketi + kapanisina kadar olan ham parca
    for m in re.finditer(r'<(span|td|p|font|strong|b|a)\b[^>]*?(?<![-a-zA-Z])color\s*[:=]\s*"?([#\w(),\s]+?)[";\s][^>]*>', s, re.I):
        tag, col = m.group(1).lower(), norm_color(m.group(2))
        if not col.startswith('#'): continue
        rest = s[m.end():]
        close = re.search(r'</'+tag+r'>', rest, re.I)
        frag = rest[:close.start()] if close else rest[:400]
        t = plain(frag)
        if 3 <= len(t) <= 120:
            out.setdefault(t, col)
    return out

def stats(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    body = s[s.find('<body'):]
    return {
      'bullet_dot'   : body.count('●') + body.count('&#9679;') + len(re.findall(r'bgcolor="#2[0-9a-fA-F]dfe7"', body)),
      'img'          : len(re.findall(r'<img\b', body, re.I)),
      'table'        : len(re.findall(r'<table\b', body, re.I)),
      'empty_para'   : len(re.findall(r'<p class=?"?MsoNormal"?[^>]*>\s*(?:<[^>]+>\s*)*(?:&nbsp;|<o:p>&nbsp;</o:p>)\s*(?:</[^>]+>\s*)*</p>', body, re.I)),
      'mso_cond'     : len(re.findall(r'<!--\[if', body)),
      'vml'          : len(re.findall(r'v:(roundrect|rect|shape)\b', body)),
    }

orig, recv = sys.argv[1], sys.argv[2]
co, cr = colored_runs(orig), colored_runs(recv)
so, sr = stats(orig), stats(recv)

print(f'ORIJINAL : {os.path.basename(orig)}')
print(f'GELEN    : {os.path.basename(recv)}')
print()
print(f'{"olcut":16s} {"orijinal":>10s} {"gelen":>10s}')
for k in so:
    flag = '' if so[k]==sr[k] else '   <-- FARK'
    print(f'{k:16s} {so[k]:>10d} {sr[k]:>10d}{flag}')
print()
print('--- RENK KARSILASTIRMASI (ayni metin, farkli renk) ---')
diff=same=miss=0
for t,c in sorted(co.items()):
    if t in cr:
        if cr[t]!=c:
            diff+=1
            print(f'  {c}  ->  {cr[t]}   "{t[:62]}"')
        else: same+=1
    else: miss+=1
print(f'  [ ayni: {same} | degismis: {diff} | gelende bulunamadi: {miss} ]')

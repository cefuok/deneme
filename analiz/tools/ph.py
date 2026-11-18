import re, sys, os, shutil
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(dst), exist_ok=True)
s = open(src, encoding='utf-8', errors='replace').read()
# sadece disaridan yuklenen (engelli) gorselleri yer tutucuya cevir
s = re.sub(r'src="https?://[^"]+"', 'src="ph.png"', s)
open(dst, 'w', encoding='utf-8').write(s)

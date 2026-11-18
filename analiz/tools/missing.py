import sys, importlib.util
spec = importlib.util.spec_from_file_location("c", sys.argv[3]); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
co, cr = c.colored_runs(sys.argv[1]), c.colored_runs(sys.argv[2])
print('  Orijinalde renkli, gelende ayni metin bulunamadi:')
for t,col in sorted(co.items()):
    if t not in cr: print(f'    [{col}] "{t[:70]}"')

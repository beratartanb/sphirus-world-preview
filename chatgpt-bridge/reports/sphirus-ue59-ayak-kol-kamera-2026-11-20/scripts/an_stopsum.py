# an_stopsum.py <label...>: compact table from an_stop3 (one line per stop: kind, v_in, stop time/path, pelvis drop, worst drift L/R, clip)
import subprocess, sys, re
out = subprocess.run([sys.executable, 'Tools/UE59_20261119/an_stop3.py'] + sys.argv[1:], capture_output=True, text=True).stdout
K = {'W': 'walk', 'W LeftShift': 'jog', 'W LeftShift LeftControl': 'sprint'}
for ln in out.splitlines():
    if ln.startswith('=='): print(ln.split('(')[0]); continue
    if 'seg' not in ln: continue
    s = re.search(r'seg +(\d+) after "([^"]*)" ([\d.]+)s', ln); v = re.search(r'v_in +(\d+)', ln); sp = re.search(r'stop ([\d.na]+)s path +(\d+)', ln)
    dr = re.search(r'drop +([-\d.]+)', ln); dl = re.search(r'drift L +([\d.]+)', ln); drr = re.search(r' R +([\d.]+)(?:\([^)]*\))? nC', ln)
    cl = ln.rsplit('| ', 1)[-1].split(' > ')
    print('  %2s %-6s %.2fs v%3s | stop %5ss %4s cm | drop %5s | drift L %5s R %5s | %s' % (s.group(1), K.get(s.group(2), s.group(2)), float(s.group(3)), v.group(1), sp.group(1), sp.group(2), dr.group(1), dl.group(1), drr.group(1) if drr else '?', [c for c in cl if 'Stop' in c or 'Turn' in c or 'Idle' in c][:1]))

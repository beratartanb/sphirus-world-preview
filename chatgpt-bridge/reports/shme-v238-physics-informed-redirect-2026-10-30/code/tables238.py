"""tables238.py <out.md> [tag=reg] [variant=cut3] : V2.38 tables from the LTP side files of ONE editor session.
(1) per scenario: worst planted-ball SLIP / DRAG (contact231, t > 2.5 s) with its owner clip, upper-body pops > 25 m/s2 (count / worst,
    from the run report), database-not-ready frames; o = saved production vs the candidate variant;
(2) hard-turn balance read (balance238): heading 80 % time, min speed through the turn, peak capsule acceleration (mu_eff), number of
    contacts in the first 1.2 s, pelvis / chest / head yaw at +1.0 and +1.4 s relative to the old heading, the clip that owned the turn.
Missing runs print '-'; runs with database-not-ready frames are marked '*' (not comparable)."""
import sys, os, re, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H]
from ltp231 import load, short
from contact231 import classify
from balance238 import analyse
REP = os.path.join(H, '..', '..', 'Saved', 'Codex', 'SHME_V212_20261017', 'Reports')
def runs(lab):
    try: return load(lab)
    except Exception: return None
def pops(lab):
    try: first = open(os.path.join(REP, lab + '.txt'), encoding='utf8', errors='replace').readline()
    except Exception: return None
    m = re.search(r'pops >25 m/s2: (\d+) \(worst (\d+)\)', first); return (int(m.group(1)), int(m.group(2))) if m else None
def worst(R):
    eps = [e for e in classify(R, 2.5, 1e9) if e['cls'] in ('SLIP', 'DRAG')]
    if not eps: return 0.0, ''
    w = max(eps, key=lambda e: e['drift']); return w['drift'], w['clip'].replace('SHM_JogQ_', '')[:28]
def nodb(R): return sum(1 for r in R if r['t'] > 2.5 and str(r.get('av_CurrentSelectedDatabase')) == 'None')
def cell(lab):
    R = runs(lab)
    if R is None: return '-', '', '-'
    w, c = worst(R); p = pops(lab); nd = nodb(R)
    return '%.1f%s' % (w, '*' if nd else ''), c, ('%d / %d' % p) if p else '-'
if __name__ == '__main__':
    out = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else 'reg'; var = sys.argv[3] if len(sys.argv) > 3 else 'cut3'
    SC = ['j38_c90r', 'j38_c90rb', 'j38_c90l', 'j38_c90lb', 'j38_c45r', 'j38_c135r', 'j38_cc90', 'w38_c90r', 's38_c90r', 's38_c90l', 'jdiag', 'jswap', 'jlean', 'ad_jog', 'chain_jogcut',
          'mt_jog', 'mtf_jog', 'cam32_j90', 'j36_stop', 'j36_stopr', 'j36_rsm', 'j36_wjs', 'j36_sside', 'j35_rev', 'j30_rel_3450', 'j34_chain1', 'jstart', 'e29_chain', 'c29_combo', 'wdiag', 'wstart', 'ter_drop_jog']
    L = ['## 1. Worst planted-ball slide (cm, owner clip) and upper-body pops (count / worst m/s2), fixed 30 FPS: production (o) vs %s; * = database-not-ready frames' % var, '',
         '| scenario | o | o owner | o pops | %s | %s owner | %s pops |' % (var, var, var), '|---|---|---|---|---|---|---|']
    for s in SC:
        a = cell('v238%s_%s_o_r1' % (tag, s)); b = cell('v238%s_%s_%s_r1' % (tag, s, var))
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (s, a[0], a[1], a[2], b[0], b[1], b[2]))
    L += ['', '## 2. Hard-turn balance read (balance238; yaw relative to the old heading, + = toward the turn)', '',
          '| run | turn | heading 80 %% s | min speed | peak a after 0.1 s (mu_eff) | contacts 0-1.2 s | pel / chest / head @+1.0 | @+1.4 | turn clip |', '|---|---|---|---|---|---|---|---|---|']
    for s in ('j38_c90r', 'j38_c90rb', 'j38_c90l', 'j38_c90lb', 'j38_c45r', 'j38_c135r', 'j38_cc90'):
        for v in ('o', var):
            lab = 'v238%s_%s_%s_r1' % (tag, s, v)
            try: a = analyse(lab, None, 1.6)
            except Exception: L.append('| %s %s | - |' % (s, v)); continue
            if 'error' in a: L.append('| %s %s | %s |' % (s, v, a['error'])); continue
            rows = a['rows']; sg = 1 if (a['turn_deg'] or 0) >= 0 else -1
            def at(t):
                r = min(rows, key=lambda x: abs(x['t'] - t)); f = lambda q: '-' if q is None else str(int(round(sg * q)))
                return '%s / %s / %s' % (f(r['pel']), f(r['chest']), f(r['head']))
            vmin = min(x['spd'] for x in rows if 0 <= x['t'] <= 1.4); amx = max(x['acc'] for x in rows if 0.1 <= x['t'] <= 1.4)   # after the request-frame CMC friction spike
            nct = sum(1 for c in a['contacts'] if c['t'] <= 1.2)
            clips = sorted(set(x['clip'] for x in rows if 0.1 <= x['t'] <= 0.9)); tc = ', '.join(c[:22] for c in clips)[:60]
            L.append('| %s %s | %s | %s | %d | %d (%.2f) | %d | %s | %s | %s |' % (s, v, a['turn_deg'], a['t80_s'], vmin, amx, amx / 981.0, nct, at(1.0), at(1.4), tc))
    # 3. frame-rate modes (worst slide cm o / var, worst pop o / var) and 4. cold first use (clean editor, no warm run)
    FS = ['j38_c90r', 'j38_c90l', 'j38_cc90', 'mtf_jog', 'jlean', 'j36_rsm']; FT = ('g60', 'g120', 'g20', 'greal'); CT = 'cold'
    if tag in ('fin3', 'fin4'): FS = ['j38_c90r', 'j38_c90l', 'j35_rev', 'j30_rel_3450', 'e29_chain', 'w38_c90r', 'jlean']; FT = tuple(None if x is None else tag.replace('fin3', 'h').replace('fin4', 'i') + x for x in ('60', '120', None, 'real')); CT = 'cold' + tag[-1]
    L += ['', '## 3. Frame-rate modes: worst slide cm o / %s (worst pop m/s2 o / %s); * = database-not-ready frames' % (var, var), '', '| scenario | 30 | 60 | 120 | 20 | real |', '|---|---|---|---|---|---|']
    for s in FS:
        cs = []
        for t in (tag,) + FT:
            if t is None: cs.append('-'); continue
            a = cell('v238%s_%s_o_r1' % (t, s)); b = cell('v238%s_%s_%s_r1' % (t, s, var))
            pa = a[2].split(' / ')[-1] if a[2] != '-' else '-'; pb = b[2].split(' / ')[-1] if b[2] != '-' else '-'
            cs.append('%s / %s (%s / %s)' % (a[0], b[0], pa, pb))
        L.append('| %s | %s |' % (s, ' | '.join(cs)))
    L += ['', '## 4. Cold first use in the clean editor (production, no warm run)', '', '| run | no-DB frames | worst cm | cut clip on the request |', '|---|---|---|---|']
    for s in ('j38_c90r', 'j38_c90l'):
        lab = 'v238%s_%s_o_r1' % (CT, s); R = runs(lab)
        if R is None: L.append('| %s | - | - | - |' % lab); continue
        cc = sorted(set(short(r.get('av_Phase27_SelectedObject')) for r in R if 5.38 < r['t'] < 5.5))
        L.append('| %s | %d | %.1f | %s |' % (lab, nodb(R), worst(R)[0], ', '.join(cc)))
    open(out, 'w', encoding='utf8').write('\n'.join(L) + '\n'); print('\n'.join(L))

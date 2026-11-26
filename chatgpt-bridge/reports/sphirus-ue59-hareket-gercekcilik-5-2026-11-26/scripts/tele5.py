# tele5.py: loader for 'sph-tele/5.1' recordings. Fails loudly on a schema mismatch or a missing / unreadable field.
import json
SCHEMA = 'sph-tele/5.1'
class TeleError(Exception): pass
def load(label, need=()):
    rows = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % label))['rows']; out = []
    for r in rows:
        h = r['hook'] if isinstance(r['hook'], dict) else {}; t = h.get('tele')
        if not t: raise TeleError('%s frame %s: no tele block (recorded without hk_tele5)' % (label, r.get('f')))
        if t.get('schema') != SCHEMA: raise TeleError('%s: schema %r != %r' % (label, t.get('schema'), SCHEMA))
        if 'error' in t: raise TeleError('%s frame %s: hook error %s' % (label, r.get('f'), t['error']))
        for n in need:
            if n not in t['f']: raise TeleError('%s: field %s was not recorded' % (label, n))
            if isinstance(t['f'][n], str) and t['f'][n].startswith('ERR:'): raise TeleError('%s: field %s unreadable (%s)' % (label, n, t['f'][n]))
        out.append((r, t))
    return out

"""Merge the CF morph sets for LOD projection: morph_data_br_all.json (SHCB rebased + BR_Neutral v6) and, after
cf_lod_helper.py, morph_data_br_hfx_all.json (helper-augmented SHCB + BR_Neutral). usage: python cf_merge_morphs.py all|hfx"""
import json, sys, pathlib
CF = pathlib.Path(__file__).resolve().parents[2]/'Saved/Codex/CharacterFinal_20260929'; which = sys.argv[1]
v6 = json.loads((CF/'br_morph_v6.json').read_text()); src = json.loads((CF/('morph_data_br_shcb.json' if which == 'all' else 'morph_data_br_hfx.json')).read_text())
out = {p: dict(src[p]) for p in ('Body', 'Head')}
for p in out: out[p]['BR_Neutral'] = v6[p]['BR_Neutral']
(CF/('morph_data_br_all.json' if which == 'all' else 'morph_data_br_hfx_all.json')).write_text(json.dumps(out)); print(which, {p: {k: len(v) for k, v in out[p].items()} for p in out})

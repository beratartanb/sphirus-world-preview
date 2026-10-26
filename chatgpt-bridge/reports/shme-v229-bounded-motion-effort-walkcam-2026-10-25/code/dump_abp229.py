"""V2.11 read-only graph dump of the production Sandbox ABP_GR_MotionMatchingBase (DB routing for the walk->sprint push) into Saved/Codex/SHME_V229_20261025/GraphsABP/."""
import unreal as u, pathlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); D = P / 'Saved/Codex/SHME_V229_20261025/GraphsABP'; D.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(P / 'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import pn, info
from editor_toolset.toolsets.blueprint import BlueprintTools as B
ROOTS = ['/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase']
def chain(ap):
    out = []
    while ap:
        bp = u.load_asset(ap)
        if bp is None or not isinstance(bp, u.Blueprint): break
        out.append(ap)
        tag = str(u.EditorAssetLibrary.find_asset_data(ap).get_tag_value('ParentClass') or '')   # e.g. /Script/Engine.BlueprintGeneratedClass'/Game/X/BP.BP_C'
        cp = tag.split("'")[1] if "'" in tag else tag
        ap = cp.rsplit('.', 1)[0] if cp.startswith('/Game/') else None
        if not ap: out.append('native:' + cp)
    return out
done = set(); res = {}
for r in ROOTS:
    ch = chain(r); print('DIRCHAIN', ' -> '.join(ch))
    for ap in ch:
        if ap.startswith('native:') or ap in done: continue
        done.add(ap); bp = u.load_asset(ap)
        for gr in B.list_graphs(bp):
            gname = pn(gr).split(':')[-1].split('.')[-1]; lines = []
            for n in B.find_nodes(gr):
                ni = info(pn(n)); short = pn(n).rsplit('.', 1)[-1]; args = []
                for p in ni.input_pins:
                    if p.connected_pins: args.append(p.name + '<-' + ','.join(pn(q.node).rsplit('.', 1)[-1] + '.' + str(q.name if hasattr(q, 'name') else q.index_id) for q in p.connected_pins))
                    elif str(p.value) not in ('', 'None'): args.append(p.name + '=' + str(p.value)[:80])
                lines.append(f"{short} [{ni.type_id}] " + '; '.join(args))
            if lines:
                (D / (ap.split('/')[-1] + '__' + gname.replace('?', 'Q').replace(' ', '_') + '.txt')).write_text('\n'.join(lines), encoding='utf8')
                res[ap.split('/')[-1] + '__' + gname] = len(lines)
print('DIRDUMP', len(res), 'graphs', sum(res.values()), 'nodes')

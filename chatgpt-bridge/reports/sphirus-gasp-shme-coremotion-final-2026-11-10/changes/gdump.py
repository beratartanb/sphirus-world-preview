# gdump.py: helper (exec'd) - dump a Blueprint graph as text: node index, type, input values/links, exec chain.
def gdump(g,out_path,only_events=None,max_depth=60):
    ns=B.find_nodes(g); P=[pn(n) for n in ns]; idx={p:i for i,p in enumerate(P)}; lines=[]
    for i,p in enumerate(P):
        try: ii=info(p)
        except Exception: continue
        ins=[]
        for x in ii.input_pins:
            nm=str(x.name)
            try:
                s=src((p,nm))
                if s: ins.append('%s<-%s'%(nm,','.join('#%s.%s'%(idx.get(a,'?'),b) for a,b in s))); continue
            except Exception: pass
            try:
                v=str(B.get_pin_value(x.pin_id))
                if v not in ('','None'): ins.append('%s=%s'%(nm,v[:60]))
            except Exception: pass
        outs=[str(x.name) for x in ii.output_pins]
        lines.append('#%d %s | IN %s | OUT %s'%(i,str(ii.type_id)[:90],'; '.join(ins),','.join(outs)))
    open(out_path,'w',encoding='utf8').write('\n'.join(lines)); return len(lines)

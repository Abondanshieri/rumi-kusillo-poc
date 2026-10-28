import json,sys,itertools
sys.path.insert(0,'.')
import layout2 as L
a=json.load(open('../snap_g1_base2.json')); b=json.load(open('../snap_g1_despues.json'))
out={}
for k in a:
    A,B=a[k],b[k]
    la=set(map(tuple,A['links'])); lb=set(map(tuple,B['links']))
    lost=sorted(la-lb); new=sorted(lb-la)
    # resolver reroutes: seguir cadenas
    nxt={}
    for s,t in lb:
        if t.startswith('Reroute') : pass
    def res(links):
        r=set()
        d={}
        for s,t in links:
            if s.startswith('Reroute'): d.setdefault(s.split('.')[0],[]).append(t)
        for s,t in links:
            if s.startswith('Reroute'): continue
            stack=[t]
            while stack:
                x=stack.pop()
                if x.startswith('Reroute'): stack+=d.get(x.split('.')[0],[])
                else: r.add((s,x))
        return r
    rb=res(lb)
    vals_changed=[p for p in A['vals'] if B['vals'].get(p)!=A['vals'][p]]
    vals_new=[p for p in B['vals'] if p not in A['vals']]
    nodes={n:v for n,v in B['nodes'].items() if v['cls']!='RigVMCommentNode'}
    coms={n:v for n,v in B['nodes'].items() if v['cls']=='RigVMCommentNode'}
    grid=[n for n,v in B['nodes'].items() if v['pos'][0]%50 or v['pos'][1]%50 or (v['cls']=='RigVMCommentNode' and (v['size'][0]%50 or v['size'][1]%50))]
    # margen nodo-caja
    def est(n): return (60,60) if n.startswith('Reroute') else L.est(n)
    marg=[];ncom={}
    for n,v in nodes.items():
        x,y=v['pos']; w,h=est(n)
        owners=[c for c,cv in coms.items() if cv['pos'][0]<=x and cv['pos'][1]<=y and x+w<=cv['pos'][0]+cv['size'][0] and y+h<=cv['pos'][1]+cv['size'][1]]
        ncom[n]=[coms[c]['text'] for c in owners]
        for c in owners:
            cv=coms[c]; m=min(x-cv['pos'][0],y-cv['pos'][1],cv['pos'][0]+cv['size'][0]-x-w,cv['pos'][1]+cv['size'][1]-y-h)
            marg.append((n,round(m)))
    fuera=[n for n,o in ncom.items() if not o]
    cov=[(p,q) for p,q in itertools.combinations(coms,2) if (lambda c1,c2: c1['pos'][0]<c2['pos'][0]+c2['size'][0] and c2['pos'][0]<c1['pos'][0]+c1['size'][0] and c1['pos'][1]<c2['pos'][1]+c2['size'][1] and c2['pos'][1]<c1['pos'][1]+c1['size'][1])(coms[p]['text'] and coms[p],coms[q])]
    pos={n:tuple(v['pos']) for n,v in nodes.items()}
    mt=L.metrics({n:p for n,p in pos.items() if not n.startswith('Reroute')},[l for l in rb])
    L.est
    out[k]=dict(links_perdidos=[list(x) for x in sorted(set(la)-rb)],links_nuevos_reales=[list(x) for x in sorted(rb-la)],links_antes=len(la),links_despues=len(lb),reroutes=[n for n in nodes if n.startswith('Reroute')],
      valores_cambiados=vals_changed,valores_nuevos=len(vals_new),fuera_rejilla=grid,margen_min=min(m for _,m in marg) if marg else None,margen_menor60=[x for x in marg if x[1]<60],nodos_sin_caja=fuera,
      solapes_cajas=cov,fuentes=sorted({v['font'] for v in coms.values()}),metricas_despues={x:y for x,y in mt.items() if not x.endswith('_l') and x!='ov'},largos=mt['long_l'],retroceso=mt['back_l'],solapes_nodos=mt['ov'])
print(json.dumps(out,indent=1,ensure_ascii=False))
json.dump(out,open('../g1_verificacion.json','w'),indent=1,ensure_ascii=False)

import sys, json, glob, itertools, os; sys.path.insert(0,'.')
from geo import *
from layout3 import SN
EVd='../'
b=json.load(open(EVd+'snap_g1c_despues.json')); com=json.load(open(EVd+'g1c_comentarios_vivo.json'))
base=json.load(open(EVd+'snap_g1c_base.json'))
out={}
for k in b:
    nodes={n:v for n,v in b[k]['nodes'].items() if v['cls']!='RigVMCommentNode'}
    sizes=load_sizes(k,nodes)
    for n in nodes:
        if n.startswith('Reroute'): sizes[n]=dict(w=50,h=50,rows=[],medido='estimado')
    pos={n:tuple(v['pos']) for n,v in nodes.items()}
    boxes=com[k]
    links=[tuple(l) for l in b[k]['links']]
    m=metrics(pos,sizes,links)
    # antes (misma geometria real, posiciones del snapshot base)
    posb={n:tuple(v['pos']) for n,v in base[k]['nodes'].items() if v['cls']!='RigVMCommentNode'}
    REN={'Add_HipsZ':'SINSALIDA_Add_HipsZ','Add_LeftFootZ':'SINSALIDA_Add_LeftFootZ','Add_RightFootZ':'SINSALIDA_Add_RightFootZ','Clamp_LeftOffset':'SINSALIDA_Clamp_LeftOffset','Clamp_RightOffset':'SINSALIDA_Clamp_RightOffset'}
    rn=lambda p:REN.get(p.split('.')[0],p.split('.')[0])+('.'+p.split('.',1)[1] if '.' in p else '')
    posb={REN.get(n,n):p for n,p in posb.items()}
    linksb=[(rn(a),rn(c)) for a,c in base[k]['links']]
    mb=metrics(posb,sizes,linksb)
    # cajas
    marg=[]; fuera=[]
    for n,p in pos.items():
        w,h=sizes[n]['w'],sizes[n]['h']
        ins=[c for c in boxes if c['pos'][0]<=p[0] and c['pos'][1]<=p[1] and p[0]+w<=c['pos'][0]+c['size'][0] and p[1]+h<=c['pos'][1]+c['size'][1]]
        par=[c for c in boxes if c['pos'][0]<p[0]+w and p[0]<c['pos'][0]+c['size'][0] and c['pos'][1]<p[1]+h and p[1]<c['pos'][1]+c['size'][1]]
        if n.startswith('Reroute'):
            if par: fuera.append((n,'dentro de caja'))
            continue
        if len(ins)!=1 or len(par)!=1: fuera.append((n,[c['texto'] for c in par])); continue
        c=ins[0]; marg.append((n,min(p[0]-c['pos'][0],p[1]-c['pos'][1],c['pos'][0]+c['size'][0]-p[0]-w,c['pos'][1]+c['size'][1]-p[1]-h)))
    solcaj=[(c1['texto'],c2['texto']) for c1,c2 in itertools.combinations(boxes,2) if c1['pos'][0]<c2['pos'][0]+c2['size'][0] and c2['pos'][0]<c1['pos'][0]+c1['size'][0] and c1['pos'][1]<c2['pos'][1]+c2['size'][1] and c2['pos'][1]<c1['pos'][1]+c1['size'][1]]
    grid=[n for n,p in pos.items() if p[0]%50 or p[1]%50]+[c['texto'] for c in boxes if any(v%50 for v in c['pos']+c['size'])]
    sl=[]
    def short(m): return dict(enlaces=m['enlaces'],retroceso=len(m['retroceso']),largos_mayor_1500=m['largos'],cruces=len(m['cruces']),cruces_lista=m['cruces'],cable_sobre_nodo=len(m['cable_sobre_nodo']),cable_sobre_nodo_lista=m['cable_sobre_nodo'],solapes_nodos_holgura20=len(m['solapes']))
    out[k]=dict(antes=short(mb),despues=short(m),margen_min_nodo_caja=min(x for _,x in marg),peor_margen=sorted(marg,key=lambda x:x[1])[:3],nodos_fuera_de_caja_o_en_ajena=fuera,solapes_cajas=solcaj,fuera_rejilla=grid,fuentes=sorted({c['fuente'] for c in boxes}),capturas_editor=sl)
    print(k); print(json.dumps({x:y for x,y in out[k].items() if x not in ('antes','despues')},ensure_ascii=False)[:1500])
    for t in ('antes','despues'): print(' ',t,{x:(y if not isinstance(y,list) else len(y)) for x,y in out[k][t].items() if not x.endswith('lista')})
json.dump(out,open(EVd+'g1c_verificacion.json','w'),indent=1,ensure_ascii=False)

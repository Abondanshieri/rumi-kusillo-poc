import sys, json; sys.path.insert(0,'.')
REN={'Add_HipsZ':'SINSALIDA_Add_HipsZ','Add_LeftFootZ':'SINSALIDA_Add_LeftFootZ','Add_RightFootZ':'SINSALIDA_Add_RightFootZ','Clamp_LeftOffset':'SINSALIDA_Clamp_LeftOffset','Clamp_RightOffset':'SINSALIDA_Clamp_RightOffset'}
EV='../'
a=json.load(open(EV+'snap_g1c_base.json')); b=json.load(open(EV+'snap_g1c_despues.json'))
def rn(p):
    n,_,r=p.partition('.')
    return REN.get(n,n)+('.'+r if r else '')
out={}
for k in a:
    la=set((rn(x),rn(y)) for x,y in a[k]['links']); lb=set((x,y) for x,y in b[k]['links'])
    va={rn(p):v for p,v in a[k]['vals'].items()}; vb=b[k]['vals']
    ch=[p for p in va if vb.get(p)!=va[p]]
    out[k]=dict(enlaces_antes=len(la),enlaces_despues=len(lb),perdidos=sorted(la-lb),nuevos=sorted(lb-la),valores_antes=len(va),valores_despues=len(vb),valores_distintos=ch,
      nodos_antes=len(a[k]['nodes']),nodos_despues=len(b[k]['nodes']),nodos_faltan=sorted(set(REN.get(n,n) for n in a[k]['nodes'])-set(b[k]['nodes'])),nodos_nuevos=sorted(set(b[k]['nodes'])-set(REN.get(n,n) for n in a[k]['nodes'])))
    print(k,{x:(len(y) if isinstance(y,list) else y) for x,y in out[k].items()})
json.dump(out,open(EV+'g1c_comparacion.json','w'),indent=1)

"""Calcula layout en rejilla de 50 u para los grafos internos del ABP (estados y reglas). Salida: g2_plan.json"""
import json,itertools,math,sys
d=json.load(open('../g2_snap_antes.json'))
def size(t):
    t=t or ''
    if 'Resultado' in t or 'Posedeanimaci' in t: return (200,120)
    if t.startswith('|Get'): return (250,80)
    if 'Secuenciadeanimaci' in t: return (300,250)
    if 'Reproductordeespacio' in t: return (320,300)
    if 'Mezclabidireccional' in t: return (260,230)
    if 'GetRelevant' in t: return (300,150)
    if 'Usarposeencach' in t: return (260,100)
    if 'float' in t or 'Booleano' in t: return (200,130)
    return (250,150)
def up(v,s=50): return int(math.ceil(v/s)*s)
def segs_cross(p1,p2,p3,p4):
    def o(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    return o(p1,p2,p3)*o(p1,p2,p4)<0 and o(p3,p4,p1)*o(p3,p4,p2)<0
def metrics(nodes,edges,pos):
    wires=[]
    for s,t in edges:
        sn=s.split('#')[0]; tn=t.split('.')[0]
        if sn not in pos or tn not in pos: continue
        sw,sh=size(nodes[sn]['type']); tw,th=size(nodes[tn]['type'])
        a=(pos[sn][0]+sw,pos[sn][1]+sh/2); b=(pos[tn][0],pos[tn][1]+th/2)
        wires.append((sn,tn,a,b))
    cross=0
    for w1,w2 in itertools.combinations(wires,2):
        if len({w1[0],w1[1],w2[0],w2[1]})<4 and (w1[0]==w2[0] or w1[1]==w2[1] or w1[0]==w2[1] or w1[1]==w2[0]): continue
        if segs_cross(w1[2],w1[3],w2[2],w2[3]): cross+=1
    back=sum(1 for w in wires if w[2][0]>w[3][0])
    names=list(pos)
    ov=0
    for a,b in itertools.combinations(names,2):
        aw,ah=size(nodes[a]['type']); bw,bh=size(nodes[b]['type'])
        if pos[a][0]<pos[b][0]+bw and pos[b][0]<pos[a][0]+aw and pos[a][1]<pos[b][1]+bh and pos[b][1]<pos[a][1]+ah: ov+=1
    return cross,back,ov
plan={}
for g,v in d.items():
    nodes=v['nodes']; edges=v['edges']
    if g=='AnimGraph' or any(k.startswith('ERR') for k in nodes): continue
    E=[(s.split('#')[0],t.split('.')[0]) for s,t in edges]
    # capas por camino mas largo desde fuentes
    layer={n:0 for n in nodes}
    for _ in range(len(nodes)):
        for s,t in E:
            if layer[t]<layer[s]+1: layer[t]=layer[s]+1
    # resultado siempre en la ultima capa
    res=[n for n in nodes if 'Result' in n]
    mx=max(layer.values()) if layer else 0
    for r in res: layer[r]=max(layer[r],mx)
    cols={}
    for n,l in layer.items(): cols.setdefault(l,[]).append(n)
    # orden por baricentro (iterativo)
    order={n:i for l in cols.values() for i,n in enumerate(sorted(l))}
    for _ in range(6):
        for l in sorted(cols):
            def bc(n):
                nb=[order[s] for s,t in E if t==n]+[order[t] for s,t in E if s==n and layer[t]>layer[n]] if l>0 else [order[t] for s,t in E if s==n]
                return sum(nb)/len(nb) if nb else order[n]
            cols[l].sort(key=lambda n:(bc(n),n))
            for i,n in enumerate(cols[l]): order[n]=i
    pos={};x=0
    for l in sorted(cols):
        w=max(size(nodes[n]['type'])[0] for n in cols[l]); y=0
        for n in cols[l]:
            pos[n]=(x,up(y,50)); y=pos[n][1]+size(nodes[n]['type'])[1]+100
        x=up(x+w+200)
    # centra columnas con un solo nodo respecto a la mas alta? (compacto: se deja a la parte superior)
    before={n:(i['x'],i['y']) for n,i in nodes.items()}
    mb=metrics(nodes,edges,before); ma=metrics(nodes,edges,pos)
    plan[g]={'pos':pos,'antes':{'cruces':mb[0],'retrocesos':mb[1],'solapes':mb[2]},'despues':{'cruces':ma[0],'retrocesos':ma[1],'solapes':ma[2]}}
json.dump(plan,open('../g2_plan.json','w'),indent=1)
tot=lambda k,m:sum(p[k][m] for p in plan.values())
for k in('antes','despues'): print(k,{m:tot(k,m) for m in('cruces','retrocesos','solapes')})
for g,p in plan.items():
    if p['despues']['cruces'] or p['despues']['solapes'] or p['despues']['retrocesos']: print(g[-45:],p['antes'],p['despues'])

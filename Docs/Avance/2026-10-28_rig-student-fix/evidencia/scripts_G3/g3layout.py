import json, math, itertools
HDR=44; ROW=28; GAPX=100; GAPY=50
def is_exec(p): return p['type'].startswith('Ejecuci')
def title(n): return n['type'].split('|')[-1]
def est_size(n, rep=None):
    ins=[p for p in n['pins'] if p['dir']=='in']; outs=[p for p in n['pins'] if p['dir']=='out']
    # delegate pins on events are hidden-ish
    outs=[p for p in outs if p['type']!='Delegado']
    rows=max(len(ins),len(outs),1)
    t=title(n)
    w1=len(t)*9+70
    li=max([len(p['name']) for p in ins] or [0]); lo=max([len(p['name']) for p in outs] or [0])
    w2=(li+lo)*8+100
    if any((not is_exec(p)) and not p['links'] and p['value'] not in ('',) for p in ins): w2+=70
    w=max(w1,w2,150)
    h=HDR+rows*ROW+8
    if rep:
        w=max(w,rep[0]); h=max(h,rep[1])
    return (int(math.ceil(w/10)*10), int(math.ceil(h/10)*10))
def pin_y(n, pidx_name, dirn, y=None):
    """y estimate of pin center"""
    y0=n['y'] if y is None else y
    pins=[p for p in n['pins'] if p['dir']==dirn and p['type']!='Delegado']
    for i,p in enumerate(pins):
        if p['idx']==pidx_name: return y0+HDR+i*ROW+ROW/2
    return y0+HDR
def edges(nodes):
    E=[]
    for k,n in nodes.items():
        for p in n['pins']:
            if p['dir']=='in':
                for (s,sidx) in p['links']:
                    E.append((s,sidx,k,p['idx'],is_exec(p)))
    return E
def seg_intersect(a,b,c,d):
    def ccw(p,q,r): return (r[1]-p[1])*(q[0]-p[0])-(q[1]-p[1])*(r[0]-p[0])
    d1=ccw(a,b,c); d2=ccw(a,b,d); d3=ccw(c,d,a); d4=ccw(c,d,b)
    return (d1*d2<0) and (d3*d4<0)
def metrics(nodes, pos, sizes):
    """pos: name->(x,y)"""
    E=edges(nodes)
    segs=[]
    back=0; longw=[]
    for (s,si,d,di,ex) in E:
        ns=dict(nodes[s]); nd=dict(nodes[d])
        sx,sy=pos[s]; dx,dy=pos[d]
        a=(sx+sizes[s][0], pin_y(nodes[s],si,'out',sy)); b=(dx, pin_y(nodes[d],di,'in',dy))
        segs.append((a,b,s,d))
        if a[0]>b[0]: back+=1
        L=math.hypot(b[0]-a[0],b[1]-a[1])
        if L>1500: longw.append((s,d,round(L)))
    cross=0
    backl=[(s,d) for (a,b,s,d) in segs if a[0]>b[0]]
    for i in range(len(segs)):
        for j in range(i+1,len(segs)):
            a,b,s1,d1=segs[i]; c,d,s2,d2=segs[j]
            if s1==s2 or d1==d2 or s1==d2 or d1==s2: continue
            if seg_intersect(a,b,c,d): cross+=1
    names=list(nodes); ov=0; ovl=[]
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            a,b=names[i],names[j]
            ax,ay=pos[a]; bx,by=pos[b]; aw,ah=sizes[a]; bw,bh=sizes[b]
            if ax<bx+bw and bx<ax+aw and ay<by+bh and by<ay+ah: ov+=1; ovl.append((a,b))
    off=sum(1 for n in names if pos[n][0]%50 or pos[n][1]%50)
    return {'cruces':cross,'retroceso':back,'largos_1500':len(longw),'solapes':ov,'fuera_rejilla50':off,'_largos':longw,'_back':backl,'_solapes':ovl}
def snap50(v,up=False):
    return int((math.ceil(v/50.0) if up else round(v/50.0))*50)
def pav(d, s):
    """minimize sum (y_i-d_i)^2 s.t. y_{i+1}>=y_i+s_i. returns y"""
    n=len(d); cum=[0]*n
    for i in range(1,n): cum[i]=cum[i-1]+s[i-1]
    dd=[d[i]-cum[i] for i in range(n)]
    blocks=[]  # [sum,count,start]
    for i in range(n):
        blocks.append([dd[i],1])
        while len(blocks)>1 and blocks[-2][0]/blocks[-2][1] > blocks[-1][0]/blocks[-1][1]:
            b=blocks.pop(); blocks[-1][0]+=b[0]; blocks[-1][1]+=b[1]
    z=[]
    for sm,c in blocks: z+= [sm/c]*c
    return [z[i]+cum[i] for i in range(n)]
def layout_group(nodes, members, sizes, ext_in=None):
    """layered layout of members (list of names). returns pos dict local (min corner 0,0), w,h"""
    M=set(members)
    E=[e for e in edges(nodes) if e[0] in M and e[2] in M]
    succ={m:[] for m in M}; pred={m:[] for m in M}
    for (s,si,d,di,ex) in E:
        if d not in succ[s]: succ[s].append(d)
        if s not in pred[d]: pred[d].append(s)
    # topo order
    indeg={m:len(pred[m]) for m in M}; order=[]; q=[m for m in members if indeg[m]==0]
    while q:
        m=q.pop(0); order.append(m)
        for t in succ[m]:
            indeg[t]-=1
            if indeg[t]==0: q.append(t)
    assert len(order)==len(M), "ciclo en grupo"
    layer={m:0 for m in M}
    for m in order:
        for t in succ[m]: layer[t]=max(layer[t],layer[m]+1)
    pure={m for m in M if not any(is_exec(p) for p in nodes[m]['pins'])}
    for m in reversed(order):
        if m in pure and succ[m]:
            layer[m]=min(layer[t] for t in succ[m])-1
    mn=min(layer.values()); 
    for m in M: layer[m]-=mn
    L=sorted(set(layer.values())); rank={l:i for i,l in enumerate(L)}
    for m in M: layer[m]=rank[layer[m]]
    nl=len(L); layers=[[m for m in members if layer[m]==i] for i in range(nl)]
    # initial order: by original y
    for l in layers: l.sort(key=lambda m:(nodes[m]['y'],nodes[m]['x']))
    idx={}
    def reidx():
        for l in layers:
            for i,m in enumerate(l): idx[m]=i
    reidx()
    nb={m:[] for m in M}
    for (s,si,d,di,ex) in E:
        nb[s].append((d,si,'out',di)); nb[d].append((s,di,'in',si))
    def bary(m, ref_dir=None):
        v=[]
        for (o,_,dr,_) in nb[m]:
            if ref_dir and dr!=ref_dir: continue
            # normalise by layer size
            v.append((idx[o]+0.5)/max(1,len(layers[layer[o]])))
        return sum(v)/len(v) if v else None
    for it in range(12):
        rng = range(1,nl) if it%2==0 else range(nl-2,-1,-1)
        for li in rng:
            ref='in' if it%2==0 else 'out'
            cur=layers[li]
            keys={}
            for i,m in enumerate(cur):
                b=bary(m,ref)
                keys[m]=b if b is not None else (i+0.5)/len(cur)
            cur.sort(key=lambda m:keys[m]); reidx()
    # x
    wmax=[max(sizes[m][0] for m in l) for l in layers]
    lx=[0]*nl
    for i in range(1,nl): lx[i]=snap50(lx[i-1]+wmax[i-1]+GAPX,up=True)
    # y: stacking then relax
    y={}
    for l in layers:
        yy=0
        for m in l: y[m]=yy; yy+=sizes[m][1]+GAPY
    def desired(m):
        ds=[];ws=[]
        for (o,mi,dr,oi) in nb[m]:
            # align pin y: o pin y - my pin offset
            if dr=='out': my=pin_y(nodes[m],mi,'out',0) - 0; ot=pin_y(nodes[o],oi,'in',y[o])
            else: my=pin_y(nodes[m],mi,'in',0); ot=pin_y(nodes[o],oi,'out',y[o])
            ds.append(ot-my); 
            ex=any(is_exec(p) for p in nodes[m]['pins'] if p['idx']==mi)
            ws.append(4 if ex else 1)
        if not ds: return y[m]
        return sum(a*b for a,b in zip(ds,ws))/sum(ws)
    for it in range(30):
        rng=list(range(nl)) if it%2==0 else list(range(nl-1,-1,-1))
        for li in rng:
            cur=layers[li]
            d=[desired(m) for m in cur]; s=[sizes[m][1]+GAPY for m in cur[:-1]]
            ys=pav(d,s) if cur else []
            for m,v in zip(cur,ys): y[m]=v
    miny=min(y.values())
    pos={}
    for m in M:
        pos[m]=(lx[layer[m]], snap50(y[m]-miny, up=False))
    # fix overlaps after snap (push down within layer)
    for l in layers:
        l.sort(key=lambda m:pos[m][1])
        cur=-1e9
        for m in l:
            yy=pos[m][1]
            if yy<cur: yy=snap50(cur,up=True)
            pos[m]=(pos[m][0],yy); cur=yy+sizes[m][1]+GAPY
    w=max(pos[m][0]+sizes[m][0] for m in M); h=max(pos[m][1]+sizes[m][1] for m in M)
    return pos,w,h,layer

BOXPAD=100; TOPPAD=250; BOXGAP=150
def place(nodes, sizes, GROUPS, SPEC):
    """SPEC: dict name -> dict(row=int, after=[groups], x=None). rows stack top->bottom. 'float':{'name':(x,y_center_of_rows(r0,r1))}"""
    allm=[m for g in GROUPS.values() for m in g['n']]
    assert len(allm)==len(set(allm)), [m for m in allm if allm.count(m)>1]
    missing=[m for m in nodes if m not in allm]; assert not missing, missing
    loc={gn:layout_group(nodes,g['n'],sizes) for gn,g in GROUPS.items()}
    dim={gn:(loc[gn][1]+2*BOXPAD, loc[gn][2]+TOPPAD+BOXPAD) for gn in GROUPS}
    rows=sorted(set(s['row'] for s in SPEC.values() if s.get('row') is not None))
    # row heights
    rowh={r:max(dim[g][1] for g,s in SPEC.items() if s.get('row')==r) for r in rows}
    rowy={}; y=0
    for r in rows: rowy[r]=y; y+=rowh[r]+BOXGAP
    boxes={}
    order=sorted(GROUPS, key=lambda g:(SPEC[g].get('ord',0)))
    pending=list(order); guard=0
    while pending and guard<100:
        guard+=1
        for g in list(pending):
            s=SPEC[g]; deps=s.get('after',[])+([s['below']] if s.get('below') else [])
            if any(d not in boxes for d in deps): continue
            x=max([boxes[d][0]+boxes[d][2]+BOXGAP for d in s.get('after',[])] or [s.get('x',0)])
            if s.get('x') is not None: x=max(x,s['x'])
            if s.get('below'): 
                b=boxes[s['below']]; yy=b[1]+b[3]+BOXGAP
                if s.get('x') is None and not s.get('after'): x=b[0]
            elif s.get('center_rows'):
                r0,r1=s['center_rows']; top=rowy[r0]; bot=rowy[r1]+rowh[r1]
                yy=snap50((top+bot)/2-dim[g][1]/2)
            else: yy=rowy[s['row']]
            boxes[g]=(snap50(x,up=True),snap50(yy),dim[g][0],dim[g][1]); pending.remove(g)
    assert not pending, pending
    pos={}
    for g,(bx,by,bw,bh) in boxes.items():
        for m,(lx,ly) in loc[g][0].items(): pos[m]=(bx+BOXPAD+lx, by+TOPPAD+ly)
    return pos,boxes,loc

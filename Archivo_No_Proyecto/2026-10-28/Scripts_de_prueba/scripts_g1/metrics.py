import sys,json,itertools,math
sys.path.insert(0,'.')
import layout
ORDER=['ExecutePin','Item','A','Euler','Value','B','Effector','PoleVector','Transform','Result','Translation','Rotation','Scale3D']
def pin_y(node_y,pinpath):
    rest=pinpath.split('.',1)[1] if '.' in pinpath else ''
    k=0
    for i,o in enumerate(ORDER):
        if rest.startswith(o): k=i; break
    return node_y+45+22*k
def metrics(nodes,links,est=layout.est):
    """nodes: {name:(x,y)} sin comentarios"""
    segs=[]; back=[]; long_=[]
    for a,b in links:
        na=a.split('.')[0]; nb=b.split('.')[0]
        if na not in nodes or nb not in nodes: continue
        # source = salida: la que no es entrada. heuristica: Result/Value/Transform/ExecutePin(del nodo anterior)
        # determinamos direccion por x: usamos la lista original ya orientada (a=origen)
        wa=est(na)[0]
        x1=nodes[na][0]+wa; y1=pin_y(nodes[na][1],a)
        x2=nodes[nb][0]; y2=pin_y(nodes[nb][1],b)
        segs.append(((x1,y1),(x2,y2),na,nb))
        if x1>x2: back.append((a,b,round(x1-x2)))
        d=math.hypot(x2-x1,y2-y1)
        if d>1500: long_.append((a,b,round(d)))
    def ccw(A,B,C): return (C[1]-A[1])*(B[0]-A[0])>(B[1]-A[1])*(C[0]-A[0])
    def inter(s,t):
        A,B=s[0],s[1]; C,D=t[0],t[1]
        return ccw(A,C,D)!=ccw(B,C,D) and ccw(A,B,C)!=ccw(A,B,D)
    cr=0
    for s,t in itertools.combinations(segs,2):
        if len({s[2],s[3]}&{t[2],t[3]})>0: continue
        if inter(s,t): cr+=1
    # solapes de nodos
    names=list(nodes); ov=[]
    for p,q in itertools.combinations(names,2):
        wp,hp=est(p); wq,hq=est(q)
        (x1,y1),(x2,y2)=nodes[p],nodes[q]
        if x1<x2+wq and x2<x1+wp and y1<y2+hq and y2<y1+hp: ov.append((p,q))
    return dict(links=len(segs),back=len(back),long=len(long_),cruces=cr,solapes=len(ov),back_l=back,long_l=long_,ov=ov)
def orient(links):
    out=[]
    for a,b in links:
        # un enlace guardado como [pin, target]: get_linked_target_pins devuelve destinos => a es origen
        out.append((a,b))
    return out
if __name__=='__main__':
    snap=json.load(open(sys.argv[1]))
    for key,fn in (('CR_Student_Procedural_fix',layout.proc),('CR_Student_IK_fix',layout.ik)):
        d=snap[key]
        # filtrar duplicados direccion: get_linked_target_pins sobre pin de salida da destino; sobre pin de entrada puede dar origen. Orientar por x.
        links=set()
        for a,b in d['links']: links.add((a,b))
        nodes_old={n:tuple(v['pos']) for n,v in d['nodes'].items() if v['cls']!='RigVMCommentNode'}
        # orientar: el origen es el pin de salida; usar posicion del layout actual no sirve; asumimos a=origen si a aparece antes (ver abajo)
        print(key,'antes',{k:v for k,v in metrics(nodes_old,list(links)).items() if not k.endswith('_l') and k!='ov'})
        newpos=fn()[0]
        print(key,'despues',{k:v for k,v in metrics(newpos,list(links)).items() if not k.endswith('_l') and k!='ov'})

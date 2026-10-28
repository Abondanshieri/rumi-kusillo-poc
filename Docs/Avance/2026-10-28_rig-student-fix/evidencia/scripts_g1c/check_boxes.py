import sys, json, itertools; sys.path.insert(0,'.')
from layout3 import SN
from geo import load_sizes
def check(key, f):
    d=json.load(open(f)); pos={k:tuple(v) for k,v in d['pos'].items()}; boxes=d['boxes']
    sizes=load_sizes(key,SN[key]['nodes'])
    for n in pos:
        if n.startswith('Reroute'): sizes[n]=dict(w=50,h=50)
    out={}
    out['fuera_rejilla']=[n for n,p in pos.items() if p[0]%50 or p[1]%50]+[b['title'] for b in boxes if b['pos'][0]%50 or b['pos'][1]%50 or b['size'][0]%50 or b['size'][1]%50]
    marg=[];sin=[];ajena=[]
    for n,p in pos.items():
        w,h=sizes[n]['w'],sizes[n]['h']
        inside=[b for b in boxes if b['pos'][0]<=p[0] and b['pos'][1]<=p[1] and p[0]+w<=b['pos'][0]+b['size'][0] and p[1]+h<=b['pos'][1]+b['size'][1]]
        part=[b for b in boxes if b['pos'][0]<p[0]+w and p[0]<b['pos'][0]+b['size'][0] and b['pos'][1]<p[1]+h and p[1]<b['pos'][1]+b['size'][1]]
        if n.startswith('Reroute'):
            if part: ajena.append((n,[b['title'] for b in part]))
            continue
        if len(inside)!=1 or len(part)!=1: ajena.append((n,[b['title'] for b in part])); continue
        b=inside[0]
        marg.append((n,min(p[0]-b['pos'][0],p[1]-b['pos'][1]-250 if False else p[1]-b['pos'][1],b['pos'][0]+b['size'][0]-p[0]-w,b['pos'][1]+b['size'][1]-p[1]-h)))
        if n not in b['nodes']: ajena.append((n,'no listado en '+b['title']))
    out['margen_min']=min(m for _,m in marg); out['peor']=sorted(marg,key=lambda x:x[1])[:3]
    out['nodo_en_caja_ajena_o_reroute_dentro']=ajena
    out['solapes_cajas']=[(a['title'],b['title']) for a,b in itertools.combinations(boxes,2) if a['pos'][0]<b['pos'][0]+b['size'][0] and b['pos'][0]<a['pos'][0]+a['size'][0] and a['pos'][1]<b['pos'][1]+b['size'][1] and b['pos'][1]<a['pos'][1]+a['size'][1]]
    # huecos entre cajas (vertical/horizontal)
    return out
if __name__=='__main__':
    print(check(sys.argv[1],sys.argv[2]))

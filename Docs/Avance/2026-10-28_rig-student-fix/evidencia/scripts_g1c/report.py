import sys; sys.path.insert(0,".")
from layout3 import *
def rep(key, pos, sizes, links, tag):
    m = metrics(pos, sizes, links)
    print(tag, key, 'enlaces', m['enlaces'], 'retroceso', len(m['retroceso']), 'largos>1500', len(m['largos']), 'cruces', len(m['cruces']), 'cable_sobre_nodo', len(m['cable_sobre_nodo']), 'solapes', len(m['solapes']))
    return m
if __name__=='__main__':
    for key in SN:
        d=SN[key]; sizes=load_sizes(key,d['nodes'])
        for n in d['nodes']:
            if n.startswith('Reroute'): sizes[n]=dict(w=50,h=50,rows=[],medido='estimado')
        pos={n:tuple(v['pos']) for n,v in d['nodes'].items() if v['cls']!='RigVMCommentNode'}
        links=[tuple(l) for l in d['links']]
        m=rep(key,pos,sizes,links,'ANTES(tam. reales)')
        print(' ',m['retroceso'][:5],m['largos'][:5],m['solapes'][:6])
        print(' cruces',m['cruces'][:12]); print(' sobre',m['cable_sobre_nodo'][:12])

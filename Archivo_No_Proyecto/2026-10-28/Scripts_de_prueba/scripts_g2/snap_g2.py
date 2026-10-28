"""Snapshot G2: AnimGraph + todos los subgrafos (estados, transiciones). Uso: python -B -I snap_g2.py out.json"""
import sys,json
sys.path.insert(0,'.')
from u import *
w=json.load(open('walk0.json'))
PRE='/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix:'
res={}
for o in w['out']:
    gp=o['g']; short=gp.replace(PRE,'')
    g={'refPath':gp}
    ns=T(BP,'find_nodes',{'graph':g,'title':'','node_class':'','entry_points_only':False})
    nodes={};edges=[];vals={}
    if isinstance(ns,list):
        for i in range(0,len(ns),15):
            infs=T(BP,'get_node_infos',{'nodes':ns[i:i+15]})
            if not isinstance(infs,list): nodes['ERR'+str(i)]=str(infs)[:200]; continue
            for inf in infs:
                nn=inf['node']['refPath'].replace(gp+'.','')
                nodes[nn]={'x':round(inf['position']['x']),'y':round(inf['position']['y']),'type':inf.get('type_id')}
                for p in inf['input_pins']:
                    if p.get('value') not in (None,''): vals[nn+'.'+p['name']]=p['value']
                    for cp in p['connected_pins']:
                        edges.append([cp['node']['refPath'].replace(gp+'.','')+'#o'+str(cp['index_id']),nn+'.'+p['name']])
    res[short]={'nodes':nodes,'edges':sorted(edges),'vals':vals}
json.dump(res,open(sys.argv[1],'w'),indent=1,ensure_ascii=False)
print(len(res),sum(len(v['nodes']) for v in res.values()),sum(len(v['edges']) for v in res.values()))

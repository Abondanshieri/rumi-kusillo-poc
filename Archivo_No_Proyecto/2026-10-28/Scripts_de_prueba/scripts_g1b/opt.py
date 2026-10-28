import json,sys,itertools,re
sys.path.insert(0,'.')
import layout2 as L
src=open('layout2.py',encoding='utf8').read()
d=json.load(open('../snap_g1_base2.json'))['CR_Student_Procedural_fix']
links=[tuple(l) for l in d['links']]
best=None
cands={'Add_HipsZ':[(5,0),(5,650),(5,900),(6,700),(5,1000)],
       'Add_LeftFootZ':[(6,0),(6,650),(6,800),(6,900)],
       'Add_RightFootZ':[(7,0),(7,650),(7,800),(7,900)],
       'Clamp_LeftOffset':[(5,0),(5,850),(5,950)],'Clamp_RightOffset':[(6,0),(6,850),(6,950)]}
names=list(cands)
for combo in itertools.product(*[cands[n] for n in names]):
    s=src
    for n,(c,y) in zip(names,combo):
        s=re.sub(r"'%s':\(\d,\d+\)"%n,"'%s':(%d,%d)"%(n,c,y),s)
    ns={}; exec(compile(s.split("if __name__")[0],'x','exec'),ns)
    pos,_=ns['proc']()
    m=ns['metrics'](pos,links)
    key=(m['solapes'],m['back'],m['long'],m['cruces'])
    if best is None or key<best[0]: best=(key,combo)
print(best)

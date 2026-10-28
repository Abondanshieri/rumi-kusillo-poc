import json,sys,itertools,re
sys.path.insert(0,'.')
src=open('layout2.py',encoding='utf8').read()
d=json.load(open('../snap_g1_base2.json'))['CR_Student_Procedural_fix']
links=[tuple(l) for l in d['links']]
def setp(s,n,c,y): return re.sub(r"'%s':\(\d,-?\d+\)"%n,"'%s':(%d,%d)"%(n,c,y),s)
best=None
slots=[0,300,600,900]
for side,(c5,c6,c7,g,cl,mk,az,mu,tb) in (('L',(5,6,7,'Get_LeftFoot','Clamp_LeftOffset','Make_LeftFoot_Offset','Add_LeftFootZ','Mul_LeftFoot_Offset','TwoBoneIK_Left')),):
  for p5 in itertools.permutations(slots,3):
    for p6 in itertools.permutations(slots,2):
      for tby in (0,150,300,450):
        s=src
        for n,y in zip((g,cl,mk),p5): s=setp(s,n,c5,y)
        for n,y in zip((az,mu),p6): s=setp(s,n,c6,y)
        s=setp(s,tb,c7,tby)
        ns={}; exec(compile(s.split("if __name__")[0],'x','exec'),ns)
        pos,_=ns['proc'](); m=ns['metrics'](pos,links)
        key=(m['solapes'],m['back'],m['cruces'])
        if best is None or key<best[0]: best=(key,p5,p6,tby)
print(best)

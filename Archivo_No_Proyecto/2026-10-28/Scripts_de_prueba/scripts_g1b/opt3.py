import json,sys,itertools,re
sys.path.insert(0,'.')
src=open('layout2.py',encoding='utf8').read()
d=json.load(open('../snap_g1_base2.json'))['CR_Student_Procedural_fix']
links=[tuple(l) for l in d['links']]
def setp(s,n,c,y): return re.sub(r"'%s':\((\d),-?\d+\)"%n,lambda m:"'%s':(%s,%d)"%(n,m.group(1),y),s)
best=None
for gy in itertools.permutations((700,850,1000,550)[:2]+(),2):
  pass
for ga in ((700,850),(850,700),(700,1000),(1000,700),(900,1050),(1050,900),(1200,1350),(1350,1200)):
  for a in ((650,900),(900,650)):
    for b in ((1400,1650),(1650,1400)):
      s=src
      s=setp(s,'Get_LeanPitch',0,ga[0]); s=setp(s,'Get_LeanRoll',0,ga[1])
      s=setp(s,'Mul_Pitch_Spine2',1,a[0]); s=setp(s,'Mul_Roll_Spine2',1,a[1])
      s=setp(s,'Mul_Pitch_Neck',2,b[0]); s=setp(s,'Mul_Roll_Neck',2,b[1])
      ns={}; exec(compile(s.split("if __name__")[0],'x','exec'),ns)
      pos,_=ns['proc'](); m=ns['metrics'](pos,links)
      key=(m['solapes'],m['back'],m['cruces'],m['long'])
      if best is None or key<best[0]: best=(key,ga,a,b)
print(best)

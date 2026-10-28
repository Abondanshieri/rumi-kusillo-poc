import sys; sys.path.insert(0,'.')
from u import *
from snaprig import SNAP_CODE
code=SNAP_CODE+'''
R="/Game/Characters/Student/Rig/"
for k,a in [("PR_fix","CR_Student_Procedural_fix"),("IK_fix","CR_Student_IK_fix"),("PR_orig","CR_Student_Procedural"),("IK_orig","CR_Student_IK")]:
    res[k]=snap_rig(R+a+"."+a)
'''
r=pyrun(code,'snap_now.out',wait=30)
json.dump(r,open('snap_ronda6_inicio.json','w'),indent=1)
for k,v in r.items():
    if k=='EXC': print(v); continue
    print(k,len(v['nodes']),'nodos',len(v['links']),'enlaces pin->pin',v['npins'],'pines')

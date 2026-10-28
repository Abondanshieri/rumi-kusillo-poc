import sys; sys.path.insert(0,'.')
from u import *
base='/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix:'
names=['nodeComment','nodePosX','nodePosY','nodeWidth','nodeHeight','fontSize','commentColor']
for gn in ['AnimGraph','EventGraph','UpdateProceduralVariables','TestFunc']:
    for n in range(0,40):
        r=base+gn+'.EdGraphNode_Comment_%d'%n
        t=T(OB,'get_properties',{'instance':{'refPath':r},'properties':names})
        if isinstance(t,str) and ('not' in t.lower() and ('found' in t.lower() or 'valid' in t.lower() or 'exist' in t.lower())): continue
        print(gn,n,str(t)[:300].replace('\n',' '))

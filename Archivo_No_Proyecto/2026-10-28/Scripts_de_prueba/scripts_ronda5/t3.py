import sys; sys.path.insert(0,'.')
from u import *
bp={'refPath':'/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'}
for gn in ['AnimGraph','EventGraph','UpdateProceduralVariables','TestFunc']:
    g=T(BP,'get_graph',{'blueprint':bp,'graph_name':gn})
    s=json.dumps(g)
    print(gn,len(s), s[:400])
    break

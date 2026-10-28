import sys; sys.path.insert(0,'.')
from u import *
L=snap()
tab=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "Student_Skeleton_AnimBlueprint_fix"')][0]
S('Click',{'ref':tab}); time.sleep(2)
L=snap()
for l in L:
    if re.search(r'^\s*tab "(EventGraph|AnimGraph|UpdateProceduralVariables)"',l) or 'INIT (' in l or 'Set references' in l: print(l.strip()[:150])

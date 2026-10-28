import sys,re,json; sys.path.insert(0,'.')
from u import *
a,g=cr('PR')
ns=T(CR,'list_nodes',{'control_rig':a,'graph':g})
names=sorted(n['refPath'].split('.')[-1] for n in ns)
old=json.load(open('../snap_ronda4/CR_Student_Procedural_fix.json'))
print(set(names)^set(old['nodes']))
for n in names:
    if n.startswith('VariableNode'):
        print(n,T(CR,'get_node_position',{'control_rig':a,'node':{'refPath':g['refPath']+'.'+n}}),old['nodes'][n])

import sys,re; sys.path.insert(0,'.')
from u import *
S('PressKey',{'key':'Escape'})
a,g=cr('PR')
n0=len(T(CR,'list_nodes',{'control_rig':a,'graph':g}))
r=T(CR,'add_variable_node',{'control_rig':a,'graph':g,'variable_name':'LeanRoll','is_getter':True,'position':{'x':9000,'y':9000}})
print('nuevo nodo:',r)
ns=T(CR,'list_nodes',{'control_rig':a,'graph':g}); print(n0,len(ns))
# intentar renombrar via ObjectTools set_properties sobre el nodo
ref=r['refPath'] if isinstance(r,dict) else None
for p in ('nodeTitle','NodeTitle','name','Name'):
    print(p, repr(T(OB,'set_properties',{'instance':{'refPath':ref},'values':json.dumps({p:'LeanRoll_L'})}))[:200])
print(T(CR,'delete_node',{'control_rig':a,'graph':g,'node':{'refPath':ref}}))
print(len(T(CR,'list_nodes',{'control_rig':a,'graph':g})))

import sys; sys.path.insert(0,".")
from pasteops import *
gn=sys.argv[1]
g,base,before=read_nodes(gn)
set_clip(t3d_knot('K2Node_Knot_9990',0,0))
for t in range(6):
    ok=atomic_paste(gn); print('intento',t,ok,where())
    g,base,after=read_nodes(gn)
    if after-before: break
    time.sleep(1)
new=after-before; print('nuevos',new)
for n in new:
    inf=J('get_node_infos',{'nodes':[{'refPath':base+n}]})[0]; print(n,inf['position'])

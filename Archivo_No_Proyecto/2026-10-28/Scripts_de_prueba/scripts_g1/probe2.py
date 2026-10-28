import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
C=unreal.RigVMController
res["d"]={m:(getattr(C,m).__doc__ or "")[:600] for m in ("set_comment_text_by_name","set_node_color_by_name","set_node_size_by_name","add_comment_node","add_reroute_node_on_link")}
'''
r=pyrun(CODE,'probe2.out')
for k,v in r["d"].items(): print(k,"\n",v,"\n")

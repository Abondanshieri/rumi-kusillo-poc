import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
out={}
for k in ["CR_Student_Procedural_fix","CR_Student_IK_fix"]:
    bp=unreal.load_asset("/Game/Characters/Student/Rig/%s.%s"%(k,k))
    g=bp.get_controller_by_name("RigVMModel").get_graph()
    L=[]
    for n in g.get_nodes():
        if n.get_class().get_name()=="RigVMCommentNode":
            c=n.get_node_color(); p=n.get_position(); s=n.get_size()
            L.append(dict(nombre=str(n.get_name()),texto=str(n.get_comment_text()),pos=[p.x,p.y],size=[s.x,s.y],fuente=n.get_comment_font_size(),color=[round(c.r,2),round(c.g,2),round(c.b,2),round(c.a,2)]))
    out[k]=L
res=out
'''
r=pyrun(CODE,'livecom.out')
json.dump(r,open('../g1c_comentarios_vivo.json','w'),indent=1,ensure_ascii=False)
for k,v in r.items():
    if k=='EXC': print(v); continue
    for c in v: print(k[-14:],c['texto'],c['pos'],c['size'],c['fuente'],c['color'])

import sys; sys.path.insert(0,'.')
from u import *
code='''
R="/Game/Characters/Student/Rig/"
cfg={"CR_Student_Procedural_fix":(120,150),"CR_Student_IK_fix":(90,120)}
for a,(font,up) in cfg.items():
    bp=unreal.load_asset(R+a+"."+a); ctrl=bp.get_controller_by_name("RigVMModel")
    log=[]
    for n in ctrl.get_graph().get_nodes():
        if n.get_class().get_name()!="RigVMCommentNode": continue
        p=n.get_position(); s=n.get_size(); txt=str(n.get_comment_text())
        old=[txt,n.get_comment_font_size(),[p.x,p.y],[s.x,s.y]]
        w=s.x
        if txt=="ORFANO": w=max(w,560)
        ok1=ctrl.set_comment_text(n,txt,font,True,True)
        ok2=ctrl.set_node_position(n,unreal.Vector2D(p.x,p.y-up))
        ok3=ctrl.set_node_size(n,unreal.Vector2D(w,s.y+up))
        p2=n.get_position(); s2=n.get_size()
        log.append({"nombre":str(n.get_name()),"antes":old,"ahora":[txt,n.get_comment_font_size(),[p2.x,p2.y],[s2.x,s2.y]],"ok":[ok1,ok2,ok3]})
    res[a]=log
'''
r=pyrun(code,'fix_cr.out',wait=20)
json.dump(r,open('cr_comentarios_ajuste.json','w'),indent=1)
for k,v in r.items():
    if k=='EXC': print(v);continue
    for x in v: print(k,x['nombre'],x['antes'][0],x['antes'][1:],'->',x['ahora'][1:],x['ok'])

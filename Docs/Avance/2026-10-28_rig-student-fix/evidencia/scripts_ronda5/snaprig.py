# Snapshot completo (nodos, pines recursivos, enlaces pin->pin) de un Control Rig via Python de editor.
SNAP_CODE='''
def snap_rig(p):
    bp=unreal.load_asset(p); ctrl=bp.get_controller_by_name("RigVMModel"); g=ctrl.get_graph()
    nodes={}; links=[]; npins=0
    for n in g.get_nodes():
        nm=str(n.get_name()); cl=n.get_class().get_name()
        pp=n.get_position(); s=n.get_size()
        d={"cls":cl,"title":str(n.get_node_title()),"pos":[pp.x,pp.y],"size":[s.x,s.y]}
        if cl=="RigVMCommentNode":
            d["text"]=str(n.get_comment_text()); d["font"]=n.get_comment_font_size(); d["bubble"]=n.get_comment_bubble_visible()
        if cl=="RigVMVariableNode": d["var"]=str(n.get_variable_name())
        nodes[nm]=d
        try: pins=n.get_all_pins_recursively()
        except Exception: pins=n.get_pins()
        for pin in pins:
            npins+=1
            for t in pin.get_linked_target_pins():
                links.append([str(pin.get_pin_path()),str(t.get_pin_path())])
    return {"nodes":nodes,"links":links,"npins":npins}
'''

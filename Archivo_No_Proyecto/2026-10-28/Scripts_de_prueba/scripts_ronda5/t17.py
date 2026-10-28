import sys; sys.path.insert(0,'.')
from u import *
code='''
a="CR_Student_Procedural_fix"
bp=unreal.load_asset("/Game/Characters/Student/Rig/"+a+"."+a)
sub=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
sub.close_all_editors_for_asset(bp)
res["cerrado"]=True
res["abrir"]=sub.open_editor_for_assets([bp])
'''
print(pyrun(code,'o17.out',wait=20))

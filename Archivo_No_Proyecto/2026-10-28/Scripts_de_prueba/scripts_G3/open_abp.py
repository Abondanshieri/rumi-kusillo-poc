import sys; sys.path.insert(0,'.')
from g3u import *
r=pyrun('''
bp=unreal.load_asset("/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix")
sub=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
res["abrir"]=sub.open_editor_for_assets([bp])
''','ab.out',wait=20)
print(r)
time.sleep(4)
L=snap()
for l in L:
    if re.search(r'tab "|Zoom|EventGraph|UpdateProc',l): print(l[:150])

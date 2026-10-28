import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
for k in ["CR_Student_Procedural_fix","CR_Student_IK_fix"]:
    bp=unreal.load_asset("/Game/Characters/Student/Rig/%s.%s"%(k,k))
    res[k]=unreal.EditorAssetLibrary.save_loaded_asset(bp,False)
    res[k+"_dirty"]=unreal.EditorAssetLibrary.get_metadata_tag(bp,"x") if False else None
'''
print(pyrun(CODE,'save.out'))

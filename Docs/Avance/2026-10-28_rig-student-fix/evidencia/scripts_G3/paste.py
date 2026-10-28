import sys,subprocess,uuid; sys.path.insert(0,'.')
from ui import *
from g3lib import G,J,EV
ABP='/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'
def guid(): return uuid.uuid4().hex.upper()
def set_clip(text):
    f=SP+'_clip.txt'; open(f,'w',encoding='utf8').write(text)
    subprocess.run(['powershell','-NoProfile','-Command','Get-Content -Raw -Encoding UTF8 "%s" | Set-Clipboard'%f],check=True)
def t3d_knot(name,x,y):
    return ('Begin Object Class=/Script/BlueprintGraph.K2Node_Knot Name="%s"\n   NodePosX=%d\n   NodePosY=%d\n   NodeGuid=%s\nEnd Object\n')%(name,x,y,guid())
def t3d_comment(name,x,y,w,h,text,col,font):
    return ('Begin Object Class=/Script/UnrealEd.EdGraphNode_Comment Name="%s"\n   NodePosX=%d\n   NodePosY=%d\n   NodeWidth=%d\n   NodeHeight=%d\n   NodeComment="%s"\n   CommentColor=(R=%.4f,G=%.4f,B=%.4f,A=%.4f)\n   FontSize=%d\n   NodeGuid=%s\nEnd Object\n')%(name,x,y,w,h,text,col[0],col[1],col[2],col[3],font,guid())

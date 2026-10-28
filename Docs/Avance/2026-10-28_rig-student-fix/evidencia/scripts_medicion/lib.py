from m import *
import math,time
E="EditorToolset.EditorAppToolset"
S="editor_toolset.toolsets.scene.SceneTools"
fs=J(S,"find_actors",{"name":"ProbeDriver","tag":"","collision_channels":[]})
PD=({'refPath':fs[0]['refPath'].replace('/Game/AnimTest/Lvl_AnimTest.Lvl_AnimTest','/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest')} if fs else None)
ABP={'refPath':CH['refPath']+'.CharacterMesh0.Student_Skeleton_AnimBlueprint_fix_C_0'}
bones=["Hips","LeftUpLeg","LeftLeg","LeftFoot","LeftToeBase","RightUpLeg","RightLeg","RightFoot","RightToeBase"]
PR=["P_"+b for b in bones]+["R_LeftFoot","R_RightFoot","R_Hips","ActorLoc"]
def sample():
    d=J(OT,"get_properties",{"instance":PD,"properties":PR})
    if isinstance(d,str): d=json.loads(d)
    return d
def v(p): return (p['x'],p['y'],p['z'])
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a,a))
def ang(a,b): return math.degrees(math.acos(max(-1,min(1,dot(a,b)/(norm(a)*norm(b))))))
def metrics(d):
    out={}
    for s in ("Left","Right"):
        hip=v(d[f"P_{s}UpLeg"]);kn=v(d[f"P_{s}Leg"]);an=v(d[f"P_{s}Foot"]);to=v(d[f"P_{s}ToeBase"])
        th=sub(kn,hip);sh=sub(an,kn)
        flex=ang(th,sh)
        ha=sub(an,hip);t=dot(sub(kn,hip),ha)/dot(ha,ha)
        proj=tuple(h+t*x for h,x in zip(hip,ha))
        dev=sub(kn,proj)  # knee offset from hip-ankle line
        f=sub(to,an)
        fyaw=math.degrees(math.atan2(f[1],f[0])); fpitch=math.degrees(math.atan2(f[2],math.hypot(f[0],f[1])))
        out[s]=dict(flex=round(flex,1),kneeDevX=round(dev[0],2),kneeDevY=round(dev[1],2),kneeDevZ=round(dev[2],2),footYaw=round(fyaw,1),footPitch=round(fpitch,1),thighLen=round(norm(th),1),shinLen=round(norm(sh),1),ankleY=round(an[1]-v(d["ActorLoc"])[1],1),kneeY=round(kn[1]-v(d["ActorLoc"])[1],1),hipY=round(hip[1]-v(d["ActorLoc"])[1],1),ankleZ=round(an[2]-v(d["ActorLoc"])[2],1),kneeZ=round(kn[2]-v(d["ActorLoc"])[2],1))
    return out
def alpha(a):
    return J(OT,"set_properties",{"instance":NODE,"values":{"alpha":a}})
B="editor_toolset.toolsets.blueprint.BlueprintTools"
ABPA={'refPath':'/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'}
NODE={'refPath':ABPA['refPath']+':AnimGraph.AnimGraphNode_ControlRig_1'}
def alpha_pin():
    i=J(B,"get_node_infos",{"nodes":[NODE]})[0]
    return [p for p in i['input_pins'] if p['name']=='Alpha'][0]
def set_alpha(a):
    p=alpha_pin()
    r=J(B,"set_pin_value",{"pin":p['pin_id'],"value":str(float(a))})
    J(OT,"set_properties",{"instance":NODE,"values":json.dumps({"node":{"alpha":a}})})
    c_=J(B,"compile_blueprint",{"blueprint":ABPA,"warnings_as_errors":False})
    return r,c_,alpha_pin()['value']
def get_alpha():
    r=J(OT,"get_properties",{"instance":NODE,"properties":["node"]})
    if isinstance(r,str): r=json.loads(r)
    return r["node"]["alpha"]
def teleport(x,y,z,yaw=0):
    return J("editor_toolset.toolsets.actor.ActorTools","set_actor_transform",{"actor":CH,"xform":{"location":{"x":x,"y":y,"z":z},"rotation":{"pitch":0,"yaw":yaw,"roll":0},"scale":{"x":1,"y":1,"z":1}},"worldspace":True})
def drive(dx,dy,scale):
    return J(OT,"set_properties",{"instance":PD,"values":json.dumps({"driveDir":{"x":dx,"y":dy,"z":0},"driveScale":scale})})
def collect(n,dt=0.05):
    res=[]
    for _ in range(n):
        res.append(metrics(sample())); time.sleep(dt)
    return res
def summarize(res):
    out={}
    for s in ("Left","Right"):
        out[s]={}
        for k in res[0][s]:
            vals=[r[s][k] for r in res]
            out[s][k]=(round(min(vals),1),round(sum(vals)/len(vals),1),round(max(vals),1))
    return out
C="animation_toolset.toolsets.controlrig.ControlRigTools"
RIG={'refPath':'/Game/Characters/Student/Rig/CR_Student_Procedural_fix.CR_Student_Procedural_fix'}
GR={'refPath':RIG['refPath']+':RigVMModel'}
def pin(node,name): return {'refPath':RIG['refPath']+':RigVMModel.'+node+'.'+name}
def getpin(node,name): return J(C,"get_pin_value",{"control_rig":RIG,"pin":pin(node,name)})
def setpin(node,name,val): 
    r=J(C,"set_pin_value",{"control_rig":RIG,"graph":GR,"pin":pin(node,name),"value":val}); return r
import base64
def capvp(name,loc,rot,annot=False):
    args={"captureTransform":{"location":{"x":loc[0],"y":loc[1],"z":loc[2]},"rotation":{"pitch":rot[0],"yaw":rot[1],"roll":rot[2]},"scale":{"x":1,"y":1,"z":1}},"annotations":[],"bShowUI":False}
    r=c.run_tool(E,"CaptureViewport",args)
    t=r["content"][0]["text"]
    try:
        j=json.loads(t)["returnValue"]["image"]
    except Exception:
        return t[:300]
    open(name+".png","wb").write(base64.b64decode(j["data"])); return "ok "+j.get("mimeType","")
def capeditor(name):
    r=c.run_tool(E,"CaptureEditorImage",{})
    j=json.loads(r["content"][0]["text"])["returnValue"]
    open(name+".png","wb").write(base64.b64decode(j["data"])); return j.get("mimeType")
BOOM={'refPath':CH['refPath']+'.CameraBoom'}
CAM={'refPath':CH['refPath']+'.FollowCamera'}
ORIG_BOOM={"targetArmLength":600,"socketOffset":{"x":0,"y":0,"z":0},"bUsePawnControlRotation":True,"relativeRotation":{"pitch":0,"yaw":0,"roll":0},"bDoCollisionTest":True}
ORIG_CAM={"relativeRotation":{"pitch":-25,"yaw":0,"roll":0},"relativeLocation":{"x":0,"y":0,"z":150},"fieldOfView":90}
def cam_leg(yaw,arm=110,fov=50,dz=-45):
    a=J(OT,"set_properties",{"instance":BOOM,"values":json.dumps({"bUsePawnControlRotation":False,"bDoCollisionTest":False,"targetArmLength":arm,"socketOffset":{"x":0,"y":0,"z":dz},"relativeRotation":{"pitch":0,"yaw":yaw,"roll":0}})})
    b=J(OT,"set_properties",{"instance":CAM,"values":json.dumps({"relativeRotation":{"pitch":0,"yaw":0,"roll":0},"relativeLocation":{"x":0,"y":0,"z":0},"fieldOfView":fov})})
    return a,b
def cam_restore():
    a=J(OT,"set_properties",{"instance":BOOM,"values":json.dumps(ORIG_BOOM)})
    b=J(OT,"set_properties",{"instance":CAM,"values":json.dumps(ORIG_CAM)})
    return a,b
def legcam_ref():
    a=J(S,"find_actors",{"name":"LegCam","tag":"","collision_channels":[]})
    return a[0]
def place_cam(ref,loc,pitch,yaw):
    return J("editor_toolset.toolsets.actor.ActorTools","set_actor_transform",{"actor":ref,"xform":{"location":{"x":loc[0],"y":loc[1],"z":loc[2]},"rotation":{"pitch":pitch,"yaw":yaw,"roll":0},"scale":{"x":1,"y":1,"z":1}},"worldspace":True})
def shot(name,ref,view,dist=125,dz=-67,pitch=0,fov=40,yaw=None):
    cc={'refPath':ref['refPath']+'.CameraComponent'}
    J(OT,"set_properties",{"instance":cc,"values":json.dumps({"fieldOfView":fov})})
    a=sample()['ActorLoc']
    x,y,z=a['x'],a['y'],a['z']+dz
    if yaw is None: yaw={'front':180,'back':0,'side':90,'sideR':-90}[view]
    import math as _m
    # camera sits opposite to its look direction
    px=x-dist*_m.cos(_m.radians(yaw)); py=y-dist*_m.sin(_m.radians(yaw))
    place_cam(ref,(px,py,z),pitch,yaw)
    time.sleep(0.8)
    return capeditor(name)
from PIL import Image
CAPDIR="D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/capturas/"
SPD="C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion_Grafica-Rumi-5-8/".replace("Computacion_Grafica-Rumi","Computacion-Grafica-Rumi")
def cropvp(name,out,box=(242,172,1030,614),scale=1):
    im=Image.open(name+".png").crop(box)
    if scale!=1: im=im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
    im.save(out); return out

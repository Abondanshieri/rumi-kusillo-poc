from lib import *
import sys
def start():
    run(E,"StopPIE"); time.sleep(2); run(E,"StartPIE",{"options":{}}); time.sleep(7)
def speed():
    r=J(OT,"get_properties",{"instance":ABP,"properties":["GroundSpeed","IsFalling"]}); return r
def scenario(name,scale,n=40,dt=0.04,x0=-2000):
    teleport(x0,0,120); drive(1,0,0); time.sleep(1.2)
    drive(1,0,scale); time.sleep(1.0)
    sp=speed()
    res=collect(n,dt)
    drive(1,0,0)
    return name,sp,summarize(res),res
def dil(x):
    return run(OT,"set_properties",{"instance":CH,"values":json.dumps({"customTimeDilation":x})})
def run_all(tag,al_list=(1.0,0.0),dil_v=0.1,n=36,scen=(("idle",0.0),("walk",0.35),("run",1.0)),out=None):
    ALL={}
    for al in al_list:
        run(E,"StopPIE"); time.sleep(2)
        set_alpha(al); start(); print("alpha",get_alpha(),flush=True)
        dil(dil_v)
        for nm,sc in scen:
            teleport(-3500,0,120); drive(1,0,0); time.sleep(1.0)
            drive(1,0,sc); time.sleep(0.5)
            sp=speed(); res=collect(n,0.0); drive(1,0,0)
            d=sample()
            ALL[f"{nm}_a{al}"]=dict(speed=sp,sum=summarize(res),actorX=d['ActorLoc']['x'],actorZ=d['ActorLoc']['z'],raw=res)
            print(nm,al,sp,round(d['ActorLoc']['x']),round(d['ActorLoc']['z'],1),flush=True)
    json.dump(ALL,open(out or f"meas_{tag}.json","w"))
    print("FIN",flush=True)
    return ALL
def frozen_idle_shots(al,tag,views=('front','side','back'),dist=125,dz=-67):
    run(E,"StopPIE"); time.sleep(2); set_alpha(al); start()
    ref=legcam_ref()
    teleport(-3500,0,120); time.sleep(3.0)
    dil(0.0001); time.sleep(0.6)
    out=[]
    for v in views:
        n=f"{tag}_{v}"
        shot(n,ref,v,dist=dist,dz=dz); cropvp(n,n+"_c.png"); out.append(n+"_c.png")
    d=sample(); m=metrics(d)
    return out,m
import random
def setup_pole(cfg):
    run(E,"StopPIE"); time.sleep(2)
    f=lambda x,y,z:f"(X={x:.6f},Y={y:.6f},Z={z:.6f})"
    if cfg=="direction":
        for n in ("TwoBoneIK_Left","TwoBoneIK_Right"):
            setpin(n,"PoleVectorKind","Direction"); setpin(n,"PoleVector",f(0,1,0))
    else:
        setpin("TwoBoneIK_Left","PoleVectorKind","Location"); setpin("TwoBoneIK_Left","PoleVector",f(6.07,60,28.1))
        setpin("TwoBoneIK_Right","PoleVectorKind","Location"); setpin("TwoBoneIK_Right","PoleVector",f(-5.78,60,28.1))
def phases(nm,scale,nph=8,x0=-3500):
    out=[]
    CMC={'refPath':CH['refPath']+'.CharMoveComp'}
    for i in range(nph):
        dil(1.0); teleport(x0,0,120); drive(1,0,0); time.sleep(0.8)
        if nm=="jump":
            drive(1,0,0.6); time.sleep(0.6)
            J(OT,"set_properties",{"instance":CMC,"values":json.dumps({"velocity":{"x":300,"y":0,"z":650}})})
            J(OT,"set_properties",{"instance":CMC,"values":json.dumps({"movementMode":"MOVE_Falling"})})
            time.sleep(random.uniform(0.05,0.9))
        else:
            drive(1,0,scale); time.sleep(0.9+random.uniform(0,0.5))
        dil(0.0001); drive(1,0,0); time.sleep(0.15)
        d=sample(); out.append((metrics(d),d['ActorLoc'],speed()))
    dil(1.0); drive(1,0,0)
    return out
def run_cfg(tag,al,pole,scen=(("idle",0.0),("walk",0.35),("run",1.0),("jump",0.0)),nph=8):
    setup_pole(pole); set_alpha(al); start()
    res={}
    for nm,sc in scen:
        res[nm]=phases(nm,sc,nph if nm!="idle" else 3)
        print(tag,nm,"done",flush=True)
    return res

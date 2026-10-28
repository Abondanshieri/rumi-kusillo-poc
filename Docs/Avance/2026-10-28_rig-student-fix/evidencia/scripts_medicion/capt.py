from sweep import *
import sys,math
def hsig(d):
    a=v(d["P_Hips"]); return [tuple(x-y for x,y in zip(v(d[f"P_{s}Foot"]),a)) for s in ("Left","Right")]
def hd(d1,d2):
    return math.sqrt(sum(sum((x-y)**2 for x,y in zip(p,r)) for p,r in zip(hsig(d1),hsig(d2))))
OFFS=json.load(open(OUT+"sweep_OFF.json"))
TARGETS={"walk":OFFS["walk"][30],"run":OFFS["run"][20],"jump":OFFS["jump"][22]}
THR={'walk':0.35,'run':0.8,'jump':1.0}
def go_phase(nm,sc,dv):
    dil(1.0); teleport(-3500,0,120); drive(1,0,0); time.sleep(1.0)
    if nm=="jump": drive(1,0,0.6); time.sleep(0.8)
    else: drive(1,0,sc); time.sleep(1.2)
    dil(dv)
    if nm=="jump":
        J(OT,"set_properties",{"instance":CMC,"values":json.dumps({"velocity":{"x":300,"y":0,"z":650}})})
        J(OT,"set_properties",{"instance":CMC,"values":json.dumps({"movementMode":"MOVE_Falling"})})
    best=None
    mn=9e9
    for i in range(300):
        d=sample(); r=hd(d,TARGETS[nm]); mn=min(mn,r)
        if (nm!='jump' and r<THR[nm]) or (nm=='jump' and i==14):
            dil(0.0001); drive(1,0,0); time.sleep(0.5)
            d2=sample(); return i,r,hd(d2,TARGETS[nm])
    dil(1.0); drive(1,0,0); print('min res',mn); return None
def shots(tag,box,items):
    run(E,"StopPIE"); time.sleep(2); start()
    ref=legcam_ref()
    log={}
    for nm,sc,dv in items:
        g=go_phase(nm,sc,dv); log[nm]=g; print(tag,nm,g,flush=True)
        if g: json.dump(sample(),open(OUT+f'frozen_{tag}_{nm}.json','w'))
        if g is None: continue
        for view in ("front","side"):
            n=f"{tag}_{nm}_{view}"
            shot(n,ref,view,dist=(520 if nm=='jump' else 300),dz=(0 if nm=='jump' else -45),fov=40)
            if box: cropvp(n,CAPDIR+n+".png",box)
        dil(1.0)
    run(E,"StopPIE")
    return log

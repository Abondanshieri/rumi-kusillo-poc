from exp import *
import sys
OUT="D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/"
CMC={'refPath':CH['refPath']+'.CharMoveComp'}
def sweep(nm,scale,n,dilv):
    dil(1.0); teleport(-3500,0,120); drive(1,0,0); time.sleep(1.0)
    if nm=="jump":
        drive(1,0,0.6); time.sleep(0.8)
    elif scale>0:
        drive(1,0,scale); time.sleep(1.2)
    t0=time.time()
    dil(dilv)
    if nm=="jump":
        J(OT,"set_properties",{"instance":CMC,"values":json.dumps({"velocity":{"x":300,"y":0,"z":650}})})
        J(OT,"set_properties",{"instance":CMC,"values":json.dumps({"movementMode":"MOVE_Falling"})})
    out=[]
    for i in range(n):
        d=sample(); out.append(d)
    dil(1.0); drive(1,0,0)
    return out
def run_sweeps(tag,al,pole,scen):
    setup_pole(pole); print(set_alpha(al)[2:],flush=True); start()
    print("pin",alpha_pin()['value'],flush=True)
    res={}
    for nm,sc,n,dv in scen:
        res[nm]=sweep(nm,sc,n,dv); print(tag,nm,len(res[nm]),flush=True)
        json.dump(res,open(OUT+f"sweep_{tag}.json","w"))
    run(E,"StopPIE")
    return res
if __name__=="__main__":
    tag,al,pole=sys.argv[1],float(sys.argv[2]),sys.argv[3]
    scen=(("idle",0,6,1.0),("walk",0.35,90,0.03),("run",1.0,90,0.03),("jump",0,70,0.05))
    run_sweeps(tag,al,pole,scen)
    print("FIN",flush=True)

from sweep import *
import sys
tag=sys.argv[1]; xl=float(sys.argv[2]); xr=float(sys.argv[3])
run(E,"StopPIE"); time.sleep(2)
f=lambda x,y,z:f"(X={x:.6f},Y={y:.6f},Z={z:.6f})"
setpin("TwoBoneIK_Left","PoleVectorKind","Location"); setpin("TwoBoneIK_Left","PoleVector",f(xl,60,28.1))
setpin("TwoBoneIK_Right","PoleVectorKind","Location"); setpin("TwoBoneIK_Right","PoleVector",f(xr,60,28.1))
print(getpin("TwoBoneIK_Left","PoleVector"),getpin("TwoBoneIK_Right","PoleVector"))
set_alpha(1.0); start()
res={}
for nm,sc,n,dv in (("walk",0.35,90,0.03),("run",1.0,90,0.03),("jump",0,70,0.05)):
    res[nm]=sweep(nm,sc,n,dv); json.dump(res,open(OUT+f"sweep_{tag}.json","w")); print(nm,flush=True)
run(E,"StopPIE")

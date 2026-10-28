from capt import *
import sys
tag=sys.argv[1]; al=float(sys.argv[2])
run(E,"StopPIE"); time.sleep(2)
if tag.endswith("FIX"):
    f=lambda x,y,z:f"(X={x:.6f},Y={y:.6f},Z={z:.6f})"
    setpin("TwoBoneIK_Left","PoleVectorKind","Location"); setpin("TwoBoneIK_Left","PoleVector",f(12,60,28.1))
    setpin("TwoBoneIK_Right","PoleVectorKind","Location"); setpin("TwoBoneIK_Right","PoleVector",f(-12,60,28.1))
set_alpha(al); print("pin",alpha_pin()['value'],get_alpha(),getpin("TwoBoneIK_Left","PoleVector"),getpin("TwoBoneIK_Right","PoleVector"),flush=True)
print(shots(tag,(400,172,870,614),(("jump",0,0.05),)))

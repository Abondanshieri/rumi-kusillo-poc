import json,math,sys,statistics as st
sys.path.insert(0,'.')
from lib import metrics,v,sub,norm
D="D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/"
S={t:json.load(open(D+f"sweep_{t}.json")) for t in ("OFF","DIR","LOC","LOCX0","LOCX12","LOCX20")}
def q(r):
    p,y,ro=[math.radians(r[k])/2 for k in ("pitch","yaw","roll")]
    sp,cp,sy,cy,sr,cr=math.sin(p),math.cos(p),math.sin(y),math.cos(y),math.sin(ro),math.cos(ro)
    return (cr*sp*sy-sr*cp*cy, -cr*sp*cy-sr*cp*sy, cr*cp*sy-sr*sp*cy, cr*cp*cy+sr*sp*sy)
def qang(a,b):
    d=abs(sum(x*y for x,y in zip(a,b)));return math.degrees(2*math.acos(min(1,d)))
def sig(d):
    a=v(d["P_Hips"]); return [tuple(x-y for x,y in zip(v(d[f"P_{s}Foot"]),a)) for s in ("Left","Right")]
def sd(d1,d2):
    s1,s2=sig(d1),sig(d2); return math.sqrt(sum(sum((x-y)**2 for x,y in zip(p,r)) for p,r in zip(s1,s2)))
rows=[];out=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s); out.append(s)
P("A/B a fase IGUALADA: cada muestra del rig ON se empareja con la muestra del rig OFF (misma escena, mismo barrido en camara lenta) de menor distancia entre posiciones de tobillo L+R relativas a la cadera (cm; se quita el desplazamiento global en Z del rig, medido aparte). res = residuo del emparejamiento. Solo se aceptan pares con res <= 1.0 cm.")
P("escena cfg | pares | res med/max cm | flex rango OFF (cubierto) | |lat| OFF med/max | |lat| ON med/max | dFlex med/max | dRotPie(deg) L med/max | R med/max | dToeVec(deg) L / R med/max")
summ={}
for nm in ("idle","walk","run","jump"):
    for cfg in ("DIR","LOCX12"):
        pairs=[]
        for a in S[cfg][nm]:
            best=min(S["OFF"][nm],key=lambda b:sd(a,b)); r=sd(a,best)
            if r<=1.0: pairs.append((a,best,r))
        if not pairs: P(nm,cfg,"sin pares"); continue
        mO=[(metrics(b)) for a,b,r in pairs]; mN=[metrics(a) for a,b,r in pairs]
        res=[r for *_,r in pairs]
        fl=[m[s]["flex"] for m in mO for s in ("Left","Right")]
        latO=[abs(m[s]["kneeDevY"]) for m in mO for s in ("Left","Right")]
        latN=[abs(m[s]["kneeDevY"]) for m in mN for s in ("Left","Right")]
        dfl=[abs(mN[i][s]["flex"]-mO[i][s]["flex"]) for i in range(len(pairs)) for s in ("Left","Right")]
        def rf(key): return [qang(q(a[key]),q(b[key])) for a,b,r in pairs]
        rL,rR=rf("R_LeftFoot"),rf("R_RightFoot")
        def toe(d,s):
            f=sub(v(d[f"P_{s}ToeBase"]),v(d[f"P_{s}Foot"])); return f
        def ang(a,b): return math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(a,b))/(norm(a)*norm(b))))))
        tL=[ang(toe(a,"Left"),toe(b,"Left")) for a,b,r in pairs]; tR=[ang(toe(a,"Right"),toe(b,"Right")) for a,b,r in pairs]
        f=lambda L:"%.2f/%.2f"%(st.median(L),max(L))
        P(f"{nm:4s} {cfg:3s} | {len(pairs):3d}/{len(S[cfg][nm])} | {f(res)} | {min(fl):.0f}-{max(fl):.0f} | {f(latO)} | {f(latN)} | {f(dfl)} | {f(rL)} | {f(rR)} | {f(tL)} / {f(tR)}")
open(D+"tabla_AB_fase_igualada.txt","w").write("\n".join(out)+"\n")

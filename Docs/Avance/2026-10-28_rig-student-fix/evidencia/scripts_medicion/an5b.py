exec(open('an3b.py').read().split("rows=[]")[0])
out=[]
def P(s): print(s); out.append(s)
P("Cambio que el rig introduce en la rodilla respecto a la animacion original, a fase igualada (signed lat = kneeDevY respecto a linea cadera-tobillo, cm; |ON-OFF| por par y pierna)")
for nm in ("idle","walk","run","jump"):
    for cfg in ("DIR","LOCX12"):
        dif=[];hi=[]
        for a in S[cfg][nm]:
            b=min(S["OFF"][nm],key=lambda b:sd(a,b))
            if sd(a,b)>1.0: continue
            ma,mb=metrics(a),metrics(b)
            for s in ("Left","Right"):
                dif.append(abs(ma[s]["kneeDevY"]-mb[s]["kneeDevY"]))
                if abs(ma[s]["kneeDevY"])>1.0: hi.append((s,ma[s]["flex"],ma[s]["kneeDevY"],mb[s]["kneeDevY"]))
        dif.sort()
        P(f"{nm:4s} {cfg}: |ON-OFF| mediana {st.median(dif):.2f}  p90 {dif[int(.9*len(dif))]:.2f}  max {dif[-1]:.2f} cm; n={len(dif)}; muestras ON con |lat|>1cm: {len(hi)}"+(f" ej {hi[:3]}" if cfg=="LOCX12" and hi else ""))
open(D+"tabla_AB_fase_igualada.txt","a").write("\n"+"\n".join(out)+"\n")

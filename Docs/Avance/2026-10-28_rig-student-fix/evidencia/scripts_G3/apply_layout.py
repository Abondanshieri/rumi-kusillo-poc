import sys; sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_G3")
from g3lib import *
from g3layout import *
import plan_upv as U, plan_event as E
APPLY = len(sys.argv)>1 and sys.argv[1]=='apply'
full=json.load(open(EV+'G3b_full_antes.json',encoding='utf8'))
out={}
for mod,gn in ((E,'EventGraph'),(U,'UpdateProceduralVariables')):
    d=full[gn]
    dd=json.load(open(EV+'G3_dump_antes.json',encoding='latin-1'))[gn]
    sizes={m:est_size(n,(dd[m]['w'],dd[m]['h'])) for m,n in d.items()}
    pos,boxes,loc=mod.place(d,sizes,mod.GROUPS,mod.SPEC)
    OFF={'EventGraph':(0,1500),'UpdateProceduralVariables':(0,4300)}[gn]
    pos={m:(x+OFF[0],y+OFF[1]) for m,(x,y) in pos.items()}
    boxes={g:(b[0]+OFF[0],b[1]+OFF[1],b[2],b[3]) for g,b in boxes.items()}
    pos0={m:(n['x'],n['y']) for m,n in d.items()}
    m0=metrics(d,pos0,sizes); m1=metrics(d,pos,sizes)
    groups={g:{'nodes':v['n'],'text':v['text'],'color':v['color'],'box':boxes[g]} for g,v in mod.GROUPS.items()}
    out[gn]={'pos':pos,'sizes':sizes,'groups':groups,'metricas_antes':{k:v for k,v in m0.items() if not k.startswith('_')},'metricas_despues':{k:v for k,v in m1.items() if not k.startswith('_')},'largos_despues':m1['_largos'],'largos_antes':m0['_largos']}
    if APPLY:
        g=G(gn); base=g['refPath']+'.'
        n=0
        for m,(x,y) in pos.items():
            J('set_node_position',{'node':{'refPath':base+m},'pos':{'x':x,'y':y}}); n+=1
        print(gn,'movidos',n)
json.dump(out,open(EV+'G3b_plan.json','w'),indent=1)
print({g:(v['metricas_antes'],v['metricas_despues']) for g,v in out.items()})

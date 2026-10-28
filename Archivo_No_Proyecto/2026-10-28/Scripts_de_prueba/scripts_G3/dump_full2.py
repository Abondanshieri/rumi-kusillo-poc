import sys; sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_G3")
from g3lib import *
out={gn:dump(gn) for gn in ['EventGraph','UpdateProceduralVariables','TestFunc']}
json.dump(out,open(EV+'G3b_full_antes.json','w',encoding='utf8'),indent=1,ensure_ascii=False)
print({k:len(v) for k,v in out.items()})

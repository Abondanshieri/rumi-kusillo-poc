import sys,json,base64,re
sys.path.insert(0,r"D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_comentarios")
from sl import S
SP=r"C:\Users\franc\AppData\Local\Temp\claude\D--Dev-Computacion-Grafica-Rumi-5-8\5d67f835-bc9e-4d91-a005-a97774592cec\scratchpad"
def snap(ref='w1',d=60):
    return json.loads(S('Snapshot',{'ref':ref,'maxDepth':d}))['returnValue']
def shot(name,box=None):
    r=json.loads(S('Screenshot',{'ref':'w1'}))['returnValue']
    p=SP+'/'+name
    open(p,'wb').write(base64.b64decode(r['data']))
    if box:
        from PIL import Image
        Image.open(p).crop(box).save(p)
    return p

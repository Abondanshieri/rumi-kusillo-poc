import sys; sys.path.insert(0,r'D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_comentarios'); sys.path.insert(0,r'C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad')
import mapbp,sl,time,json,re,base64
def snapall(): return json.loads(sl.S('Snapshot',{'ref':'w1','maxDepth':60}))['returnValue'].split('\n')
def zoomfit():
    for i in range(40): sl.S('PressKey',{'key':'Subtract'})
def shotp(name,box):
    j=json.loads(sl.S('Screenshot',{'ref':'w1'}))['returnValue']
    p=r'C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad/'+name
    open(p,'wb').write(base64.b64decode(j['data']))
    from PIL import Image
    Image.open(p).crop(box).save(p)

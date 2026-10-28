import sys; sys.path.insert(0,".")
from pasteops import *
import base64
from PIL import Image
gn=sys.argv[1]; out=sys.argv[2]
CAP='D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/capturas/'
for t in range(8):
    S('Click',{'ref':'t76'}); S('Click',{'ref':TAB[gn]}); time.sleep(.6)
    z=fit()
    btn=[l for l in snap() if re.match(r'\s*button "%s " \[pos=\d+,13\d'%gn,l)]
    if btn and 'Student_Skeleton_AnimBlueprint_fix' in where():
        j=json.loads(S('Screenshot',{'ref':'w1'}))['returnValue']
        raw=SP+'_cap.png'; open(raw,'wb').write(base64.b64decode(j['data']))
        # verificar otra vez que seguia siendo mi grafo
        btn2=[l for l in snap() if re.match(r'\s*button "%s " \[pos=\d+,13\d'%gn,l)]
        if btn2:
            Image.open(raw).crop((461,160,1531,850)).save(CAP+out); print('ok',z,CAP+out); break
    time.sleep(1)

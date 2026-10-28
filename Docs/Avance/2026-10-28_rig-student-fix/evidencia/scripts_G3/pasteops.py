import sys; sys.path.insert(0,".")
from paste import *
TAB={'AnimGraph':'t79','UpdateProceduralVariables':'t80','EventGraph':'t81'}
def atomic_paste(gn):
    """selecciona ABP+grafo, click en centro del panel, verifica y pega. devuelve True si verificado antes del Ctrl+V"""
    S('Click',{'ref':'t76'}); S('Click',{'ref':TAB[gn]}); time.sleep(.5)
    S('Click',{'ref':'sp91'})
    w=where(); btn=[l for l in snap() if re.match(r'\s*button "%s " \[pos=\d+,13\d'%gn,l)]
    if 'Student_Skeleton_AnimBlueprint_fix' in w and btn:
        S('PressKey',{'key':'Ctrl+V'}); time.sleep(1.5); return True
    return False
def read_nodes(gn):
    g=G(gn); base=g['refPath']+'.'
    ns=J('find_nodes',{'graph':g,'title':'','node_class':'','entry_points_only':False})
    return g,base,{n['refPath'].replace(base,'') for n in ns}

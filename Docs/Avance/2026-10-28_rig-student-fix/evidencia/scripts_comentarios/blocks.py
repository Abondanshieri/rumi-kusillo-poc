import json,sl,mapn,sys
SNAP='D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/snap_antes/%s.json'
def do(rig,panel,xr,title):
    f=SNAP%rig
    d=json.load(open(f))['nodes']
    names=[n for n,(x,y) in d.items() if xr[0]<=x<=xr[1]]
    m,k=mapn.mapping(f,panel)
    refs=[m[n][0] for n in names]
    print(title,len(refs),max(m[n][1] for n in names))
    sl.S('Click',{'ref':refs[0]})
    sl.comment(refs,title)
if __name__=="__main__":
    do('CR_Student_Procedural_fix','sp7',(0,1600),'LEAN')
    sl.shot('sp7','shot_pr8.png')

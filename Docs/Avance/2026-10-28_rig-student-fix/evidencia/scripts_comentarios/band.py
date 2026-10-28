import json,sl,mapbp,sys
def run(graph,panel,K,pred,title,doit=True):
    d=json.load(open(mapbp.SN))[graph]['nodes']
    r,k,a,b=mapbp.mapping(graph,panel,K)
    names=[n for n,v in d.items() if pred(v['x'],v['y'],n)]
    bad=[n for n in names if r[n][1]>12]
    refs=[r[n][0] for n in names if r[n][1]<=12]
    print(title,len(names),'bad',bad)
    if not doit: return refs
    sl.S('Click',{'ref':refs[0]})
    sl.multi(refs)
    return refs

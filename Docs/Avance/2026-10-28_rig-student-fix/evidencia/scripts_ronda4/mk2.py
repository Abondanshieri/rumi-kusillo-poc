from mp import *
NEW=r'C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad/abp_new.json'
band=json.load(open(r'C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad/band.json'))
def mk(b,title):
    sl.S('PressKey',{'key':'Ctrl+A'}); sl.S('PressKey',{'key':'Home'}); time.sleep(2)
    r,k,e=mapping2(NEW)
    names=[n for n in r if band[n]==b]
    assert all(r[n][1]<4 for n in names)
    refs=[r[n][0] for n in names]
    print(b,len(refs))
    sl.S('Click',{'ref':refs[0]}); sl.S('Click',{'ref':refs[0]})
    sl.multi(refs)
    sl.commentsel(title,'sp32')

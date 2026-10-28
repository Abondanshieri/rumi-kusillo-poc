import sys; sys.path.insert(0,'.')
from u import *
S('Click',{'ref':'i6665'}); time.sleep(1)
S('PressKey',{'key':'Home'}); time.sleep(4)
for l in snap():
    if 'INIT (' in l or 'Set references' in l or re.search(r'text "Zoom',l): print(l.strip()[:150])
print(shot('abp_sel.png',(0,56,1920,1080)))

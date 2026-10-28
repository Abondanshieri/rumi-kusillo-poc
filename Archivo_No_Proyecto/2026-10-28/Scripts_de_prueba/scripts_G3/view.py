import sys; sys.path.insert(0,'.')
from g3u import *
tab=sys.argv[1]; out=sys.argv[2]
L=snap()
ref=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%tab) and 'pos=' in l and ',102' in l][0]
S('Click',{'ref':ref}); time.sleep(1.5)
S('PressKey',{'key':'Home'}); time.sleep(3)
print(shot(out,(389,125,1531,855)))
print([re.search(r'text "(Zoom[^"]*)"',l).group(1) for l in snap() if re.search(r'text "Zoom',l)])

import sys; sys.path.insert(0,'.')
from u import *
import base64
j=json.loads(S('Screenshot',{'ref':'w1'}))['returnValue']
open(SP+'full.png','wb').write(base64.b64decode(j['data']))

import sys; sys.stdout.reconfigure(encoding="utf-8")
import sys,json
sys.path.insert(0,r"D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts")
from ue_mcp import UnrealMCPClient
c=UnrealMCPClient()
def run(ts,tool,args=None):
    r=c.run_tool(ts,tool,args or {})
    try: return r["content"][0]["text"]
    except Exception: return json.dumps(r)[:3000]
CH={'refPath':'/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0'}
def J(ts,tool,args=None):
    t=run(ts,tool,args)
    try: return json.loads(t)["returnValue"]
    except Exception: return t
OT="editor_toolset.toolsets.object.ObjectTools"

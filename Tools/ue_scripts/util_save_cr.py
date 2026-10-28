import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json, os

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural'

save_res = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': [cr_path]})
print("Save result:", save_res.get('content', [{}])[0].get('text', ''))

uasset_file = r"D:\Dev\Computacion_Grafica\Rumi 5.8\Content\Characters\Student\Rig\CR_Student_Procedural.uasset"
print(f"File exists: {os.path.exists(uasset_file)}")
print(f"File size: {os.path.getsize(uasset_file):,} bytes")

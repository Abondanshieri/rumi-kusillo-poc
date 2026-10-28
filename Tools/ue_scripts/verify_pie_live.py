import ue_mcp, json, time

c = ue_mcp.UnrealMCPClient()
anim_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0.CharacterMesh0.Student_Skeleton_AnimBlueprint_C_0'}
char_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0'}

time.sleep(1.0)
props = ['FootOffsetL', 'FootOffsetR', 'PelvisOffset', 'LandCrouch', 'LeanPitch', 'LeanRoll', 'GroundSpeed', 'IsFalling']
res = c.run_tool('editor_toolset.toolsets.object.ObjectTools', 'get_properties', {'instance': anim_ref, 'properties': props})
print('ANIM INSTANCE PROPS ON FLAT GROUND:')
print(res['content'][0]['text'])

loc = c.run_tool('editor_toolset.toolsets.actor.ActorTools', 'get_actor_transform', {'actor': char_ref})
print('CHAR TRANSFORM:', loc['content'][0]['text'])

import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
mesh_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0.CharacterMesh0'}
capsule_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0.CollisionCylinder'}

res_mesh = c.run_tool('editor_toolset.toolsets.object.ObjectTools', 'get_properties', {
    'instance': mesh_ref,
    'properties': ['BodyInstance', 'CollisionProfileName', 'CollisionEnabled']
})
print('Mesh collision:', res_mesh['content'][0]['text'])

res_capsule = c.run_tool('editor_toolset.toolsets.object.ObjectTools', 'get_properties', {
    'instance': capsule_ref,
    'properties': ['BodyInstance', 'CollisionProfileName', 'CollisionEnabled']
})
print('Capsule collision:', res_capsule['content'][0]['text'])

import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
anim_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0.CharacterMesh0.Student_Skeleton_AnimBlueprint_C_0'}
mesh_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0.CharacterMesh0'}
char_ref = {'refPath': '/Game/AnimTest/UEDPIE_0_Lvl_AnimTest.Lvl_AnimTest:PersistentLevel.BP_ThirdPersonCharacter_C_0'}

# Get char transform
char_loc = json.loads(c.run_tool('editor_toolset.toolsets.actor.ActorTools', 'get_actor_transform', {'actor': char_ref})['content'][0]['text'])['returnValue']['location']
print(f"Char Location: {char_loc}")

# Trace using SceneTools.trace_world
# From ActorLocation.Z down 150 cm at different Y offsets
for name, dx, dy in [('LeftFoot_approx', 0, -15), ('RightFoot_approx', 0, 15), ('Center', 0, 0)]:
    start = {'x': char_loc['x'] + dx, 'y': char_loc['y'] + dy, 'z': char_loc['z']}
    end = {'x': char_loc['x'] + dx, 'y': char_loc['y'] + dy, 'z': char_loc['z'] - 150.0}
    dist = c.run_tool('editor_toolset.toolsets.scene.SceneTools', 'trace_world', {'start': start, 'end': end})
    d_val = json.loads(dist['content'][0]['text']).get('returnValue')
    print(f"Trace {name} at ({start['x']}, {start['y']}): dist={d_val}")
    if d_val is not None:
        hit_z = start['z'] - d_val
        offset = 90.0 - d_val
        print(f"   Hit floor at Z={hit_z:.2f}, calculated Offset={offset:.2f} cm")

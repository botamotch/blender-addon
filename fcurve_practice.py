import bpy

ob = bpy.context.object

# ob.animation_data : bpy.types.AnimData
# ob.animation_data.action : bpy.types.Action
# ob.animation_data.action.fcurves : bpy_prop_collection
# ob.animation_data.action.fcurves[n] : bpy.types.FCurve
#   location(x, y, z), rotation(x, y, z) 毎に格納されている
# ob.animation_data.action.fcurves[n].keyframe_points : bpy_prop_collection
#   .insert(frame, value)
#   .values() -> list bpy.types.Keyframe
# ob.animation_data.action.fcurves[n].keyframe_points[n] : bpy.types.Keyframe
#   .co -> Vector
#   .keyframe_insert(data_path, index, frame)
#   .keyframe_delete(data_path, index, frame)
#   .id_data -> bpy.types.Action

# ob.animation_data.action.fcurves[n].group : bpy.types.ActionGroup

# ドープシート上の選択／非選択を変更
ob.animation_data.action.fcurves[0].keyframe_points[0].select_control_point = True
# ## よくわからん
# ob.animation_data.action.fcurves[0].keyframe_points[0].select_left_handle = True
# ob.animation_data.action.fcurves[0].keyframe_points[0].select_right_handle = True
# ob.animation_data.action.fcurves[0].keyframe_points[0].handle_right = True
# ob.animation_data.action.fcurves[0].keyframe_points[0].handle_right_type = True
# ob.animation_data.action.fcurves[0].keyframe_points[0].handle_left = True
# ob.animation_data.action.fcurves[0].keyframe_points[0].handle_left_type = True

fs = ob.animation_data.action.fcurves[0].keyframe_points[0].co


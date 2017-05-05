import bpy

# ------------------------------------------------------------------------------
# 1. bl_info
# ------------------------------------------------------------------------------

bl_info = {
    'name': 'Keyframe Select Extention',
    'author': 'botamotch',
    'version': (0,1),
    'blender': (2, 78, 0),
    "location": 'Dope Sheet > Select > ',
    'description': 'Keyframe Select Extention',
    'warning': '',
    'support': 'TESTING',
    'category': 'Animation',
}

# ------------------------------------------------------------------------------
# 2. Operator class
# ------------------------------------------------------------------------------

class SelectKeyframeRight(bpy.types.Operator):
    bl_idname = 'action.select_keyframe_right'
    bl_label = '選択中のキーフレームの右を選択'
    bl_description = '選択中のキーフレームの右を追加で選択します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                select_keyframe_index(fc, [i+1 for i in index])
        return {'FINISHED'}

class SelectKeyframeLeft(bpy.types.Operator):
    bl_idname = 'action.select_keyframe_left'
    bl_label = '選択中のキーフレームの左を選択'
    bl_description = '選択中のキーフレームの左を追加で選択します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                select_keyframe_index(fc, [i-1 for i in index])
        return {'FINISHED'}

class DeselectKeyframeRight(bpy.types.Operator):
    bl_idname = 'action.deselect_keyframe_right'
    bl_label = '選択中のキーフレームの右を選択解除'
    bl_description = '選択中のキーフレームの右を選択解除します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                try:
                    deselect_keyframe_index(fc, [index[-1]])
                except IndexError:
                    continue
        return {'FINISHED'}

class DeselectKeyframeLeft(bpy.types.Operator):
    bl_idname = 'action.deselect_keyframe_left'
    bl_label = '選択中のキーフレームの左を選択解除'
    bl_description = '選択中のキーフレームの左を選択解除します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                try:
                    deselect_keyframe_index(fc, [index[0]])
                except IndexError:
                    continue
        return {'FINISHED'}

'''
class SelectKeyframeSelected(bpy.types.Operator):
    bl_idname = 'action.select_keyframe_selected'
    bl_label = '選択中のキーフレームと同フレームを選択'
    bl_description = '選択中のキーフレームと同フレームのキーフレームを選択します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        timeline = []
        anim_obs = [ob for ob in bpy.context.scene.objects if ob.animation_data]
        for ob in anim_obs:
            for fc in ob.animation_data.action.fcurves:
                timeline.append(get_frame_selectedkeyframe(fc))
        for ob in anim_obs:
            for fc in ob.animation_data.action.fcurves:
                select_keyframe_timeline(fc, timeline)
        return {'FINISHED'}
'''

class ShiftKeyframeRight(bpy.types.Operator):
    bl_idname = 'action.shift_keyframe_right'
    bl_label = 'キーフレーム選択を右に移動'
    bl_description = 'キーフレームの選択範囲を右にずらします'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                deselect_keyframe_index(fc, index)
                select_keyframe_index(fc, [i+1 for i in index])
        return {'FINISHED'}

class ShiftKeyframeLeft(bpy.types.Operator):
    bl_idname = 'action.shift_keyframe_left'
    bl_label = 'キーフレーム選択を左に移動'
    bl_description = 'キーフレームの選択範囲を左にずらします'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                deselect_keyframe_index(fc, index)
                select_keyframe_index(fc, [i-1 for i in index])
        return {'FINISHED'}

class MoveKeyframeRight(bpy.types.Operator):
    bl_idname = 'action.move_keyframe_right'
    bl_label = 'キーフレームを右に移動'
    bl_description = 'キーフレームを右に１フレーム移動します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                move_keyframe(fc,index,1)
        move_marker(1)
        return {'FINISHED'}

class MoveKeyframeLeft(bpy.types.Operator):
    bl_idname = 'action.move_keyframe_left'
    bl_label = 'キーフレームを左に移動'
    bl_description = 'キーフレームを左に１フレーム移動します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                index = get_index_selectedkeyframe(fc)
                move_keyframe(fc,index,-1)
        move_marker(-1)
        return {'FINISHED'}

class SelectMarkerSelected(bpy.types.Operator):
    bl_idname = 'action.select_marker_selected'
    bl_label = '選択中のキーフレームと同フレームのマーカーを選択'
    bl_description = '選択中のキーフレームと同フレームのマーカーを選択します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for mk in bpy.context.scene.timeline_markers:
            mk.select = False
        for ob in [ob for ob in bpy.context.scene.objects if ob.animation_data]:
            for fc in ob.animation_data.action.fcurves:
                time = get_frame_selectedkeyframe(fc)
                select_marker_timeline(time)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# 3. Panel class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4. Property Group class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5. Menu class
# ------------------------------------------------------------------------------

class KeyframeSelectMenu(bpy.types.Menu):
    bl_idname = 'action.keyframe_select_menu'
    bl_label = 'キーフレーム／マーカーの選択'
    bl_description = 'キーフレーム／マーカーを選択します'

    def draw(self, context):
        layout = self.layout
        layout.operator(SelectKeyframeRight.bl_idname)
        layout.operator(SelectKeyframeLeft.bl_idname)
        layout.operator(DeselectKeyframeRight.bl_idname)
        layout.operator(DeselectKeyframeLeft.bl_idname)
        layout.operator(ShiftKeyframeRight.bl_idname)
        layout.operator(ShiftKeyframeLeft.bl_idname)
        layout.operator(MoveKeyframeRight.bl_idname)
        layout.operator(MoveKeyframeLeft.bl_idname)
        layout.operator(SelectMarkerSelected.bl_idname)

# ------------------------------------------------------------------------------
# 6. function
# ------------------------------------------------------------------------------

# 選択中のキーフレームのインデックスを取得
def get_index_selectedkeyframe(fc):
    return [i for i, kf in enumerate(fc.keyframe_points) if kf.select_control_point]
# 選択中のキーフレームの時刻を取得
def get_frame_selectedkeyframe(fc):
    return [kf.co[0] for kf in fc.keyframe_points if kf.select_control_point]
# 時間指定でキーフレームを選択
def select_keyframe_timeline(fc, time=[0]):
    for kf in fc.keyframe_points:
        if kf.co[0] in time:
            kf.select_control_point = True
# 時間指定でキーフレームを選択解除
def deselect_keyframe_timeline(fc, time=[0]):
    for kf in fc.keyframe_points:
        if kf.co[0] in time:
            kf.select_control_point = False
# インデックス指定でキーフレームを選択
def select_keyframe_index(fc,index=[0]):
    for i in index:
        try:
            fc.keyframe_points[i].select_control_point = True
            fc.keyframe_points[i].select_left_handle = True
            fc.keyframe_points[i].select_right_handle = True
        except IndexError:
            continue
# インデックス指定でキーフレームを選択解除
def deselect_keyframe_index(fc,index=[0]):
    for i in index:
        try:
            fc.keyframe_points[i].select_control_point = False
            fc.keyframe_points[i].select_left_handle = False
            fc.keyframe_points[i].select_right_handle = False
        except IndexError:
            continue
# フレーム指定でマーカーを選択
def select_marker_timeline(time=[0]):
    for mk in bpy.context.scene.timeline_markers:
        if mk.frame in time:
            mk.select = True
# インデックス指定でキーフレームを移動
def move_keyframe(fc,index=[0],x=1):
    for i, kf in enumerate(fc.keyframe_points):
        if i in index:
            kf.co[0] += x
# 選択中のマーカーを移動
def move_marker(x=1):
    for mk in bpy.context.scene.timeline_markers:
        if mk.select:
            mk.frame += x

# ------------------------------------------------------------------------------
# 7. menu_fn/register/unregister/register_shortcut/unregister_shortcut
# ------------------------------------------------------------------------------

addon_keymaps = []

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=SelectKeyframeRight.bl_idname,
            type='RIGHT_BRACKET',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=False
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=SelectKeyframeLeft.bl_idname,
            type='LEFT_BRACKET',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=False
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=DeselectKeyframeRight.bl_idname,
            type='RIGHT_BRACKET',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=True
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=DeselectKeyframeLeft.bl_idname,
            type='LEFT_BRACKET',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=True
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=SelectMarkerSelected.bl_idname,
            type='M',
            value='PRESS',
            shift=True,
            ctrl=False,
            alt=False
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=MoveKeyframeRight.bl_idname,
            type='RIGHT_ARROW',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=False
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=MoveKeyframeLeft.bl_idname,
            type='LEFT_ARROW',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=False
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=ShiftKeyframeRight.bl_idname,
            type='PERIOD',
            value='PRESS',
            shift=True,
            ctrl=False,
            alt=False
        )
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=ShiftKeyframeLeft.bl_idname,
            type='COMMA',
            value='PRESS',
            shift=True,
            ctrl=False,
            alt=False
        )
        addon_keymaps.append((km, kmi))

def unregister_shortcut():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(KeyframeSelectMenu.bl_idname)

def register():
    bpy.utils.register_module(__name__)
    bpy.types.DOPESHEET_MT_select.append(menu_fn)
    register_shortcut()

def unregister():
    unregister_shortcut()
    bpy.types.DOPESHEET_MT_select.remove(menu_fn)
    bpy.utils.unregister_module(__name__)

# ------------------------------------------------------------------------------
# 8. main process
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    register()


import bpy
import xml.etree.ElementTree as ET
import re

# ------------------------------------------------------------------------------
# 1. bl_info
# ------------------------------------------------------------------------------

bl_info = {
    'name': 'Text Animation from XML',
    'author': 'botamotch',
    'version': (0,1),
    'blender': (2, 78, 0),
    "location": 'View 3D > Tool Shelf > ',
    'description': 'Text animation input from XML',
    'warning': '',
    'support': 'TESTING',
    'category': 'Animation',
}

# ------------------------------------------------------------------------------
# 2. Operator class
# ------------------------------------------------------------------------------

class SetTextAnimation(bpy.types.Operator):
    bl_idname = 'scene.set_text_animation'
    bl_label = 'Set scene form XML'
    bl_description = 'Set text object animation from XML config file.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sc_main = bpy.context.scene
        if sc_main.name + '_link' in bpy.data.scenes:
            sc_link = bpy.data.scenes[sc_main.name + '_link']
        else:
            sc_link = bpy.data.scenes.new(sc_main.name + '_link')
        tx_pattern = re.compile('text_[0-9][0-9]_base|text_[0-9][0-9]_deco')
        # XML config 取り込み
        try:
            elem = import_xml(sc_main.xml_filepath.path)
        except FileNotFoundError:
            self.report({'ERROR'}, 'File was not found')
            return {'FINISHED'}
        except ET.ParseError:
            self.report({'ERROR'}, 'XML parse error occured')
            return {'FINISHED'}
        read_config(elem)
        # マーカー消去（メインシーン）
        init_marker(sc_main)
        # テキスト・マーカー消去（連携シーン）
        init_marker(sc_link)
        init_object(sc_link, tx_pattern , 'FONT')
        # カメラ作成（連携シーン）
        ob = set_camera(sc_link, 'camera_link')
        ob.location = tuple(config.camera)
        ob.rotation_euler = (0, 0, 0)
        ob.data.type = 'ORTHO'
        ob.data.clip_start = ob.location[2] - 0.15
        ob.data.clip_end = ob.location[2] + 0.15
        ob.data.ortho_scale = 20
        # ランプ作成（連携シーン）
        ob = set_lamp(sc_link, 'lamp_link', 'SUN')
        ob.location = (0, 0, 5)
        ob.rotation_euler = (0, 0, 0)
        ob.data.color = (1, 1, 1)
        ob.data.energy = 1
        ob.data.use_specular = False
        ob.data.use_diffuse = True
        ob.data.use_own_layer = True
        ob.data.use_negative = False
        # XML play 取り込み
        read_play(elem, sc_link, sc_main)
        return {'FINISHED'}

class SyncMarker(bpy.types.Operator):
    bl_idname = 'scene.sync_marker'
    bl_label = '全シーンでマーカー同期'
    bl_description = '現在のシーンを基準に、全シーンでマーカーを同期します'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        message = ''
        for sc in bpy.data.scenes:
            if sc == bpy.context.scene:
                continue
            sync_marker(bpy.context.scene, sc)
            message += "'" + sc.name + "', "
        message = message[:-2]
        message += " were synchornized with '" + bpy.context.scene.name + "'"
        self.report({'INFO'}, message)
        return {'FINISHED'}

class SetBoneShapeAtOnce(bpy.types.Operator):
    bl_idname = 'armature.setbonesatonce'
    bl_label = 'Set Bone Shapes at once'
    bl_description = 'Set Bone Shapes at once'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bn = bpy.context.active_bone
        pbn = bpy.context.active_pose_bone
        bones = bpy.context.selected_pose_bones
        shape = pbn.custom_shape
        use_scale = pbn.use_custom_shape_bone_size
        scale = pbn.custom_shape_scale
        wired = bn.show_wire
        if bpy.context.object.type != 'ARMATURE':
            self.report({'WARNING'}, 'Selected Object is not armature')
            return {'CANCELLED'}
        for b in bones:
            b.custom_shape = shape
            b.use_custom_shape_bone_size = use_scale
            b.custom_shape_scale = scale
            bpy.context.object.data.bones[b.name].show_wire = wired
        self.report({'INFO'}, 'Set Bone Shapes at once Operator was executed')
        return {'FINISHED'}

# ------------------------------------------------------------------------------
# 3. Panel class
# ------------------------------------------------------------------------------

class VIEW3D_PT_InputFilePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_idname = 'inputfile'
    bl_label = 'Text Anim'
    bl_category = 'Input file'

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='',icon='PLUGIN')

    def draw(self, context):
        layout = self.layout
        sc = bpy.context.scene
        layout.operator('scene.set_text_animation')
        layout.operator('scene.sync_marker')
        layout.prop(sc.xml_filepath, 'path', text='')
        # layout.prop(sc.xml_filepath, 'font', text='')

class VIEW3D_PT_SetBoneShapeAtOncePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = ''
    bl_idname = 'setboneatonce'
    bl_label = 'Bone Shape at Once'
    bl_category = 'Input file'

    def draw(self,context):
        ob = bpy.context.object
        bn = bpy.context.active_bone
        pbn = bpy.context.active_pose_bone
        layout = self.layout

        if ob and pbn:
            col = layout.column()
            col.operator('armature.setbonesatonce',text='Set Bone at once')
            if ob.mode == 'POSE':
                split = col.split()

                col = split.column()
                col.prop(bn, "hide", text="Hide")
                col = col.column()
                col.active = bool(pbn.custom_shape)
                col.prop(bn, "show_wire", text="Wireframe")

                col = split.column()
                col.label(text='Custom Shape:')
                col.prop(pbn,'custom_shape',text='')
                if pbn.custom_shape:
                    col.prop(pbn, "use_custom_shape_bone_size", text="Bone Size")
                    col.prop(pbn, "custom_shape_scale", text="Scale")
                    col.prop_search(pbn, "custom_shape_transform", ob.pose, "bones", text="At")

# ------------------------------------------------------------------------------
# 4. Property Group class
# ------------------------------------------------------------------------------

class XMLFilePathProp(bpy.types.PropertyGroup):
    path = bpy.props.StringProperty(
            name = 'Path to XML File',
            subtype = 'FILE_PATH')
    # font = bpy.props.PointerProperty(
            # name = 'font',
            # type=bpy.types.VectorFont)

# ------------------------------------------------------------------------------
# 5. function
#  - import_xml(file_path) -> etree
#  - read_config()
#  - read_config()
# ------------------------------------------------------------------------------

class config:
    speed = 1.0
    font = {}
    character = []
    camera = [0.0, 0.0, 0.0]
    width = 960
    height = 540

def import_xml(file_path):
    tree = ET.parse(file_path)
    elem = tree.getroot()
    return elem

def read_config(elem):
    # 'Bfont'を使えるようにするために一時的に作成、あとで消す
    cv_tmp = bpy.data.curves.new('cv_tmp','FONT')
    elem_conf = elem.find('.//config')
    config.speed = elem_conf.get('speed', 1.0)
    config.camera = [float(i) for i in elem_conf.get('camera', '').split(',')]
    config.width = float(elem_conf.get('width', 960))
    config.height = float(elem_conf.get('height', 540))
    # フォント取り込み
    config.font['default'] = bpy.data.fonts['Bfont']
    for ft in elem_conf.findall('.//font'):
        name = ft.get('name', None)
        try:
            if name:
                config.font[name] = bpy.data.fonts.load(ft.text.strip(), True)
            else:
                config.font['default'] = bpy.data.fonts.load(ft.text.strip(), True)
        except RutimeError:
            continue
    for ch in elem_conf.findall('.//character'):
        ch_dic = {
            'name': ch.get('name'),
            'color': tuple([float(i) for i in ch.get('color', '').split(',')]),
            'font': ch.get('font', None),
        }
        config.character.append(ch_dic)
    # マテリアル作成
    if 'white' not in bpy.data.materials:
        mt = bpy.data.materials.new('white')
    else:
        mt = bpy.data.materials['white']
    mt.diffuse_color = (1, 1, 1)
    mt.diffuse_intensity = 1
    mt.specular_intensity = 0
    if 'black' not in bpy.data.materials:
        mt = bpy.data.materials.new('black')
    else:
        mt = bpy.data.materials['black']
    mt.diffuse_color = (0, 0, 0)
    mt.diffuse_intensity = 1
    mt.specular_intensity = 0
    for ch in config.character:
        if ch['name'] not in bpy.data.materials:
            mt = bpy.data.materials.new(ch['name'])
        else:
            mt = bpy.data.materials[ch['name']]
        mt.diffuse_color = ch['color']
        mt.diffuse_intensity = 1
        mt.specular_intensity = 0
    bpy.data.curves.remove(cv_tmp)

def read_play(elem, sc_link, sc_main):
    sc_main.render.resolution_x = config.width
    sc_main.render.resolution_y = config.height
    sc_link.render.resolution_x = config.width
    sc_link.render.resolution_y = config.height
    n_camera = 0
    n_text = 0
    time = 0
    for e in elem.find('.//play'):
        if e.tag == 'camera':
            # カメラ作成・マーカー作成・バインド
            ob = set_camera(sc_main, 'camera_' + '{0:02d}'.format(n_camera))
            sc_link.timeline_markers.new('cm' + '{0:02d}'.format(n_camera), time)
            tm = sc_main.timeline_markers.new('cm' + '{0:02d}'.format(n_camera), time)
            tm.camera = ob
            n_camera += 1
        elif e.tag == 'screen':
            # セリフを作成
            end = time + float(e.get('time', '0'))
            for sp in e.findall('.//speak'):
                # source_text 取り込み
                source_text = [ct.text for ct in sp.findall('.//content')]
                if sp.get('emotion', 'false') == 'true' or sp.get('name') == None:
                    source_text = '\n'.join(source_text)
                else:
                    source_text[0] = sp.get('name') + '：' + source_text[0]
                    for i in range(1, source_text[1:]+1):
                        source_text[i] = (len(sp.get('name'))+1)*u'\u3000' + source_text[i]
                    source_text = '\n'.join(source_text)
                # タイムライン設定
                if sp.get('emotion', 'false') == 'true':
                    sc_link.timeline_markers.new(source_text[:5], time)
                    sc_main.timeline_markers.new(source_text[:5], time)
                else:
                    sc_link.timeline_markers.new(source_text[len(sp.get('name'))+1:][:5], time)
                    sc_main.timeline_markers.new(source_text[len(sp.get('name'))+1:][:5], time)
                # keyframes 取り込み
                if float(sp.get('speed', '1.0')) == 0:
                    keyframes = get_keyframes_noanim(source_text, time, end)
                elif sp.get('emotion', 'false') == 'true' or sp.get('name') == None:
                    speed = float(sp.get('speed', '1.0'))
                    keyframes = get_keyframes_nospeak(source_text, speed, time, end)
                else:
                    speed = float(sp.get('speed', '1.0'))
                    start = len(sp.get('name')) + 1
                    t2 = time + float(sp.get('wait', '0'))
                    keyframes = get_keyframes_speak(source_text, speed, start, time, t2, end)
                # テキストオブジェクト (ob_base, ob_daco) 作成
                ob_base = set_text(sc_link, 'text_'+'{0:02d}'.format(n_text)+'_base', source_text)
                ob_deco = set_text(sc_link, 'text_'+'{0:02d}'.format(n_text)+'_deco', source_text)
                set_text_keyframe(ob_base.data, keyframes)
                set_text_keyframe(ob_deco.data, keyframes)
                ob_base.data.extrude = 0.055
                ob_deco.data.extrude = 0.000
                ob_base.data.bevel_depth = 0.00
                ob_deco.data.bevel_depth = 0.05
                ob_base.data.materials.append(bpy.data.materials['white'])
                if sp.get('name') in bpy.data.materials:
                    ob_deco.data.materials.append(bpy.data.materials[sp.get('name')])
                else:
                    ob_deco.data.materials.append(bpy.data.materials['black'])
                # フォント設定
                ft = sp.get('font', None)
                if ft in config.font.keys():
                    ob_base.data.font = config.font[ft]
                    ob_deco.data.font = config.font[ft]
                else:
                    ob_base.data.font = config.font['default']
                    ob_deco.data.font = config.font['default']
                n_text += 1
            # time 更新
            time = end
    sc_main.frame_start = 0
    sc_main.frame_end = end
    sc_link.frame_start = 0
    sc_link.frame_end = end

def init_object(sc, pattern, ob_type):
    for ob in sc.objects:
        if pattern.match(ob.name) != None and ob.type == ob_type:
            sc.objects.unlink(ob)
            bpy.data.objects.remove(ob)
    for cv in bpy.data.curves:
        if pattern.match(cv.name) != None:
            bpy.data.curves.remove(cv)

def init_marker(sc):
    for tm in sc.timeline_markers:
        sc.timeline_markers.remove(tm)

def set_text(sc, name, source_text):
    if name in bpy.data.curves:
        cv = bpy.data.curves[name]
    else:
        cv = bpy.data.curves.new(name,'FONT')
    if name in bpy.data.objects:
        ob = bpy.data.objects[name]
        if ob.type != 'FONT':
            for sc in bpy.data.scenes:
                if ob.name in sc.objects:
                    sc.unlink(ob)
            bpy.data.objects.remove(ob)
            ob = bpy.data.objects.new(name,cv)
    else:
        ob = bpy.data.objects.new(name,cv)
    ob.data.source_text = source_text
    if ob.name not in sc.objects:
        sc.objects.link(ob)
    return ob

def set_camera(sc, name):
    if name in bpy.data.cameras:
        cm = bpy.data.cameras[name]
    else:
        cm = bpy.data.cameras.new(name)
    if name in bpy.data.objects:
        ob = bpy.data.objects[name]
        if ob.type != 'CAMERA':
            for sc in bpy.data.scenes:
                if ob.name in sc.objects:
                    sc.unlink(ob)
            bpy.data.objects.remove(ob)
            ob = bpy.data.objects.new(name,cm)
    else:
        ob = bpy.data.objects.new(name, cm)
    if ob.name not in sc.objects:
        sc.objects.link(ob)
    return ob

def set_lamp(sc, name, lamp_type):
    if name in bpy.data.lamps:
        cm = bpy.data.lamps[name]
        cm.type = lamp_type
    else:
        cm = bpy.data.lamps.new(name, lamp_type)
    if name in bpy.data.objects:
        ob = bpy.data.objects[name]
        if ob.type != 'LAMP':
            for sc in bpy.data.scenes:
                if ob.name in sc.objects:
                    sc.unlink(ob)
            bpy.data.objects.remove(ob)
            ob = bpy.data.objects.new(name,cm)
    else:
        ob = bpy.data.objects.new(name, cm)
    if ob.name not in sc.objects:
        sc.objects.link(ob)
    return ob

def set_text_keyframe(cv, keyframe=[{'count':0,'frame':0}]):
    cv.use_animated_text = True
    for kf in keyframe:
        cv.character_count = kf['count']
        cv.keyframe_insert('character_count', frame=kf['frame'])

def get_keyframes_nospeak(source_text, speed, t1, t2):
    keyframes = []
    keyframes.append({'count':0, 'frame':t1})
    keyframes.append({'count':len(source_text), 'frame':t1 + len(source_text) * speed})
    keyframes.append({'count':len(source_text), 'frame':t2-1})
    keyframes.append({'count':0, 'frame':t2})
    return keyframes

def get_keyframes_speak(source_text, speed, start, t1, t2, t3):
    keyframes = []
    keyframes.append({'count':0, 'frame':t1})
    keyframes.append({'count':start, 'frame':t1+1})
    keyframes.append({'count':start, 'frame':t2})
    keyframes.append({'count':len(source_text), 'frame':t2 + (len(source_text) - start) * speed})
    keyframes.append({'count':len(source_text), 'frame':t3-1})
    keyframes.append({'count':0, 'frame':t3})
    return keyframes

def get_keyframes_noanim(source_text, t1, t2):
    keyframes = []
    keyframes.append({'count':0, 'frame':t1})
    keyframes.append({'count':len(source_text), 'frame':t1+1})
    keyframes.append({'count':len(source_text), 'frame':t2-1})
    keyframes.append({'count':0, 'frame':t2})
    return keyframes

def sync_marker(sc_from, sc_to):
    for mk_from in sc_from.timeline_markers:
        if mk_from.name in sc_to.timeline_markers.keys():
            sc_to.timeline_markers[mk_from.name].frame = mk_from.frame

# ------------------------------------------------------------------------------
# 6. menu_fn/register/unregister/register_shortcut/unregister_shortcut
# ------------------------------------------------------------------------------

addon_keymaps = []

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi = km.keymap_items.new(
            idname=SyncMarker.bl_idname,
            type='M',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=True
        )
        addon_keymaps.append((km, kmi))

def unregister_shortcut():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(SyncMarker.bl_idname)

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.xml_filepath = bpy.props.PointerProperty(type=XMLFilePathProp)
    bpy.types.DOPESHEET_MT_marker.append(menu_fn)
    register_shortcut()

def unregister():
    unregister_shortcut()
    bpy.types.DOPESHEET_MT_marker.remove(menu_fn)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.xml_filepath

# ------------------------------------------------------------------------------
# 7. main process
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    register()


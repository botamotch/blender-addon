import bpy
import xml.etree.ElementTree as ET

# ------------------------------------------------------------------------------
# bl_info
# ------------------------------------------------------------------------------

bl_info = {
    'name': 'Keyframe Select Extention',
    'author': 'botamotch',
    'version': (0,1),
    'blender': (2, 78, 0),
    "location": 'Dope Sheet -> Select -> ',
    'description': 'Keyframe Select Extention',
    'warning': '',
    'support': 'TESTING',
    'category': 'Animation',
}

# ------------------------------------------------------------------------------
# Operator class
# ------------------------------------------------------------------------------

class SetMarker(bpy.types.Operator):
    bl_idname = 'marker.setmarker'
    bl_label = 'Set Marker form config file'
    bl_description = 'Set marker into current scene and Text scene'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

# ------------------------------------------------------------------------------
# Menu class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# function
#  - import_xml(file_path) -> etree
#  - read_config()
#  - read_config()
# ------------------------------------------------------------------------------

def import_xml(file_path):
    try:
        tree = ET.parse(file_path)
    except FileNotFoundError:
        return None
    elem = tree.getroot()
    return None

def read_config():
    return

def read_play():
    return

def set_camera():
    return

def set_speak():
    return

# ------------------------------------------------------------------------------
# menu_fn/register/unregister
# ------------------------------------------------------------------------------

def menu_fn(self, context):
    self.layout.separator()
    # self.layout.operator(EnlargeObject2.bl_idname)
    # self.layout.operator(ReduceObject2.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    # bpy.types.VIEW3D_MT_object.append(menu_fn)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_fn)
    # bpy.utils.unregister_module(__name__)

# ------------------------------------------------------------------------------
# main process
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    register()


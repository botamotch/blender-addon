import bpy

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

# ------------------------------------------------------------------------------
# Menu class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# function
# ------------------------------------------------------------------------------

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

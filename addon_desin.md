# Blender Addon
## 1. bl\_info
- name
- author
- version
- blender
- location
- description
- warning
- support
- wiki\_url
- tracker\_url
- category

## 2. Operator class (bpy.types.Operator)
- bl\_idname
- bl\_label
- bl\_description
- bl\_options
- def execute(self, context)
  - return {'FINISHED'}

## 3. Panel class(bpy.types.Panel)
- bl\_space\_type
- bl\_region\_type
- bl\_context
- bl\_idname
- bl\_label
- bl\_category
- def draw(self, context)

## 4. Property Group class (bpy.tepes.PropertyGroup)

## 5. function

## 6. menu\_fn, register, unregister
- def menu\_fn(self, context)
- def register()
  - bpy.types.INFO\_MT\_mesh\_add.append(menu\_fn)
  - bpy.utils.register\_module(__name__)
  - bpy.types.Scene.mmdrama\_inputfile = bpy.props.PointerProperty(type=FilepathProp)
- def unregister()
  - bpy.utils.unregister\_module(__name__)
  - bpy.types.INFO\_MT\_mesh\_add.remove(menu\_fn)
  - del bpy.types.Scene.mmdrama\_inputfile

# 設定ファイル読み込み＆テキストアニメーション設定

# キーフレーム選択で
- キーフレームを操作してマーカーを更新 (use\_marker\_sync = True)
- キーフレーム選択を強化するオペレータ
- 連携しているシーン同士でマーカーを同期 (カメラのバインドは維持しない)

# 参考
- [Blender API documentation](https://docs.blender.org/api)
- [Blender Documentation Contents - Blener 2.78.0 e8299c8](https://docs.blender.org/api/blender_python_api_current/)
- [Main Page - BlenderWiki](https://wiki.blender.org/index.php/Main_Page)
- [Dev:Contents - BlenderWiki](https://wiki.blender.org/index.php/Dev:Contents)
- [Dev:Py/Scripts/Cookbook/Code snippets/Actions and drivers - BlenderWiki](https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Actions_and_drivers)
- [Extensions:Py/Scripts](https://wiki.blender.org/index.php/Extensions:Py/Scripts)

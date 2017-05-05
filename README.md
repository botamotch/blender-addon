# Blender Addon 構造
## 1. bl\_info
```
name
author
version
blender
location
description
warning
support
wiki_url
tracker_url
category
```

## 2. Operator class (bpy.types.Operator)
```
bl_idname
bl_label
bl_description
bl_options
def execute(self, context)
  return {'FINISHED'}
```

## 3. Panel class(bpy.types.Panel)
```
bl_space_type
bl_region_type
bl_context
bl_idname
bl_label
bl_category
def draw(self, context)
```

## 4. Property Group class (bpy.tepes.PropertyGroup)

## 5. function

## 6. menu\_fn, register, unregister
```
def menu_fn(self, context)
def register()
  bpy.types.INFO_MT_mesh_add.append(menu_fn)
  bpy.utils.register_module(__name__)
  bpy.types.Scene.mmdrama_inputfile = bpy.props.PointerProperty(type=FilepathProp)
def unregister()
  bpy.utils.unregister_module(__name__)
  bpy.types.INFO_MT_mesh_add.remove(menu_fn)
  del bpy.types.Scene.mmdrama_inputfile
```

# テキストアニメーション - text\_animatin.py
## オブジェクト初期化
- メインシーン
  - マーカー消去
  - カメラそのまま
- テキストシーン
  - マーカー消去
  - カメラそのまま
  - ランプそのまま
  - テキスト消去
- set\_text(), set\_camera() で、オブジェクトがあってもそのままそれを返すようにする

# キーフレーム選択拡張 - keyframe\_select\_extension.py
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
- [はじめてのBlenderアドオン開発](https://nutti.gitbooks.io/introduction-to-add-on-development-in-blender/)


# キーフレーム選択拡張 - keyframe\_select\_extension.py
## 本アドオンについて
キーフレームやマーカの操作をショートカットキーにより便利に操作できるようにするためのアドオン。

## Operator class
- action.select\_keyframe\_right (Ctrl + RIGHT\_BRACKET)
  - 選択中のキーフレームの右を追加で選択
- action.select\_keyframe\_left (Ctrl + LEFT\_BRACKET)
  - 選択中のキーフレームの左を追加で選択
- action.deselect\_keyframe\_right (Ctrl + Alt + RIGHT\_BRACKET)
  - 選択中のキーフレームの右を選択解除
- action.deselect\_keyframe\_left (Ctrl + Alt + LEFT\_BRACKET)
  - 選択中のキーフレームの左を選択解除
- action.shift\_keyframe\_right (Shift + PERIOD)
  - キーフレーム選択を右に移動
- action.shift\_keyframe\_left (Shift + COMMA)
  - キーフレーム選択を左に移動
- action.move\_keyframe\_right (Ctrl + RIGHT\_ARROW)
  - 選択中のキーフレームを右に移動
- action.move\_keyframe\_left (Ctrl + LEFT\_ARROW)
  - 選択中のキーフレームを左に移動
- action.select\_marker\_selected (Shift + M)
  - 選択中のキーフレームと同フレームのマーカーを選択
- scene.sync\_marker (Ctrl + Alt + M)
  - 現在のシーンを基準に全シーンでマーカーを同期

## function
- Operator class でよく使う関数
- fc (bpy.types.FCurve) : キーフレームのデータタイプ (アクセス例 : bpy.context.object.animation\_data.action.fcurves[0])
- index : 整数リスト、FCurve のインデックスを指定
- time : 整数リスト、FCurve のフレームを指定
- 関数一覧
  - get\_index\_selectedkeyframe(fc)-> index
  - get\_frame\_selectedkeyframe(fc)-> time
  - select\_keyframe\_timeline(fc, time)
  - deselect\_keyframe\_timeline(fc, time)
  - select\_keyframe\_index(fc, index)
  - deselect\_keyframe\_index(fc, index)
  - select\_marker\_timline(time)
  - move\_keyframe(fc, index, x)
  - move\_marker(x)

# テキストアニメーション - text\_animatin.py
## 本アドオンについて
XML ファイルから設定を読み込み、テキストオブジェクトのアニメーションを自動で作成するもの。
カメラの切り替えやマーカーの作成も行う。
ついでに、ボーン形状の一括変更も同じツールシェルフから行える。

Dope Sheet > View > Sync Markers にチェックを入れて編集すること

## Operator class
- SetTextAnimation
- SetBoneShapeAtOnce

## function
- 関数一覧
  - import\_xml(file\_path) -> elem
  - read\_config(elem)
  - read\_play(elem, sc\_link, sc\_main)
  - init\_object(sc, pattern, ob\_type)
  - init\_marker(sc)
  - set\_text(sc, name, source\_text) -> ob
  - set\_camera(sc, name) -> ob
  - set\_lamp(sc, name, lamp\_type) -> ob
  - set\_text\_keyframe(sc, keyframe)
  - get\_keyframe\_nospeak(source\_text, speed, t1, t2) -> keyframe
  - get\_keyframe\_speak(source\_text, speed, start, t1, t2, t3) -> keyframe
  - get\_keyframe\_noanim(source\_text, t1, t2) -> keyframe
  - sync\_marker(sc\_from, sc\_to)

## 実装を見送った機能
- シーン・フォント選択をツールシェルフに表示
  - 表示させる方法がわからなかったのでパス
- シーン同士のノード接続
  - 毎回少しずつ変わるからいいかな・・・

# 参考
- [Blender API documentation](https://docs.blender.org/api)
- [Blender Documentation Contents - Blener 2.78.0 e8299c8](https://docs.blender.org/api/blender_python_api_current/)
- [Main Page - BlenderWiki](https://wiki.blender.org/index.php/Main_Page)
- [Dev:Contents - BlenderWiki](https://wiki.blender.org/index.php/Dev:Contents)
- [Dev:Py/Scripts/Cookbook/Code snippets/Actions and drivers - BlenderWiki](https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Actions_and_drivers)
- [Extensions:Py/Scripts](https://wiki.blender.org/index.php/Extensions:Py/Scripts)
- [はじめてのBlenderアドオン開発](https://nutti.gitbooks.io/introduction-to-add-on-development-in-blender/)


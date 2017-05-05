import xml.etree.ElementTree as ET

tree = ET.parse('example.xml')
elem = tree.getroot()

conf = elem.find('.//config')
play = elem.findall('.//play')[0]

# ============= 設定ファイル読み込み開始 ================
speed = float(conf.get('speed', '1.0'))
camera_loc = [float(i) for i in conf.get('camera', '').split(',')]

for e in list(conf):
    if e.tag == 'defaultfont':
        print('Defaultfont path is ' + e.text.strip())
    elif e.tag == 'optionalfont':
        print('Optionalfont path is ' + e.text.strip())
    elif e.tag == 'character':
        print("Character's name is " + e.get('name'))
        col = [float (i) for i in e.get('color').split(',')]

# ============= 設定ファイル読み込み終了 ================

print('')
# ============= 会話シーン読み込み開始 ================
for e in list(play):
    if e.tag == 'screen':
        for ee in list(e):
            print(ee.get('name'))
            for eee in list(ee):
                if eee.tag == 'content':
                    print(eee.text)
# ============= 会話シーン読み込み終了 ================


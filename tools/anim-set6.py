# -*- coding: utf-8 -*-
"""动态表情：同一张表里画 8 个相位（眨眼/点头），切出来后合成 GIF。
思路跟静态的「总表切片」一样：一次渲染，多相位在一张图上。
"""
import os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util

spec = importlib.util.spec_from_file_location('s6', os.path.join(HERE, 'draw-set6.py'))
s6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s6)

OUT = os.path.join(os.path.expanduser('~'), '.dsh', 'qq-stickers', 'set6')
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
CELL = s6.CELL
COLS, ROWS = 4, 2
W, H = CELL * COLS, CELL * ROWS

# 8 相位：睁 → 半闭 → 闭 → 半闭 → 睁，同时整体轻微上下
PHASES = [
    ('open', 0), ('open', -4), ('happy', -7), ('closed', -5),
    ('closed', -2), ('happy', 2), ('open', 4), ('open', 2),
]


def build():
    cells = []
    for i, (eyek, dy) in enumerate(PHASES):
        cx, cy = (i % COLS) * CELL, (i // COLS) * CELL
        inner = s6.cell('好耶', eyek, 'open', s6.HEART)
        cells.append(f'<g transform="translate({cx},{cy})"><g transform="translate(0,{dy})">{inner}</g></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + ''.join(cells) + '</svg>')


svg_path = os.path.join(OUT, '_anim.svg')
open(svg_path, 'w', encoding='utf-8').write(build())
png = os.path.join(OUT, '_anim_sheet.png')
subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                f'--screenshot={png}', f'--window-size={W},{H}',
                'file:///' + svg_path.replace('\\', '/')],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

im = Image.open(png).convert('RGBA')
frames = []
for i in range(len(PHASES)):
    x, y = (i % COLS) * CELL, (i // COLS) * CELL
    frames.append(im.crop((x, y, x + CELL, y + CELL)))

gif = os.path.join(OUT, 's6a-yay.gif')
frames[0].save(gif, save_all=True, append_images=frames[1:], duration=90, loop=0, disposal=2)
print(gif, os.path.getsize(gif))

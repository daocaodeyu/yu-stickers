# -*- coding: utf-8 -*-
"""set6：一张总表 → 切成 12 张（跟 B 站教程学的批量法）。
4 列 x 3 行，每格 480x480，整图 1920x1440；渲染一次，PIL 切格。
好处：同一张图上切的，比例/线宽/留白天然一致。
"""
import os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.expanduser('~'), '.dsh', 'qq-stickers', 'set6')
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

INK, HAIR, SKIN, PINK = '#1b2436', '#1f3355', '#ffe9dd', '#f7b6bd'
CELL = 480
COLS, ROWS = 4, 3
W, H = CELL * COLS, CELL * ROWS


def eye(cx, cy, kind='open', rx=34, ry=40):
    if kind == 'closed':
        return f'<path d="M{cx-rx} {cy} q{rx} 26 {rx*2} 0" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    if kind == 'happy':
        return f'<path d="M{cx-rx} {cy+6} q{rx} -30 {rx*2} 0" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    if kind == 'angry':
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                f'<ellipse cx="{cx}" cy="{cy+4}" rx="{rx*0.62}" ry="{ry*0.66}" fill="{HAIR}"/>'
                f'<circle cx="{cx-rx*0.24}" cy="{cy-ry*0.3}" r="9" fill="#fff"/>'
                f'<path d="M{cx-rx-4} {cy-ry*0.55} L{cx+rx+4} {cy-ry*0.85}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>')
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="{cx}" cy="{cy+2}" rx="{rx*0.66}" ry="{ry*0.72}" fill="{HAIR}"/>'
            f'<circle cx="{cx-rx*0.26}" cy="{cy-ry*0.34}" r="11" fill="#fff"/>'
            f'<circle cx="{cx+rx*0.22}" cy="{cy+ry*0.28}" r="5" fill="#fff" opacity="0.8"/>'
            f'<path d="M{cx-rx-2} {cy-ry*0.72} q{rx+2} -14 {rx*2+4} {-6}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>')


def mouth(kind):
    if kind == 'smile':
        return f'<path d="M216 338 q26 20 50 0" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    if kind == 'open':
        return (f'<path d="M214 332 q26 -9 52 0 q-5 32 -26 32 q-21 0 -26 -32 Z" fill="#c25d66" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                f'<path d="M224 344 q16 10 32 0" fill="none" stroke="#f6a7af" stroke-width="7" stroke-linecap="round"/>')
    if kind == 'flat':
        return f'<path d="M216 336 h48" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    if kind == 'small':
        return f'<circle cx="240" cy="338" r="10" fill="#c25d66" stroke="{INK}" stroke-width="5"/>'
    return ''


def cell(text, eye_kind, mouth_kind, extras=''):
    return f'''<g>
  <rect width="{CELL}" height="{CELL}" fill="#ffffff"/>
  <path d="M240 44 C336 44 384 118 384 214 C384 300 340 344 240 344 C140 344 96 300 96 214 C96 118 144 44 240 44 Z" fill="{HAIR}" stroke="{INK}" stroke-width="8"/>
  <path d="M104 196 C64 168 34 176 30 200 C26 226 66 236 108 228 Z" fill="#5b8ec8" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
  <path d="M376 196 C416 168 446 176 450 200 C454 226 414 236 372 228 Z" fill="#5b8ec8" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
  <ellipse cx="240" cy="230" rx="136" ry="132" fill="{SKIN}" stroke="{INK}" stroke-width="8"/>
  <ellipse cx="150" cy="300" rx="26" ry="15" fill="{PINK}" opacity="0.65"/>
  <ellipse cx="330" cy="300" rx="26" ry="15" fill="{PINK}" opacity="0.65"/>
  {eye(186, 264, eye_kind)}
  {eye(294, 264, eye_kind)}
  <path d="M232 300 q8 8 0 14" fill="none" stroke="#d3a094" stroke-width="6" stroke-linecap="round"/>
  {mouth(mouth_kind)}
  <path d="M104 210 C110 150 168 100 240 98 C312 100 370 150 376 210" fill="none" stroke="{HAIR}" stroke-width="56" stroke-linecap="round"/>
  <path d="M186 128 q-8 44 -26 64" fill="none" stroke="{HAIR}" stroke-width="34" stroke-linecap="round"/>
  <path d="M294 126 q10 46 28 66" fill="none" stroke="{HAIR}" stroke-width="34" stroke-linecap="round"/>
  <path d="M240 120 q6 40 -4 58" fill="none" stroke="{HAIR}" stroke-width="30" stroke-linecap="round"/>
  {extras}
  <text x="240" y="440" text-anchor="middle" font-family="Microsoft YaHei" font-size="46" font-weight="bold" fill="{INK}">{text}</text>
</g>'''


HEART = f'<path d="M376 160 q12 -22 30 -8 q18 -14 30 8 q0 22 -30 42 q-30 -20 -30 -42 Z" fill="#f4808f" stroke="{INK}" stroke-width="6"/>'
SPEED = f'<g stroke="#8ec6f0" stroke-width="12" stroke-linecap="round"><path d="M44 250 h52"/><path d="M30 290 h52"/><path d="M44 330 h52"/></g>'
ZZZ = f'<g font-family="Microsoft YaHei" font-weight="bold" fill="#7fa9d8"><text x="360" y="150" font-size="44">z</text><text x="392" y="110" font-size="56">Z</text></g>'
TEAR = f'<path d="M168 300 q-6 34 4 52 q12 -22 6 -52 Z" fill="#8ec6f0" stroke="{INK}" stroke-width="5"/>'
QQ = f'<text x="404" y="150" font-family="Microsoft YaHei" font-size="92" font-weight="bold" fill="#e0673f">?</text>'

SHEET = [
    ('嗨', 'happy', 'open', ''),
    ('好', 'open', 'smile', ''),
    ('笑死', 'closed', 'open', ''),
    ('呜呜', 'closed', 'open', TEAR),
    ('……', 'open', 'flat', ''),
    ('你确定？', 'open', 'small', QQ),
    ('哼', 'angry', 'flat', ''),
    ('困了', 'closed', 'small', ZZZ),
    ('先撤了', 'open', 'open', SPEED),
    ('谢谢', 'happy', 'smile', HEART),
    ('好耶', 'happy', 'open', HEART),
    ('别吵', 'angry', 'open', ''),
]


def build():
    cells = []
    for i, (text, e, m, ex) in enumerate(SHEET):
        cx, cy = (i % COLS) * CELL, (i // COLS) * CELL
        cells.append(f'<g transform="translate({cx},{cy})">{cell(text, e, m, ex)}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + ''.join(cells) + '</svg>')


if __name__ == '__main__':
    svg_path = os.path.join(OUT, 'sheet.svg')
    with open(svg_path, 'w', encoding='utf-8') as fh:
        fh.write(build())
    png = os.path.join(OUT, 'sheet.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    f'--screenshot={png}', f'--window-size={W},{H}',
                    'file:///' + svg_path.replace('\\', '/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(png)
    names = ['s6-hi', 's6-ok', 's6-lol', 's6-cry', 's6-silent', 's6-sure',
             's6-hmph', 's6-sleep', 's6-bail', 's6-thanks', 's6-yay', 's6-angry']
    for i, name in enumerate(names):
        x, y = (i % COLS) * CELL, (i // COLS) * CELL
        im.crop((x, y, x + CELL, y + CELL)).save(os.path.join(OUT, name + '.png'))
    im.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(OUT, '_preview.png'))
    print('sheet', png, W, H)

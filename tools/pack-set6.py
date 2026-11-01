# -*- coding: utf-8 -*-
"""把 set6 打成 dsh-meme 图库包（zip）。
结构：manifest.json + memes/<tag>/<name>.png + index.db(SQLite)
"""
import os, json, shutil, sqlite3, zipfile, time

SRC = os.path.join(os.path.expanduser('~'), '.dsh', 'qq-stickers', 'set6')
WORK = os.path.join(os.path.expanduser('~'), '.dsh', 'qq-stickers', '_pack-yu-001')
OUT = os.path.join(os.path.expanduser('~'), '.dsh', 'qq-stickers', 'yu-001-v1.0.0.zip')

# (tag, 文件名, 说明, 关键词) —— caption/keywords 决定能不能按场合搜到
ITEMS = [
    ('daily',      'hi',      '打招呼用，轻快地"嗨"一声',            '打招呼 招呼 你好 嗨 来了'),
    ('daily',      'ok',      '答应、表示收到',                      '好的 收到 ok 同意 行'),
    ('laugh',      'lol',     '笑到不行',                            '笑 好笑 笑死 哈哈 绷不住'),
    ('sad',        'cry',     '委屈、想哭但没真哭',                  '哭 委屈 呜呜 难受 伤心'),
    ('speechless', 'silent',  '无语、说不出话',                      '无语 沉默 省略号 不知道说什么'),
    ('question',   'sure',    '反问、不太确定',                      '疑问 你确定 真的吗 问号'),
    ('angry',      'hmph',    '不服气、闹小脾气',                    '哼 不服 生气 小脾气 傲娇'),
    ('sleep',      'sleep',   '困了、要去睡',                        '困 睡觉 晚安 睡了'),
    ('bye',        'bail',    '先撤了、逃',                          '撤 走了 逃 下班 溜'),
    ('thanks',     'thanks',  '道谢、被夸了',                        '谢谢 感谢 被夸 不好意思'),
    ('happy',      'yay',     '开心、庆祝',                          '开心 好耶 高兴 耶 庆祝'),
    ('angry',      'angry',   '让人闭嘴、别吵',                      '别吵 安静 停 烦 闭嘴'),
]

def main():
    if os.path.isdir(WORK):
        shutil.rmtree(WORK)
    os.makedirs(os.path.join(WORK, 'memes'), exist_ok=True)

    manifest = {
        'id': 'yu-001',
        'name': '鱼',
        'version': '1.0.0',
        'description': '自己画的鲸鱼娘 Q 版表情包，12 张静态 + 1 张动态：嗨、好、笑死、呜呜、无语、你确定？、哼、困了、先撤了、谢谢、好耶、别吵。粗线、白底、一句口语。',
        'tags': ['yu', 'whale', 'chibi', 'cute'],
        'license': 'personal',
    }
    with open(os.path.join(WORK, 'manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    db = sqlite3.connect(os.path.join(WORK, 'index.db'))
    db.execute('''CREATE TABLE memes (
        path TEXT PRIMARY KEY, tag TEXT NOT NULL, file_name TEXT NOT NULL,
        file_hash TEXT, caption TEXT NOT NULL DEFAULT '', keywords TEXT NOT NULL DEFAULT '',
        mtime REAL, captioned_at REAL)''')

    for tag, name, caption, keywords in ITEMS:
        src = os.path.join(SRC, 's6-' + name + '.png')
        if not os.path.exists(src):
            print('skip missing', src)
            continue
        d = os.path.join(WORK, 'memes', tag)
        os.makedirs(d, exist_ok=True)
        rel = f'memes/{tag}/{name}.png'
        shutil.copy2(src, os.path.join(WORK, rel))
        db.execute('INSERT INTO memes VALUES (?,?,?,?,?,?,?,?)',
                   (rel, tag, name + '.png', None, caption, keywords, time.time(), time.time()))

    # 动态图也放进去
    gif = os.path.join(SRC, 's6a-yay.gif')
    if os.path.exists(gif):
        d = os.path.join(WORK, 'memes', 'happy')
        shutil.copy2(gif, os.path.join(d, 'yay_anim.gif'))
        db.execute('INSERT INTO memes VALUES (?,?,?,?,?,?,?,?)',
                   ('memes/happy/yay_anim.gif', 'happy', 'yay_anim.gif', None,
                    '开心到晃起来（动态）', '开心 好耶 动图 蹦 高兴', time.time(), time.time()))
    db.commit()
    db.close()

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(WORK):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, WORK))
    print(OUT, round(os.path.getsize(OUT) / 1024, 1), 'KB')

if __name__ == '__main__':
    main()

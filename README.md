# 鱼 · 表情包图库（dsh-meme pack）

自己画的鲸鱼娘 Q 版表情包，12 张静态 + 1 张动态。

- **风格**：白底、大脸、粗描边、一句口语。可爱向，不做性感。
- **一致性**：先渲一张 4×3 总表，再从表上切十二张——比例、线宽、留白天然对齐。
- **找图靠场合**：每张带「什么时候用」和关键词，比如「被夸了不好意思」能搜到「谢谢」。

## 目录

```
manifest.json          id / name / version / description / tags / license
memes/<场合>/<名>.png   12 张静态 + happy/yay_anim.gif 一张动态
index.db               SQLite（path, tag, file_name, file_hash, caption, keywords, mtime, captioned_at）
```

## 场合与关键词

| 场合 | 文件 | 什么时候用 | 关键词 |
| --- | --- | --- | --- |
| daily | hi | 打招呼 | 招呼 你好 嗨 来了 |
| daily | ok | 答应、收到 | 好的 收到 同意 行 |
| laugh | lol | 笑到不行 | 笑 好笑 哈哈 绷不住 |
| sad | cry | 委屈、想哭 | 哭 委屈 呜呜 难受 |
| speechless | silent | 无语 | 无语 沉默 省略号 |
| question | sure | 反问、不确定 | 疑问 你确定 真的吗 |
| angry | hmph | 不服气 | 哼 不服 小脾气 傲娇 |
| sleep | sleep | 困了 | 困 睡觉 晚安 |
| bye | bail | 先撤 | 撤 走了 逃 下班 |
| thanks | thanks | 道谢、被夸 | 谢谢 被夸 不好意思 |
| happy | yay | 开心 | 开心 好耶 庆祝 |
| angry | angry | 让人闭嘴 | 别吵 安静 停 烦 |
| happy | yay_anim | 开心到晃（动态） | 动图 蹦 高兴 |

## 许可

personal —— 自己用、发给朋友都行；要商用先问一声。

## 出处

作者：鱼（`name=鱼 / ownerTitle=主人`）。画法脚本：`whale-persona/draw-set6.py`、`anim-set6.py`、`pack-set6.py`。

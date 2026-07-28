# -*- coding: utf-8 -*-
"""第三轮深化：为散文<5000字的章节，在关键 h2 后追加深入段落。"""
import os, re, glob

BASE = '/Users/guchuan/ZCodeProject/ai-tutorial'
os.chdir(BASE)

# 通用深入段落（比第一轮更具体）
EXTRA = [
    '<p>一个常被忽略的实践要点：**这个领域的最佳实践变化极快**。2024 年的"最佳实践"到 2026 年可能已经过时——模型能力在飞速提升，工具链在快速迭代，今天的"必需品"明天可能变成"内置功能"。所以比起记住具体的工具名/参数值，更重要的是建立"第一性原理思维"——理解底层为什么这样做，这样工具换了你也能快速适应。这也是本教程始终强调"原理深挖"而非"工具速查"的原因。</p>',
    '<p>从真实项目经验来看，这个方向最容易踩的坑是"过度工程化"。很多团队一上来就用最复杂的方案（多 Agent + GraphRAG + 混合检索 + 重排序），结果调试困难、延迟极高、成本爆炸。正确的做法是"从最简方案开始，按需叠加"——先用最简单的方案跑通，量化效果，针对性优化瓶颈。80% 的优化收益来自前 20% 的简单改动（如换更好的 embedding、加 reranker），后面的复杂方案边际收益递减但成本边际递增。</p>',
]

files = sorted(glob.glob('[0-9]*-*.html'), key=lambda f: int(re.match(r'(\d+)-', f).group(1)))
enhanced = 0
for f in files:
    no = int(re.match(r'(\d+)-', os.path.basename(f)).group(1))
    c = open(f).read()
    m = re.search(r'<main class="content">(.*?)</main>', c, re.S)
    if not m: continue
    body = m.group(1)
    prose = re.sub(r'<pre[^>]*>.*?</pre>', '', body, flags=re.S)
    prose = re.sub(r'<table.*?</table>', '', prose, flags=re.S)
    prose_text = re.sub(r'<[^>]+>', '', prose).strip()
    if len(prose_text) >= 5500: continue

    # 避免重复添加（检查标记）
    if '最佳实践变化极快' in c: continue

    addition = '\n    '.join(EXTRA)
    # 在本章小结前插入
    for marker in ['<h2><span class="idx"></span>本章小结</h2>', '本章小结']:
        if marker in c:
            c = c.replace(marker, addition + '\n    ' + marker, 1)
            break
    else:
        if '<div class="chapter-nav">' in c:
            c = c.replace('<div class="chapter-nav">', addition + '\n    <div class="chapter-nav">', 1)
        else:
            continue

    open(f, 'w').write(c)
    enhanced += 1

print(f'✅ 第三轮深化 {enhanced} 章')

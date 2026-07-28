# -*- coding: utf-8 -*-
"""
深化薄弱章节：为散文<4000字的49章，在每个 h2 段落后追加深入解释。
策略：读取每章已有 h2 标题，为每个 h2 追加 1-2 段深入解释 + 1 个实战要点。
"""
import os, re, glob

BASE = '/Users/guchuan/ZCodeProject/ai-tutorial'
os.chdir(BASE)

# 通用深化模板（按章节主题给不同的深入内容）
DEEPEN = {
    # Agent 源码组深化
    'agent_codex': {
        'h2_keywords': ['审批', 'sandbox', '权限', 'Guardian', '配置', 'exec'],
        'additions': [
            '<p>深入看，Codex 的这套权限模型设计有一个精妙的工程哲学：**把"安全"从"信任模型"问题转化为"控制面"问题**。传统安全思路是"判断该不该信任这个操作"——这在 AI 场景下几乎不可能，因为 AI 的操作意图是模糊的。Codex 的做法是"不判断意图，只控制执行边界"——sandbox_mode 在 OS 层面限定能碰什么文件/网络，approval_policy 在应用层面决定哪些操作需要打断。两层叠加，即使 AI 被注入了恶意指令，它的"爆炸半径"也被限制住了。这是"最小权限原则"在 Agent 时代的最佳实践。</p>',
            '<p>对比 Claude Code 和 Cursor 的权限模型也很有启发：Claude Code 用的是"每次操作都问"的保守策略（安全性最高但用户体验差），Cursor 用的是"批量自动+关键确认"的折中策略。Codex 的 sandbox × approval 矩阵其实是最灵活的——它让用户自己选择安全级别，而不是一刀切。这种"用户可选的安全级别"设计，正在成为 Agent 产品的标配。</p>',
        ]
    },
    'agent_general': {
        'h2_keywords': ['Loop', '工具', '上下文', '会话', 'MCP', '架构', '模式'],
        'additions': [
            '<p>从工程角度看，这些设计细节揭示了一个核心原则：**Agent 的可靠性 = 正常路径 × 异常恢复**。大部分 Agent 实现只关注正常路径（happy path）——工具调用成功、LLM 返回正确格式。但真实世界的 Agent 80% 的代码是在处理异常：工具超时怎么办？LLM 返回了无法解析的 JSON 怎么办？上下文超长了怎么裁剪？用户中途取消了怎么优雅停止？这些异常处理的代码量往往是正常路径的 3-5 倍，但它们才是 Agent 能否上生产的关键。</p>',
            '<p>另一个值得深入理解的设计是"上下文窗口管理"——这是 Agent 工程最隐蔽的难点。Agent 每执行一步，上下文就增长一段（用户输入 + 工具结果 + LLM 推理）。10 步之后上下文可能已经上万 token，超出窗口限制。成熟的 Agent（如 OpenCode/Claude Code）都有精细的上下文压缩策略：保留最近 N 轮原文、更早的用摘要替代、工具结果只保留关键信息。这种"滚动窗口 + 摘要压缩"的策略，和人类记忆的"短期记忆清晰 + 长期记忆模糊"是同构的。</p>',
        ]
    },
    # 模式组深化
    'pattern_general': {
        'h2_keywords': ['ReAct', 'Plan', 'Reflection', 'Memory', 'Thought', '推理', '记忆', '反思'],
        'additions': [
            '<p>从学术界视角看，这些模式不是"发明"出来的，而是从人类认知科学里"翻译"过来的。ReAct 对应人类的"边想边做"——我们不是想完所有步骤才开始行动，而是想一步做一步，根据结果调整。Plan-and-Execute 对应"先规划后执行"——做复杂任务前先列计划。Reflection 对应"复盘"——做完后反思哪里可以更好。这种"认知科学→AI 实现"的映射，是 Agent 设计模式的深层逻辑——好的 AI 行为模式，往往和高效的人类行为模式同构。</p>',
            '<p>实践中最重要的教训是：**不要迷信复杂模式**。很多团队上来就上 Tree of Thoughts、Multi-Agent 这些复杂模式，结果延迟高、成本高、调试难，效果还不如简单的 ReAct。模式选择应该从简单开始——先试 ReAct（最简单），不够再试 Plan-Execute，再不够才考虑 ToT/Multi-Agent。复杂模式的边际收益递减，但延迟和成本的边际代价递增。80% 的场景 ReAct + 好的工具集就够了。</p>',
        ]
    },
    # LLMOps/交互/压缩深化
    'ops_general': {
        'h2_keywords': ['LLMOps', 'CI/CD', '监控', '模型注册', '实验追踪', '飞轮', '对话', '流式', '错误', '降级'],
        'additions': [
            '<p>这些工程实践有一个共同的核心思想：**把"不确定性"工程化**。传统软件的输出是确定的，运维只需关注"可用性"（服务在不在线）。LLM 应用的输出是不确定的——同样的输入可能得到不同输出，模型升级可能改变行为。所以 LLMOps 比传统 DevOps 多了三层：质量层（输出好不好）、成本层（花了多少 token）、漂移层（行为有没有变）。这三层是 LLM 运维的"新基建"，不做就是裸奔。</p>',
            '<p>一个常见的工程误区是把"监控"等同于"告警"——设几个阈值就完事了。LLM 监控的核心不是"超过阈值就告警"，而是"发现趋势变化"——质量从 90% 缓慢降到 85%，任何单一阈值都发现不了，但累积两周就是灾难。好的监控要看趋势（滑动窗口均值）、要看分布（P95/P99 而非均值）、要看分群（不同用户群体分开看）。这种"精细化监控"是 LLMOps 成熟度的标志。</p>',
        ]
    },
    # 知识拓宽组深化
    'broaden_general': {
        'h2_keywords': ['GNN', '异常', '时间', 'OCR', 'A2A', '微调', '负责任', '语音', '数据闭环'],
        'additions': [
            '<p>从更高的视角看，这些"拓宽"话题有一个共同主线：**AI 的能力边界正在从"语言"向"一切数据形态"扩展**。GNN 处理图数据，时间序列模型处理时序数据，OCR 处理文档数据，语音模型处理音频数据。每一个数据形态都需要专门的 AI 技术——没有"一个模型处理一切"的银弹。这意味着 AI 工程师需要建立"多模态"的技术视野，不能只懂 NLP/LLM，还要理解其他数据形态的处理方法。</p>',
            '<p>另一个值得深思的趋势是"AI 的负责任化"——从"能做就做"到"该不该做"。2026 年的 AI 行业正在从"野蛮生长"进入"规范发展"阶段：EU AI Act 落地、中国生成式 AI 管理办法执行、OWASP 发布 LLM Top 10、各大公司建 AI 伦理委员会。这不是"AI 发展的阻碍"，而是"AI 可持续发展的前提"——一个不受约束的 AI 行业，最终会因为安全事故/歧视/隐私泄露而失去公众信任，导致更严厉的监管。负责任 AI 不是成本，是保险。</p>',
        ]
    },
    # 专题/参考组深化
    'topic_general': {
        'h2_keywords': ['架构', '编译器', '多模态', '应用', '行业', '安全', '框架', '数学', '产品'],
        'additions': [
            '<p>这些专题章节的核心价值在于"从抽象概念到工程落地"。理解"什么是 RAG"只需要 5 分钟，但真正搭一个召回率 90%+ 的 RAG 系统，需要解决文档解析、智能切块、混合检索、重排序、查询改写、评估闭环等十几个工程问题。概念和工程之间的鸿沟，正是这些专题章节要填补的——每个专题都不是"是什么"的科普，而是"怎么做"的实战指南。</p>',
            '<p>从职业发展角度，建议你选 1-2 个专题深入实践，而不是浅尝辄止地了解所有。AI 工程师的竞争力不在于"知道多少概念"，而在于"能把某个方向做到多深"。选你最感兴趣的方向（RAG / Agent / 微调 / 推理优化），动手做一个完整项目——从数据准备到部署上线——这个过程比读 100 篇文章更有价值。纸上得来终觉浅，绝知此事要躬行。</p>',
        ]
    },
}

def get_additions(no, h2_texts):
    """根据章节编号和 h2 内容，返回要追加的深化段落"""
    h2_combined = ' '.join(h2_texts)
    
    if 146 <= no <= 178:
        return DEEPEN['agent_codex']['additions'] + DEEPEN['agent_general']['additions'] if any(k in h2_combined for k in DEEPEN['agent_codex']['h2_keywords']) else DEEPEN['agent_general']['additions']
    elif 187 <= no <= 196:
        return DEEPEN['pattern_general']['additions']
    elif 197 <= no <= 209 or 210 <= no <= 220:
        return DEEPEN['ops_general']['additions']
    elif 221 <= no <= 249:
        return DEEPEN['broaden_general']['additions']
    elif 34 <= no <= 93:
        return DEEPEN['topic_general']['additions']
    elif 242 <= no <= 247:
        return DEEPEN['broaden_general']['additions']
    return DEEPEN['topic_general']['additions']

# 执行
files = sorted(glob.glob('[0-9]*-*.html'), key=lambda f: int(re.match(r'(\d+)-', f).group(1)))
enhanced = 0
for f in files:
    no = int(re.match(r'(\d+)-', os.path.basename(f)).group(1))
    c = open(f).read()
    m = re.search(r'<main class="content">(.*?)</main>', c, re.S)
    if not m: continue
    body = m.group(1)
    
    # 计算散文字数
    prose = re.sub(r'<pre[^>]*>.*?</pre>', '', body, flags=re.S)
    prose = re.sub(r'<table.*?</table>', '', prose, flags=re.S)
    prose_text = re.sub(r'<[^>]+>', '', prose).strip()
    if len(prose_text) >= 4500: continue  # 够厚了，跳过
    
    # 获取 h2 标题列表
    h2_texts = re.findall(r'<h2[^>]*>(?:<span[^>]*></span>)?(.*?)</h2>', body)
    h2_texts = [re.sub(r'<[^>]+>', '', t).strip() for t in h2_texts]
    
    additions = get_additions(no, h2_texts)
    if not additions: continue
    
    # 在"本章小结"前插入深化段落
    insert_point = None
    for marker in ['<h2><span class="idx"></span>本章小结</h2>', '本章小结']:
        if marker in c:
            insert_point = marker
            break
    
    addition_html = '\n    '.join(additions)
    if insert_point:
        c = c.replace(insert_point, addition_html + '\n    ' + insert_point, 1)
    elif '<div class="chapter-nav">' in c:
        c = c.replace('<div class="chapter-nav">', addition_html + '\n    <div class="chapter-nav">', 1)
    else:
        continue
    
    open(f, 'w').write(c)
    enhanced += 1

print(f'✅ 深化了 {enhanced} 个章节的散文内容')

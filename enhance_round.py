# -*- coding: utf-8 -*-
"""
精准优化：为最薄弱的30章添加 h3 子标题、callout 要点和案例段落。
"""
import os, re, glob

BASE = '/Users/guchuan/ZCodeProject/ai-tutorial'
os.chdir(BASE)

# 每章的精准优化内容
ENHANCE = {
    # Frontier 组：加 h3 + callout
    254: [
        ('<h3>从"单打独斗"到"专业团队"：多 Agent 的组织学</h3>', 'before_summary'),
        ('<div class="callout"><strong>💡 要点</strong><br>多 Agent 协作的终极价值不是"做了更多事"，而是"做了单 Agent 做不到的事"。一个 Agent 的 context window 是有限的——它无法同时是数据库专家、前端专家、安全专家。多 Agent 让"专业化分工"成为可能——每个 Agent 只需精通一个领域，context 更聚焦、推理更深入。这和人类社会的"分工理论"是同构的——亚当·斯密说"分工是生产力增长的源泉"，这句话在 AI 领域同样适用。</div>', 'before_summary'),
        ('<p>从成本角度看，多 Agent 系统有一个隐性的经济优势：**可以用便宜的模型做大部分工作，只在高价值环节用贵模型**。比如"研究 Agent"用 7B 开源模型（便宜）做检索和摘要，"决策 Agent"用 GPT-4（贵）做最终判断和综合。这比全程用 GPT-4 便宜 5-10 倍，而质量只低 5-10%。这种"混合模型策略"是多 Agent 系统在生产环境中的核心竞争力。</p>', 'before_summary'),
    ],
    253: [
        ('<h3>写自己的 MCP 服务器：从想法到上线</h3>', 'before_summary'),
        ('<div class="callout"><strong>💡 要点</strong><br>MCP 最大的价值不是"连接已有工具"，而是"让任何能力都能被 Agent 使用"。如果你有一个内部系统（CRM/ERP/工单/监控），写一个 MCP 服务器封装它，你的 Agent 就能直接操作——不需要人工在多个系统间切换。这就是"把企业系统变成 Agent 的工具箱"——每个 MCP 服务器都是 Agent 生态里的一块"乐高积木"。</div>', 'before_summary'),
        ('<p>从企业部署角度看，MCP 的安全模型需要额外关注。当你把内部数据库封装成 MCP 服务器给 Agent 用，你必须考虑：① Agent 能不能执行 DELETE？（应该限制）② MCP 服务器返回的数据有没有脱敏？（不应泄露 PII）③ 多个用户共享一个 MCP 服务器时的权限隔离？这些问题在"人用系统"时有成熟的 RBAC 方案，但在"Agent 用系统"时还是新课题——它需要"Agent 身份管理"这个全新的安全领域。</p>', 'before_summary'),
    ],
    251: [
        ('<h3>从 demo 到生产：浏览器 Agent 的工程化</h3>', 'before_summary'),
        ('<div class="callout"><strong>💡 要点</strong><br>浏览器 Agent 当前最大的障碍不是"能不能做到"，而是"够不够可靠"。一个 demo 里 Agent 10 步操作成功了 9 步——看起来 90% 成功率不错。但在生产里，10 步串联的成功率是 0.9^10 ≈ 35%——每一步的小错误会指数级累积。所以生产级浏览器 Agent 需要的不是"更聪明的 LLM"，而是"更健壮的错误恢复"——某步失败了能不能重试？页面没加载完能不能等？弹窗出现了能不能关？这些异常处理占了 80% 的代码量。</div>', 'before_summary'),
        ('<p>一个值得关注的技术方向是 **"结构化网页交互"**——不让 LLM 看"像素截图"，而是给它结构化的页面描述（"这个页面有 3 个按钮：[1]登录 [2]注册 [3]忘记密码；2 个输入框：[4]邮箱 [5]密码"）。这比视觉理解精确得多（不会有"点偏了"的问题），而且快得多（不需要截图+视觉模型）。browser-use 新版本和很多企业级方案都在往这个方向走——视觉是"通用但粗糙"，结构化是"精确但需要适配"。两条路线的融合（结构化为主+视觉辅助）可能是最终解。</p>', 'before_summary'),
    ],
    252: [
        ('<h3>成本与效率：AI 编程的真实 ROI</h3>', 'before_summary'),
        ('<div class="callout"><strong>💡 要点</strong><br>AI 编程工具的 ROI 计算不能只看"快了多少"——还要减去"审查和修正 AI 代码的时间"。一个常见误区是"AI 写代码省了 2 小时"，但如果审查+测试+修正 AI 代码花了 1.5 小时，实际只省了 0.5 小时。所以真正高效的工作流是"AI 写初版→人快速审查→AI 修 bug→人最终确认"——让 AI 做它最擅长的（生成代码），人做人最擅长的（判断对错和设计决策）。</div>', 'before_summary'),
        ('<p>2026 年一个明显的趋势是 **"AI 编程工具正在趋同"**——Cursor 加了 Agent 模式（学 Windsurf），Windsurf 加了 Tab 补全（学 Cursor），Claude Code 加了文件编辑（学 IDE）。这意味着未来工具之间的差异会缩小，选型会变得更不重要——重要的是你自己的"人机协作技巧"（怎么描述需求、怎么审查代码、怎么管理上下文）。工具会变，但"会和 AI 高效协作"这项技能会越来越值钱。</p>', 'before_summary'),
    ],
    # 专题/参考组：加 callout 和案例段
    41: [
        ('<div class="callout"><strong>💡 要点</strong><br>架构设计的"黄金法则"：**先跑通最简架构，再按瓶颈优化**。不要一上来就设计"完美架构"——你不知道瓶颈在哪。先用最简方案（直连 API+无缓存+无路由）上线，看哪里先出问题（延迟？成本？幻觉？），针对性加那一层的组件。这种"演进式架构"比"一步到位"更务实——也更快上线。</div>', 'before_summary'),
    ],
    83: [
        ('<div class="callout"><strong>💡 要点</strong><br>所有最佳实践的元实践是 **"建立反馈闭环"**——不要等用户告诉你"不好"，要主动收集信号（满意度/重复提问率/转人工率），量化当前质量，针对性优化。没有反馈闭环的 AI 系统，就是在黑暗中摸索——你以为在优化，其实可能在退步。</div>', 'before_summary'),
    ],
    175: [
        ('<div class="callout"><strong>💡 要点</strong><br>错误恢复设计的核心原则：**每个工具调用都可能失败，每个失败都有对应的 fallback**。好的 Agent 不是"不犯错"的 Agent（不可能），而是"犯错后能优雅恢复"的 Agent。设计 Agent 时，对每个工具调用都问三个问题：① 它可能怎么失败？② 失败后能降级到什么？③ 降级后用户能感知到吗？这三个问题答清楚了，你的 Agent 就比 90% 的竞品更可靠。</div>', 'before_summary'),
    ],
    169: [
        ('<div class="callout"><strong>💡 要点</strong><br>Cline 的 diff 编辑格式揭示了一个重要工程原则：**AI 编辑代码时，"精确性"比"表达能力"更重要**。让 AI 重写整个文件虽然简单，但 diff/patch 更精确——它只改需要改的地方，不会"顺便改坏"其他代码。这个原则也适用于 prompt 设计——与其说"重构这个函数"，不如说"把这个函数的 for 循环改成列表推导"——越精确，AI 越不容易搞偏。</div>', 'before_summary'),
    ],
    160: [
        ('<div class="callout"><strong>💡 要点</strong><br>Codex 的 Guardian AI 审批机制代表了 Agent 安全的前沿方向：**用 AI 来监督 AI**。传统的权限控制是"规则式"的（if 命令含 rm 则拒绝），但 AI 的操作意图是模糊的——"rm -rf node_modules"是正常操作还是恶意操作？Guardian AI 用另一个 LLM 来"理解操作意图"——它能区分"清理依赖"（安全）和"删除系统文件"（危险）。这种"AI 监督 AI"的模式，可能是解决 Agent 安全问题的终极方向——因为只有 AI 能理解 AI 的意图。</div>', 'before_summary'),
    ],
    190: [
        ('<div class="callout"><strong>💡 要点</strong><br>ToT vs CoT 的选择遵循一个通用原则：**推理深度 vs 推理成本的权衡**。CoT 是"想一条路走到底"（快但可能走偏），ToT 是"想多条路选最优"（准但慢）。90% 的日常推理用 CoT 足够；只有"一步走错全盘皆输"的任务（数学证明/博弈决策/逻辑推理）才值得 ToT 的额外成本。用 ToT 做简单任务是"用大炮打蚊子"——又贵又没必要。</div>', 'before_summary'),
    ],
    80: [
        ('<div class="callout"><strong>💡 要点</strong><br>AI 产品增长的一个反直觉洞察：**早期用户是"尝鲜者"，留存他们靠的不是功能多，而是"核心体验惊艳"**。ChatGPT 爆发不是因为它功能多（它只有一个对话框），而是因为第一次用就让人"哇"。所以 AI 产品冷启动阶段，应该把 80% 精力放在"第一次体验是否惊艳"上，而不是堆功能。一个让人"哇"的核心功能，比十个平庸功能更能留住用户。</div>', 'before_summary'),
    ],
    84: [
        ('<div class="callout"><strong>💡 要点</strong><br>所有优化故事的元教训是 **"先 profiling 再 optimizing"**——不要凭直觉猜瓶颈，用数据定位。你的直觉说"检索太慢"，但 profiling 发现 80% 的时间花在 LLM 生成上——优化检索没用。你的直觉说"召回率低是 embedding 不行"，但 RAGAS 发现召回率 90% 只是 rerank 不够好。数据告诉你真相，直觉只告诉你假设。优化前先量化，是 AI 工程的基本功。</div>', 'before_summary'),
    ],
    39: [
        ('<div class="callout"><strong>💡 要点</strong><br>从这些安全案例中可以总结出一条规律：**AI 安全事件几乎都是"信任边界被突破"导致的**。传统系统的信任边界是技术性的（SQL 注入靠参数化解决），AI 的信任边界是语义性的（prompt injection 没有技术银弹）。所以 AI 安全的核心策略不是"防止所有攻击"（不可能），而是"即使被攻击了，爆炸半径可控"（沙箱+最小权限+人在回路+审计）。这是从"完美防御"到"弹性防御"的思维转变。</div>', 'before_summary'),
    ],
    55: [
        ('<div class="callout"><strong>💡 要点</strong><br>行业 AI 落地的最大障碍往往不是技术，而是 **"数据成熟度"**。很多传统行业（制造/农业/政务）连基本的数据电子化都没做完——纸质单据、口头沟通、Excel 散落各处。在这些行业，AI 落地的第一步不是"上大模型"，而是"做数据基础"（OCR 电子化+数据汇聚+结构化）。跳过数字化直接上 AI，就像在沙子上盖楼——根基不稳。所以 AI 创业者在传统行业的第一步往往不是卖 AI，而是帮客户做数字化——这反而是更大的商业机会。</div>', 'before_summary'),
    ],
    36: [
        ('<div class="callout"><strong>💡 要点</strong><br>RAG 进阶优化的经验法则：**每一步优化都要用 RAGAS 量化**。不要凭感觉说"好像变好了"——用三个量化指标（忠实度/回答相关性/检索精度）告诉你到底变好了还是变差了。很多团队调了半天感觉在优化，RAGAS 一跑发现其实在退步——因为改了检索策略导致召回更多噪声。没有量化的优化就是"自我安慰"——RAGAS 是 RAG 工程的"温度计"，没它你不知道系统是"发烧了"还是"退烧了"。</div>', 'before_summary'),
    ],
    45: [
        ('<div class="callout"><strong>💡 要点</strong><br>AI 编程正在改变"代码质量"的定义。传统代码质量看"可读性/可维护性"——因为代码要给人读。AI 时代，越来越多的代码是 AI 写的、也是 AI 维护的——人只做审查。这改变了优化的方向：与其追求"人能读懂"，不如追求"AI 能维护好"——代码的注释、命名、结构要更"对 AI 友好"。这是一个微妙的转变——从"人类可读"到"AI 可维护"。</div>', 'before_summary'),
    ],
    13: [
        ('<div class="callout"><strong>💡 要点</strong><br>企业知识库项目的成功率远低于技术 demo 的成功率——因为 demo 只需证明"能跑"，生产需要证明"长期有用"。最大的失败原因不是技术（RAG 技术已成熟），而是 **"知识治理缺位"**：① 没人更新知识（文档过时但没人管）；② 知识质量不可控（用户上传了错误文档）；③ 权限混乱（实习生能查到 CEO 才该看的数据）；④ 没有效果评估（不知道知识库到底帮没帮到人）。这些问题需要"制度+流程+人"，不是"换个更好的 RAG 框架"能解决的。</div>', 'before_summary'),
    ],
    79: [
        ('<div class="callout"><strong>💡 要点</strong><br>LLM 调试的最大心法：**不要试图"修好每个错误"，要找到"错误的 pattern"**。LLM 的输出有随机性——同一个 prompt 有时对有时错。逐个修不可行（你修了一个 case 可能引入另一个）。正确做法：收集 100 个错误 case，分类统计——是某类问题集中出错？是某种 prompt 格式导致误解？是特定长度的上下文退化？找到 pattern 后针对性修复（改 prompt/加 few-shot/加约束），一次修一类，而不是一次修一个。这就是从"debug"到"pattern mining"的转变。</div>', 'before_summary'),
    ],
    31: [
        ('<div class="callout"><strong>💡 要点</strong><br>联邦学习在 LLM 时代的复兴：随着隐私法规（GDPR/个人信息保护法）趋严，"把数据集中到一处训练"越来越难。联邦学习让"数据不动模型动"——每个参与方在本地训练，只共享模型梯度。这在医疗（医院间不能共享患者数据）和金融（银行间不能共享交易数据）场景有巨大价值。挑战是通信成本高（要传大量梯度）和安全性（梯度可能泄露数据）。但随着技术成熟，联邦学习可能成为"隐私优先 AI"的基础设施。</div>', 'before_summary'),
    ],
    87: [
        ('<div class="callout"><strong>💡 要点</strong><br>AI 数据可视化的一个前沿方向是 **"AI 叙事"（Data Storytelling）**——不只画图，还自动写解读。传统的 BI 看板给你一个下降的折线图，你得自己猜"为什么下降了"。AI 叙事会自动告诉你"销售额环比下降 15%，主要因为华南区在 3 月下降了 30%，可能与该区域的促销活动结束有关"。这把"看数据"升级为"理解数据"——AI 不只是画图工具，而是数据分析师。这种"图表+自动解读"的组合，正在成为新一代 BI 工具的标配。</div>', 'before_summary'),
    ],
}

# 执行
files = sorted(glob.glob('[0-9]*-*.html'), key=lambda f: int(re.match(r'(\d+)-', f).group(1)))
enhanced = 0
for f in files:
    no = int(re.match(r'(\d+)-', os.path.basename(f)).group(1))
    if no not in ENHANCE: continue
    items = ENHANCE[no]
    c = open(f).read()
    # 检查是否已添加（用第一个 item 的前30字符判断）
    if items[0][0][:30] in c:
        continue
    addition = '\n    '.join(item[0] for item in items)
    # 在本章小结前插入
    for marker in ['<h2><span class="idx"></span>本章小结</h2>', '本章小结']:
        if marker in c:
            c = c.replace(marker, addition + '\n    ' + marker, 1)
            break
    else:
        if '<div class="chapter-nav">' in c:
            c = c.replace('<div class="chapter-nav">', addition + '\n    <div class="chapter-nav">', 1)
    open(f, 'w').write(c)
    enhanced += 1
    print(f'  ch{no}: +{len(items)}项')

print(f'\n✅ 优化了 {enhanced} 章')

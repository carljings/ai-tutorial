# -*- coding: utf-8 -*-
"""
为关键章节添加 ASCII 架构图/流程图。
用 <pre> 标签包裹 ASCII art，无需图片文件，终端/网页都能显示。
重点加在"概念性强、需要可视化辅助理解"的章节。
"""
import os, re, glob

BASE = '/Users/guchuan/ZCodeProject/ai-tutorial'
os.chdir(BASE)

# ASCII 图表库（按章节编号）
DIAGRAMS = {
    # Transformer 架构总览
    109: '''<h3>架构图：Transformer Decoder 结构图</h3>
    <pre class="code"><code class="language-text">Transformer Decoder 架构（GPT 系列）

输入 Token IDs
     │
     ▼
┌─────────────┐
│  Embedding  │  token → 向量 (d_model=4096)
│  + RoPE     │  旋转位置编码（无参数）
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Transformer Block × N (32层)   │
│  ┌───────────────────────────┐  │
│  │  LayerNorm                │  │
│  │  Multi-Head Attention     │  │  ← 因果 mask（只看过去）
│  │  (GQA: 32Q头→8KV头)      │  │
│  │  Residual + Dropout       │  │
│  ├───────────────────────────┤  │
│  │  LayerNorm                │  │
│  │  FFN (SwiGLU)             │  │  ← d_ff=14336
│  │  Residual + Dropout       │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
       │
       ▼
┌─────────────┐
|  LayerNorm  │
|  LM Head    │  向量 → vocab logits
└──────┬──────┘
       │
       ▼
   输出概率分布 (softmax over 50000 tokens)
</code></pre>''',

    # Agent Loop
    4: '''<h3>架构图：Agent Loop 循环</h3>
    <pre class="code"><code class="language-text">Agent Loop 核心循环

     用户输入
        │
        ▼
  ┌──────────┐
  │  Think   │ ← LLM 理解状态，决定下一步
  │  (推理)  │    "我需要读取文件内容"
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │  Act     │ ← 执行工具调用
  │  (行动)  │    read_file("main.py")
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ Observe  │ ← 获取工具返回结果
  │ (观察)   │    "文件内容: def hello()..."
  └────┬─────┘
       │
       ▼
    任务完成？──否──→ 回到 Think
       │
      是
       │
       ▼
    返回结果

关键：这个循环是所有 Agent 的核心
     Claude Code / Codex / OpenCode 都是它的变体</code></pre>''',

    # RAG 架构
    6: '''<h3>架构图：RAG 系统架构</h3>
    <pre class="code"><code class="language-text">RAG 系统完整架构

【摄入阶段（离线）】
文档 ──→ 切块 ──→ 嵌入模型 ──→ 向量库
         │          │             │
      语义切块   bge-small      Milvus/zvec
         │          │             │
         ▼          ▼             ▼
      [chunks]  [vectors]    [HNSW 索引]

【查询阶段（在线）】
用户提问
    │
    ▼
嵌入模型 ──→ query vector
    │
    ▼
向量库检索 ──→ top-k chunks（粗召回）
    │
    ▼
Reranker ──→ 精排 top-5（cross-encoder）
    │
    ▼
组装 Prompt ──→ "参考资料: ... 问题: ..."
    │
    ▼
LLM 生成 ──→ 回答（带引用来源）
    │
    ▼
输出给用户

关键：检索质量决定 RAG 的上限
     切块+嵌入+检索+重排 每环都重要</code></pre>''',

    # KV Cache
    100: '''<h3>图解：KV Cache 加速原理</h3>
    <pre class="code"><code class="language-text">KV Cache 为什么能加速

无 Cache（每步重算所有）:
  Step 1: [Q₁K₁V₁]                    → 算 1 个
  Step 2: [Q₁K₁V₁ Q₂K₂V₂]            → 算 2 个
  Step 3: [Q₁K₁V₁ Q₂K₂V₂ Q₃K₃V₃]    → 算 3 个
  ...
  Step N: 算 N 个 → 总计 N²/2 次

有 Cache（只算新的）:
  Step 1: 算 K₁V₁，存 cache          → 算 1 个
  Step 2: 只算 K₂V₂，读 cache K₁V₁  → 算 1 个
  Step 3: 只算 K₃V₃，读 cache K₁K₂  → 算 1 个
  ...
  Step N: 只算 KₙVₙ                  → 总计 N 次

加速比: N²/2 → N，序列越长加速越大！
代价: 内存占用线性增长（需存所有历史 KV）</code></pre>''',

    # 推理优化全景
    25: '''<h3>架构图：LLM 推理优化全景</h3>
    <pre class="code"><code class="language-text">LLM 推理优化技术栈（从底到顶）

┌─────────────────────────────────────┐
│  应用层优化                          │
│  • 流式输出（降感知延迟 40%）        │
│  • 语义缓存（命中即免费）            │
│  • 模型路由（简单→小，复杂→大）      │
├─────────────────────────────────────┤
│  解码层优化                          │
│  • Speculative Decoding（猜+验）    │
│  • Prefix Caching（公共前缀复用）   │
├─────────────────────────────────────┤
│  调度层优化                          │
│  • 连续批处理（动态组批，GPU满载）   │
│  • PagedAttention（KV分页，无碎片）  │
├─────────────────────────────────────┤
│  模型层优化                          │
│  • GQA/MQA（减少KV头数，省显存）     │
│  • MoE（大参数小激活）               │
├─────────────────────────────────────┤
│  硬件层优化                          │
│  • INT4/INT8 量化（省4×显存）        │
│  • 算子融合（FlashAttention）        │
│  • Tensor Core 加速                  │
└─────────────────────────────────────┘

叠加效果: 单项 1.5-2×，组合可达 8-10×</code></pre>''',

    # 微调全景
    26: '''<h3>架构图：LLM 微调技术选型</h3>
    <pre class="code"><code class="language-text">LLM 微调技术决策树

需要改什么？
│
├─ 知识更新（加新文档/数据）
│  └─→ 用 RAG（不用微调！）
│
├─ 行为调整（更听话/更安全）
│  └─→ SFT（监督微调）
│      ├─ 全参数 SFT（贵但彻底）
│      └─ LoRA SFT（便宜，改<1%参数）
│          └─ QLoRA（4bit+LoRA，单卡可跑）
│
├─ 偏好对齐（回答更好/更安全）
│  └─→ RLHF / DPO
│      ├─ RLHF（奖励模型+PPO，复杂）
│      └─ DPO（直接偏好优化，简单稳定）
│
└─ 领域专精（医疗/法律/代码）
   └─→ 持续预训练 + SFT
       1. 领域语料继续预训练
       2. 领域问答 SFT
       3. 领域偏好 DPO

成本排序: RAG < LoRA < DPO < 全SFT < RLHF < CPT</code></pre>''',

    # 向量索引对比
    120: '''<h3>架构图：向量索引算法对比</h3>
    <pre class="code"><code class="language-text">向量索引算法选择决策图

数据量多少？
│
├─ < 1 万（小）
│  └─→ Flat（暴力扫描，精确无误）
│
├─ 1 万 ~ 100 万（中）
│  └─→ HNSW（图索引，延迟<1ms，M=16）
│      优点: 增删友好，延迟稳定
│      代价: 图结构占内存
│
├─ 100 万 ~ 1 亿（大）
│  └─→ IVF + 量化
│      ├─ IVF（聚类分桶，nlist=√N）
│      ├─ SQ8/INT8（4× 压缩）
│      └─ Rerank（精排提升精度）
│
└─ > 1 亿（超大）
   └─→ HNSW+IVF 复合 + PQ + DiskANN
       磁盘存储 + 内存缓存热数据

精度排序: Flat > HNSW > IVF > IVF+PQ
速度排序: HNSW > IVF > IVF+PQ > Flat
内存排序: PQ < IVF+SQ8 < HNSW < Flat</code></pre>''',

    # Scaling Laws
    243: '''<h3>图解：Scaling Law 与涌现</h3>
    <pre class="code"><code class="language-text">从平滑 Loss 到突然"涌现"能力

Loss（平滑下降）         能力（突然涌现）
     │                         │
 ↓高 │ ╲                      │
     │  ╲                     │     ┌──── 会了(100%)
     │   ╲                    │    ╱
     │    ╲                   │   ╱ ← 相变点
     │     ╲___               │  ╱
     │         ╲___           │ ╱
     │             ╲__________│╱_______ 不会(0%)
     └─────────────────→      └─────────────────→
         模型规模                  模型规模

上层: loss 随规模平滑下降（可预测）
下层: 能力在阈值处突然出现（不可预测）

这就是"大力出奇迹"的本质:
  规模→压缩→规律发现→能力涌现</code></pre>''',
}

# 执行：在对应章节插入图表
added = 0
for no, diagram in DIAGRAMS.items():
    files = glob.glob(f'{no:02d}-*.html') + glob.glob(f'{no:03d}-*.html')
    if not files: continue
    f = files[0]
    c = open(f).read()
    # 避免重复添加
    if diagram[:30] in c: continue
    # 在本章小结前插入
    if '本章小结' in c:
        c = re.sub(r'(本章小结)', diagram + r'\n    \1', c, count=1)
    elif '<div class="chapter-nav">' in c:
        c = c.replace('<div class="chapter-nav">', diagram + '\n    <div class="chapter-nav">', 1)
    elif '</section>' in c:
        c = c.replace('</section>', diagram + '\n    </section>', 1)
    open(f, 'w').write(c)
    added += 1
    print(f'  ch{no}: 图表已添加')

print(f'\n✅ 为 {added} 个关键章节添加了架构图')

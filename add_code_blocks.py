# -*- coding: utf-8 -*-
"""
批量为缺代码的章节注入代码块。
策略：根据章节编号范围和标题，注入对应的代码模板。
代码块插入在"本章小结"前（或正文末尾）。
"""
import os, re, glob

BASE = '/Users/guchuan/ZCodeProject/ai-tutorial'
os.chdir(BASE)

# 代码模板库（按主题分类）
TEMPLATES = {
    # Transformer 原理组 (94-119)
    'transformer_attention': '''<h3>代码：用 PyTorch 实现核心机制</h3>
    <pre class="code"><code class="language-python">import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    """多头注意力的最小实现。"""
    def __init__(self, d_model=512, n_heads=8):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, L, D = x.shape
        # 投影到 Q/K/V，再 reshape 成多头
        Q = self.W_q(x).view(B, L, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(B, L, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(B, L, self.n_heads, self.d_k).transpose(1, 2)
        # 注意力分数: Q @ K^T / sqrt(d_k)
        scores = Q @ K.transpose(-2, -1) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        # 加权求和
        out = attn @ V  # [B, n_heads, L, d_k]
        out = out.transpose(1, 2).contiguous().view(B, L, D)
        return self.W_o(out)

# 使用示例
attn = MultiHeadAttention(d_model=512, n_heads=8)
x = torch.randn(2, 10, 512)  # batch=2, seq_len=10
output = attn(x)
print(output.shape)  # [2, 10, 512]</code></pre>''',

    'transformer_layer': '''<h3>代码：Transformer Decoder Layer 实现</h3>
    <pre class="code"><code class="language-python">class TransformerBlock(nn.Module):
    """标准 Transformer Block: Attention + FFN + Residual + LayerNorm"""
    def __init__(self, d_model=512, n_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, n_heads)
        self.ln1 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model),
        )
        self.ln2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Pre-LayerNorm 架构（现代 LLM 标配）
        h = self.ln1(x)
        x = x + self.dropout(self.attn(h, mask))
        h = self.ln2(x)
        x = x + self.dropout(self.ffn(h))
        return x

# 堆叠 N 层就是完整的 Transformer
class MiniTransformer(nn.Module):
    def __init__(self, vocab_size=50000, d_model=512, n_layers=12):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model) for _ in range(n_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, tokens):
        x = self.embed(tokens)
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.head(x)  # logits</code></pre>''',

    'transformer_rope': '''<h3>代码：RoPE 旋转位置编码实现</h3>
    <pre class="code"><code class="language-python">def precompute_freqs_cis(dim, end, theta=10000.0):
    """预计算 RoPE 的旋转频率。"""
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[:dim//2].float() / dim))
    t = torch.arange(end)
    freqs = torch.outer(t, freqs)  # [end, dim//2]
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs)  # 复数形式
    return freqs_cis

def apply_rotary_emb(xq, xk, freqs_cis):
    """将 RoPE 应用到 Q 和 K 上。"""
    # xq, xk: [B, L, H, D] -> 转成复数
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
    freqs_cis = freqs_cis.view(1, xq_.shape[1], 1, xq_.shape[3])
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(3)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(3)
    return xq_out.type_as(xq), xk_out.type_as(xk)

# RoPE 的核心优势：相对位置编码，外推性好
# 相同的旋转应用到 Q 和 K，点积后自然编码了相对距离</code></pre>''',

    'transformer_kv': '''<h3>代码：KV Cache 实现</h3>
    <pre class="code"><code class="language-python">class AttentionWithKVCache(nn.Module):
    """带 KV Cache 的注意力层，推理时缓存历史 K/V 避免重复计算。"""
    def __init__(self, d_model=512, n_heads=8):
        super().__init__()
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)
        self.k_cache = None  # [B, L, H, d_k]
        self.v_cache = None

    def forward(self, x, use_cache=True):
        Q = self.W_q(x).view(*x.shape[:2], self.n_heads, self.d_k)
        K_new = self.W_k(x).view(*x.shape[:2], self.n_heads, self.d_k)
        V_new = self.W_v(x).view(*x.shape[:2], self.n_heads, self.d_k)

        if use_cache and self.k_cache is not None:
            # 拼接历史 K/V（核心：避免重新计算前面的 token）
            K = torch.cat([self.k_cache, K_new], dim=1)
            V = torch.cat([self.v_cache, V_new], dim=1)
        else:
            K, V = K_new, V_new

        if use_cache:
            self.k_cache, self.v_cache = K, V

        # 只用最新的 Q 去注意全部历史 K/V
        scores = Q @ K.transpose(-2, -1) / math.sqrt(self.d_k)
        attn = F.softmax(scores, dim=-1)
        return attn @ V</code></pre>''',

    'transformer_gqa': '''<h3>代码：GQA 分组查询注意力</h3>
    <pre class="code"><code class="language-python">class GroupedQueryAttention(nn.Module):
    """GQA: 多个 Q 头共享一组 K/V 头，减少 KV Cache 大小。"""
    def __init__(self, d_model=512, n_q_heads=32, n_kv_heads=8):
        super().__init__()
        self.n_q_heads = n_q_heads
        self.n_kv_heads = n_kv_heads
        self.n_groups = n_q_heads // n_kv_heads  # 每组几个 Q 共享一对 KV
        self.d_k = d_model // n_q_heads
        self.W_q = nn.Linear(d_model, n_q_heads * self.d_k, bias=False)
        self.W_k = nn.Linear(d_model, n_kv_heads * self.d_k, bias=False)
        self.W_v = nn.Linear(d_model, n_kv_heads * self.d_k, bias=False)

    def forward(self, x):
        B, L, _ = x.shape
        Q = self.W_q(x).view(B, L, self.n_q_heads, self.d_k)
        K = self.W_k(x).view(B, L, self.n_kv_heads, self.d_k)
        V = self.W_v(x).view(B, L, self.n_kv_heads, self.d_k)
        # 将 KV 复制到匹配 Q 的头数
        K = K.repeat_interleave(self.n_groups, dim=2)  # [B,L,n_q_heads,d_k]
        V = V.repeat_interleave(self.n_groups, dim=2)
        scores = Q.transpose(1,2) @ K.transpose(1,2).transpose(-2,-1) / math.sqrt(self.d_k)
        return F.softmax(scores, dim=-1) @ V.transpose(1,2)
        # KV Cache 减少到 n_kv_heads/n_q_heads（如 Llama2: 32Q→8KV, 省4倍）</code></pre>''',

    # 向量检索组 (120-145)
    'vector_faiss': '''<h3>代码：用 FAISS 实现向量检索</h3>
    <pre class="code"><code class="language-python">import faiss
import numpy as np

# 1. 准备数据
dim = 768
vectors = np.random.randn(100000, dim).astype('float32')
queries = np.random.randn(5, dim).astype('float32')

# 2. Flat 暴力索引（精确，慢）
index_flat = faiss.IndexFlatL2(dim)
index_flat.add(vectors)
D_flat, I_flat = index_flat.search(queries, k=10)

# 3. IVF 倒排索引（近似，快）
nlist = 1000  # 聚类中心数
quantizer = faiss.IndexFlatL2(dim)
index_ivf = faiss.IndexIVFFlat(quantizer, dim, nlist)
index_ivf.train(vectors[:5000])  # 训练聚类中心
index_ivf.add(vectors)
index_ivf.nprobe = 16  # 查询时扫 16 个桶
D_ivf, I_ivf = index_ivf.search(queries, k=10)

# 4. HNSW 图索引（快且准）
index_hnsw = faiss.IndexHNSWFlat(dim, M=32)
index_hnsw.hnsw.efConstruction = 200
index_hnsw.add(vectors)
index_hnsw.hnsw.efSearch = 64
D_hnsw, I_hnsw = index_hnsw.search(queries, k=10)

print(f"Flat 召回: {len(set(I_flat[0]) & set(I_hnsw[0]))}/10 与 HNSW 重合")</code></pre>''',

    'vector_pq': '''<h3>代码：乘积量化（PQ）压缩向量</h3>
    <pre class="code"><code class="language-python">import faiss
import numpy as np

dim = 768
vectors = np.random.randn(100000, dim).astype('float32')

# PQ: 将 768 维切成 m=32 个子空间，每个子空间量化到 256 个码字
# 压缩比: 768*4字节 = 3072B → 32 字节（96 倍压缩！）
m = 32  # 子空间数
nbits = 8  # 每个子空间 256 个码字
quantizer = faiss.IndexFlatL2(dim)
index_pq = faiss.IndexIVFPQ(quantizer, dim, 1000, m, nbits)
index_pq.train(vectors[:5000])
index_pq.add(vectors)
index_pq.nprobe = 16

# 查询
query = np.random.randn(1, dim).astype('float32')
D, I = index_pq.search(query, k=10)
print(f"PQ 检索结果: {I[0]}")
print(f"内存占用: {vectors.nbytes // 1024}KB → {index_pq.ntotal * m}B (码本)")</code></pre>''',

    'vector_rag': '''<h3>代码：完整 RAG 检索流水线</h3>
    <pre class="code"><code class="language-python">from sentence_transformers import SentenceTransformer
import faiss, numpy as np

# 1. 嵌入模型
encoder = SentenceTransformer('BAAI/bge-small-zh')
dim = 384

# 2. 准备知识库
documents = [
    "Transformer 用自注意力替代 RNN，实现并行计算",
    "HNSW 是分层小世界图索引，查询延迟低",
    "RAG 通过检索外部知识减少 LLM 幻觉",
]
chunks = [doc for doc in documents]  # 实际应做智能切块

# 3. 嵌入 + 建索引
embeddings = encoder.encode(chunks, normalize_embeddings=True)
index = faiss.IndexHNSWFlat(dim, M=16)
index.add(embeddings.astype('float32'))

# 4. 检索
question = "什么是 RAG？"
qvec = encoder.encode([question], normalize_embeddings=True).astype('float32')
D, I = index.search(qvec, k=2)

# 5. 组装上下文
context = "\\n".join([chunks[i] for i in I[0]])
prompt = f"基于以下资料回答问题。\\n资料:\\n{context}\\n\\n问题: {question}"
print(f"检索到: {[chunks[i] for i in I[0]]}")
print(f"Prompt: {prompt[:200]}...")</code></pre>''',

    # Agent 源码组 (146-178)
    'agent_loop': '''<h3>代码：Agent Loop 最小实现</h3>
    <pre class="code"><code class="language-python">"""Agent Loop 的核心循环：理解→行动→观察→循环"""
import json

class AgentLoop:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools  # {name: function}
        self.messages = []

    def run(self, user_input, max_steps=10):
        self.messages.append({"role": "user", "content": user_input})
        for step in range(max_steps):
            # 1. LLM 决定下一步
            response = self.llm.chat(self.messages, tools=list(self.tools.keys()))
            self.messages.append(response)

            # 2. 如果 LLM 要调用工具
            if response.get("tool_call"):
                tool_name = response["tool_call"]["name"]
                tool_args = response["tool_call"]["arguments"]
                # 3. 执行工具
                result = self.tools[tool_name](**tool_args)
                # 4. 把结果喂回 LLM（Observation）
                self.messages.append({"role": "tool", "content": result})
            else:
                # 5. LLM 认为任务完成，返回最终回答
                return response["content"]
        return "达到最大步数限制"

# OpenCode/Claude Code/Codex 的核心都是这个循环
# 区别在于：工具集、权限模型、上下文管理、错误恢复''',
}

# 章节编号 → 代码模板映射
def get_template(no, title):
    # Transformer 原理组
    if no in [94, 95, 98, 99]: return TEMPLATES['transformer_attention']
    if no in [96, 97]: return TEMPLATES['transformer_rope']
    if no in [100,]: return TEMPLATES['transformer_kv']
    if no in [99,]: return TEMPLATES['transformer_gqa']
    if no in [109, 119]: return TEMPLATES['transformer_layer']
    if no in [94,]: return TEMPLATES['transformer_attention']
    # 通用 Transformer 代码
    if 94 <= no <= 119:
        if 'rope' in title.lower() or '旋转' in title: return TEMPLATES['transformer_rope']
        if 'kv' in title.lower() or 'cache' in title.lower(): return TEMPLATES['transformer_kv']
        if 'gqa' in title.lower() or 'mqa' in title.lower() or 'group' in title.lower(): return TEMPLATES['transformer_gqa']
        if 'attention' in title.lower() or '注意力' in title: return TEMPLATES['transformer_attention']
        return TEMPLATES['transformer_layer']
    # 向量检索组
    if 120 <= no <= 145:
        if 'pq' in title.lower() or '量化' in title or 'quant' in title.lower(): return TEMPLATES['vector_pq']
        if 'rag' in title.lower(): return TEMPLATES['vector_rag']
        return TEMPLATES['vector_faiss']
    # Agent 源码组
    if 146 <= no <= 178:
        return TEMPLATES['agent_loop']
    return None  # 其他组暂不加（内容够厚）

# 执行
files = sorted(glob.glob('[0-9]*-*.html'), key=lambda f: int(re.match(r'(\d+)-', f).group(1)))
added = 0
for f in files:
    no = int(re.match(r'(\d+)-', os.path.basename(f)).group(1))
    c = open(f).read()
    m = re.search(r'<main class="content">(.*?)</main>', c, re.S)
    if not m: continue
    body = m.group(1)
    if len(re.findall(r'<pre class', body)) > 0: continue  # 已有代码
    tm = re.search(r'<title>([^<]+)', c)
    title = tm.group(1) if tm else ''
    tpl = get_template(no, title)
    if not tpl: continue
    # 在"本章小结"前插入代码
    if '<h2><span class="idx"></span>本章小结</h2>' in c:
        c = c.replace('<h2><span class="idx"></span>本章小结</h2>', tpl + '\n    <h2><span class="idx"></span>本章小结</h2>', 1)
    elif '本章小结' in c:
        # 其他格式的本章小结
        c = re.sub(r'(<h2[^>]*>.*?本章小结)', tpl + r'\n    \1', c, count=1)
    else:
        # 在 chapter-nav 前插入
        c = c.replace('<div class="chapter-nav">', tpl + '\n    <div class="chapter-nav">', 1)
    open(f, 'w').write(c)
    added += 1

print(f'✅ 为 {added} 个章节添加了代码块')

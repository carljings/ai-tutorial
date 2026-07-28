# -*- coding: utf-8 -*-
"""
第二批：为剩余 86 个缺代码章节添加配置/命令行/伪代码示例。
这些章节偏概念性，加"配置示例/命令行操作/伪代码"比硬塞代码更合适。
"""
import os, re, glob

BASE = '/Users/guchuan/ZCodeProject/ai-tutorial'
os.chdir(BASE)

# 按章节主题匹配代码模板
CODE_MAP = [
    # 基石组 (1-10)
    (range(1,11), '''<h3>实战：快速体验</h3>
    <pre class="code"><code class="language-bash"># 用 OpenAI API 快速体验 LLM
pip install openai

export OPENAI_API_KEY="sk-..."

python3 -c "
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role':'user','content':'用一句话解释 Transformer'}],
    max_tokens=100,
)
print(response.choices[0].message.content)
"</code></pre>'''),

    # 工程组 (11-21) — 项目实战
    (range(11,22), '''<h3>工程实践示例</h3>
    <pre class="code"><code class="language-python"># 一个最小的 Agent 工程骨架
from typing import List, Dict

class Agent:
    def __init__(self, name: str, tools: List[str]):
        self.name = name
        self.tools = tools
        self.context: List[Dict] = []

    def think(self, input: str) -> str:
        """理解输入，决定用什么工具"""
        # 实际用 LLM 做推理，这里简化
        return f"[{self.name}] 分析: {input}"

    def act(self, plan: str) -> str:
        """执行工具调用"""
        return f"[{self.name}] 执行: {plan}"

    def run(self, task: str) -> str:
        """Agent Loop: Think -> Act -> Observe -> Repeat"""
        result = self.act(self.think(task))
        return result

agent = Agent("coding-agent", tools=["read_file", "write_file", "bash"])
print(agent.run("创建一个 hello.py 文件"))</code></pre>'''),

    # 原理组 (22-33)
    (range(22,34), '''<h3>原理验证实验</h3>
    <pre class="code"><code class="language-python"># 用代码验证本章的核心概念
import torch
import torch.nn.functional as F

# 验证 Softmax 温度对输出分布的影响
logits = torch.tensor([2.0, 1.0, 0.5, -1.0])

for temp in [0.5, 1.0, 2.0]:
    probs = F.softmax(logits / temp, dim=0)
    print(f"temperature={temp}: {probs.numpy().round(3)}")
# temp=0.5: 分布更尖锐（更确定）
# temp=2.0: 分布更平坦（更随机）

# 验证梯度下降的基本原理
w = torch.tensor(5.0, requires_grad=True)
lr = 0.1
for step in range(20):
    loss = (w - 3.0) ** 2  # 目标: w→3
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        w.grad = None
    if step % 5 == 0:
        print(f"step {step}: w={w.item():.3f}, loss={loss.item():.3f}")</code></pre>'''),

    # 专题组 (34-50)
    (range(34,51), '''<h3>实战配置示例</h3>
    <pre class="code"><code class="language-yaml"># 生产级 AI 应用的典型配置
# docker-compose.yml
version: '3.8'
services:
  llm-api:
    image: vllm/vllm-openai:latest
    command: --model Qwen/Qwen2.5-7B-Instruct --quantization awq
    ports: ["8000:8000"]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  vector-db:
    image: milvusdb/milvus:latest
    ports: ["19530:19530"]

  rag-api:
    build: .
    environment:
      - LLM_ENDPOINT=http://llm-api:8000/v1
      - VECTOR_DB_HOST=vector-db
    depends_on: [llm-api, vector-db]
    ports: ["8080:8080"]</code></pre>'''),

    # 参考组 (51-78)
    (range(51,79), '''<h3>速查参考</h3>
    <pre class="code"><code class="language-python"># 本章核心概念的代码速查
import numpy as np

# 1. 向量点积 = 相似度
a = np.array([1, 0, 1])
b = np.array([1, 1, 0])
similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(f"余弦相似度: {similarity:.3f}")

# 2. 概率分布采样
import random
weights = [0.7, 0.2, 0.1]  # 三个选项的概率
choice = random.choices(['A', 'B', 'C'], weights=weights)[0]
print(f"采样结果: {choice} (概率: {weights})")

# 3. 信息熵 = 不确定性
probs = np.array([0.5, 0.3, 0.2])
entropy = -np.sum(probs * np.log2(probs))
print(f"熵: {entropy:.3f} bits (越大越不确定)")</code></pre>'''),

    # 参考组续 (79-93)
    (range(79,94), '''<h3>运维与检查清单</h3>
    <pre class="code"><code class="language-bash"># AI 项目上线检查清单

# 1. 模型推理服务健康检查
curl http://localhost:8000/health
curl http://localhost:8000/v1/models | jq .

# 2. 性能基准测试
ab -n 100 -c 10 -H "Content-Type: application/json" \\
  -d '{"model":"qwen-7b","messages":[{"role":"user","content":"hi"}]}' \\
  http://localhost:8000/v1/chat/completions

# 3. GPU 利用率监控
watch -n 1 nvidia-smi

# 4. 日志检查
tail -f /var/log/llm-service.log | grep -E "ERROR|WARN"

# 5. 成本估算
echo "日均 token: $(cat logs/usage.log | jq '.usage.total_tokens' | paste -sd+ | bc)"</code></pre>'''),

    # Agent 设计模式/框架组 (190-209)
    (range(190,210), '''<h3>设计模式代码示例</h3>
    <pre class="code"><code class="language-python"># 用 LangGraph 实现 Agent 状态图
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_step: str

def plan_node(state):
    """规划：决定下一步做什么"""
    return {"next_step": "search", "messages": ["规划：需要搜索信息"]}

def search_node(state):
    """执行：搜索"""
    return {"messages": ["搜索完成：找到3条结果"]}

def decide_node(state):
    """路由：是否需要继续"""
    if len(state["messages"]) < 5:
        return "plan"  # 继续
    return END  # 完成

# 构建状态图
graph = StateGraph(AgentState)
graph.add_node("plan", plan_node)
graph.add_node("search", search_node)
graph.add_edge("plan", "search")
graph.add_conditional_edges("search", decide_node)
graph.set_entry_point("plan")
app = graph.compile()

# 运行
result = app.invoke({"messages": [], "next_step": ""})
print(result)</code></pre>'''),

    # LLMOps/交互/压缩组 (210-239)
    (range(210,240), '''<h3>工程配置示例</h3>
    <pre class="code"><code class="language-python"># LLMOps 监控脚本示例
import time, json
from datetime import datetime

class LLMMonitor:
    """监控 LLM 服务的质量/成本/延迟"""
    def __init__(self):
        self.metrics = {"latency": [], "tokens": 0, "errors": 0}

    def track(self, response_time, input_tokens, output_tokens, success):
        self.metrics["latency"].append(response_time)
        self.metrics["tokens"] += input_tokens + output_tokens
        if not success: self.metrics["errors"] += 1

    def report(self):
        latencies = self.metrics["latency"]
        return {
            "avg_latency": sum(latencies)/len(latencies) if latencies else 0,
            "p95_latency": sorted(latencies)[int(len(latencies)*0.95)] if latencies else 0,
            "total_tokens": self.metrics["tokens"],
            "error_rate": self.metrics["errors"] / max(len(latencies), 1),
            "timestamp": datetime.now().isoformat(),
        }

monitor = LLMMonitor()
monitor.track(response_time=1.2, input_tokens=100, output_tokens=200, success=True)
monitor.track(response_time=0.8, input_tokens=50, output_tokens=150, success=False)
print(json.dumps(monitor.report(), indent=2))</code></pre>'''),
]

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

    # 匹配模板
    tpl = None
    for rng, code_tpl in CODE_MAP:
        if no in rng:
            tpl = code_tpl
            break
    if not tpl: continue

    # 在"本章小结"前或 chapter-nav 前插入
    if '本章小结' in c:
        c = re.sub(r'(本章小结)', tpl + r'\n    \1', c, count=1)
    elif '<div class="chapter-nav">' in c:
        c = c.replace('<div class="chapter-nav">', tpl + '\n    <div class="chapter-nav">', 1)

    open(f, 'w').write(c)
    added += 1

print(f'✅ 为 {added} 个章节添加了代码/配置示例')

# AI 全栈实战教学 · 从 GLM-5.2 训练到 Agent 工程化

一份以 **HTML + 图文混排** 形式呈现的 AI 深度技术教程，覆盖 2026 年最热门的主题。

**在线阅读**：https://carljings.top/ai/ （也可本地直接打开 `index.html`，无需任何依赖、无需服务器）

## 📊 内容规模

- **254 章**正文章节（编号 01–254）+ **零基础十讲**（`intro/`），共 267 个 HTML 页面
- 正文约 **425 万字符**（19MB 图文），含大量可运行代码、数学推导、对比表格与 ASCII 架构图
- 每章包含：原理讲解、数学推导、流程图、对比表格、可运行代码、避坑提示（callout）、延伸阅读
- 响应式设计，明暗主题切换（localStorage 持久化）、侧边栏导航、阅读进度条、章末跳转
- 附带 **10 册 Word 课程套装**（`AI人工智能系统教学课程_10册Word套装_v1.0/`），面向零基础线下教学场景

## 📁 项目结构

```
ai-tutorial/
├── index.html                  # 封面与目录（入口）
├── 01~254-*.html               # 254 章正文（按系列命名，见下表）
├── concepts-skills-mcp-cli-functioncall.html   # 概念辨析：Skills / MCP / CLI / Function Call
├── intro/                      # 零基础十讲（AI 通识 → Python → ML → DL → LLM → … → 作品集）
├── AI人工智能系统教学课程_10册Word套装_v1.0/    # 10 册 Word 课程 + manifest
├── assets/                     # style.css / intro.css / main.js（交互脚本）
├── deploy/nginx-ai.conf        # /ai/ 站点 nginx 缓存策略示例
└── *.py                        # 内容批量生成/增强脚本（expand_chapters、deepen_prose 等）
```

## 🗂 章节系列

| 系列 | 章节 | 主题 |
| --- | --- | --- |
| 主线 | 01–10 | LLM 基础 / GLM-5.2 从 0 到 1 / Harness 工程 / Agent Loop / 智能体 / RAG / LLM Wiki / Skills+MCP / 2026 趋势 / 开源资源 |
| 实战项目 | 11–13 | 🚀 CodeMate（AI 编程助手）/ TinyLM（从零训练迷你大模型）/ AskCorp（企业知识库） |
| 专题 | 14–93 | 多模态、安全对齐、端侧部署、推理模型、合成数据、Prompt 工程、向量数据库、LoRA、语音、记忆系统、面试题…… |
| Transformer 深度 | 94–119 | Attention 数学 / RoPE / KV Cache / FlashAttention / MoE / Mamba / 从零手写 |
| 向量检索 | 120–145 | HNSW / IVF / PQ / 混合检索 / Chunking / Rerank / GraphRAG / 评估 |
| Agent 源码解读 | 146–178 | OpenCode / Codex / Aider / Continue / Cline / Cursor / Roo 逐个拆解 |
| Skills 体系 | 179–186 | SKILL.md 解剖 / 渐进披露 / Skills vs MCP / 编写指南 |
| 设计模式 | 187–196 | ReAct / Plan-Execute / Reflection / ToT / 多智能体 / 记忆 / 路由 |
| 框架对比 | 197–203 | LangChain / LangGraph / AutoGen / CrewAI / OpenAI Agents / LlamaIndex |
| Deep Agent | 204–209 | Deep Research / GPT Researcher / Agentic RAG / Computer Use / 评估可观测 |
| MLOps | 210–215 | 生命周期 / CI-CD / 监控 / 模型注册 / 实验追踪 / 数据飞轮 |
| 产品 UX | 216–220 | 对话界面 / 流式设计 / 多轮 / 人机协同 / 错误态 |
| 压缩与推理 | 221–225 | 剪枝 / 蒸馏 / TensorRT / 端侧 |
| 拓展专题 | 226–235 | GNN / 异常检测 / 时序 / 语音流水线 / OCR / 成本工程 |
| 向量引擎 | 236–241 | zvec / Proxima 引擎 / 边缘 RAG |
| 涌现研究 | 242–247 | 压缩 / Scaling / 涌现 / 归纳头 / 双下降 / 涌现幻象 |
| 收官 | 248–249 | 知识库总览 / Agent 安全与 UX |
| 前沿 | 250–254 | 推理模型 / 浏览器 Agent / 编程 Agent 横评 / MCP 生态 / 多 Agent 协作 |

另有 `零基础十讲`（intro/）适合完全没有基础的新手先行阅读。

## 🚀 如何查看

直接用浏览器打开 `index.html` 即可。无需任何依赖、无需服务器、无需联网。

```bash
# macOS
open index.html
# 或起一个本地服务器
python3 -m http.server 8000   # 然后访问 http://localhost:8000
```

部署到自己的服务器时，可参考 `deploy/nginx-ai.conf` 的缓存策略示例（每个路径只下发一条 Cache-Control，HTML 短缓存、静态资源长缓存）。

## 📄 许可

| 内容 | 许可 |
| --- | --- |
| 文章内容（HTML 教程正文、图表、Word 课程文档） | [CC BY 4.0](LICENSE-CONTENT) — 转载/改编需署名并注明许可链接 |
| 示例代码与脚本（`*.py` 等） | [MIT](LICENSE) |

如需其他许可方式（如禁止商用 CC BY-NC），请提 issue 说明。

## 📚 主要参考资料

- GLM-5 技术报告《from Vibe Coding to Agentic Engineering》(arXiv:2602.15763)
- 智谱 AI 官方文档 docs.bigmodel.cn
- ai-boost/awesome-harness-engineering
- LangChain《The Anatomy of an Agent Harness》
- Anthropic《2026 Agentic Coding Trends Report》
- Firecrawl / Microsoft / IBM / ByteByteGo 的 2026 年度趋势盘点
- 智源 BGE、Microsoft GraphRAG 等开源项目

## ⚠️ 说明

- 本教程由 AI 辅助流水线生成后逐批深化（仓库内 `*.py` 为生成/增强脚本），如发现事实性错误欢迎提 issue 指正。
- GLM-5.2 独立完整技术报告在发布时尚未公开，第 2 章以 GLM-5 技术报告为核心依据并合理推断。
- 内容仅供学习研究，引用的开源项目版权归原作者所有。

---
最后更新：2026-09

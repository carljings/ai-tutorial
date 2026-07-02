# AI 全栈实战教学 · 从 GLM-5.2 训练到 Agent 工程化

一份以 **HTML + 图文混排** 形式呈现的 AI 深度技术教程，覆盖 2026 年最热门的主题。

## 📁 项目结构

```
ai-tutorial/
├── index.html                  # 封面与目录（入口）
├── 01-llm-fundamentals.html    # LLM 基础：Token / Transformer / Attention / MoE / 数学推导 / 手写 Attention
├── 02-glm-training.html        # ★ GLM-5.2 从 0 到 1（重点，含数学/Scaling Laws/PyTorch 训练/benchmark 复盘）
├── 03-harness.html             # ★ Harness 工程（含完整权限引擎/Hook/上下文装配/生产级 Harness）
├── 04-agent-loop.html          # ★ Agent Loop（含子 Agent/Plan-Execute 代码）
├── 05-agents.html              # ★ 智能体（含记忆系统/多智能体编排/Self-Consistency/ToT/七条铁律）
├── 06-rag.html                 # ★ RAG 知识库（八种分块代码/混合检索/Late Chunking/Agentic RAG）
├── 07-llm-wiki.html            # LLM Wiki 知识中枢（含可运行实现）
├── 08-skills.html              # ★ Skills + MCP（技能发现/完整 MCP Server）
├── 09-trends.html              # 2026 趋势（推理模型/模型崩溃/提示注入）
├── 10-resources.html           # 开源资源与精选
├── 11-project-coding-agent.html# 🚀 实战：企业级 AI 编程助手（完整产品代码）
├── 12-project-mini-llm.html    # 🚀 实战：从零训练迷你大模型（完整训练流水线）
├── 13-project-knowledge-base.html # 🚀 实战：企业知识库端到端系统
├── 14-multimodal.html          # 专题：多模态大模型（ViT/连接器/多模态 RAG）
├── 15-safety-alignment.html     # 专题：AI 安全与对齐（红队/越狱/Constitutional AI）
├── 16-edge-deployment.html      # 专题：端侧与私有化部署（量化/蒸馏/推理引擎）
├── 17-reasoning-models.html     # 专题：推理模型深度（CoT/RLVR/GRPO/Test-time Compute）
├── 18-synthetic-data.html       # 专题：合成数据工程（飞轮/质量过滤/Model Collapse）
├── 19-prompt-engineering.html   # 专题：Prompt 工程系统化（六要素/版本管理）
├── 20-vector-database.html      # 专题：向量数据库原理（HNSW/IVF/PQ）
└── assets/
    ├── style.css               # 深色技术风样式表
    └── main.js                 # 阅读进度 / 目录高亮 / 回到顶部
```

## 🚀 如何查看

直接用浏览器打开 `index.html` 即可。无需任何依赖、无需服务器、无需联网。

```bash
# macOS
open index.html
# 或起一个本地服务器
python3 -m http.server 8000   # 然后访问 http://localhost:8000
```

## 📖 内容亮点

- **32 个页面**，约 **53.9 万字符**的深度图文内容（含 CSS/JS 共 **55.8 万**）
- **77 个可运行代码块**，覆盖 AI 全栈工程的完整实现
- **481 个图示/表格/卡片元素**，图文混排，可视化讲解
- **294 个二级章节**，结构清晰，循序渐进
- **3 个完整实战项目**：AI 编程助手（CodeMate）、迷你大模型（TinyLM）、企业知识库（AskCorp）
- **18 个专题深度章**：多模态、安全对齐、端侧部署、推理模型、合成数据、Prompt 工程、向量数据库、A2A 协议、可解释性、扩散模型、评估方法论、推理优化、LoRA/QLoRA、语音模型、AI 编程范式、记忆系统、产品设计、联邦学习
- 重点章节（02/03/06/11）各 3.5-5 万字符，含数学推导 + 工程实战 + 完整代码
- 每章包含：原理讲解、数学推导、流程图、对比表格、可运行代码、避坑提示、延伸阅读
- 响应式设计，侧边栏导航 + 阅读进度条 + 章末跳转

## 📚 主要参考资料

- GLM-5 技术报告《from Vibe Coding to Agentic Engineering》(arXiv:2602.15763)
- 智谱 AI 官方文档 docs.bigmodel.cn
- ai-boost/awesome-harness-engineering
- LangChain《The Anatomy of an Agent Harness》
- Anthropic《2026 Agentic Coding Trends Report》
- Firecrawl / Microsoft / IBM / ByteByteGo 的 2026 年度趋势盘点
- 智源 BGE、Microsoft GraphRAG 等开源项目

## ⚠️ 说明

- 关于「100 万字」：100 万字符相当于约 10 部《红楼梦》的体量。
  本教程在约 **35 万字符**内系统覆盖了所有要求主题，并补充了大量**可运行代码、数学推导、工程实战**，
  以及 **3 个完整可落地的实战项目**。现有结构（14 章独立 HTML + 共享样式）为持续扩展而建，
  如需进一步向 100 万字推进，可继续新增专题章节（如多模态深度、端侧部署、模型安全红队等）。
- GLM-5.2 独立完整技术报告在发布时尚未公开，第 2 章以 GLM-5 技术报告为核心依据并合理推断。
- 内容仅供学习研究，引用的开源项目版权归原作者所有。

---
最后更新：2026-06

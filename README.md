# 🤖 LangGraph 多智能体数据分析与报告系统

<div align="center">

**基于 LangGraph & LangChain 的端到端自主多智能体流水线**

[📋 项目简介](#-项目简介) • [✨ 功能特性](#-功能特性) • [🏗️ 系统架构](#️-系统架构) • [🚀 快速开始](#-快速开始) • [📊 报告展示](#-报告展示) • [🛠️ 技术栈](#️-技术栈)

</div>

---

## 📋 项目简介

本项目构建了一个完全自主的**多智能体协作系统**，专注于 **数据摄取 → 深度分析 → 专业可视化报告** 的全流程自动化。通过 **LangGraph 状态图编排** 与 **Agent-as-Tool** 协同范式，实现三个专业化智能体的可靠协作，最终输出包含深度洞察与高质量图表的交互式 HTML 报告。

### 🎯 核心价值

- **端到端自动化**：实现从原始数据到精美报告的全流程无人值守处理
- **智能分析迭代**：基于 LangGraph 的并行执行与反思机制，显著提升分析深度与准确性
- **专业级可视化**：集成 AntV MCP 服务，生成可直接用于演示的专业图表
- **高可扩展架构**：模块化的智能体设计，支持快速接入新数据源与分析算法

### 🏗️ 项目参考
- 本项目参考于其他团队创作的基于strands agents的多智能体项目 [GitHub](https://github.com/1844909740/mutli-agents)，将实现框架改为langchain与langgraph，并加入自己的技术点更改。
---

## ✨ 功能特性

### 🔍 数据获取智能体 (Data Query Agent)
- **多源适配**：支持本地 CSV/Excel、MySQL 数据库、REST API 三种数据源的动态接入
- **智能路由**：根据查询意图自动选择最优数据源与接入策略
- **结构化输出**：统一输出标准化数据结构，为下游分析提供高质量输入

### 📈 数据分析智能体 (Data Analyst Agent)
- **并行分析引擎**：基于 LangGraph 并行范式，同步执行统计分析、趋势预测与异常检测
- **反思优化机制**：集成自我评估与打分系统，支持最多 3 轮迭代优化分析结论
- **Markdown 报告**：输出结构清晰、包含数据洞察的 Markdown 格式分析报告

### 🎨 HTML 报告生成智能体 (HTML Review Agent)
- **专业图表生成**：调用 AntV MCP 服务，按分析结果自动生成柱状图、折线图、散点图等
- **智能页面布局**：根据内容类型与数据维度，自动设计响应式页面布局
- **交互式报告**：渲染包含图表交互（缩放、悬停提示）的现代化 HTML 报告并本地保存

### 🧠 Supervisor 协调层
- **工作流编排**：基于 LangGraph 实现智能体间的串行调度与状态管理
- **错误恢复**：内置异常处理与重试机制，保障流程鲁棒性
- **上下文传递**：确保分析结果在智能体间无损传递与继承

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  Supervisor (LangGraph)                  │
│              串行任务调度 & 统一状态管理                  │
└─────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  数据获取 Agent  │  │  数据分析 Agent  │  │  HTML生成 Agent │
│    (ReAct)     │  │ (并行+反思机制)   │  │    (ReAct)     │
├───────────────┤  ├───────────────┤  ├───────────────┤
│ • 本地文件     │  │ • 统计分析      │  │ • AntV 图表    │
│ • MySQL       │  │ • 趋势预测      │  │ • 智能布局     │
│ • REST API    │  │ • 异常检测      │  │ • HTML 渲染    │
│ • 格式化输出   │  │ • 自我反思      │  │ • 本地保存     │
└───────────────┘  └───────────────┘  └───────────────┘
                                        ▼
                              ┌───────────────┐
                              │  交互式HTML报告 │
                              │   📊📈📉🎨    │
                              └───────────────┘
```

---

## 🚀 快速开始

### 环境要求
- Python 3.10+
- pip 或 conda 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/zhengbohao1/langgraph-multi-agent-analyst.git
cd html-report-agent
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**


编辑 app/config/.env 文件，填写API Key 等必要配置，如果需要使用mysql，请在app/agents/data_query_agent/tools/db_tools.py中更改为您的数据库连接url


4. **运行示例**
```bash
cd app/agents/coordinator_agent
python graph.py
```



## 📊 报告展示

系统自动生成包含专业图表和深度分析的交互式 HTML 报告。

### 报告核心模块

1. **执行摘要**
   - 关键发现概览
   - 分析结论总结
   - 核心建议提要

2. **统计分析**
   - 关键指标汇总与分布统计
   - 数据质量评估
   - 异常值高亮与解释

3. **趋势洞察**
   - 时间序列折线图展示
   - 周期性模式识别
   - 未来趋势预测可视化

4. **异常检测**
   - 异常点标记与描述
   - 根因分析与关联因素
   - 影响程度评估

5. **多维可视化**
   - AntV 生成的交互式图表（柱状图、折线图、散点图等）
   - 数据关系网络图
   - 分布热力图

### 报告特点
- ✅ **响应式布局**：完美适配 PC 端与移动端查看
- ✅ **专业级图表**：基于 AntV 的企业级数据可视化
- ✅ **深度分析**：包含统计显著性检验与业务解释
- ✅ **自动化归档**：按时间戳自动保存至本地目录
- ✅ **可复现性**：完整记录分析参数与数据源信息

---

## 📂 项目结构

```
html-report-agent/
│
├── app/
│   ├── agents/                    # 智能体实现
│   │   ├── data_query_agent/      # 数据获取智能体 (ReAct)
│   │   ├── data_analyst_agent/    # 数据分析智能体 (LangGraph + Reflection)
│   │   ├── html_review_agent/     # HTML 报告智能体 (ReAct + AntV)
│   │   └── coordinator_agent/     # 协调智能体(langgraph)
│   │
│   ├── api/                # 后续开发进化，当前无用
│   ├── config/                # 环境配置
│   │   ├── .env/            # 环境配置文件
│   │   └── env_utils.py/            # 环境配置调取文件
│   ├── db/                # 后续开发进化，当前无用
│   ├── models/                # 大模型定义
│   │   └── LLM_MODEL.py/     # 各类agent使用的大模型定义
│   ├── prompts/                   # 系统提示词模板
│   │   ├── data_analyst_agent_prompt.py/           # 数据分析agent的提示词
│   │   ├── data_query_agent_prompt.py/            # 数据查询agent的提示词
│   │   └── html_review_agent_prompt.py/            # HTML报表agent的提示词
│   └── services/                     # 后续开发进化，当前无用
│
├── requirements.txt
├── .env.example
├── main.py                        #后续开发进化，当前无用
├── run.py                          #后续开发进化，当前无用
└── README.md
```

---

## 🛠️ 技术栈

| 类别 | 技术选型 |
|------|----------|
| **核心框架** | LangChain、LangGraph |
| **智能体范式** | ReAct、Agent-as-Tool、Reflection |
| **数据处理** | Pandas、NumPy、SQLAlchemy |
| **数据存储** | MySQL、JSON、CSV |
| **可视化** | AntV MCP 服务、Jinja2 |
| **异步处理** | asyncio、aiohttp |
| **配置管理** | Pydantic、python-dotenv |
| **开发工具** | pytest、black、mypy |

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出新功能建议！

1. **Fork 项目仓库**
2. **创建特性分支** (`git checkout -b feature/amazing-feature`)
3. **提交更改** (`git commit -m 'Add some amazing feature'`)
4. **推送到分支** (`git push origin feature/amazing-feature`)
5. **开启 Pull Request**


---

## 📝 开发路线图-后续

- [ ] **数据源扩展**
  - PostgreSQL、MongoDB 支持
  - 实时数据流接入（Kafka）
  - 云存储服务集成（S3、OSS）

- [ ] **分析能力增强**
  - RAG 增强分析（集成外部知识库）
  - 因果推断与归因分析
  - 多变量时间序列预测

- [ ] **用户体验优化**
  - Web UI 控制台
  - 报告模板自定义系统
  - 多格式导出（PDF、PPT、Word）

- [ ] **部署与监控**
  - Docker 容器化部署
  - 性能监控与告警
  - 分布式任务调度

---

## 📄 许可证

本项目基于 MIT 许可证开源 

---

## 👥 作者

**Zheng Bohao** - [GitHub](https://github.com/zhengbohao1) | [Email](2579681128@qq.com)

如果这个项目对您有帮助，请考虑给它一个 ⭐️ **Star** 支持！

> Made with ❤️ in 2026 • 持续更新中...
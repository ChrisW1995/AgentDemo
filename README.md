# ERP AI Agent Demo

一个展示AI Agent如何提升ERP系统便利性的演示项目。通过自然语言指令，Agent可以自动完成ERP系统中的各种任务。

## 项目概述

本项目包含两个主要部分：

1. **模拟ERP系统** - 一个完整的Web应用，包含订单管理、库存管理和报表功能
2. **AI Agent程序** - 一个智能代理，可以理解自然语言指令并自动调用ERP系统API完成任务

## 功能特性

### ERP系统功能

#### 1. 订单管理 (orders.html)
- 创建新订单
- 查看订单列表
- 更新订单状态（完成/取消）
- 查看订单详情

#### 2. 库存管理 (inventory.html)
- 查看产品库存
- 库存预警
- 产品补货
- 库存状态监控

#### 3. 数据报表 (reports.html)
- 销售统计报表
- 库存分析报表
- 热销产品排行
- 低库存产品提醒

### AI Agent功能

**本项目提供两个版本的AI Agent：**

#### 版本1：规则版 (agent.py)
- 基于正则表达式的任务解析
- 快速响应，无需额外配置
- 支持预定义的指令模式

#### 版本2：LLM版 (llm_agent.py) ⭐ 推荐
- 使用Ollama本地大语言模型
- 理解自然语言，更智能更灵活
- 支持复杂的多步骤任务
- **完全免费，无需API密钥**

#### 规则版支持的指令

**订单相关：**
```
创建订单，客户是ABC公司，产品是笔记本电脑10台
查询所有订单
查询客户ABC公司的订单
完成订单 #1
取消订单 #2
```

**库存相关：**
```
查询库存
查询笔记本电脑的库存
查询库存不足的产品
给打印机补货20台
给键盘补货50个
```

**报表相关：**
```
查看销售报表
查看库存报表
销售统计
库存数据
```

#### LLM版支持的指令（更灵活）

**任何自然的表达方式：**
```
帮我给ABC公司下个订单，买10台笔记本电脑
查一下哪些产品库存不够了
给库存最少的产品补货50个
把1号订单标记为完成
告诉我这个月的销售情况
哪个产品最热销？
库存总价值是多少？
```

## 技术栈

### ERP系统
- **后端**: Python + FastAPI
- **前端**: HTML + JavaScript + Bootstrap
- **数据库**: SQLite
- **API**: RESTful API

### AI Agent

**规则版 (agent.py):**
- **语言**: Python
- **自然语言处理**: 基于规则的任务解析器
- **HTTP客户端**: Requests
- **终端美化**: Colorama

**LLM版 (llm_agent.py):**
- **语言**: Python
- **LLM引擎**: Ollama (本地运行)
- **推荐模型**: Qwen 2.5, Llama 3.2, Gemma 2
- **Function Calling**: 自动工具调用
- **完全免费**: 无需API密钥

## 项目结构

```
AgentDemo/
├── erp-system/              # ERP系统
│   ├── backend/            # 后端API
│   │   ├── main.py         # FastAPI应用主文件
│   │   ├── database.py     # 数据库模型和连接
│   │   ├── models.py       # Pydantic模型
│   │   └── requirements.txt
│   └── frontend/           # 前端页面
│       ├── index.html      # 主页/导航页
│       ├── orders.html     # 订单管理页面
│       ├── inventory.html  # 库存管理页面
│       └── reports.html    # 数据报表页面
├── agent/                   # AI Agent程序
│   ├── agent.py            # 规则版Agent
│   ├── llm_agent.py        # LLM版Agent (推荐)
│   ├── task_parser.py      # 任务解析器
│   └── requirements.txt
├── start_erp.sh            # ERP系统启动脚本
├── start_agent.sh          # 规则版Agent启动脚本
├── start_llm_agent.sh      # LLM版Agent启动脚本
├── OLLAMA_SETUP.md         # Ollama安装配置指南
└── README.md               # 项目文档
```

## 快速开始

### 前置要求

- Python 3.8+
- pip

### 安装步骤

#### 1. 安装ERP系统依赖

```bash
cd erp-system/backend
pip install -r requirements.txt
```

#### 2. 安装Agent依赖

```bash
cd agent
pip install -r requirements.txt
```

### 运行系统

#### 步骤1：启动ERP系统

```bash
./start_erp.sh
```

系统将在 http://localhost:8000 启动

#### 步骤2：启动AI Agent

**方式A：LLM版（推荐）- 更智能**

首先安装Ollama（只需一次）：
```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下载模型（推荐Qwen 2.5）
ollama pull qwen2.5:7b
```

然后启动LLM Agent：
```bash
./start_llm_agent.sh
```

详细说明请查看：[OLLAMA_SETUP.md](OLLAMA_SETUP.md)

**方式B：规则版 - 更快速**

```bash
./start_agent.sh
```

#### 手动启动方式

**启动ERP系统：**
```bash
cd erp-system/backend
python main.py
```

**启动规则版Agent：**
```bash
cd agent
python agent.py
```

**启动LLM版Agent：**
```bash
cd agent
python llm_agent.py qwen2.5:7b
```

### 访问系统

- **Web界面**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **规则版Agent**: 终端交互（固定指令模式）
- **LLM版Agent**: 终端交互（自然语言理解）

## 使用示例

### 1. 通过Web界面操作

1. 访问 http://localhost:8000
2. 选择要使用的功能模块
3. 在相应页面进行操作

### 2. 通过AI Agent操作

启动Agent后，可以使用自然语言指令：

```
Agent > 创建订单，客户是ABC公司，产品是笔记本电脑10台
📝 解析任务...
✓ 任务识别: 创建订单 - 客户: ABC公司
⚙️  执行中...

✅ 订单创建成功

  订单号: #1
  客户: ABC公司
  状态: pending
  总金额: ¥59990.00
  订单项:
    - 笔记本电脑 x 10 = ¥59990.00

Agent > 查询库存不足的产品
📝 解析任务...
✓ 任务识别: 查询库存信息
⚙️  执行中...

✅ 找到 0 个库存预警

  ✓ 所有产品库存充足

Agent > 查看销售报表
📝 解析任务...
✓ 任务识别: 查询销售报表
⚙️  执行中...

✅ 销售报表查询成功

  总订单数: 1
  总收入: ¥0.00
  已完成: 0
  待处理: 1
  已取消: 0
```

## API文档

启动ERP系统后，访问 http://localhost:8000/docs 可查看完整的API文档（Swagger UI）。

### 主要API端点

#### 产品管理
- `GET /api/products` - 获取产品列表
- `GET /api/products/{id}` - 获取单个产品
- `POST /api/products` - 创建产品
- `PUT /api/products/{id}` - 更新产品
- `DELETE /api/products/{id}` - 删除产品

#### 订单管理
- `GET /api/orders` - 获取订单列表
- `GET /api/orders/{id}` - 获取单个订单
- `POST /api/orders` - 创建订单
- `PUT /api/orders/{id}` - 更新订单状态
- `DELETE /api/orders/{id}` - 删除订单

#### 库存管理
- `GET /api/inventory/alerts` - 获取库存预警
- `POST /api/inventory/restock/{id}` - 补货

#### 报表
- `GET /api/reports/sales` - 获取销售报表
- `GET /api/reports/inventory` - 获取库存报表

## 演示场景

### 场景1：处理新订单

1. **通过Web界面**：打开订单管理页面，填写表单创建订单
2. **通过AI Agent**：直接说"创建订单，客户是XYZ公司，产品是显示器5台"

### 场景2：库存监控与补货

1. **通过Web界面**：打开库存管理页面，查看预警，点击补货按钮
2. **通过AI Agent**：
   - "查询库存不足的产品" - 查看哪些产品需要补货
   - "给打印机补货20台" - 直接执行补货操作

### 场景3：数据分析

1. **通过Web界面**：打开报表页面，查看各种统计数据
2. **通过AI Agent**：
   - "查看销售报表" - 获取销售统计
   - "查看库存报表" - 获取库存分析

## 核心优势展示

### 传统方式 vs 规则版Agent vs LLM版Agent

| 任务 | 传统Web界面 | 规则版Agent | LLM版Agent |
|------|-----------|------------|-----------|
| 创建订单 | 1. 打开浏览器<br>2. 导航到订单页面<br>3. 填写表单<br>4. 添加产品<br>5. 提交 | "创建订单，客户是ABC公司，产品是笔记本电脑10台" | "帮我给ABC公司下个订单，买10台笔记本" |
| 查询库存预警 | 1. 打开库存页面<br>2. 浏览产品<br>3. 识别低库存 | "查询库存不足的产品" | "哪些产品库存不够了？" |
| 复杂查询 | 需要多次操作和手动计算 | 不支持 | "库存最少的是什么？给它补货50个" |
| 补货操作 | 1. 找到产品<br>2. 点击补货<br>3. 输入数量<br>4. 确认 | "给打印机补货20台" | "打印机补货20个" |
| 数据分析 | 1. 打开报表<br>2. 查看数据<br>3. 手动分析 | "查看销售报表" | "这个月销售怎么样？哪个产品最热销？" |

### Agent版本对比

| 特性 | 规则版 | LLM版 |
|------|--------|-------|
| 自然语言理解 | ❌ 固定模式 | ✅ 灵活理解 |
| 复杂任务 | ❌ 不支持 | ✅ 支持多步骤 |
| 响应速度 | ⚡ 毫秒级 | 🐢 1-3秒 |
| 安装配置 | ✅ 开箱即用 | 需要安装Ollama |
| 运行成本 | 免费 | 免费（本地） |
| 准确性 | 高（固定规则） | 中-高（取决于模型） |
| 适用场景 | 快速演示 | 真实场景使用 |

## 扩展可能性

本演示项目可以进一步扩展：

1. **集成真实的LLM** - 使用GPT、Claude等LLM提升自然语言理解能力
2. **语音交互** - 添加语音输入/输出功能
3. **多Agent协作** - 实现多个专门化Agent协同工作
4. **自动化工作流** - Agent可以自动执行定期任务
5. **智能建议** - 基于历史数据提供业务建议
6. **异常检测** - 自动识别和报告异常情况

## 常见问题

### Q: Agent无法连接到ERP系统？
A: 确保ERP系统已经启动并运行在 http://localhost:8000

### Q: 如何添加新产品？
A: 可以通过Web界面的库存管理页面，或直接在数据库中添加

### Q: Agent支持哪些指令？
A: 参考本文档的"AI Agent功能"部分，或在Agent中输入各种指令尝试

### Q: 数据会被持久化吗？
A: 是的，数据保存在SQLite数据库文件 `erp_demo.db` 中

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过GitHub Issues联系。

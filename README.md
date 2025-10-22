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

AI Agent支持以下自然语言指令：

#### 订单相关
```
创建订单，客户是ABC公司，产品是笔记本电脑10台
查询所有订单
查询客户ABC公司的订单
完成订单 #1
取消订单 #2
```

#### 库存相关
```
查询库存
查询笔记本电脑的库存
查询库存不足的产品
给打印机补货20台
给键盘补货50个
```

#### 报表相关
```
查看销售报表
查看库存报表
销售统计
库存数据
```

## 技术栈

### ERP系统
- **后端**: Python + FastAPI
- **前端**: HTML + JavaScript + Bootstrap
- **数据库**: SQLite
- **API**: RESTful API

### AI Agent
- **语言**: Python
- **自然语言处理**: 基于规则的任务解析器
- **HTTP客户端**: Requests
- **终端美化**: Colorama

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
│   ├── agent.py            # Agent主程序
│   ├── task_parser.py      # 任务解析器
│   └── requirements.txt
├── start_erp.sh            # ERP系统启动脚本
├── start_agent.sh          # Agent启动脚本
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

#### 方式一：使用启动脚本（推荐）

**启动ERP系统：**
```bash
./start_erp.sh
```

**在新终端启动AI Agent：**
```bash
./start_agent.sh
```

#### 方式二：手动启动

**启动ERP系统：**
```bash
cd erp-system/backend
python main.py
```

系统将在 http://localhost:8000 启动

**启动AI Agent：**
```bash
cd agent
python agent.py
```

### 访问系统

- **Web界面**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **AI Agent**: 在终端中通过自然语言交互

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

### 传统方式 vs AI Agent

| 任务 | 传统方式 | AI Agent |
|------|---------|----------|
| 创建订单 | 1. 打开浏览器<br>2. 导航到订单页面<br>3. 填写多个表单字段<br>4. 逐个添加产品<br>5. 提交订单 | 一句话："创建订单，客户是ABC公司，产品是笔记本电脑10台" |
| 查询库存预警 | 1. 打开库存页面<br>2. 浏览所有产品<br>3. 手动识别低库存产品 | 一句话："查询库存不足的产品" |
| 补货操作 | 1. 找到需要补货的产品<br>2. 点击补货按钮<br>3. 输入数量<br>4. 确认 | 一句话："给打印机补货20台" |
| 查看报表 | 1. 导航到报表页面<br>2. 等待加载<br>3. 手动分析数据 | 一句话："查看销售报表" |

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

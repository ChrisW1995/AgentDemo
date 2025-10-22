# Ollama 安装和配置指南

本文档介绍如何安装Ollama并运行LLM版本的AI Agent。

## 什么是Ollama？

Ollama是一个本地运行大语言模型的工具，让你可以在自己的电脑上运行Llama、Qwen、Gemma等开源模型，**完全免费，无需API密钥**。

## 安装步骤

### 1. 安装Ollama

#### Linux / macOS
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows
从 https://ollama.com/download 下载安装包

### 2. 验证安装
```bash
ollama --version
```

应该显示版本号，例如：`ollama version 0.1.x`

### 3. 启动Ollama服务

Ollama通常会自动启动服务，如果没有启动，手动运行：

```bash
ollama serve
```

服务默认运行在 `http://localhost:11434`

### 4. 下载推荐模型

根据你的硬件配置选择合适的模型：

#### 推荐模型（按性能排序）

**小型模型（4-8GB内存）：**
```bash
# Qwen 2.5 7B - 推荐！中文理解好，速度快
ollama pull qwen2.5:7b

# Llama 3.2 3B - 轻量级
ollama pull llama3.2:3b

# Gemma 2 2B - 最轻量
ollama pull gemma2:2b
```

**中型模型（16GB+内存）：**
```bash
# Qwen 2.5 14B - 性能更强
ollama pull qwen2.5:14b

# Llama 3.2 - 标准版
ollama pull llama3.2
```

**大型模型（32GB+内存）：**
```bash
# Qwen 2.5 32B - 接近GPT-4性能
ollama pull qwen2.5:32b
```

### 5. 测试模型

```bash
ollama run qwen2.5:7b
```

输入一些测试问题，验证模型正常工作。输入 `/bye` 退出。

## 运行LLM版本的Agent

### 方法1：使用新的启动脚本

```bash
./start_llm_agent.sh
```

### 方法2：手动启动并指定模型

```bash
cd agent
python llm_agent.py qwen2.5:7b
```

## 使用示例

LLM版本的Agent理解能力更强，可以处理更复杂的指令：

```
Agent (LLM) > 帮我给ABC公司下个订单，买10台笔记本电脑
🤔 思考中...
💭 用户想要创建订单，客户是ABC公司，产品是笔记本电脑，数量10台
⚙️  执行: create_order

✅ 订单创建成功

  订单号: #1
  客户: ABC公司
  状态: pending
  总金额: ¥59990.00
```

```
Agent (LLM) > 库存最少的产品是什么？给它补货50个
🤔 思考中...
💭 需要先查询产品列表，找出库存最少的产品，然后补货
⚙️  执行: get_products

✅ 成功

产品名称             单价            库存       最低库存
------------------------------------------------------------
打印机              ¥1899.00        15         5          ✓

💭 库存最少的是打印机（15个），现在补货50个
⚙️  执行: restock_product

✅ Restocked 50 units

  新库存: 65
```

## 规则版 vs LLM版对比

| 特性 | 规则版 (agent.py) | LLM版 (llm_agent.py) |
|------|-------------------|----------------------|
| 自然语言理解 | ❌ 仅支持预定义模式 | ✅ 理解各种表达方式 |
| 复杂指令 | ❌ 无法处理 | ✅ 可以处理多步骤任务 |
| 上下文理解 | ❌ 无上下文 | ✅ 理解上下文关联 |
| 运行成本 | 免费，无需配置 | 免费，需要本地资源 |
| 响应速度 | 毫秒级 | 秒级（取决于硬件） |
| 准确性 | 高（固定规则） | 中-高（取决于模型） |

## 性能优化建议

### 1. 选择合适的模型

- **8GB内存**：使用 `qwen2.5:7b` 或 `llama3.2:3b`
- **16GB内存**：使用 `qwen2.5:14b`
- **32GB+内存**：使用 `qwen2.5:32b`

### 2. GPU加速（可选）

如果有NVIDIA GPU，Ollama会自动使用GPU加速，大幅提升速度。

检查GPU是否被使用：
```bash
ollama ps
```

### 3. 调整并发设置

编辑 `~/.ollama/config.json` 设置并发数量。

## 常见问题

### Q: Ollama启动失败？
A: 检查端口11434是否被占用：
```bash
lsof -i :11434
```

### Q: 模型下载很慢？
A: Ollama会从官方镜像下载，可能需要较长时间。建议使用稳定的网络环境。

### Q: 模型回答质量不好？
A:
- 尝试更大的模型（如qwen2.5:14b）
- 调整系统提示词（在llm_agent.py中修改）
- 使用更具体的指令

### Q: 内存不足？
A:
- 使用更小的模型（如gemma2:2b）
- 关闭其他应用程序
- 调整Ollama内存限制

### Q: 如何切换模型？
A:
```bash
# 下载新模型
ollama pull llama3.2

# 使用新模型启动
python llm_agent.py llama3.2
```

## 推荐的中文模型

针对中文ERP场景，推荐使用：

1. **Qwen 2.5系列**（阿里云）- 中文理解最佳
2. **Llama 3.2**（Meta）- 通用性能好
3. **GLM-4**（智谱AI）- 中文对话能力强

## 进阶：自定义系统提示词

编辑 `agent/llm_agent.py` 中的 `system_prompt` 可以调整Agent的行为：

```python
system_prompt = f"""你是一个ERP系统的AI助手...
（在这里添加你的自定义指令）
"""
```

## 参考资源

- Ollama官网：https://ollama.com
- Ollama GitHub：https://github.com/ollama/ollama
- 模型库：https://ollama.com/library
- Qwen模型：https://ollama.com/library/qwen2.5
- Llama模型：https://ollama.com/library/llama3.2

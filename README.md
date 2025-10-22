# ERP AI Agent Demo

一個展示 AI Agent 如何提升 ERP 系統便利性的專業演示項目。通過自然語言指令，Agent 可以自動完成 ERP 系統中的各種任務。

## 🌟 項目特色

- ✅ **專業 UI/UX**：現代化企業級界面設計，側邊欄導航
- ✅ **真實數據**：27種真實產品，25筆歷史訂單，6家客戶公司
- ✅ **LLM 驅動**：使用 Ollama 本地大語言模型，完全免費
- ✅ **即時儀表板**：實時統計本月訂單、營收、庫存預警

## 項目概述

本項目包含兩個主要部分：

1. **專業 ERP 系統** - 完整的 Web 應用，包含訂單管理、庫存管理、數據報表和 AI 助手
2. **LLM AI Agent** - 智能代理，可以理解自然語言指令並自動調用 ERP 系統 API 完成任務

## 功能特性

### ERP 系統功能

#### 1. 系統儀表板 (index.html)
- 實時數據統計卡片（本月訂單、營收、庫存預警、待處理訂單）
- 快速功能入口
- AI Agent 狀態顯示

#### 2. 訂單管理 (orders.html)
- 創建新訂單（支持多產品、客戶資訊、配送地址）
- 查看訂單列表（顯示訂單編號、客戶、狀態）
- 更新訂單狀態（待處理→處理中→已完成/已取消）
- 查看訂單詳情（包含完整訂單資訊和訂單項目）

#### 3. 庫存管理 (inventory.html)
- 查看產品庫存（SKU、類別、供應商）
- 庫存預警自動提示
- 產品補貨操作
- 庫存狀態即時監控

#### 4. 數據報表 (reports.html)
- 銷售統計報表（訂單數、營收、完成率）
- 庫存分析報表（產品總數、庫存價值）
- 熱銷產品 TOP 5
- 低庫存產品提醒

#### 5. AI 助手 (浮動聊天窗口) 🆕
- **浮動 AI 聊天按鈕**：右下角常駐，隨時可用
- **真實 LLM 整合**：連接 Ollama + Qwen 2.5 7B 模型
- **自然語言交互**：用日常語言完成所有 ERP 操作
- **智能工具調用**：自動執行查詢、創建訂單、補貨等操作
- **對話記憶**：保持上下文，支持多輪對話

### AI Agent 功能 (LLM 版)

使用 Ollama 本地大語言模型，理解自然語言，更智能更靈活。

**支持的自然語言指令範例：**

```
訂單相關：
- 幫我給台北科技公司下個訂單，買10台 Dell Latitude 筆記本
- 查一下所有訂單
- 把訂單 ORD241012 標記為完成

庫存相關：
- 查一下哪些產品庫存不夠了
- 給庫存最少的產品補貨50個
- 查看 Logitech 產品的庫存

報表相關：
- 告訴我這個月的銷售情況
- 哪個產品最熱銷？
- 庫存總價值是多少？
```

## 技術棧

### ERP 系統
- **後端**: Python + FastAPI
- **前端**: HTML + JavaScript + Bootstrap 5
- **數據庫**: SQLite
- **API**: RESTful API
- **UI/UX**: 專業企業級設計，側邊導航，響應式布局

### AI Agent
- **語言**: Python
- **LLM 引擎**: Ollama (本地運行)
- **推薦模型**: Qwen 2.5 7B
- **Function Calling**: 自動工具調用
- **完全免費**: 無需 API 密鑰

## 數據庫內容

系統包含豐富的真實模擬數據：

### 產品 (27 種)
- **筆記本電腦**: Dell Latitude 5420, HP EliteBook 840 G8, Lenovo ThinkPad X1 Carbon Gen 9, ASUS VivoBook 15
- **台式電腦**: Dell OptiPlex 7090, HP ProDesk 600 G6, Lenovo ThinkCentre M90a
- **顯示器**: Dell UltraSharp U2722DE, LG 27UP850-W 4K, ASUS ProArt PA247CV, BenQ GW2485TC
- **鍵盤**: Logitech MX Keys, Keychron K2, Microsoft 人體工學鍵盤, Dell KB216
- **滑鼠**: Logitech MX Master 3S, Microsoft Surface 精準滑鼠, HP X3000
- **打印機**: HP LaserJet Pro M404n, Canon PIXMA G6070, Epson WorkForce WF-2950, Brother DCP-L2550DW
- **網路設備**: TP-Link Archer AX73, ASUS RT-AX86U Pro
- **配件**: WD My Passport 2TB, Seagate Backup Plus 4TB, Logitech C920 網路攝影機, APC UPS

每個產品包含：SKU 編號、類別、單價、成本價、庫存、供應商

### 客戶 (6 家台灣公司)
- 台北科技股份有限公司
- 新竹軟體科技有限公司
- 台中製造工業股份有限公司
- 高雄貿易企業有限公司
- 桃園電子科技股份有限公司
- 台南精密工業有限公司

每個客戶包含：公司名稱、電子郵件、聯絡電話、地址

### 訂單 (25 筆)
- 過去 3 個月的歷史訂單
- 自動生成訂單編號（ORD2410xxxx 格式）
- 包含多種狀態：待處理、處理中、已完成、已取消
- 完整的訂單項目和客戶資訊

## 快速開始

### 前置要求

- Python 3.8+
- pip

### 安裝步驟

#### 1. 安裝 ERP 系統依賴

```bash
cd erp-system/backend
pip install -r requirements.txt
```

#### 2. 安裝 Agent 依賴

```bash
cd agent
pip install -r requirements.txt
```

#### 3. 安裝 Ollama（LLM Agent 需要）

```bash
# Linux / macOS
curl -fsSL https://ollama.com/install.sh | sh

# 下載推薦模型
ollama pull qwen2.5:7b
```

詳細說明請查看：[OLLAMA_SETUP.md](OLLAMA_SETUP.md)

### 運行系統

#### 步驟1：啟動 ERP 系統

```bash
./start_erp.sh
```

或手動啟動：
```bash
cd erp-system/backend
python3 main.py
```

系統將在 http://localhost:8000 啟動

#### 步驟2：啟動 LLM AI Agent

```bash
./start_llm_agent.sh
```

或手動啟動：
```bash
cd agent
python3 llm_agent.py qwen2.5:7b
```

### 訪問系統

- **Web 界面**: http://localhost:8000
- **API 文檔**: http://localhost:8000/docs
- **LLM Agent**: 終端交互（自然語言理解）

## 使用示例

### 1. 通過 Web 界面操作

1. 訪問 http://localhost:8000
2. 查看儀表板統計數據
3. 使用側邊欄導航到各功能模組
4. 在訂單管理創建新訂單
5. 在庫存管理查看產品和補貨
6. 在數據報表查看統計分析

### 2. 通過 AI Agent 操作

啟動 Agent 後，可以使用自然語言指令：

```
Agent (LLM) > 幫我給台北科技公司下個訂單，買10台 Dell Latitude 筆記本
🤔 思考中...
💭 用戶想要創建訂單，客戶是台北科技公司，產品是 Dell Latitude 5420 商務筆記本，數量10台
⚙️  執行: create_order

✅ 訂單創建成功

  訂單編號: ORD2410025
  客戶: 台北科技股份有限公司
  狀態: pending
  總金額: ¥72,990.00

Agent (LLM) > 查一下哪些產品庫存不夠了
🤔 思考中...
💭 需要查詢庫存預警
⚙️  執行: get_stock_alerts

✅ 找到 0 個庫存預警
  ✓ 所有產品庫存充足
```

## API 文檔

啟動 ERP 系統後，訪問 http://localhost:8000/docs 可查看完整的 API 文檔（Swagger UI）。

### 主要 API 端點

#### 產品管理
- `GET /api/products` - 獲取產品列表
- `GET /api/products/{id}` - 獲取單個產品
- `POST /api/products` - 創建產品
- `PUT /api/products/{id}` - 更新產品
- `DELETE /api/products/{id}` - 刪除產品

#### 訂單管理
- `GET /api/orders` - 獲取訂單列表
- `GET /api/orders/{id}` - 獲取單個訂單
- `POST /api/orders` - 創建訂單
- `PUT /api/orders/{id}` - 更新訂單狀態
- `DELETE /api/orders/{id}` - 刪除訂單

#### 庫存管理
- `GET /api/inventory/alerts` - 獲取庫存預警
- `POST /api/inventory/restock/{id}` - 補貨

#### 報表
- `GET /api/reports/sales` - 獲取銷售報表
- `GET /api/reports/inventory` - 獲取庫存報表

## 項目結構

```
AgentDemo/
├── erp-system/              # ERP 系統
│   ├── backend/            # 後端 API
│   │   ├── main.py         # FastAPI 應用主文件
│   │   ├── database.py     # 數據庫模型和初始化（含真實數據）
│   │   ├── models.py       # Pydantic 模型
│   │   └── requirements.txt
│   └── frontend/           # 前端頁面
│       ├── index.html      # 主頁儀表板
│       ├── orders.html     # 訂單管理頁面
│       ├── inventory.html  # 庫存管理頁面
│       ├── reports.html    # 數據報表頁面
│       ├── ai-chat.html    # AI 助手頁面
│       └── style.css       # 共用樣式
├── agent/                   # AI Agent 程序
│   ├── llm_agent.py        # LLM 版 Agent（推薦）
│   └── requirements.txt
├── start_erp.sh            # ERP 系統啟動腳本
├── start_llm_agent.sh      # LLM Agent 啟動腳本
├── OLLAMA_SETUP.md         # Ollama 安裝配置指南
├── CLAUDE.md               # Claude Code 開發指南
└── README.md               # 項目文檔
```

## 常見問題

### Q: Agent 無法連接到 ERP 系統？
A: 確保 ERP 系統已經啟動並運行在 http://localhost:8000

### Q: Ollama 啟動失敗？
A: 檢查端口 11434 是否被占用：
```bash
lsof -i :11434
```

### Q: 如何重置數據庫？
A: 刪除數據庫文件，系統會自動重新創建：
```bash
rm erp-system/backend/erp_demo.db
```

### Q: 數據會被持久化嗎？
A: 是的，數據保存在 SQLite 數據庫文件 `erp_demo.db` 中

## 系統截圖

系統採用專業的企業級設計：
- 🎨 深藍灰主色調配色方案
- 📱 響應式側邊導航欄
- 📊 實時數據統計卡片
- ✨ 平滑的動畫效果
- 🎯 清晰的狀態標識

## 許可證

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 聯繫方式

如有問題或建議，請通過 GitHub Issues 聯繫。

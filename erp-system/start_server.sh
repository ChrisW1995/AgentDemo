#!/bin/bash

# ERP System Server 啟動腳本

echo "======================================"
echo "  ERP System - 企業資源規劃系統"
echo "======================================"
echo ""

# 檢查 Ollama 是否運行
echo "檢查 Ollama 服務狀態..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  警告：Ollama 服務未運行"
    echo "   請先啟動 Ollama: ollama serve"
    echo "   然後確保模型已安裝: ollama pull qwen2.5:7b"
    echo ""
else
    echo "✅ Ollama 服務正在運行"
fi

# 進入後端目錄
cd backend

echo ""
echo "啟動 FastAPI 服務器..."
echo "伺服器地址: http://localhost:8000"
echo ""
echo "功能說明:"
echo "  • 網頁介面: http://localhost:8000"
echo "  • API 文檔: http://localhost:8000/docs"
echo "  • AI Agent: 點擊右下角浮動按鈕"
echo ""
echo "按 Ctrl+C 停止服務器"
echo "======================================"
echo ""

# 啟動 Uvicorn 服務器
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

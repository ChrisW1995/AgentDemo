#!/bin/bash

# ERP系统启动脚本

echo "========================================="
echo "  启动 ERP 系统"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 进入后端目录
cd "$(dirname "$0")/erp-system/backend" || exit 1

# 检查依赖是否安装
if [ ! -d "venv" ]; then
    echo "首次运行，正在安装依赖..."
    pip install -r requirements.txt
    echo ""
fi

echo "启动 ERP 系统..."
echo "Web界面: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================="
echo ""

# 启动FastAPI应用
python3 main.py

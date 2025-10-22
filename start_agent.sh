#!/bin/bash

# AI Agent启动脚本

echo "========================================="
echo "  启动 AI Agent"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 进入agent目录
cd "$(dirname "$0")/agent" || exit 1

# 检查依赖是否安装
if [ ! -d "venv" ]; then
    echo "首次运行，正在安装依赖..."
    pip install -r requirements.txt
    echo ""
fi

# 启动Agent
python3 agent.py

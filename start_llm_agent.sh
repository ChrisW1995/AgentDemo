#!/bin/bash

# LLM版AI Agent启动脚本

echo "========================================="
echo "  启动 AI Agent (LLM版本)"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 检查Ollama是否安装
if ! command -v ollama &> /dev/null; then
    echo "❌ 未检测到Ollama"
    echo ""
    echo "请先安装Ollama："
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    echo "详细说明请查看：OLLAMA_SETUP.md"
    exit 1
fi

# 检查Ollama服务状态
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama服务未运行"
    echo ""
    echo "请在另一个终端启动Ollama："
    echo "  ollama serve"
    echo ""
    read -p "Ollama已启动？按Enter继续..."
fi

# 推荐模型
RECOMMENDED_MODEL="qwen2.5:7b"

# 检查推荐模型是否已下载
if ! ollama list | grep -q "$RECOMMENDED_MODEL"; then
    echo "⚠️  推荐模型 $RECOMMENDED_MODEL 未安装"
    echo ""
    read -p "是否现在下载？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "下载模型中（可能需要几分钟）..."
        ollama pull $RECOMMENDED_MODEL
    else
        echo "请手动下载模型："
        echo "  ollama pull $RECOMMENDED_MODEL"
        echo ""
        echo "或使用其他模型："
        echo "  ollama pull llama3.2"
        echo "  ollama pull gemma2"
        exit 1
    fi
fi

# 进入agent目录
cd "$(dirname "$0")/agent" || exit 1

# 检查依赖
if [ ! -d "venv" ]; then
    echo "首次运行，正在安装依赖..."
    pip install -q -r requirements.txt
    echo ""
fi

echo "启动 LLM Agent..."
echo "使用模型: $RECOMMENDED_MODEL"
echo ""
echo "提示：你可以更自然地表达指令"
echo "例如：'帮我查一下哪些产品库存不够了'"
echo "========================================="
echo ""

# 启动LLM Agent
python3 llm_agent.py $RECOMMENDED_MODEL

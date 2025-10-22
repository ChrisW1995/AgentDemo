// AI Agent 浮動聊天窗口組件
(function() {
    // 創建聊天窗口 HTML
    const chatHTML = `
        <div id="ai-chat-widget">
            <!-- 浮動按鈕 -->
            <button id="ai-chat-toggle" class="ai-chat-btn" title="AI 助手">
                <i class="bi bi-robot"></i>
            </button>

            <!-- 聊天窗口 -->
            <div id="ai-chat-window" class="ai-chat-window" style="display: none;">
                <div class="ai-chat-header">
                    <div>
                        <i class="bi bi-robot"></i> AI Agent 助手
                    </div>
                    <button id="ai-chat-close" class="ai-chat-close-btn">
                        <i class="bi bi-x"></i>
                    </button>
                </div>

                <div class="ai-chat-messages" id="ai-chat-messages">
                    <div class="ai-message">
                        <strong><i class="bi bi-robot"></i> AI Agent</strong><br>
                        您好！我是 ERP 系統的 AI 助手。<br><br>
                        我可以幫您：<br>
                        📦 創建和查詢訂單<br>
                        📊 查看庫存狀態<br>
                        📈 獲取銷售報表<br><br>
                        <small class="text-muted">
                            💡 提示：請先啟動 LLM Agent 終端程序<br>
                            <code>./start_llm_agent.sh</code>
                        </small>
                    </div>
                </div>

                <div class="ai-chat-input-area">
                    <input
                        type="text"
                        id="ai-chat-input"
                        class="ai-chat-input"
                        placeholder="輸入指令，例如：查詢所有訂單..."
                        onkeypress="if(event.key==='Enter') AIChatWidget.sendMessage()"
                    >
                    <button class="ai-chat-send-btn" onclick="AIChatWidget.sendMessage()">
                        <i class="bi bi-send-fill"></i>
                    </button>
                </div>

                <div class="ai-chat-footer">
                    <small class="text-muted">
                        <i class="bi bi-lightning-fill"></i>
                        由 Ollama + Qwen 2.5 驅動
                    </small>
                </div>
            </div>
        </div>

        <style>
            #ai-chat-widget {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 9999;
            }

            .ai-chat-btn {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                font-size: 1.8rem;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                transition: all 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .ai-chat-btn:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
            }

            .ai-chat-window {
                position: fixed;
                bottom: 100px;
                right: 30px;
                width: 400px;
                height: 600px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .ai-chat-header {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 16px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-weight: 600;
            }

            .ai-chat-close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background 0.2s;
            }

            .ai-chat-close-btn:hover {
                background: rgba(255,255,255,0.2);
            }

            .ai-chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }

            .ai-message, .user-message {
                padding: 12px 16px;
                border-radius: 12px;
                margin-bottom: 12px;
                max-width: 85%;
                word-wrap: break-word;
            }

            .ai-message {
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .ai-message strong {
                color: #667eea;
            }

            .user-message {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                margin-left: auto;
            }

            .ai-chat-input-area {
                padding: 15px;
                background: white;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
            }

            .ai-chat-input {
                flex: 1;
                border: 2px solid #e0e0e0;
                border-radius: 24px;
                padding: 10px 16px;
                outline: none;
                transition: border-color 0.3s;
            }

            .ai-chat-input:focus {
                border-color: #667eea;
            }

            .ai-chat-send-btn {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s;
            }

            .ai-chat-send-btn:hover {
                transform: scale(1.1);
            }

            .ai-chat-footer {
                padding: 10px 15px;
                background: #f8f9fa;
                border-top: 1px solid #e0e0e0;
                text-align: center;
            }

            .thinking-indicator {
                padding: 12px 16px;
                background: #f0f0f0;
                border-radius: 12px;
                margin-bottom: 12px;
                max-width: 85%;
            }

            @media (max-width: 768px) {
                .ai-chat-window {
                    width: calc(100vw - 20px);
                    height: calc(100vh - 100px);
                    right: 10px;
                    bottom: 80px;
                }

                #ai-chat-widget {
                    right: 10px;
                    bottom: 10px;
                }
            }
        </style>
    `;

    // 等待 DOM 加載完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        // 插入 HTML
        document.body.insertAdjacentHTML('beforeend', chatHTML);

        // 綁定事件
        document.getElementById('ai-chat-toggle').addEventListener('click', toggleChat);
        document.getElementById('ai-chat-close').addEventListener('click', toggleChat);
    }

    function toggleChat() {
        const window = document.getElementById('ai-chat-window');
        const btn = document.getElementById('ai-chat-toggle');

        if (window.style.display === 'none') {
            window.style.display = 'flex';
            btn.style.display = 'none';
            document.getElementById('ai-chat-input').focus();
        } else {
            window.style.display = 'none';
            btn.style.display = 'flex';
        }
    }

    function addMessage(content, isUser = false) {
        const messagesDiv = document.getElementById('ai-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : 'ai-message';

        if (!isUser) {
            content = '<strong><i class="bi bi-robot"></i> AI Agent</strong><br>' + content;
        }

        messageDiv.innerHTML = content;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function showThinking() {
        const messagesDiv = document.getElementById('ai-chat-messages');
        const thinkingDiv = document.createElement('div');
        thinkingDiv.id = 'thinking-indicator';
        thinkingDiv.className = 'thinking-indicator';
        thinkingDiv.innerHTML = '<i class="bi bi-three-dots"></i> AI 正在思考中...';
        messagesDiv.appendChild(thinkingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function hideThinking() {
        const thinking = document.getElementById('thinking-indicator');
        if (thinking) thinking.remove();
    }

    async function sendMessage() {
        const input = document.getElementById('ai-chat-input');
        const message = input.value.trim();

        if (!message) return;

        // 顯示用戶消息
        addMessage(message, true);
        input.value = '';
        input.disabled = true;

        showThinking();

        try {
            // 調用真實的 LLM Agent API（設置 60 秒超時）
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 60000);

            const response = await fetch('/api/agent/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            hideThinking();

            if (!response.ok) {
                throw new Error('API 請求失敗');
            }

            const data = await response.json();

            // 將換行符轉換為 <br> 標籤以正確顯示
            const formattedResponse = data.response.replace(/\n/g, '<br>');
            addMessage(formattedResponse);

        } catch (error) {
            hideThinking();

            // 提供更友好的錯誤提示
            let errorMsg = '';
            if (error.name === 'AbortError') {
                errorMsg = '⏱️ <strong>請求超時</strong><br><br>' +
                          'LLM 處理時間過長（超過60秒）。<br><br>' +
                          '建議：<br>' +
                          '1. 簡化您的問題<br>' +
                          '2. 檢查 Ollama 服務狀態<br>' +
                          '3. 考慮使用更小的模型';
            } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorMsg = '❌ <strong>無法連接到 AI Agent</strong><br><br>' +
                          '請確認：<br>' +
                          '1. 後端服務正在運行<br>' +
                          '2. Ollama 服務已啟動 <code>ollama serve</code><br>' +
                          '3. Qwen 2.5 模型已安裝 <code>ollama pull qwen2.5:7b</code>';
            } else {
                errorMsg = '抱歉，發生錯誤：' + error.message;
            }

            addMessage(errorMsg);
        } finally {
            input.disabled = false;
            input.focus();
        }
    }

    // 暴露到全局
    window.AIChatWidget = {
        sendMessage: sendMessage,
        toggleChat: toggleChat,
        addMessage: addMessage
    };
})();

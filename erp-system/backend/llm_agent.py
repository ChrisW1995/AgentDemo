"""
LLM-based ERP AI Agent using Ollama
使用 Ollama 的 LLM 智能 ERP 代理
"""
import json
import requests
from typing import List, Dict, Any, Optional
from database import SessionLocal, Product as DBProduct, Order as DBOrder, OrderItem as DBOrderItem
from datetime import datetime


class ERPAgent:
    """LLM-based ERP Agent with function calling capabilities"""

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/chat"
        self.conversation_history = []

        # 定義可用的工具函數
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_products",
                    "description": "查詢產品列表，可選擇性地過濾低庫存產品",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "low_stock_only": {
                                "type": "boolean",
                                "description": "是否只查詢低庫存產品"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_orders",
                    "description": "查詢訂單列表，可選擇性地按狀態過濾",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "processing", "completed", "cancelled"],
                                "description": "訂單狀態"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_order",
                    "description": "創建新訂單",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_name": {
                                "type": "string",
                                "description": "客戶名稱"
                            },
                            "customer_email": {
                                "type": "string",
                                "description": "客戶郵箱（可選）"
                            },
                            "customer_phone": {
                                "type": "string",
                                "description": "客戶電話（可選）"
                            },
                            "shipping_address": {
                                "type": "string",
                                "description": "送貨地址（可選）"
                            },
                            "items": {
                                "type": "array",
                                "description": "訂單項目列表",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "product_id": {"type": "integer"},
                                        "quantity": {"type": "integer"}
                                    },
                                    "required": ["product_id", "quantity"]
                                }
                            }
                        },
                        "required": ["customer_name", "items"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_stock",
                    "description": "更新產品庫存（補貨）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_id": {
                                "type": "integer",
                                "description": "產品ID"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "補貨數量"
                            }
                        },
                        "required": ["product_id", "quantity"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_sales_report",
                    "description": "獲取銷售報表統計",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    # ===== 工具函數實現 =====

    def get_products(self, low_stock_only: bool = False) -> Dict[str, Any]:
        """查詢產品列表"""
        db = SessionLocal()
        try:
            query = db.query(DBProduct)
            if low_stock_only:
                products = [p for p in query.all() if p.stock_quantity < p.min_stock_level]
            else:
                products = query.all()

            result = []
            for p in products:
                result.append({
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "price": float(p.price),
                    "stock_quantity": p.stock_quantity,
                    "min_stock_level": p.min_stock_level,
                    "category": p.category,
                    "supplier": p.supplier
                })
            return {"success": True, "products": result, "count": len(result)}
        finally:
            db.close()

    def get_orders(self, status: Optional[str] = None) -> Dict[str, Any]:
        """查詢訂單列表"""
        db = SessionLocal()
        try:
            query = db.query(DBOrder)
            if status:
                query = query.filter(DBOrder.status == status)
            orders = query.all()

            result = []
            for o in orders:
                result.append({
                    "id": o.id,
                    "order_number": o.order_number,
                    "customer_name": o.customer_name,
                    "total_amount": float(o.total_amount),
                    "status": o.status,
                    "order_date": o.order_date.isoformat()
                })
            return {"success": True, "orders": result, "count": len(result)}
        finally:
            db.close()

    def create_order(self, customer_name: str, items: List[Dict],
                     customer_email: Optional[str] = None,
                     customer_phone: Optional[str] = None,
                     shipping_address: Optional[str] = None) -> Dict[str, Any]:
        """創建新訂單"""
        db = SessionLocal()
        try:
            # 生成訂單號
            now = datetime.now()
            count = db.query(DBOrder).count() + 1
            order_number = f"ORD{now.year % 100:02d}{now.month:02d}{count:04d}"

            # 計算總金額並檢查庫存
            total_amount = 0
            order_items_data = []
            for item in items:
                product = db.query(DBProduct).filter(DBProduct.id == item["product_id"]).first()
                if not product:
                    return {"success": False, "error": f"產品 ID {item['product_id']} 不存在"}
                if product.stock_quantity < item["quantity"]:
                    return {"success": False, "error": f"產品 {product.name} 庫存不足"}

                subtotal = product.price * item["quantity"]
                total_amount += subtotal
                order_items_data.append({
                    "product": product,
                    "quantity": item["quantity"],
                    "unit_price": product.price,
                    "subtotal": subtotal
                })

            # 創建訂單
            db_order = DBOrder(
                order_number=order_number,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                shipping_address=shipping_address,
                total_amount=total_amount,
                status="pending"
            )
            db.add(db_order)
            db.flush()

            # 創建訂單項目並扣減庫存
            for item_data in order_items_data:
                db_item = DBOrderItem(
                    order_id=db_order.id,
                    product_id=item_data["product"].id,
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    subtotal=item_data["subtotal"]
                )
                db.add(db_item)

                # 扣減庫存
                item_data["product"].stock_quantity -= item_data["quantity"]

            db.commit()

            return {
                "success": True,
                "order": {
                    "id": db_order.id,
                    "order_number": order_number,
                    "customer_name": customer_name,
                    "total_amount": float(total_amount),
                    "status": "pending"
                }
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def update_stock(self, product_id: int, quantity: int) -> Dict[str, Any]:
        """更新產品庫存"""
        db = SessionLocal()
        try:
            product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
            if not product:
                return {"success": False, "error": f"產品 ID {product_id} 不存在"}

            old_stock = product.stock_quantity
            product.stock_quantity += quantity
            db.commit()

            return {
                "success": True,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "old_stock": old_stock,
                    "new_stock": product.stock_quantity,
                    "added": quantity
                }
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def get_sales_report(self) -> Dict[str, Any]:
        """獲取銷售報表"""
        db = SessionLocal()
        try:
            orders = db.query(DBOrder).all()
            total_orders = len(orders)
            completed_orders = len([o for o in orders if o.status == "completed"])
            pending_orders = len([o for o in orders if o.status == "pending"])
            total_revenue = sum(float(o.total_amount) for o in orders if o.status == "completed")

            return {
                "success": True,
                "report": {
                    "total_orders": total_orders,
                    "completed_orders": completed_orders,
                    "pending_orders": pending_orders,
                    "total_revenue": total_revenue
                }
            }
        finally:
            db.close()

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行工具函數"""
        if tool_name == "get_products":
            return self.get_products(**arguments)
        elif tool_name == "get_orders":
            return self.get_orders(**arguments)
        elif tool_name == "create_order":
            return self.create_order(**arguments)
        elif tool_name == "update_stock":
            return self.update_stock(**arguments)
        elif tool_name == "get_sales_report":
            return self.get_sales_report(**arguments)
        else:
            return {"success": False, "error": f"未知的工具: {tool_name}"}

    def chat(self, user_message: str) -> str:
        """與 LLM 對話並處理工具調用"""
        # 添加用戶消息到歷史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # 系統提示（強制繁體中文輸出）
        system_prompt = """你是 ERP 系統 AI 助手。

【重要】你必須使用繁體中文（台灣用語）回答，不可使用簡體中文。

功能：查詢產品/訂單、創建訂單、補貨、查看報表。

規則：
1. 必須用繁體中文簡潔回答（例如：「您」而非「你」，「訂單」而非「订单」）
2. 需要執行操作時調用工具
3. 工具返回結果後，用繁體中文簡單總結給用戶
4. 不要重複用戶的問題

範例回答格式：
- 「系統目前有 25 筆訂單」
- 「已為您查詢庫存狀態」"""

        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # 調用 Ollama API
            try:
                print(f"[LLM Agent] 迭代 {iteration}/{max_iterations}，發送請求到 Ollama...")
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "tools": self.tools,
                        "stream": False
                    },
                    timeout=45  # 減少超時時間到 45 秒
                )
                response.raise_for_status()
                result = response.json()
                print(f"[LLM Agent] Ollama 響應成功")

                assistant_message = result["message"]
                messages.append(assistant_message)

                # 檢查是否有工具調用
                if "tool_calls" in assistant_message and assistant_message["tool_calls"]:
                    print(f"[LLM Agent] 檢測到 {len(assistant_message['tool_calls'])} 個工具調用")
                    for tool_call in assistant_message["tool_calls"]:
                        function_name = tool_call["function"]["name"]
                        arguments = tool_call["function"]["arguments"]

                        print(f"[LLM Agent] 執行工具: {function_name}，參數: {arguments}")
                        # 執行工具
                        tool_result = self.execute_tool(function_name, arguments)
                        print(f"[LLM Agent] 工具執行結果: {tool_result.get('success', False)}")

                        # 添加工具結果到消息
                        messages.append({
                            "role": "tool",
                            "content": json.dumps(tool_result, ensure_ascii=False)
                        })

                    # 繼續循環讓 LLM 處理工具結果
                    continue
                else:
                    # 沒有工具調用，返回最終回答
                    final_response = assistant_message["content"]
                    print(f"[LLM Agent] 最終回答: {final_response[:100]}...")
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_response
                    })
                    return final_response

            except requests.exceptions.ConnectionError:
                return "錯誤：無法連接到 Ollama 服務。請確保 Ollama 正在運行（執行 'ollama serve'）。"
            except requests.exceptions.Timeout:
                return "錯誤：請求超時。請稍後再試。"
            except Exception as e:
                return f"錯誤：{str(e)}"

        return "抱歉，處理您的請求時遇到問題。請重新表述您的需求。"

    def reset_conversation(self):
        """重置對話歷史"""
        self.conversation_history = []


# 全局 agent 實例
agent = ERPAgent()


def get_agent() -> ERPAgent:
    """獲取 agent 實例"""
    return agent

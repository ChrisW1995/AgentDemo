#!/usr/bin/env python3
"""
ERP AI Agent - LLM版本 (使用Ollama本地模型)
通过大语言模型理解自然语言指令并自动化完成ERP系统操作
"""

import requests
import json
import sys
from typing import Dict, List, Optional, Any
from colorama import init, Fore, Style

# 初始化colorama
init()


class LLMAgent:
    """基于LLM的ERP系统AI代理"""

    def __init__(
        self,
        api_base_url: str = "http://localhost:8000/api",
        ollama_base_url: str = "http://localhost:11434",
        model: str = "qwen2.5:7b"
    ):
        self.api_base_url = api_base_url
        self.ollama_base_url = ollama_base_url
        self.model = model
        self.conversation_history = []
        self.products_cache = None

        # 定义可用的工具（Function Calling）
        self.tools = [
            {
                "name": "get_products",
                "description": "获取产品列表，可用于查询库存信息",
                "parameters": {}
            },
            {
                "name": "create_order",
                "description": "创建新订单",
                "parameters": {
                    "customer_name": "客户名称（必填）",
                    "items": "订单项列表，每项包含product_id和quantity"
                }
            },
            {
                "name": "get_orders",
                "description": "获取订单列表",
                "parameters": {}
            },
            {
                "name": "update_order_status",
                "description": "更新订单状态",
                "parameters": {
                    "order_id": "订单ID（必填）",
                    "status": "状态：completed(完成) 或 cancelled(取消)"
                }
            },
            {
                "name": "get_stock_alerts",
                "description": "获取库存预警，查看哪些产品库存不足",
                "parameters": {}
            },
            {
                "name": "restock_product",
                "description": "给产品补货",
                "parameters": {
                    "product_id": "产品ID（必填）",
                    "quantity": "补货数量（必填）"
                }
            },
            {
                "name": "get_sales_report",
                "description": "获取销售报表统计数据",
                "parameters": {}
            },
            {
                "name": "get_inventory_report",
                "description": "获取库存报表统计数据",
                "parameters": {}
            }
        ]

    def print_header(self):
        """打印欢迎信息"""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}{Style.BRIGHT}🤖 ERP AI Agent - LLM版本{Style.RESET_ALL}")
        print("="*60)
        print(f"{Fore.YELLOW}使用本地LLM ({self.model}) 理解自然语言指令{Style.RESET_ALL}")
        print("\n可用指令示例（更智能，更灵活）：")
        print("  • 帮我给ABC公司下个订单，买10台笔记本电脑")
        print("  • 查一下哪些产品库存不够了")
        print("  • 给库存最少的产品补货50个")
        print("  • 把1号订单标记为完成")
        print("  • 告诉我这个月的销售情况")
        print("  • 哪个产品最热销？")
        print("\n输入 'exit' 或 'quit' 退出程序")
        print("="*60 + "\n")

    def check_ollama_status(self) -> bool:
        """检查Ollama服务状态"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def check_model_available(self) -> bool:
        """检查模型是否可用"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model in m.get('name', '') for m in models)
            return False
        except:
            return False

    def chat_with_llm(self, user_message: str) -> str:
        """与LLM对话"""
        # 构建系统提示词
        system_prompt = f"""你是一个ERP系统的AI助手。你可以帮助用户完成以下任务：

可用工具：
{json.dumps(self.tools, indent=2, ensure_ascii=False)}

当用户提出请求时，你需要：
1. 理解用户的意图
2. 决定需要调用哪个工具
3. 以JSON格式返回工具调用信息

返回格式：
{{
    "thought": "你的思考过程",
    "action": "工具名称",
    "action_input": {{参数字典}}
}}

如果不需要调用工具，只需要回答问题，返回：
{{
    "thought": "你的思考过程",
    "action": "none",
    "response": "你的回答"
}}

注意：
- 产品名称和ID的对应关系：笔记本电脑(1), 台式电脑(2), 显示器(3), 键盘(4), 鼠标(5), 打印机(6)
- 订单状态只能是：completed(完成) 或 cancelled(取消)
- 补货数量必须是正整数
"""

        # 调用Ollama API
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\n用户问题：{user_message}\n\n请以JSON格式返回你的决策：",
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return '{"action": "error", "response": "LLM调用失败"}'

        except Exception as e:
            return f'{{"action": "error", "response": "LLM调用异常: {str(e)}"}}'

    def execute_command(self, command: str) -> bool:
        """执行用户命令"""
        if command.lower() in ['exit', 'quit', '退出']:
            print(f"\n{Fore.GREEN}感谢使用 ERP AI Agent！{Style.RESET_ALL}\n")
            return False

        print(f"{Fore.CYAN}🤔 思考中...{Style.RESET_ALL}")

        # 调用LLM理解用户意图
        llm_response = self.chat_with_llm(command)

        try:
            decision = json.loads(llm_response)
        except json.JSONDecodeError:
            print(f"{Fore.RED}❌ LLM返回格式错误{Style.RESET_ALL}")
            print(f"原始返回: {llm_response[:200]}")
            return True

        # 显示LLM的思考过程
        if "thought" in decision:
            print(f"{Fore.YELLOW}💭 {decision['thought']}{Style.RESET_ALL}")

        action = decision.get("action")

        if action == "none":
            print(f"\n{Fore.GREEN}{decision.get('response', '好的')}{Style.RESET_ALL}\n")
            return True

        if action == "error":
            print(f"{Fore.RED}❌ {decision.get('response', '发生错误')}{Style.RESET_ALL}")
            return True

        # 执行工具调用
        print(f"{Fore.CYAN}⚙️  执行: {action}{Style.RESET_ALL}")

        try:
            action_input = decision.get("action_input", {})
            result = self.execute_tool(action, action_input)
            self.display_result(result)
        except Exception as e:
            print(f"{Fore.RED}❌ 执行失败: {str(e)}{Style.RESET_ALL}")

        return True

    def execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """执行工具调用"""
        tool_map = {
            "get_products": self.tool_get_products,
            "create_order": self.tool_create_order,
            "get_orders": self.tool_get_orders,
            "update_order_status": self.tool_update_order_status,
            "get_stock_alerts": self.tool_get_stock_alerts,
            "restock_product": self.tool_restock_product,
            "get_sales_report": self.tool_get_sales_report,
            "get_inventory_report": self.tool_get_inventory_report,
        }

        tool_func = tool_map.get(tool_name)
        if not tool_func:
            raise Exception(f"未知工具: {tool_name}")

        return tool_func(params)

    # ==================== 工具函数 ====================

    def tool_get_products(self, params: Dict) -> Dict:
        """获取产品列表"""
        response = requests.get(f"{self.api_base_url}/products")
        if response.status_code == 200:
            products = response.json()
            return {
                "success": True,
                "data": products,
                "type": "products"
            }
        return {"success": False, "error": "获取产品列表失败"}

    def tool_create_order(self, params: Dict) -> Dict:
        """创建订单"""
        customer_name = params.get("customer_name")
        items = params.get("items", [])

        if not customer_name or not items:
            return {"success": False, "error": "缺少客户名称或订单项"}

        order_data = {
            "customer_name": customer_name,
            "items": items
        }

        response = requests.post(f"{self.api_base_url}/orders", json=order_data)
        if response.status_code == 200:
            order = response.json()
            return {
                "success": True,
                "message": "订单创建成功",
                "data": order,
                "type": "order"
            }
        else:
            error = response.json()
            return {"success": False, "error": error.get("detail", "创建失败")}

    def tool_get_orders(self, params: Dict) -> Dict:
        """获取订单列表"""
        response = requests.get(f"{self.api_base_url}/orders")
        if response.status_code == 200:
            orders = response.json()
            return {
                "success": True,
                "data": orders,
                "type": "orders"
            }
        return {"success": False, "error": "获取订单列表失败"}

    def tool_update_order_status(self, params: Dict) -> Dict:
        """更新订单状态"""
        order_id = params.get("order_id")
        status = params.get("status")

        if not order_id or not status:
            return {"success": False, "error": "缺少订单ID或状态"}

        response = requests.put(
            f"{self.api_base_url}/orders/{order_id}",
            json={"status": status}
        )

        if response.status_code == 200:
            order = response.json()
            return {
                "success": True,
                "message": "订单状态更新成功",
                "data": order,
                "type": "order"
            }
        else:
            error = response.json()
            return {"success": False, "error": error.get("detail", "更新失败")}

    def tool_get_stock_alerts(self, params: Dict) -> Dict:
        """获取库存预警"""
        response = requests.get(f"{self.api_base_url}/inventory/alerts")
        if response.status_code == 200:
            alerts = response.json()
            return {
                "success": True,
                "data": alerts,
                "type": "alerts"
            }
        return {"success": False, "error": "获取库存预警失败"}

    def tool_restock_product(self, params: Dict) -> Dict:
        """补货"""
        product_id = params.get("product_id")
        quantity = params.get("quantity")

        if not product_id or not quantity:
            return {"success": False, "error": "缺少产品ID或数量"}

        response = requests.post(
            f"{self.api_base_url}/inventory/restock/{product_id}?quantity={quantity}"
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": result["message"],
                "data": {"new_stock": result["new_stock"]}
            }
        return {"success": False, "error": "补货失败"}

    def tool_get_sales_report(self, params: Dict) -> Dict:
        """获取销售报表"""
        response = requests.get(f"{self.api_base_url}/reports/sales")
        if response.status_code == 200:
            report = response.json()
            return {
                "success": True,
                "data": report,
                "type": "sales_report"
            }
        return {"success": False, "error": "获取销售报表失败"}

    def tool_get_inventory_report(self, params: Dict) -> Dict:
        """获取库存报表"""
        response = requests.get(f"{self.api_base_url}/reports/inventory")
        if response.status_code == 200:
            report = response.json()
            return {
                "success": True,
                "data": report,
                "type": "inventory_report"
            }
        return {"success": False, "error": "获取库存报表失败"}

    # ==================== 结果显示 ====================

    def display_result(self, result: Dict):
        """显示执行结果"""
        if not result.get("success"):
            print(f"\n{Fore.RED}❌ 失败: {result.get('error', '未知错误')}{Style.RESET_ALL}\n")
            return

        print(f"\n{Fore.GREEN}✅ {result.get('message', '成功')}{Style.RESET_ALL}\n")

        data = result.get("data")
        if not data:
            return

        result_type = result.get("type")

        # 根据类型显示结果
        if result_type == "products":
            self.display_products(data)
        elif result_type == "order":
            self.display_order(data)
        elif result_type == "orders":
            self.display_orders(data)
        elif result_type == "alerts":
            self.display_alerts(data)
        elif result_type == "sales_report":
            self.display_sales_report(data)
        elif result_type == "inventory_report":
            self.display_inventory_report(data)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))

    def display_products(self, products: List[Dict]):
        """显示产品列表"""
        if not products:
            print("  没有产品")
            return

        print(f"{'产品名称':<20} {'单价':<15} {'库存':<10} {'最低库存':<10}")
        print("-" * 60)
        for product in products:
            stock_status = "⚠️" if product['stock_quantity'] < product['min_stock_level'] else "✓"
            print(f"{product['name']:<20} ¥{product['price']:<14.2f} {product['stock_quantity']:<10} {product['min_stock_level']:<10} {stock_status}")
        print()

    def display_order(self, order: Dict):
        """显示订单信息"""
        print(f"  订单号: #{order['id']}")
        print(f"  客户: {order['customer_name']}")
        print(f"  状态: {order['status']}")
        print(f"  总金额: ¥{order['total_amount']:.2f}")
        if order.get('items'):
            print(f"  订单项:")
            for item in order['items']:
                print(f"    - {item['product']['name']} x {item['quantity']} = ¥{item['subtotal']:.2f}")
        print()

    def display_orders(self, orders: List[Dict]):
        """显示订单列表"""
        if not orders:
            print("  没有订单")
            return

        print(f"{'订单号':<10} {'客户':<20} {'状态':<10} {'总金额':<15}")
        print("-" * 60)
        for order in orders:
            print(f"#{order['id']:<9} {order['customer_name']:<20} {order['status']:<10} ¥{order['total_amount']:<14.2f}")
        print()

    def display_alerts(self, alerts: List[Dict]):
        """显示库存预警"""
        if not alerts:
            print("  ✓ 所有产品库存充足")
            return

        print(f"{'产品名称':<20} {'当前库存':<12} {'最低库存':<12} {'缺货数量':<10}")
        print("-" * 60)
        for alert in alerts:
            print(f"{alert['product_name']:<20} {alert['current_stock']:<12} {alert['min_stock_level']:<12} {alert['shortage']:<10}")
        print()

    def display_sales_report(self, report: Dict):
        """显示销售报表"""
        print(f"  总订单数: {report['total_orders']}")
        print(f"  总收入: ¥{report['total_revenue']:.2f}")
        print(f"  已完成: {report['completed_orders']}")
        print(f"  待处理: {report['pending_orders']}")
        print(f"  已取消: {report['cancelled_orders']}")

        if report.get('top_products'):
            print(f"\n  热销产品 TOP 5:")
            for i, product in enumerate(report['top_products'], 1):
                print(f"    {i}. {product['product_name']} - 销量: {product['quantity']}, 销售额: ¥{product['revenue']:.2f}")
        print()

    def display_inventory_report(self, report: Dict):
        """显示库存报表"""
        print(f"  产品总数: {report['total_products']}")
        print(f"  库存总价值: ¥{report['total_stock_value']:.2f}")
        print(f"  缺货产品数: {report['out_of_stock_count']}")

        if report.get('low_stock_products'):
            print(f"\n  低库存产品:")
            for product in report['low_stock_products']:
                print(f"    - {product['product_name']}: 当前 {product['current_stock']}, 需要 {product['min_stock_level']}")
        print()

    def run(self):
        """运行Agent"""
        self.print_header()

        # 检查ERP系统
        try:
            response = requests.get(f"{self.api_base_url}/products", timeout=2)
            if response.status_code != 200:
                print(f"{Fore.RED}❌ 无法连接到ERP系统{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 请先运行: ./start_erp.sh{Style.RESET_ALL}\n")
                return
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}❌ 无法连接到ERP系统 ({self.api_base_url}){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 请先运行: ./start_erp.sh{Style.RESET_ALL}\n")
            return

        # 检查Ollama服务
        if not self.check_ollama_status():
            print(f"{Fore.RED}❌ 无法连接到Ollama服务{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 请确保Ollama正在运行：{Style.RESET_ALL}")
            print(f"   1. 安装Ollama: curl -fsSL https://ollama.com/install.sh | sh")
            print(f"   2. 启动服务: ollama serve")
            print(f"   3. 下载模型: ollama pull {self.model}\n")
            return

        # 检查模型是否可用
        if not self.check_model_available():
            print(f"{Fore.YELLOW}⚠️  模型 {self.model} 未找到{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 请下载模型: ollama pull {self.model}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}ℹ️  推荐模型：qwen2.5:7b, llama3.2, gemma2{Style.RESET_ALL}\n")
            return

        print(f"{Fore.GREEN}✅ 所有系统就绪！{Style.RESET_ALL}\n")

        # 主循环
        while True:
            try:
                command = input(f"{Fore.CYAN}Agent (LLM) > {Style.RESET_ALL}").strip()
                if not command:
                    continue

                if not self.execute_command(command):
                    break

            except KeyboardInterrupt:
                print(f"\n\n{Fore.GREEN}感谢使用 ERP AI Agent！{Style.RESET_ALL}\n")
                break
            except Exception as e:
                print(f"{Fore.RED}错误: {str(e)}{Style.RESET_ALL}")


def main():
    """主函数"""
    # 可以通过命令行参数指定模型
    model = "qwen2.5:7b"  # 默认使用qwen2.5:7b，也可以改为 llama3.2, gemma2 等

    if len(sys.argv) > 1:
        model = sys.argv[1]

    print(f"使用模型: {model}")

    agent = LLMAgent(model=model)
    agent.run()


if __name__ == "__main__":
    main()

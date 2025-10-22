#!/usr/bin/env python3
"""
ERP AI Agent - 智能ERP系统代理
通过自然语言指令自动化完成ERP系统操作
"""

import requests
import json
import sys
from typing import Dict, List, Optional
from colorama import init, Fore, Style
from task_parser import TaskParser

# 初始化colorama
init()


class ERPAgent:
    """ERP系统AI代理"""

    def __init__(self, api_base_url: str = "http://localhost:8000/api"):
        self.api_base_url = api_base_url
        self.task_parser = TaskParser()
        self.products_cache = None

    def print_header(self):
        """打印欢迎信息"""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}{Style.BRIGHT}🤖 ERP AI Agent - 智能ERP系统代理{Style.RESET_ALL}")
        print("="*60)
        print(f"{Fore.YELLOW}通过自然语言指令控制ERP系统{Style.RESET_ALL}")
        print("\n可用指令示例：")
        print("  • 创建订单，客户是ABC公司，产品是笔记本电脑10台")
        print("  • 查询库存不足的产品")
        print("  • 给打印机补货20台")
        print("  • 查看销售报表")
        print("  • 完成订单 #1")
        print("\n输入 'exit' 或 'quit' 退出程序")
        print("="*60 + "\n")

    def execute_command(self, command: str) -> bool:
        """
        执行用户命令

        Returns:
            True 继续执行，False 退出程序
        """
        if command.lower() in ['exit', 'quit', '退出']:
            print(f"\n{Fore.GREEN}感谢使用 ERP AI Agent！{Style.RESET_ALL}\n")
            return False

        # 解析任务
        print(f"{Fore.CYAN}📝 解析任务...{Style.RESET_ALL}")
        task = self.task_parser.parse(command)

        if task['task_type'] == 'unknown':
            print(f"{Fore.RED}❌ {task['error']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 {task['suggestion']}{Style.RESET_ALL}")
            return True

        # 显示解析结果
        print(f"{Fore.GREEN}✓ 任务识别: {self.task_parser.get_task_description(task)}{Style.RESET_ALL}")

        # 执行任务
        print(f"{Fore.CYAN}⚙️  执行中...{Style.RESET_ALL}")
        try:
            result = self.execute_task(task)
            self.display_result(result)
        except Exception as e:
            print(f"{Fore.RED}❌ 执行失败: {str(e)}{Style.RESET_ALL}")

        return True

    def execute_task(self, task: Dict) -> Dict:
        """执行任务"""
        task_type = task['task_type']
        params = task.get('params', {})

        # 路由到对应的处理方法
        handlers = {
            'create_order': self.handle_create_order,
            'query_orders': self.handle_query_orders,
            'update_order_status': self.handle_update_order_status,
            'query_inventory': self.handle_query_inventory,
            'restock': self.handle_restock,
            'query_sales_report': self.handle_query_sales_report,
            'query_inventory_report': self.handle_query_inventory_report,
        }

        handler = handlers.get(task_type)
        if handler:
            return handler(params)
        else:
            raise Exception(f"不支持的任务类型: {task_type}")

    # ==================== 任务处理方法 ====================

    def handle_create_order(self, params: Dict) -> Dict:
        """处理创建订单任务"""
        customer_name = params.get('customer_name')
        items = params.get('items', [])

        if not customer_name:
            return {'success': False, 'error': '缺少客户名称'}

        if not items:
            return {'success': False, 'error': '缺少订单项'}

        # 获取产品列表
        products = self.get_products()

        # 转换产品名称为产品ID
        order_items = []
        for item in items:
            product = next((p for p in products if p['name'] == item['product_name']), None)
            if not product:
                return {'success': False, 'error': f"找不到产品: {item['product_name']}"}

            order_items.append({
                'product_id': product['id'],
                'quantity': item['quantity']
            })

        # 创建订单
        order_data = {
            'customer_name': customer_name,
            'items': order_items
        }

        response = requests.post(f"{self.api_base_url}/orders", json=order_data)
        if response.status_code == 200:
            order = response.json()
            return {
                'success': True,
                'message': '订单创建成功',
                'data': order
            }
        else:
            error = response.json()
            return {'success': False, 'error': error.get('detail', '未知错误')}

    def handle_query_orders(self, params: Dict) -> Dict:
        """处理查询订单任务"""
        response = requests.get(f"{self.api_base_url}/orders")
        if response.status_code == 200:
            orders = response.json()

            # 过滤（如果指定了客户名称）
            customer_name = params.get('customer_name')
            if customer_name:
                orders = [o for o in orders if customer_name in o['customer_name']]

            return {
                'success': True,
                'message': f'找到 {len(orders)} 个订单',
                'data': orders
            }
        else:
            return {'success': False, 'error': '查询失败'}

    def handle_update_order_status(self, params: Dict) -> Dict:
        """处理更新订单状态任务"""
        order_id = params.get('order_id')
        status = params.get('status')

        if not order_id or not status:
            return {'success': False, 'error': '缺少订单ID或状态'}

        response = requests.put(
            f"{self.api_base_url}/orders/{order_id}",
            json={'status': status}
        )

        if response.status_code == 200:
            order = response.json()
            return {
                'success': True,
                'message': '订单状态更新成功',
                'data': order
            }
        else:
            error = response.json()
            return {'success': False, 'error': error.get('detail', '更新失败')}

    def handle_query_inventory(self, params: Dict) -> Dict:
        """处理查询库存任务"""
        if params.get('low_stock_only'):
            # 查询库存预警
            response = requests.get(f"{self.api_base_url}/inventory/alerts")
            if response.status_code == 200:
                alerts = response.json()
                return {
                    'success': True,
                    'message': f'找到 {len(alerts)} 个库存预警',
                    'data': alerts,
                    'type': 'alerts'
                }
        else:
            # 查询所有产品库存
            response = requests.get(f"{self.api_base_url}/products")
            if response.status_code == 200:
                products = response.json()

                # 过滤（如果指定了产品名称）
                product_name = params.get('product_name')
                if product_name:
                    products = [p for p in products if product_name in p['name']]

                return {
                    'success': True,
                    'message': f'找到 {len(products)} 个产品',
                    'data': products,
                    'type': 'products'
                }

        return {'success': False, 'error': '查询失败'}

    def handle_restock(self, params: Dict) -> Dict:
        """处理补货任务"""
        product_name = params.get('product_name')
        quantity = params.get('quantity')

        if not product_name:
            return {'success': False, 'error': '缺少产品名称'}

        if not quantity:
            return {'success': False, 'error': '缺少补货数量'}

        # 查找产品
        products = self.get_products()
        product = next((p for p in products if p['name'] == product_name), None)

        if not product:
            return {'success': False, 'error': f"找不到产品: {product_name}"}

        # 补货
        response = requests.post(
            f"{self.api_base_url}/inventory/restock/{product['id']}?quantity={quantity}"
        )

        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'message': result['message'],
                'data': {'product_name': product_name, 'new_stock': result['new_stock']}
            }
        else:
            return {'success': False, 'error': '补货失败'}

    def handle_query_sales_report(self, params: Dict) -> Dict:
        """处理查询销售报表任务"""
        response = requests.get(f"{self.api_base_url}/reports/sales")
        if response.status_code == 200:
            report = response.json()
            return {
                'success': True,
                'message': '销售报表查询成功',
                'data': report,
                'type': 'sales_report'
            }
        else:
            return {'success': False, 'error': '查询失败'}

    def handle_query_inventory_report(self, params: Dict) -> Dict:
        """处理查询库存报表任务"""
        response = requests.get(f"{self.api_base_url}/reports/inventory")
        if response.status_code == 200:
            report = response.json()
            return {
                'success': True,
                'message': '库存报表查询成功',
                'data': report,
                'type': 'inventory_report'
            }
        else:
            return {'success': False, 'error': '查询失败'}

    # ==================== 辅助方法 ====================

    def get_products(self) -> List[Dict]:
        """获取产品列表（带缓存）"""
        if self.products_cache is None:
            response = requests.get(f"{self.api_base_url}/products")
            if response.status_code == 200:
                self.products_cache = response.json()
            else:
                raise Exception("无法获取产品列表")
        return self.products_cache

    def display_result(self, result: Dict):
        """显示执行结果"""
        if not result.get('success'):
            print(f"\n{Fore.RED}❌ 失败: {result.get('error', '未知错误')}{Style.RESET_ALL}\n")
            return

        print(f"\n{Fore.GREEN}✅ {result.get('message', '成功')}{Style.RESET_ALL}\n")

        data = result.get('data')
        if not data:
            return

        result_type = result.get('type')

        # 根据数据类型显示结果
        if result_type == 'alerts':
            self.display_alerts(data)
        elif result_type == 'products':
            self.display_products(data)
        elif result_type == 'sales_report':
            self.display_sales_report(data)
        elif result_type == 'inventory_report':
            self.display_inventory_report(data)
        elif isinstance(data, list):
            self.display_orders(data)
        elif isinstance(data, dict):
            if 'id' in data and 'customer_name' in data:
                self.display_order(data)
            else:
                print(json.dumps(data, indent=2, ensure_ascii=False))

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

    def display_products(self, products: List[Dict]):
        """显示产品库存"""
        if not products:
            print("  没有产品")
            return

        print(f"{'产品名称':<20} {'单价':<15} {'库存':<10} {'最低库存':<10}")
        print("-" * 60)
        for product in products:
            stock_status = "⚠️" if product['stock_quantity'] < product['min_stock_level'] else "✓"
            print(f"{product['name']:<20} ¥{product['price']:<14.2f} {product['stock_quantity']:<10} {product['min_stock_level']:<10} {stock_status}")
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

        # 测试连接
        try:
            response = requests.get(f"{self.api_base_url}/products", timeout=2)
            if response.status_code != 200:
                print(f"{Fore.RED}❌ 无法连接到ERP系统，请确保系统正在运行{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 请先运行: cd erp-system/backend && python main.py{Style.RESET_ALL}\n")
                return
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}❌ 无法连接到ERP系统 ({self.api_base_url}){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 请先运行: cd erp-system/backend && python main.py{Style.RESET_ALL}\n")
            return

        # 主循环
        while True:
            try:
                command = input(f"{Fore.CYAN}Agent > {Style.RESET_ALL}").strip()
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
    agent = ERPAgent()
    agent.run()


if __name__ == "__main__":
    main()

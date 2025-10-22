import re
from typing import Dict, List, Optional, Tuple


class TaskParser:
    """任务解析器 - 将自然语言指令解析为结构化任务"""

    def __init__(self):
        # 任务类型关键词
        self.task_patterns = {
            'create_order': [
                r'创建.*订单',
                r'下.*订单',
                r'新建.*订单',
                r'添加.*订单',
            ],
            'query_orders': [
                r'查询.*订单',
                r'查看.*订单',
                r'显示.*订单',
                r'订单.*列表',
            ],
            'update_order_status': [
                r'完成.*订单',
                r'取消.*订单',
                r'更新.*订单.*状态',
                r'订单.*状态',
            ],
            'query_inventory': [
                r'查询.*库存',
                r'查看.*库存',
                r'库存.*查询',
                r'库存.*情况',
                r'库存.*不足',
            ],
            'restock': [
                r'补货',
                r'进货',
                r'增加.*库存',
                r'添加.*库存',
            ],
            'query_sales_report': [
                r'销售.*报表',
                r'销售.*统计',
                r'销售.*数据',
                r'查看.*销售',
            ],
            'query_inventory_report': [
                r'库存.*报表',
                r'库存.*统计',
                r'库存.*数据',
            ],
        }

        # 产品名称映射
        self.product_names = {
            '笔记本': '笔记本电脑',
            '笔记本电脑': '笔记本电脑',
            '台式机': '台式电脑',
            '台式电脑': '台式电脑',
            '显示器': '显示器',
            '键盘': '键盘',
            '鼠标': '鼠标',
            '打印机': '打印机',
        }

    def parse(self, text: str) -> Dict:
        """
        解析用户输入的自然语言指令

        Args:
            text: 用户输入的文本

        Returns:
            包含任务类型和参数的字典
        """
        text = text.strip()

        # 识别任务类型
        task_type = self._identify_task_type(text)

        if not task_type:
            return {
                'task_type': 'unknown',
                'error': '无法识别的任务类型',
                'suggestion': '请尝试使用"创建订单"、"查询库存"、"查看报表"等关键词'
            }

        # 根据任务类型提取参数
        params = self._extract_params(task_type, text)

        return {
            'task_type': task_type,
            'params': params,
            'original_text': text
        }

    def _identify_task_type(self, text: str) -> Optional[str]:
        """识别任务类型"""
        for task_type, patterns in self.task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return task_type
        return None

    def _extract_params(self, task_type: str, text: str) -> Dict:
        """提取任务参数"""
        params = {}

        if task_type == 'create_order':
            # 提取客户名称
            customer_match = re.search(r'客户[是为]?[:：]?\s*([^\s,，]+)', text)
            if customer_match:
                params['customer_name'] = customer_match.group(1)
            else:
                # 尝试其他模式
                customer_match = re.search(r'([^\s,，]+)公司', text)
                if customer_match:
                    params['customer_name'] = customer_match.group(1) + '公司'

            # 提取产品和数量
            items = self._extract_order_items(text)
            if items:
                params['items'] = items

        elif task_type == 'query_orders':
            # 提取客户名称（如果有）
            customer_match = re.search(r'客户[是为]?[:：]?\s*([^\s,，]+)', text)
            if customer_match:
                params['customer_name'] = customer_match.group(1)

        elif task_type == 'update_order_status':
            # 提取订单ID
            order_id_match = re.search(r'订单[号]?[:：]?\s*#?(\d+)', text)
            if order_id_match:
                params['order_id'] = int(order_id_match.group(1))

            # 提取状态
            if re.search(r'完成', text):
                params['status'] = 'completed'
            elif re.search(r'取消', text):
                params['status'] = 'cancelled'

        elif task_type == 'query_inventory':
            # 提取产品名称
            for key, value in self.product_names.items():
                if key in text:
                    params['product_name'] = value
                    break

            # 检查是否查询低库存
            if re.search(r'不足|预警|低库存', text):
                params['low_stock_only'] = True

        elif task_type == 'restock':
            # 提取产品名称
            for key, value in self.product_names.items():
                if key in text:
                    params['product_name'] = value
                    break

            # 提取数量
            quantity_match = re.search(r'(\d+)\s*[个台件]', text)
            if quantity_match:
                params['quantity'] = int(quantity_match.group(1))

        return params

    def _extract_order_items(self, text: str) -> List[Dict]:
        """提取订单项（产品和数量）"""
        items = []

        # 尝试匹配 "产品名 数量" 模式
        for product_key, product_name in self.product_names.items():
            if product_key in text:
                # 查找数量
                pattern = f'{product_key}[^0-9]*?(\\d+)\\s*[个台件台]?'
                match = re.search(pattern, text)
                if match:
                    quantity = int(match.group(1))
                    items.append({
                        'product_name': product_name,
                        'quantity': quantity
                    })

        return items

    def get_task_description(self, task: Dict) -> str:
        """获取任务的可读描述"""
        task_type = task.get('task_type')
        params = task.get('params', {})

        descriptions = {
            'create_order': f"创建订单 - 客户: {params.get('customer_name', '未指定')}",
            'query_orders': '查询订单列表',
            'update_order_status': f"更新订单 #{params.get('order_id', '?')} 状态为 {params.get('status', '?')}",
            'query_inventory': '查询库存信息',
            'restock': f"补货 - {params.get('product_name', '未指定产品')}",
            'query_sales_report': '查询销售报表',
            'query_inventory_report': '查询库存报表',
        }

        return descriptions.get(task_type, '未知任务')

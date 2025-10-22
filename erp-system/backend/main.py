from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import os

from database import get_db, init_db, Product as DBProduct, Order as DBOrder, OrderItem as DBOrderItem
from models import (
    Product, ProductCreate, ProductUpdate,
    Order, OrderCreate, OrderUpdate,
    StockAlert, SalesReport, InventoryReport
)
from llm_agent import get_agent

app = FastAPI(title="ERP System API", version="1.0.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
def startup_event():
    init_db()


# ==================== 产品管理 API ====================

@app.get("/api/products", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取产品列表"""
    products = db.query(DBProduct).offset(skip).limit(limit).all()
    return products


@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取单个产品"""
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/api/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """创建新产品"""
    db_product = db.query(DBProduct).filter(DBProduct.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    db_product = DBProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/api/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """更新产品信息"""
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除产品"""
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


# ==================== 订单管理 API ====================

@app.get("/api/orders", response_model=List[Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取订单列表"""
    orders = db.query(DBOrder).offset(skip).limit(limit).all()
    return orders


@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取单个订单"""
    order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/api/orders", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """创建新订单"""
    from datetime import datetime

    # 生成訂單編號
    now = datetime.now()
    count = db.query(DBOrder).count() + 1
    order_number = f"ORD{now.year % 100:02d}{now.month:02d}{count:04d}"

    # 创建订单
    db_order = DBOrder(
        order_number=order_number,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,
        notes=order.notes
    )
    db.add(db_order)
    db.flush()

    total_amount = 0.0

    # 添加订单项
    for item in order.items:
        product = db.query(DBProduct).filter(DBProduct.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        if product.stock_quantity < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
            )

        subtotal = product.price * item.quantity
        db_item = DBOrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=subtotal
        )
        db.add(db_item)
        total_amount += subtotal

        # 更新库存
        product.stock_quantity -= item.quantity

    db_order.total_amount = total_amount
    db.commit()
    db.refresh(db_order)
    return db_order


@app.put("/api/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    """更新订单状态"""
    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status:
        # 如果訂單被取消，恢復庫存
        if order.status == "cancelled" and db_order.status not in ["cancelled", "completed"]:
            for item in db_order.items:
                item.product.stock_quantity += item.quantity

        # 如果訂單從pending變為processing，不做庫存變動（在創建時已扣除）
        # 如果訂單完成，也不做庫存變動

        db_order.status = order.status

    db.commit()
    db.refresh(db_order)
    return db_order


@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """删除订单"""
    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 如果订单未完成，恢复库存
    if db_order.status != "cancelled":
        for item in db_order.items:
            item.product.stock_quantity += item.quantity

    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}


# ==================== 库存管理 API ====================

@app.get("/api/inventory/alerts", response_model=List[StockAlert])
def get_stock_alerts(db: Session = Depends(get_db)):
    """获取库存预警"""
    products = db.query(DBProduct).all()
    alerts = []

    for product in products:
        if product.stock_quantity < product.min_stock_level:
            alerts.append(StockAlert(
                product_id=product.id,
                product_name=product.name,
                current_stock=product.stock_quantity,
                min_stock_level=product.min_stock_level,
                shortage=product.min_stock_level - product.stock_quantity
            ))

    return alerts


@app.post("/api/inventory/restock/{product_id}")
def restock_product(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """补货"""
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock_quantity += quantity
    db.commit()
    db.refresh(product)
    return {"message": f"Restocked {quantity} units", "new_stock": product.stock_quantity}


# ==================== 报表 API ====================

@app.get("/api/reports/sales", response_model=SalesReport)
def get_sales_report(db: Session = Depends(get_db)):
    """获取销售报表"""
    orders = db.query(DBOrder).all()

    total_orders = len(orders)
    completed_orders = len([o for o in orders if o.status == "completed"])
    pending_orders = len([o for o in orders if o.status == "pending"])
    cancelled_orders = len([o for o in orders if o.status == "cancelled"])
    total_revenue = sum(o.total_amount for o in orders if o.status == "completed")

    # 统计产品销量
    product_sales = {}
    for order in orders:
        if order.status == "completed":
            for item in order.items:
                if item.product_id not in product_sales:
                    product_sales[item.product_id] = {
                        "product_name": item.product.name,
                        "quantity": 0,
                        "revenue": 0.0
                    }
                product_sales[item.product_id]["quantity"] += item.quantity
                product_sales[item.product_id]["revenue"] += item.subtotal

    top_products = sorted(
        product_sales.values(),
        key=lambda x: x["revenue"],
        reverse=True
    )[:5]

    return SalesReport(
        total_orders=total_orders,
        total_revenue=total_revenue,
        completed_orders=completed_orders,
        pending_orders=pending_orders,
        cancelled_orders=cancelled_orders,
        top_products=top_products
    )


@app.get("/api/reports/inventory", response_model=InventoryReport)
def get_inventory_report(db: Session = Depends(get_db)):
    """获取库存报表"""
    products = db.query(DBProduct).all()

    total_products = len(products)
    total_stock_value = sum(p.price * p.stock_quantity for p in products)
    out_of_stock_count = len([p for p in products if p.stock_quantity == 0])

    low_stock_products = []
    for product in products:
        if product.stock_quantity < product.min_stock_level:
            low_stock_products.append(StockAlert(
                product_id=product.id,
                product_name=product.name,
                current_stock=product.stock_quantity,
                min_stock_level=product.min_stock_level,
                shortage=product.min_stock_level - product.stock_quantity
            ))

    return InventoryReport(
        total_products=total_products,
        total_stock_value=total_stock_value,
        low_stock_products=low_stock_products,
        out_of_stock_count=out_of_stock_count
    )


# ==================== AI Agent API ====================

class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/api/agent/chat", response_model=ChatResponse)
def chat_with_agent(chat_message: ChatMessage):
    """與 AI Agent 對話"""
    agent = get_agent()
    response = agent.chat(chat_message.message)
    return ChatResponse(response=response)


@app.post("/api/agent/reset")
def reset_agent():
    """重置 Agent 對話歷史"""
    agent = get_agent()
    agent.reset_conversation()
    return {"message": "對話歷史已重置"}


# ==================== 静态文件服务 ====================
# 注意：必须放在所有API路由之后，这样API路由会优先匹配
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

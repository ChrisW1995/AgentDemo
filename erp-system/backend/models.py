from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    min_stock_level: int = Field(ge=0, default=10)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int
    unit_price: float
    subtotal: float
    product: Optional[Product] = None

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_name: str


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: datetime
    status: str
    total_amount: float
    items: List[OrderItem] = []

    class Config:
        from_attributes = True


class StockAlert(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    min_stock_level: int
    shortage: int


class SalesReport(BaseModel):
    total_orders: int
    total_revenue: float
    completed_orders: int
    pending_orders: int
    cancelled_orders: int
    top_products: List[dict]


class InventoryReport(BaseModel):
    total_products: int
    total_stock_value: float
    low_stock_products: List[StockAlert]
    out_of_stock_count: int

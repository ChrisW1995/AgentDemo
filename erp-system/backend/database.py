from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./erp_demo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=10)

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, completed, cancelled
    total_amount = Column(Float, default=0.0)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


def init_db():
    Base.metadata.create_all(bind=engine)

    # 添加初始数据
    db = SessionLocal()

    # 检查是否已有数据
    if db.query(Product).count() == 0:
        initial_products = [
            Product(name="笔记本电脑", description="高性能办公笔记本", price=5999.00, stock_quantity=50, min_stock_level=10),
            Product(name="台式电脑", description="企业级台式电脑", price=4599.00, stock_quantity=30, min_stock_level=8),
            Product(name="显示器", description="27寸4K显示器", price=2199.00, stock_quantity=100, min_stock_level=20),
            Product(name="键盘", description="机械键盘", price=299.00, stock_quantity=200, min_stock_level=50),
            Product(name="鼠标", description="无线鼠标", price=149.00, stock_quantity=250, min_stock_level=50),
            Product(name="打印机", description="激光打印机", price=1899.00, stock_quantity=15, min_stock_level=5),
        ]
        db.add_all(initial_products)
        db.commit()

    db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

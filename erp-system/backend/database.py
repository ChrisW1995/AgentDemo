from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
import random

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
    sku = Column(String, unique=True, index=True)  # 產品編號
    category = Column(String, index=True)  # 產品類別
    description = Column(Text)
    price = Column(Float)
    cost = Column(Float)  # 成本價
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=10)
    supplier = Column(String)  # 供應商

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)  # 訂單編號
    customer_name = Column(String, index=True)
    customer_email = Column(String)
    customer_phone = Column(String)
    shipping_address = Column(Text)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, processing, completed, cancelled
    total_amount = Column(Float, default=0.0)
    notes = Column(Text)  # 備註

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)
    discount = Column(Float, default=0.0)  # 折扣

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


def init_db():
    Base.metadata.create_all(bind=engine)

    # 添加初始數據
    db = SessionLocal()

    # 檢查是否已有數據
    if db.query(Product).count() == 0:
        # 真實的產品數據 - 電腦及辦公用品類別
        initial_products = [
            # 筆記本電腦系列
            Product(
                name="Dell Latitude 5420 商務筆記本",
                sku="NB-DELL-5420",
                category="筆記本電腦",
                description="14吋 FHD, Intel i5-1135G7, 8GB RAM, 256GB SSD, Windows 11 Pro",
                price=7299.00,
                cost=5800.00,
                stock_quantity=45,
                min_stock_level=15,
                supplier="Dell 台灣"
            ),
            Product(
                name="HP EliteBook 840 G8",
                sku="NB-HP-840G8",
                category="筆記本電腦",
                description="14吋 FHD, Intel i7-1165G7, 16GB RAM, 512GB SSD, Windows 11 Pro",
                price=9899.00,
                cost=7900.00,
                stock_quantity=32,
                min_stock_level=10,
                supplier="HP 台灣"
            ),
            Product(
                name="Lenovo ThinkPad X1 Carbon Gen 9",
                sku="NB-LEN-X1C9",
                category="筆記本電腦",
                description="14吋 WQHD, Intel i7-1185G7, 16GB RAM, 1TB SSD, 碳纖維機身",
                price=12999.00,
                cost=10200.00,
                stock_quantity=18,
                min_stock_level=8,
                supplier="Lenovo 台灣"
            ),
            Product(
                name="ASUS VivoBook 15",
                sku="NB-ASUS-VB15",
                category="筆記本電腦",
                description="15.6吋 FHD, AMD Ryzen 5 5500U, 8GB RAM, 512GB SSD, 輕薄設計",
                price=5499.00,
                cost=4200.00,
                stock_quantity=65,
                min_stock_level=20,
                supplier="華碩台灣"
            ),

            # 台式電腦系列
            Product(
                name="Dell OptiPlex 7090 Tower",
                sku="PC-DELL-7090",
                category="台式電腦",
                description="Intel i7-11700, 16GB DDR4, 512GB SSD + 1TB HDD, Windows 11 Pro",
                price=8599.00,
                cost=6800.00,
                stock_quantity=28,
                min_stock_level=10,
                supplier="Dell 台灣"
            ),
            Product(
                name="HP ProDesk 600 G6 SFF",
                sku="PC-HP-600G6",
                category="台式電腦",
                description="Intel i5-10500, 8GB DDR4, 256GB SSD, 小機殼設計",
                price=6299.00,
                cost=4900.00,
                stock_quantity=38,
                min_stock_level=12,
                supplier="HP 台灣"
            ),
            Product(
                name="Lenovo ThinkCentre M90a AIO",
                sku="PC-LEN-M90A",
                category="一體機",
                description="23.8吋 FHD All-in-One, Intel i5-10500, 8GB RAM, 512GB SSD",
                price=7899.00,
                cost=6200.00,
                stock_quantity=22,
                min_stock_level=8,
                supplier="Lenovo 台灣"
            ),

            # 顯示器系列
            Product(
                name="Dell UltraSharp U2722DE",
                sku="MON-DELL-U27",
                category="顯示器",
                description="27吋 QHD IPS, USB-C, 高度可調, 防眩光",
                price=4599.00,
                cost=3500.00,
                stock_quantity=85,
                min_stock_level=25,
                supplier="Dell 台灣"
            ),
            Product(
                name="LG 27UP850-W 4K",
                sku="MON-LG-27UP",
                category="顯示器",
                description="27吋 4K UHD IPS, HDR10, USB-C 96W 供電",
                price=5299.00,
                cost=4100.00,
                stock_quantity=72,
                min_stock_level=20,
                supplier="LG 台灣"
            ),
            Product(
                name="ASUS ProArt PA247CV",
                sku="MON-ASUS-PA24",
                category="顯示器",
                description="23.8吋 FHD IPS, 100% sRGB, 專業色彩校準",
                price=3299.00,
                cost=2500.00,
                stock_quantity=95,
                min_stock_level=30,
                supplier="華碩台灣"
            ),
            Product(
                name="BenQ GW2485TC 護眼螢幕",
                sku="MON-BENQ-GW24",
                category="顯示器",
                description="24吋 FHD IPS, 低藍光不閃屏, 內建喇叭",
                price=2899.00,
                cost=2200.00,
                stock_quantity=110,
                min_stock_level=35,
                supplier="明基台灣"
            ),

            # 鍵盤系列
            Product(
                name="Logitech MX Keys 無線鍵盤",
                sku="KB-LOG-MXK",
                category="鍵盤",
                description="背光無線鍵盤, 智能感應, 多設備切換, 可充電",
                price=2499.00,
                cost=1800.00,
                stock_quantity=156,
                min_stock_level=50,
                supplier="羅技台灣"
            ),
            Product(
                name="Keychron K2 機械鍵盤",
                sku="KB-KEY-K2",
                category="鍵盤",
                description="無線/有線雙模, 青軸, RGB背光, Mac/Win兼容",
                price=1899.00,
                cost=1400.00,
                stock_quantity=188,
                min_stock_level=60,
                supplier="Keychron"
            ),
            Product(
                name="Microsoft 人體工學鍵盤",
                sku="KB-MS-ERGO",
                category="鍵盤",
                description="分離式設計, 掌托, 減輕手腕壓力",
                price=1599.00,
                cost=1200.00,
                stock_quantity=142,
                min_stock_level=45,
                supplier="微軟台灣"
            ),
            Product(
                name="Dell KB216 有線鍵盤",
                sku="KB-DELL-216",
                category="鍵盤",
                description="標準薄膜鍵盤, 防潑濺設計, 靜音按鍵",
                price=399.00,
                cost=280.00,
                stock_quantity=245,
                min_stock_level=80,
                supplier="Dell 台灣"
            ),

            # 滑鼠系列
            Product(
                name="Logitech MX Master 3S",
                sku="MS-LOG-MX3S",
                category="滑鼠",
                description="無線滑鼠, 8K DPI, 靜音點擊, 快速充電, 多設備",
                price=1999.00,
                cost=1500.00,
                stock_quantity=198,
                min_stock_level=65,
                supplier="羅技台灣"
            ),
            Product(
                name="Microsoft Surface 精準滑鼠",
                sku="MS-MS-SURF",
                category="滑鼠",
                description="藍牙無線, 三設備切換, 符合人體工學",
                price=1299.00,
                cost=950.00,
                stock_quantity=175,
                min_stock_level=55,
                supplier="微軟台灣"
            ),
            Product(
                name="HP X3000 無線滑鼠",
                sku="MS-HP-X3000",
                category="滑鼠",
                description="2.4GHz 無線, 1200 DPI, 節能設計",
                price=299.00,
                cost=200.00,
                stock_quantity=285,
                min_stock_level=95,
                supplier="HP 台灣"
            ),

            # 打印機系列
            Product(
                name="HP LaserJet Pro M404n",
                sku="PR-HP-M404",
                category="打印機",
                description="黑白雷射印表機, 38ppm, 網路列印, 雙面列印",
                price=6599.00,
                cost=5100.00,
                stock_quantity=24,
                min_stock_level=8,
                supplier="HP 台灣"
            ),
            Product(
                name="Canon PIXMA G6070",
                sku="PR-CAN-G6070",
                category="打印機",
                description="大供墨多功能事務機, 彩色列印/掃描/影印, WiFi",
                price=5299.00,
                cost=4000.00,
                stock_quantity=18,
                min_stock_level=6,
                supplier="Canon 台灣"
            ),
            Product(
                name="Epson WorkForce WF-2950",
                sku="PR-EP-WF2950",
                category="打印機",
                description="四合一彩色噴墨, WiFi Direct, 自動雙面列印",
                price=3899.00,
                cost=2900.00,
                stock_quantity=32,
                min_stock_level=10,
                supplier="Epson 台灣"
            ),
            Product(
                name="Brother DCP-L2550DW",
                sku="PR-BR-L2550",
                category="打印機",
                description="黑白雷射多功能複合機, 34ppm, 雙面列印掃描",
                price=4799.00,
                cost=3600.00,
                stock_quantity=21,
                min_stock_level=7,
                supplier="Brother 台灣"
            ),

            # 網路設備
            Product(
                name="TP-Link Archer AX73 路由器",
                sku="NET-TPL-AX73",
                category="網路設備",
                description="Wi-Fi 6 雙頻路由器, AX5400, 5 GHz 4804Mbps",
                price=2599.00,
                cost=1900.00,
                stock_quantity=68,
                min_stock_level=22,
                supplier="TP-Link 台灣"
            ),
            Product(
                name="ASUS RT-AX86U Pro",
                sku="NET-ASUS-AX86",
                category="網路設備",
                description="Wi-Fi 6 電競路由器, AX5700, AiMesh, 2.5G 網口",
                price=5299.00,
                cost=4100.00,
                stock_quantity=42,
                min_stock_level=15,
                supplier="華碩台灣"
            ),

            # 辦公配件
            Product(
                name="WD My Passport 2TB 外接硬碟",
                sku="ACC-WD-PP2TB",
                category="儲存設備",
                description="2.5吋 USB 3.2, 密碼保護, 自動備份軟體",
                price=1899.00,
                cost=1400.00,
                stock_quantity=135,
                min_stock_level=45,
                supplier="威騰電子"
            ),
            Product(
                name="Seagate Backup Plus 4TB",
                sku="ACC-SG-BP4TB",
                category="儲存設備",
                description="桌上型外接硬碟, USB 3.0, 200GB 雲端儲存",
                price=2899.00,
                cost=2200.00,
                stock_quantity=98,
                min_stock_level=32,
                supplier="希捷科技"
            ),
            Product(
                name="Logitech C920 HD Pro 網路攝影機",
                sku="ACC-LOG-C920",
                category="視訊設備",
                description="1080p Full HD, 自動對焦, 立體聲音訊, 視訊會議",
                price=1599.00,
                cost=1200.00,
                stock_quantity=88,
                min_stock_level=30,
                supplier="羅技台灣"
            ),
            Product(
                name="APC BX1000M UPS 不斷電系統",
                sku="ACC-APC-BX1000",
                category="電源設備",
                description="1000VA/600W, 6個插座, AVR穩壓, LCD顯示",
                price=3299.00,
                cost=2500.00,
                stock_quantity=45,
                min_stock_level=15,
                supplier="APC 台灣"
            ),
        ]
        db.add_all(initial_products)
        db.commit()

        # 創建真實的客戶訂單數據
        customers = [
            {
                "name": "台北科技股份有限公司",
                "email": "purchasing@taipeitech.com.tw",
                "phone": "02-2712-3456",
                "address": "台北市信義區信義路五段7號15樓"
            },
            {
                "name": "新竹軟體科技有限公司",
                "email": "admin@hcsoftware.com.tw",
                "phone": "03-5678-9012",
                "address": "新竹市東區光復路二段101號8樓"
            },
            {
                "name": "台中製造工業股份有限公司",
                "email": "order@tcmanufacturing.com.tw",
                "phone": "04-2358-7890",
                "address": "台中市西屯區工業區一路88號"
            },
            {
                "name": "高雄貿易企業有限公司",
                "email": "info@khtrade.com.tw",
                "phone": "07-3456-7890",
                "address": "高雄市前鎮區中山四路100號3樓"
            },
            {
                "name": "桃園電子科技股份有限公司",
                "email": "contact@tyelectronics.com.tw",
                "phone": "03-3345-6789",
                "address": "桃園市中壢區中山東路四段525號"
            },
            {
                "name": "台南精密工業有限公司",
                "email": "sales@tnprecision.com.tw",
                "phone": "06-2789-1234",
                "address": "台南市永康區中正南路539號"
            },
        ]

        # 創建過去三個月的訂單
        products_list = db.query(Product).all()
        base_date = datetime.now() - timedelta(days=90)

        order_statuses = ["completed", "completed", "completed", "completed", "processing", "pending"]

        for i in range(25):  # 創建25筆訂單
            customer = random.choice(customers)
            order_date = base_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
            status = random.choice(order_statuses)

            order_num = f"ORD{(base_date.year % 100):02d}{order_date.month:02d}{(i+1):04d}"

            order = Order(
                order_number=order_num,
                customer_name=customer["name"],
                customer_email=customer["email"],
                customer_phone=customer["phone"],
                shipping_address=customer["address"],
                order_date=order_date,
                status=status,
                notes=f"{'批量採購' if random.random() > 0.7 else '常規訂單'}"
            )
            db.add(order)
            db.flush()

            # 每個訂單添加1-5個商品
            num_items = random.randint(1, 5)
            selected_products = random.sample(products_list, num_items)
            total = 0.0

            for product in selected_products:
                quantity = random.randint(1, 15)
                discount = round(random.choice([0, 0, 0, 0.05, 0.1]), 2)  # 80% 沒折扣
                unit_price = product.price
                subtotal = round(unit_price * quantity * (1 - discount), 2)

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal,
                    discount=discount
                )
                db.add(order_item)
                total += subtotal

                # 如果訂單已完成，減少庫存
                if status == "completed":
                    product.stock_quantity -= quantity

            order.total_amount = total

        db.commit()

    db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

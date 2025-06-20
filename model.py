from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    orders = relationship('Order', back_populates='customer')

class ShopItemCategory(Base):
    __tablename__ = 'shop_item_categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    items = relationship('ShopItem', back_populates='category')

class ShopItem(Base):
    __tablename__ = 'shop_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('shop_item_categories.id'))
    category = relationship('ShopItemCategory', back_populates='items')
    order_items = relationship('OrderItem', back_populates='shop_item')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    shop_item_id = Column(Integer, ForeignKey('shop_items.id'))
    quantity = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='items')
    shop_item = relationship('ShopItem', back_populates='order_items')

def init_db(database_url: str):
    """
    Initialize the database and create all tables.
    :param database_url: SQLAlchemy database URL (e.g., 'sqlite:///./test.db')
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
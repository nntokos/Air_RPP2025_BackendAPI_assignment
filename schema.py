# schema.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

def get_engine(database_url: str):
    """Create and return a SQLAlchemy engine."""
    return create_engine(database_url, connect_args={"check_same_thread": False})

def init_db(database_url: str):
    """Initialize the database and create all tables."""
    engine = get_engine(database_url)
    Base.metadata.create_all(bind=engine)
    return engine

def get_session(engine):
    """Return a session factory bound to the given engine."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_test_data(session):
    """Insert initial test data into the database."""
    from model import Customer, ShopItemCategory, ShopItem, Order, OrderItem

    # Create customers
    customer1 = Customer(name="Alice Smith", email="alice@example.com")
    customer2 = Customer(name="Bob Johnson", email="bob@example.com")

    # Create categories
    cat1 = ShopItemCategory(name="Books")
    cat2 = ShopItemCategory(name="Electronics")

    # Create shop items
    item1 = ShopItem(name="Python 101", price=29.99, category=cat1)
    item2 = ShopItem(name="Laptop", price=999.99, category=cat2)
    item3 = ShopItem(name="Headphones", price=199.99, category=cat2)

    # Create orders
    order1 = Order(customer=customer1)
    order2 = Order(customer=customer2)

    # Create order items
    order_item1 = OrderItem(order=order1, shop_item=item1, quantity=2)
    order_item2 = OrderItem(order=order1, shop_item=item2, quantity=1)
    order_item3 = OrderItem(order=order2, shop_item=item3, quantity=3)

    session.add_all([
        customer1, customer2,
        cat1, cat2,
        item1, item2, item3,
        order1, order2,
        order_item1, order_item2, order_item3
    ])
    session.commit()

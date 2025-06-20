from sqlalchemy.orm import Session
from model import Customer, ShopItemCategory, ShopItem, Order

# --- Customer CRUD ---
def create_customer(db: Session, name: str, email: str):
    customer = Customer(name=name, email=email)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def update_customer(db: Session, customer_id: int, name: str = None, email: str = None):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    if name:
        customer.name = name
    if email:
        customer.email = email
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    db.delete(customer)
    db.commit()
    return customer

# --- ShopItemCategory CRUD ---
def create_category(db: Session, name: str):
    category = ShopItemCategory(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, category_id: int):
    return db.query(ShopItemCategory).filter(ShopItemCategory.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ShopItemCategory).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, name: str = None):
    category = db.query(ShopItemCategory).filter(ShopItemCategory.id == category_id).first()
    if not category:
        return None
    if name:
        category.name = name
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(ShopItemCategory).filter(ShopItemCategory.id == category_id).first()
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category

# --- ShopItem CRUD ---
def create_shop_item(db: Session, name: str, price: float, category_id: int):
    item = ShopItem(name=name, price=price, category_id=category_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_shop_item(db: Session, item_id: int):
    return db.query(ShopItem).filter(ShopItem.id == item_id).first()

def get_shop_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ShopItem).offset(skip).limit(limit).all()

def update_shop_item(db: Session, item_id: int, name: str = None, price: float = None, category_id: int = None):
    item = db.query(ShopItem).filter(ShopItem.id == item_id).first()
    if not item:
        return None
    if name:
        item.name = name
    if price is not None:
        item.price = price
    if category_id is not None:
        item.category_id = category_id
    db.commit()
    db.refresh(item)
    return item

def delete_shop_item(db: Session, item_id: int):
    item = db.query(ShopItem).filter(ShopItem.id == item_id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item

# --- Order CRUD ---
def create_order(db: Session, customer_id: int):
    order = Order(customer_id=customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, customer_id: int = None):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    if customer_id is not None:
        order.customer_id = customer_id
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    db.delete(order)
    db.commit()
    return order

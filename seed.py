from sqlalchemy.orm import Session
from model import Customer, ShopItemCategory, ShopItem, Order
from schema import get_engine, get_session, init_db

DATABASE_URL = "sqlite:///./test.db"

def seed_data(db: Session):
    # Add initial customers
    if not db.query(Customer).first():
        customers = [
            Customer(name="Alice", email="alice@example.com"),
            Customer(name="Bob", email="bob@example.com"),
            Customer(name="Charlie", email="charlie@example.com"),
            Customer(name="Diana", email="diana@example.com"),
        ]
        db.add_all(customers)
        db.commit()
    else:
        customers = db.query(Customer).all()

    # Add initial categories
    if not db.query(ShopItemCategory).first():
        categories = [
            ShopItemCategory(name="Books"),
            ShopItemCategory(name="Electronics"),
            ShopItemCategory(name="Clothing"),
            ShopItemCategory(name="Toys"),
        ]
        db.add_all(categories)
        db.commit()
    else:
        categories = db.query(ShopItemCategory).all()

    # Add initial shop items
    if not db.query(ShopItem).first():
        books_cat = next((c for c in categories if c.name == "Books"), None)
        electronics_cat = next((c for c in categories if c.name == "Electronics"), None)
        clothing_cat = next((c for c in categories if c.name == "Clothing"), None)
        toys_cat = next((c for c in categories if c.name == "Toys"), None)
        items = [
            ShopItem(name="The Great Gatsby", price=10.99, category_id=books_cat.id),
            ShopItem(name="Python Programming", price=29.99, category_id=books_cat.id),
            ShopItem(name="Smartphone", price=199.99, category_id=electronics_cat.id),
            ShopItem(name="Headphones", price=49.99, category_id=electronics_cat.id),
            ShopItem(name="T-shirt", price=15.99, category_id=clothing_cat.id),
            ShopItem(name="Jeans", price=39.99, category_id=clothing_cat.id),
            ShopItem(name="Lego Set", price=59.99, category_id=toys_cat.id),
            ShopItem(name="Action Figure", price=12.99, category_id=toys_cat.id),
        ]
        db.add_all(items)
        db.commit()
    else:
        items = db.query(ShopItem).all()

    # Add initial orders
    if hasattr(Order, "customer_id") and not db.query(Order).first():
        # Create one order per customer
        for customer in db.query(Customer).all():
            order = Order(customer_id=customer.id)
            db.add(order)
        db.commit()

if __name__ == "__main__":
    engine = get_engine(DATABASE_URL)
    init_db(DATABASE_URL)
    SessionLocal = get_session(engine)
    db = SessionLocal()
    seed_data(db)
    db.close()
    print("Database seeded successfully.")

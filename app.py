from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import get_engine, get_session, init_db
import crud
from model import Customer, ShopItemCategory, ShopItem, Order
from schemas import (
    CustomerCreate, CustomerUpdate, CustomerOut,
    ShopItemCategoryCreate, ShopItemCategoryUpdate, ShopItemCategoryOut,
    ShopItemCreate, ShopItemUpdate, ShopItemOut,
    OrderCreate, OrderUpdate, OrderOut
)
from typing import List

DATABASE_URL = "sqlite:///./test.db"
engine = get_engine(DATABASE_URL)
init_db(DATABASE_URL)
SessionLocal = get_session(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Customer Endpoints ---

@app.post("/customers/", response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, name=customer.name, email=customer.email)

@app.get("/customers/", response_model=List[CustomerOut])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.get("/customers/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, name=customer.name, email=customer.email)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.delete("/customers/{customer_id}", response_model=CustomerOut)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# --- ShopItemCategory Endpoints ---

@app.post("/categories/", response_model=ShopItemCategoryOut)
def create_category(category: ShopItemCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, name=category.name)

@app.get("/categories/", response_model=List[ShopItemCategoryOut])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

@app.get("/categories/{category_id}", response_model=ShopItemCategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.put("/categories/{category_id}", response_model=ShopItemCategoryOut)
def update_category(category_id: int, category: ShopItemCategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id, name=category.name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/categories/{category_id}", response_model=ShopItemCategoryOut)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# --- ShopItem Endpoints ---

@app.post("/items/", response_model=ShopItemOut)
def create_shop_item(item: ShopItemCreate, db: Session = Depends(get_db)):
    return crud.create_shop_item(db, name=item.name, price=item.price, category_id=item.category_id)

@app.get("/items/", response_model=List[ShopItemOut])
def read_shop_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_shop_items(db, skip=skip, limit=limit)

@app.get("/items/{item_id}", response_model=ShopItemOut)
def read_shop_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_shop_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ShopItemOut)
def update_shop_item(item_id: int, item: ShopItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_shop_item(db, item_id, name=item.name, price=item.price, category_id=item.category_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=ShopItemOut)
def delete_shop_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_shop_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item

# --- Order Endpoints ---

@app.post("/orders/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, customer_id=order.customer_id)

@app.get("/orders/", response_model=List[OrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id, customer_id=order.customer_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.delete("/orders/{order_id}", response_model=OrderOut)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5001, reload=True)

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# --- Customer Tests ---

def test_create_customer():
    response = client.post("/customers/", json={"name": "Test User", "email": "testuser@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_read_customers():
    response = client.get("/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_customer():
    # Create a customer first
    post = client.post("/customers/", json={"name": "Read User", "email": "readuser@example.com"})
    cid = post.json()["id"]
    response = client.get(f"/customers/{cid}")
    assert response.status_code == 200
    assert response.json()["id"] == cid

def test_update_customer():
    post = client.post("/customers/", json={"name": "Update User", "email": "updateuser@example.com"})
    cid = post.json()["id"]
    response = client.put(f"/customers/{cid}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_customer():
    post = client.post("/customers/", json={"name": "Delete User", "email": "deleteuser@example.com"})
    cid = post.json()["id"]
    response = client.delete(f"/customers/{cid}")
    assert response.status_code == 200
    # Ensure deleted
    get = client.get(f"/customers/{cid}")
    assert get.status_code == 404

# --- ShopItemCategory Tests ---

def test_create_category():
    response = client.post("/categories/", json={"name": "Test Category"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data

def test_read_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_category():
    post = client.post("/categories/", json={"name": "Read Category"})
    cid = post.json()["id"]
    response = client.get(f"/categories/{cid}")
    assert response.status_code == 200
    assert response.json()["id"] == cid

def test_update_category():
    post = client.post("/categories/", json={"name": "Update Category"})
    cid = post.json()["id"]
    response = client.put(f"/categories/{cid}", json={"name": "Updated Category"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Category"

def test_delete_category():
    post = client.post("/categories/", json={"name": "Delete Category"})
    cid = post.json()["id"]
    response = client.delete(f"/categories/{cid}")
    assert response.status_code == 200
    get = client.get(f"/categories/{cid}")
    assert get.status_code == 404

# --- ShopItem Tests ---

def test_create_shop_item():
    # Need a category first
    cat = client.post("/categories/", json={"name": "ItemCat"}).json()
    response = client.post("/items/", json={"name": "Test Item", "price": 9.99, "category_id": cat["id"]})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 9.99
    assert data["category_id"] == cat["id"]
    assert "id" in data

def test_read_shop_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_shop_item():
    cat = client.post("/categories/", json={"name": "ReadItemCat"}).json()
    post = client.post("/items/", json={"name": "Read Item", "price": 5.55, "category_id": cat["id"]})
    iid = post.json()["id"]
    response = client.get(f"/items/{iid}")
    assert response.status_code == 200
    assert response.json()["id"] == iid

def test_update_shop_item():
    cat = client.post("/categories/", json={"name": "UpdateItemCat"}).json()
    post = client.post("/items/", json={"name": "Update Item", "price": 1.23, "category_id": cat["id"]})
    iid = post.json()["id"]
    response = client.put(f"/items/{iid}", json={"name": "Updated Item", "price": 2.34})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"
    assert response.json()["price"] == 2.34

def test_delete_shop_item():
    cat = client.post("/categories/", json={"name": "DeleteItemCat"}).json()
    post = client.post("/items/", json={"name": "Delete Item", "price": 7.77, "category_id": cat["id"]})
    iid = post.json()["id"]
    response = client.delete(f"/items/{iid}")
    assert response.status_code == 200
    get = client.get(f"/items/{iid}")
    assert get.status_code == 404

# --- Order Tests ---

def test_create_order():
    cust = client.post("/customers/", json={"name": "Order User", "email": "orderuser@example.com"}).json()
    response = client.post("/orders/", json={"customer_id": cust["id"]})
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == cust["id"]
    assert "id" in data

def test_read_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_order():
    cust = client.post("/customers/", json={"name": "ReadOrderUser", "email": "readorderuser@example.com"}).json()
    post = client.post("/orders/", json={"customer_id": cust["id"]})
    oid = post.json()["id"]
    response = client.get(f"/orders/{oid}")
    assert response.status_code == 200
    assert response.json()["id"] == oid

def test_update_order():
    cust1 = client.post("/customers/", json={"name": "OrderUser1", "email": "orderuser1@example.com"}).json()
    cust2 = client.post("/customers/", json={"name": "OrderUser2", "email": "orderuser2@example.com"}).json()
    post = client.post("/orders/", json={"customer_id": cust1["id"]})
    oid = post.json()["id"]
    response = client.put(f"/orders/{oid}", json={"customer_id": cust2["id"]})
    assert response.status_code == 200
    assert response.json()["customer_id"] == cust2["id"]

def test_delete_order():
    cust = client.post("/customers/", json={"name": "DeleteOrderUser", "email": "deleteorderuser@example.com"}).json()
    post = client.post("/orders/", json={"customer_id": cust["id"]})
    oid = post.json()["id"]
    response = client.delete(f"/orders/{oid}")
    assert response.status_code == 200
    get = client.get(f"/orders/{oid}")
    assert get.status_code == 404

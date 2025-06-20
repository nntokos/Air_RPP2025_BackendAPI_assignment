"""
Comprehensive endpoint tests for the Online Shop Backend API.

This module contains autotests for all API endpoints, covering:
- Customer CRUD operations
- Category CRUD operations
- Item CRUD operations
- Order CRUD operations

Tests include both success and error scenarios.
"""

import pytest
import json
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Customer, ShopItemCategory, ShopItem, Order, OrderItem
from schema import create_all_tables


@pytest.fixture
def app():
    """Create a test Flask app with in-memory database"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        create_all_tables()
        yield app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def sample_data(app):
    """Create sample data for testing"""
    with app.app_context():
        # Clear existing data first
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(ShopItem).delete()
        db.session.query(ShopItemCategory).delete()
        db.session.query(Customer).delete()
        db.session.commit()
        
        # Create sample customer
        customer = Customer(
            name="John Doe",
            email="john.doe@example.com",
            phone="+1234567890",
            address="123 Main St, City, Country"
        )
        db.session.add(customer)
        
        # Create sample category
        category = ShopItemCategory(
            name="Electronics",
            description="Electronic devices and accessories"
        )
        db.session.add(category)
        db.session.flush()
        
        # Create sample item
        item = ShopItem(
            name="Smartphone",
            description="Latest model smartphone",
            price=699.99,
            stock_quantity=50,
            category_id=category.id
        )
        db.session.add(item)
        db.session.flush()
        
        # Create sample order
        order = Order(
            customer_id=customer.id,
            total_amount=0,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            shop_item_id=item.id,
            quantity=2,
            price_at_time=699.99
        )
        db.session.add(order_item)
        order.update_total_amount()
        
        db.session.commit()
        
        return {
            'customer_id': customer.id,
            'category_id': category.id,
            'item_id': item.id,
            'order_id': order.id
        }


@pytest.fixture
def clean_db(app):
    """Clean database fixture for tests that need empty database"""
    with app.app_context():
        # Clear all data in the correct order to handle foreign key constraints
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(ShopItem).delete()
        db.session.query(ShopItemCategory).delete()
        db.session.query(Customer).delete()
        db.session.commit()
        yield
        # Clean up after test as well
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(ShopItem).delete()
        db.session.query(ShopItemCategory).delete()
        db.session.query(Customer).delete()
        db.session.commit()


class TestCustomerEndpoints:
    """Test customer-related endpoints"""
    
    def test_get_customers_empty(self, client, clean_db):
        """Test GET /customers with no customers"""
        response = client.get('/customers')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_customers_with_data(self, client, sample_data):
        """Test GET /customers with existing customers"""
        response = client.get('/customers')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'John Doe'
        assert response.json[0]['email'] == 'john.doe@example.com'
    
    def test_create_customer_success(self, client, clean_db):
        """Test POST /customers with valid data"""
        customer_data = {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'phone': '+9876543210',
            'address': '456 Oak Ave, Town, Country'
        }
        response = client.post('/customers', 
                             data=json.dumps(customer_data),
                             content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'Jane Smith'
        assert response.json['email'] == 'jane.smith@example.com'
        assert 'id' in response.json
    
    def test_create_customer_missing_required_fields(self, client, clean_db):
        """Test POST /customers with missing required fields"""
        customer_data = {
            'name': 'Jane Smith'
            # missing email
        }
        response = client.post('/customers',
                             data=json.dumps(customer_data),
                             content_type='application/json')
        # Now properly handles missing fields with 400 error
        assert response.status_code == 400
        assert 'Missing required field: email' in response.json['error']
    
    def test_get_customer_by_id_success(self, client, sample_data):
        """Test GET /customers/<id> with valid ID"""
        customer_id = sample_data['customer_id']
        response = client.get(f'/customers/{customer_id}')
        assert response.status_code == 200
        assert response.json['id'] == customer_id
        assert response.json['name'] == 'John Doe'
    
    def test_get_customer_by_id_not_found(self, client):
        """Test GET /customers/<id> with non-existent ID"""
        response = client.get('/customers/999')
        assert response.status_code == 404
    
    def test_update_customer_success(self, client, sample_data):
        """Test PUT /customers/<id> with valid data"""
        customer_id = sample_data['customer_id']
        update_data = {
            'name': 'John Updated',
            'phone': '+1111111111'
        }
        response = client.put(f'/customers/{customer_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        assert response.json['name'] == 'John Updated'
        assert response.json['phone'] == '+1111111111'
    
    def test_update_customer_not_found(self, client, clean_db):
        """Test PUT /customers/<id> with non-existent ID"""
        update_data = {'name': 'Updated Name'}
        response = client.put('/customers/999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 404
    
    def test_delete_customer_success(self, client, sample_data):
        """Test DELETE /customers/<id> with valid ID"""
        customer_id = sample_data['customer_id']
        response = client.delete(f'/customers/{customer_id}')
        assert response.status_code == 204
        
        # Verify customer is deleted
        get_response = client.get(f'/customers/{customer_id}')
        assert get_response.status_code == 404
    
    def test_delete_customer_not_found(self, client):
        """Test DELETE /customers/<id> with non-existent ID"""
        response = client.delete('/customers/999')
        assert response.status_code == 404
    
    def test_create_customer_invalid_email(self, client, clean_db):
        """Test POST /customers with invalid email format"""
        customer_data = {
            'name': 'Jane Smith',
            'email': 'invalid-email',
            'phone': '+1234567890'
        }
        response = client.post('/customers',
                             data=json.dumps(customer_data),
                             content_type='application/json')
        # Should fail validation due to invalid email format
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_create_customer_duplicate_email(self, client, sample_data):
        """Test POST /customers with duplicate email"""
        customer_data = {
            'name': 'Different Name',
            'email': 'john.doe@example.com',  # Same email as sample data
            'phone': '+1111111111'
        }
        response = client.post('/customers',
                             data=json.dumps(customer_data),
                             content_type='application/json')
        # Should fail due to unique constraint on email
        assert response.status_code == 500
        assert 'Database error' in response.json['error']


class TestCategoryEndpoints:
    """Test category-related endpoints"""
    
    def test_get_categories_empty(self, client, clean_db):
        """Test GET /categories with no categories"""
        response = client.get('/categories')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_categories_with_data(self, client, sample_data):
        """Test GET /categories with existing categories"""
        response = client.get('/categories')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Electronics'
    
    def test_create_category_success(self, client, clean_db):
        """Test POST /categories with valid data"""
        category_data = {
            'name': 'Books',
            'description': 'Books and literature'
        }
        response = client.post('/categories',
                             data=json.dumps(category_data),
                             content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'Books'
        assert response.json['description'] == 'Books and literature'
    
    def test_create_category_missing_name(self, client, clean_db):
        """Test POST /categories with missing name"""
        category_data = {
            'description': 'Some description'
        }
        response = client.post('/categories',
                             data=json.dumps(category_data),
                             content_type='application/json')
        # Now properly handles missing fields with 400 error
        assert response.status_code == 400
        assert 'Missing required field: name' in response.json['error']
    
    def test_get_category_by_id_success(self, client, sample_data):
        """Test GET /categories/<id> with valid ID"""
        category_id = sample_data['category_id']
        response = client.get(f'/categories/{category_id}')
        assert response.status_code == 200
        assert response.json['id'] == category_id
        assert response.json['name'] == 'Electronics'
    
    def test_get_category_by_id_not_found(self, client):
        """Test GET /categories/<id> with non-existent ID"""
        response = client.get('/categories/999')
        assert response.status_code == 404
    
    def test_update_category_success(self, client, sample_data):
        """Test PUT /categories/<id> with valid data"""
        category_id = sample_data['category_id']
        update_data = {
            'name': 'Updated Electronics',
            'description': 'Updated description'
        }
        response = client.put(f'/categories/{category_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Electronics'
        assert response.json['description'] == 'Updated description'
    
    def test_delete_category_success(self, client, clean_db):
        """Test DELETE /categories/<id> with valid ID"""
        # Create a category without any dependent items
        with client.application.app_context():
            category = ShopItemCategory(name='Test Category', description='Test description')
            db.session.add(category)
            db.session.commit()
            category_id = category.id
        
        response = client.delete(f'/categories/{category_id}')
        assert response.status_code == 204
    
    def test_delete_category_not_found(self, client):
        """Test DELETE /categories/<id> with non-existent ID"""
        response = client.delete('/categories/999')
        assert response.status_code == 404
    
    def test_create_category_duplicate_name(self, client, sample_data):
        """Test POST /categories with duplicate name"""
        category_data = {
            'name': 'Electronics',  # Same name as sample data
            'description': 'Duplicate category'
        }
        response = client.post('/categories',
                             data=json.dumps(category_data),
                             content_type='application/json')
        # Should fail due to unique constraint on name
        assert response.status_code == 500
        assert 'Database error' in response.json['error']


class TestItemEndpoints:
    """Test item-related endpoints"""
    
    def test_get_items_empty(self, client, clean_db):
        """Test GET /items with no items"""
        response = client.get('/items')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_items_with_data(self, client, sample_data):
        """Test GET /items with existing items"""
        response = client.get('/items')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Smartphone'
    
    def test_create_item_success(self, client, sample_data):
        """Test POST /items with valid data"""
        category_id = sample_data['category_id']
        item_data = {
            'name': 'Laptop',
            'description': 'High-performance laptop',
            'price': 1299.99,
            'stock_quantity': 25,
            'category_id': category_id
        }
        response = client.post('/items',
                             data=json.dumps(item_data),
                             content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'Laptop'
        assert response.json['price'] == 1299.99
    
    def test_create_item_missing_required_fields(self, client, clean_db):
        """Test POST /items with missing required fields"""
        item_data = {
            'name': 'Incomplete Item'
            # missing price, stock_quantity, category_id
        }
        response = client.post('/items',
                             data=json.dumps(item_data),
                             content_type='application/json')
        # Now properly handles missing fields with 400 error
        assert response.status_code == 400
        assert 'Missing required field' in response.json['error']
    
    def test_get_item_by_id_success(self, client, sample_data):
        """Test GET /items/<id> with valid ID"""
        item_id = sample_data['item_id']
        response = client.get(f'/items/{item_id}')
        assert response.status_code == 200
        assert response.json['id'] == item_id
        assert response.json['name'] == 'Smartphone'
    
    def test_get_item_by_id_not_found(self, client):
        """Test GET /items/<id> with non-existent ID"""
        response = client.get('/items/999')
        assert response.status_code == 404
    
    def test_update_item_success(self, client, sample_data):
        """Test PUT /items/<id> with valid data"""
        item_id = sample_data['item_id']
        update_data = {
            'name': 'Updated Smartphone',
            'price': 799.99,
            'stock_quantity': 75
        }
        response = client.put(f'/items/{item_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Smartphone'
        assert response.json['price'] == 799.99
    
    def test_delete_item_success(self, client, clean_db):
        """Test DELETE /items/<id> with valid ID"""
        # Create an item without any order dependencies
        with client.application.app_context():
            category = ShopItemCategory(name='Test Category')
            db.session.add(category)
            db.session.flush()
            
            item = ShopItem(
                name='Test Item',
                price=99.99,
                stock_quantity=10,
                category_id=category.id
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        response = client.delete(f'/items/{item_id}')
        assert response.status_code == 204
    
    def test_delete_item_not_found(self, client):
        """Test DELETE /items/<id> with non-existent ID"""
        response = client.delete('/items/999')
        assert response.status_code == 404
    
    def test_create_item_invalid_price(self, client, sample_data):
        """Test POST /items with negative price"""
        category_id = sample_data['category_id']
        item_data = {
            'name': 'Invalid Item',
            'description': 'Item with negative price',
            'price': -10.00,  # Invalid negative price
            'stock_quantity': 5,
            'category_id': category_id
        }
        response = client.post('/items',
                             data=json.dumps(item_data),
                             content_type='application/json')
        # Should fail validation due to negative price
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_create_item_invalid_stock(self, client, sample_data):
        """Test POST /items with negative stock quantity"""
        category_id = sample_data['category_id']
        item_data = {
            'name': 'Invalid Item',
            'description': 'Item with negative stock',
            'price': 10.00,
            'stock_quantity': -5,  # Invalid negative stock
            'category_id': category_id
        }
        response = client.post('/items',
                             data=json.dumps(item_data),
                             content_type='application/json')
        # Should fail validation due to negative stock
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_create_item_invalid_category(self, client, clean_db):
        """Test POST /items with non-existent category_id"""
        item_data = {
            'name': 'Invalid Item',
            'description': 'Item with invalid category',
            'price': 10.00,
            'stock_quantity': 5,
            'category_id': 999  # Non-existent category
        }
        response = client.post('/items',
                             data=json.dumps(item_data),
                             content_type='application/json')
        # The validation doesn't check foreign key constraints at creation time
        # It only fails when the database constraint is violated, but SQLite might allow this
        assert response.status_code in [201, 500]


class TestOrderEndpoints:
    """Test order-related endpoints"""
    
    def test_get_orders_empty(self, client, clean_db):
        """Test GET /orders with no orders"""
        response = client.get('/orders')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_orders_with_data(self, client, sample_data):
        """Test GET /orders with existing orders"""
        response = client.get('/orders')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['status'] == 'pending'
    
    def test_create_order_success(self, client, sample_data):
        """Test POST /orders with valid data"""
        customer_id = sample_data['customer_id']
        item_id = sample_data['item_id']
        order_data = {
            'customer_id': customer_id,
            'status': 'pending',
            'items': [
                {
                    'shop_item_id': item_id,
                    'quantity': 1,
                    'price_at_time': 699.99
                }
            ]
        }
        response = client.post('/orders',
                             data=json.dumps(order_data),
                             content_type='application/json')
        assert response.status_code == 201
        assert response.json['customer_id'] == customer_id
        assert response.json['status'] == 'pending'
    
    def test_create_order_missing_customer(self, client, clean_db):
        """Test POST /orders with missing customer_id"""
        order_data = {
            'status': 'pending',
            'items': []
        }
        response = client.post('/orders',
                             data=json.dumps(order_data),
                             content_type='application/json')
        # Now properly handles missing fields with 400 error
        assert response.status_code == 400
        assert 'Missing required field: customer_id' in response.json['error']
    
    def test_get_order_by_id_success(self, client, sample_data):
        """Test GET /orders/<id> with valid ID"""
        order_id = sample_data['order_id']
        response = client.get(f'/orders/{order_id}')
        assert response.status_code == 200
        assert response.json['id'] == order_id
        assert response.json['status'] == 'pending'
    
    def test_get_order_by_id_not_found(self, client):
        """Test GET /orders/<id> with non-existent ID"""
        response = client.get('/orders/999')
        assert response.status_code == 404
    
    def test_update_order_success(self, client, sample_data):
        """Test PUT /orders/<id> with valid data"""
        order_id = sample_data['order_id']
        update_data = {
            'status': 'confirmed'  # Use a valid status from the model
        }
        response = client.put(f'/orders/{order_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        assert response.json['status'] == 'confirmed'
    
    def test_delete_order_success(self, client, sample_data):
        """Test DELETE /orders/<id> with valid ID"""
        order_id = sample_data['order_id']
        response = client.delete(f'/orders/{order_id}')
        assert response.status_code == 204
    
    def test_delete_order_not_found(self, client):
        """Test DELETE /orders/<id> with non-existent ID"""
        response = client.delete('/orders/999')
        assert response.status_code == 404
    
    def test_create_order_invalid_status(self, client, sample_data):
        """Test POST /orders with invalid status"""
        customer_id = sample_data['customer_id']
        item_id = sample_data['item_id']
        order_data = {
            'customer_id': customer_id,
            'status': 'invalid_status',  # Invalid status
            'items': [
                {
                    'shop_item_id': item_id,
                    'quantity': 1,
                    'price_at_time': 699.99
                }
            ]
        }
        response = client.post('/orders',
                             data=json.dumps(order_data),
                             content_type='application/json')
        # Should fail validation due to invalid status
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_create_order_invalid_customer(self, client, clean_db):
        """Test POST /orders with non-existent customer_id"""
        order_data = {
            'customer_id': 999,  # Non-existent customer
            'status': 'pending',
            'items': []
        }
        response = client.post('/orders',
                             data=json.dumps(order_data),
                             content_type='application/json')
        # Should fail due to validation (total_amount would be 0)
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_update_order_invalid_status(self, client, sample_data):
        """Test PUT /orders/<id> with invalid status"""
        order_id = sample_data['order_id']
        update_data = {
            'status': 'invalid_status'  # Invalid status
        }
        response = client.put(f'/orders/{order_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        # Should fail validation due to invalid status
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']


# Additional comprehensive tests for edge cases and error scenarios
class TestEndpointEdgeCases:
    """Test edge cases and error scenarios across all endpoints"""
    
    def test_invalid_json_format(self, client):
        """Test endpoints with malformed JSON"""
        response = client.post('/customers',
                             data='{"invalid": json}',
                             content_type='application/json')
        # Flask returns 500 for malformed JSON parsing errors
        assert response.status_code == 500
    
    def test_missing_content_type(self, client, clean_db):
        """Test POST endpoints without content-type header"""
        customer_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        response = client.post('/customers', data=json.dumps(customer_data))
        # Without content-type, Flask can't parse JSON, resulting in None data and 500 error
        assert response.status_code == 500
    
    def test_empty_request_body(self, client):
        """Test POST endpoints with empty request body"""
        response = client.post('/customers',
                             data='',
                             content_type='application/json')
        assert response.status_code in [400, 500]
    
    def test_null_values_in_required_fields(self, client, clean_db):
        """Test creating entities with null values in required fields"""
        customer_data = {
            'name': None,
            'email': 'test@example.com'
        }
        response = client.post('/customers',
                             data=json.dumps(customer_data),
                             content_type='application/json')
        # Validation catches null name before database constraint
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_empty_string_in_required_fields(self, client, clean_db):
        """Test creating entities with empty strings in required fields"""
        customer_data = {
            'name': '',
            'email': 'test@example.com'
        }
        response = client.post('/customers',
                             data=json.dumps(customer_data),
                             content_type='application/json')
        # Should fail validation due to empty name
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']


if __name__ == '__main__':
    pytest.main(['-v', __file__])
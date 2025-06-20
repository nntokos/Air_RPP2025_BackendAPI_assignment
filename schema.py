"""
Database schema initialization and test data setup for the Online Shop API.

This module handles:
- Database table creation
- Test data initialization
- Schema management utilities
"""

from models import db, Customer, ShopItemCategory, ShopItem, Order, OrderItem
from decimal import Decimal
from datetime import datetime


def create_all_tables():
    """Create all database tables based on the defined models."""
    try:
        db.create_all()
        print("✅ All database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False


def drop_all_tables():
    """Drop all database tables. Use with caution!"""
    try:
        db.drop_all()
        print("⚠️  All database tables dropped!")
        return True
    except Exception as e:
        print(f"❌ Error dropping tables: {str(e)}")
        return False


def init_test_data():
    """Initialize the database with test data for development and testing."""
    try:
        # Clear existing data first
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(ShopItem).delete()
        db.session.query(ShopItemCategory).delete()
        db.session.query(Customer).delete()
        db.session.commit()
        
        # Create test categories
        categories = [
            ShopItemCategory(
                name="Electronics",
                description="Electronic devices and gadgets"
            ),
            ShopItemCategory(
                name="Clothing",
                description="Fashion and apparel items"
            ),
            ShopItemCategory(
                name="Books",
                description="Books and educational materials"
            ),
            ShopItemCategory(
                name="Home & Garden",
                description="Home improvement and gardening supplies"
            ),
            ShopItemCategory(
                name="Sports",
                description="Sports equipment and fitness gear"
            )
        ]
        
        for category in categories:
            db.session.add(category)
        db.session.commit()
        
        # Create test shop items
        shop_items = [
            # Electronics
            ShopItem(
                name="iPhone 15 Pro",
                description="Latest Apple smartphone with advanced features",
                price=Decimal("999.99"),
                stock_quantity=25,
                category_id=1
            ),
            ShopItem(
                name="MacBook Air M2",
                description="Lightweight laptop with Apple M2 chip",
                price=Decimal("1199.00"),
                stock_quantity=15,
                category_id=1
            ),
            ShopItem(
                name="AirPods Pro",
                description="Wireless earbuds with noise cancellation",
                price=Decimal("249.99"),
                stock_quantity=50,
                category_id=1
            ),
            
            # Clothing
            ShopItem(
                name="Classic Blue Jeans",
                description="Comfortable denim jeans in classic blue",
                price=Decimal("79.99"),
                stock_quantity=100,
                category_id=2
            ),
            ShopItem(
                name="Cotton T-Shirt",
                description="Premium cotton t-shirt in various colors",
                price=Decimal("24.99"),
                stock_quantity=200,
                category_id=2
            ),
            ShopItem(
                name="Winter Jacket",
                description="Warm winter jacket for cold weather",
                price=Decimal("159.99"),
                stock_quantity=30,
                category_id=2
            ),
            
            # Books
            ShopItem(
                name="Python Programming Guide",
                description="Comprehensive guide to Python programming",
                price=Decimal("45.00"),
                stock_quantity=75,
                category_id=3
            ),
            ShopItem(
                name="Web Development Handbook",
                description="Modern web development techniques and best practices",
                price=Decimal("52.99"),
                stock_quantity=40,
                category_id=3
            ),
            
            # Home & Garden
            ShopItem(
                name="Garden Tool Set",
                description="Complete set of essential gardening tools",
                price=Decimal("89.99"),
                stock_quantity=35,
                category_id=4
            ),
            ShopItem(
                name="LED Desk Lamp",
                description="Adjustable LED desk lamp with USB charging",
                price=Decimal("39.99"),
                stock_quantity=60,
                category_id=4
            ),
            
            # Sports
            ShopItem(
                name="Yoga Mat",
                description="Non-slip yoga mat for exercise and meditation",
                price=Decimal("29.99"),
                stock_quantity=80,
                category_id=5
            ),
            ShopItem(
                name="Basketball",
                description="Official size basketball for indoor/outdoor use",
                price=Decimal("34.99"),
                stock_quantity=45,
                category_id=5
            )
        ]
        
        for item in shop_items:
            db.session.add(item)
        db.session.commit()
        
        # Create test customers
        customers = [
            Customer(
                name="John Smith",
                email="john.smith@email.com",
                phone="+12345678901",
                address="123 Main St, Anytown, AN 12345"
            ),
            Customer(
                name="Emma Johnson",
                email="emma.johnson@email.com",
                phone="+12345678902",
                address="456 Oak Ave, Somewhere, SW 67890"
            ),
            Customer(
                name="Michael Brown",
                email="michael.brown@email.com",
                phone="+12345678903",
                address="789 Pine Rd, Elsewhere, EL 13579"
            ),
            Customer(
                name="Sarah Davis",
                email="sarah.davis@email.com",
                phone="+12345678904",
                address="321 Elm St, Nowhere, NW 24680"
            ),
            Customer(
                name="David Wilson",
                email="david.wilson@email.com",
                phone="+12345678905",
                address="654 Maple Dr, Anywhere, AW 97531"
            )
        ]
        
        for customer in customers:
            db.session.add(customer)
        db.session.commit()
        
        # Create test orders with order items
        orders_data = [
            {
                "customer_id": 1,
                "status": "delivered",
                "items": [
                    {"shop_item_id": 3, "quantity": 1, "price": Decimal("249.99")},  # AirPods Pro
                    {"shop_item_id": 5, "quantity": 2, "price": Decimal("24.99")}    # Cotton T-Shirt
                ]
            },
            {
                "customer_id": 2,
                "status": "shipped",
                "items": [
                    {"shop_item_id": 1, "quantity": 1, "price": Decimal("999.99")},  # iPhone 15 Pro
                    {"shop_item_id": 10, "quantity": 1, "price": Decimal("39.99")}   # LED Desk Lamp
                ]
            },
            {
                "customer_id": 3,
                "status": "confirmed",
                "items": [
                    {"shop_item_id": 7, "quantity": 2, "price": Decimal("45.00")},   # Python Programming Guide
                    {"shop_item_id": 11, "quantity": 1, "price": Decimal("29.99")}   # Yoga Mat
                ]
            },
            {
                "customer_id": 1,
                "status": "pending",
                "items": [
                    {"shop_item_id": 2, "quantity": 1, "price": Decimal("1199.00")}, # MacBook Air M2
                ]
            },
            {
                "customer_id": 4,
                "status": "cancelled",
                "items": [
                    {"shop_item_id": 6, "quantity": 1, "price": Decimal("159.99")},  # Winter Jacket
                    {"shop_item_id": 12, "quantity": 1, "price": Decimal("34.99")}   # Basketball
                ]
            }
        ]
        
        for order_data in orders_data:
            # Calculate total amount
            total_amount = sum(item["quantity"] * item["price"] for item in order_data["items"])
            
            # Create order
            order = Order(
                customer_id=order_data["customer_id"],
                total_amount=total_amount,
                status=order_data["status"]
            )
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Create order items
            for item_data in order_data["items"]:
                order_item = OrderItem(
                    order_id=order.id,
                    shop_item_id=item_data["shop_item_id"],
                    quantity=item_data["quantity"],
                    price_at_time=item_data["price"]
                )
                db.session.add(order_item)
        
        db.session.commit()
        
        print("✅ Test data initialized successfully!")
        print(f"   - {len(categories)} categories created")
        print(f"   - {len(shop_items)} shop items created")
        print(f"   - {len(customers)} customers created")
        print(f"   - {len(orders_data)} orders with items created")
        
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error initializing test data: {str(e)}")
        return False


def init_database(with_test_data=True):
    """
    Complete database initialization.
    
    Args:
        with_test_data (bool): Whether to populate with test data
        
    Returns:
        bool: True if successful, False otherwise
    """
    print("🔄 Initializing database...")
    
    # Create tables
    if not create_all_tables():
        return False
    
    # Initialize test data if requested
    if with_test_data:
        if not init_test_data():
            return False
    
    print("🎉 Database initialization completed successfully!")
    return True


def reset_database():
    """Reset the entire database (drop and recreate with test data)."""
    print("⚠️  Resetting database...")
    
    if drop_all_tables():
        return init_database(with_test_data=True)
    
    return False


def get_database_stats():
    """Get statistics about the current database content."""
    try:
        stats = {
            "customers": Customer.query.count(),
            "categories": ShopItemCategory.query.count(),
            "shop_items": ShopItem.query.count(),
            "orders": Order.query.count(),
            "order_items": OrderItem.query.count()
        }
        
        print("📊 Database Statistics:")
        for table, count in stats.items():
            print(f"   - {table.capitalize()}: {count}")
        
        return stats
        
    except Exception as e:
        print(f"❌ Error getting database stats: {str(e)}")
        return None


if __name__ == "__main__":
    # This allows running the schema file directly for database setup
    from flask import Flask
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        reset_database()
        get_database_stats()
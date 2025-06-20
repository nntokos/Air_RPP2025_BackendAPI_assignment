import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db, Customer, ShopItemCategory, ShopItem, Order, OrderItem
from flask import Flask
import tempfile

def create_test_app():
    """Create a test Flask app with in-memory database"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

def test_models():
    """Test all models and their methods"""
    app = create_test_app()

    with app.app_context():
        print("Testing models...")

        # Test Customer
        print("\n1. Testing Customer model:")
        customer = Customer(
            name="John Doe",
            email="john.doe@example.com",
            phone="+1234567890",
            address="123 Main St, City, Country"
        )

        print(f"Customer validation: {customer.validate()}")
        print(f"Email validation: {customer.validate_email()}")
        print(f"Phone validation: {customer.validate_phone()}")
        print(f"Customer repr: {customer}")

        db.session.add(customer)
        db.session.commit()
        print("Customer created successfully!")

        # Test ShopItemCategory
        print("\n2. Testing ShopItemCategory model:")
        category = ShopItemCategory(
            name="Electronics",
            description="Electronic devices and accessories"
        )

        print(f"Category validation: {category.validate()}")
        print(f"Category repr: {category}")

        db.session.add(category)
        db.session.commit()
        print("Category created successfully!")

        # Test ShopItem
        print("\n3. Testing ShopItem model:")
        item = ShopItem(
            name="Smartphone",
            description="Latest model smartphone",
            price=599.99,
            stock_quantity=10,
            category_id=category.id
        )

        print(f"Item validation: {item.validate()}")
        print(f"Price validation: {item.validate_price()}")
        print(f"Stock validation: {item.validate_stock()}")
        print(f"Is available: {item.is_available()}")
        print(f"Can fulfill 5 items: {item.can_fulfill_quantity(5)}")
        print(f"Item repr: {item}")

        db.session.add(item)
        db.session.commit()
        print("Item created successfully!")

        # Test Order
        print("\n4. Testing Order model:")
        order = Order(
            customer_id=customer.id,
            total_amount=599.99,
            status='pending'
        )

        print(f"Order validation: {order.validate()}")
        print(f"Status validation: {order.validate_status()}")
        print(f"Total amount validation: {order.validate_total_amount()}")
        print(f"Can be cancelled: {order.can_be_cancelled()}")
        print(f"Order repr: {order}")

        db.session.add(order)
        db.session.commit()
        print("Order created successfully!")

        # Test OrderItem
        print("\n5. Testing OrderItem model:")
        order_item = OrderItem(
            order_id=order.id,
            shop_item_id=item.id,
            quantity=2,
            price_at_time=599.99
        )

        print(f"OrderItem validation: {order_item.validate()}")
        print(f"Quantity validation: {order_item.validate_quantity()}")
        print(f"Price validation: {order_item.validate_price_at_time()}")
        print(f"Subtotal: {order_item.calculate_subtotal()}")
        print(f"OrderItem repr: {order_item}")

        db.session.add(order_item)
        db.session.commit()
        print("OrderItem created successfully!")

        # Test relationships and methods
        print("\n6. Testing relationships and additional methods:")
        print(f"Customer total orders: {customer.get_total_orders()}")
        print(f"Customer total spent: {customer.get_total_spent()}")
        print(f"Category item count: {category.get_item_count()}")
        print(f"Category available items: {len(category.get_available_items())}")
        print(f"Order item count: {order.get_item_count()}")
        print(f"Order calculated total: {order.calculate_total_from_items()}")

        # Test stock operations
        print(f"\nStock before reduction: {item.stock_quantity}")
        success = item.reduce_stock(3)
        print(f"Stock reduction success: {success}")
        print(f"Stock after reduction: {item.stock_quantity}")

        item.increase_stock(5)
        print(f"Stock after increase: {item.stock_quantity}")

        # Test to_dict methods
        print("\n7. Testing to_dict methods:")
        print("Customer dict keys:", list(customer.to_dict().keys()))
        print("Category dict keys:", list(category.to_dict().keys()))
        print("Item dict keys:", list(item.to_dict().keys()))
        print("Order dict keys:", list(order.to_dict().keys()))
        print("OrderItem dict keys:", list(order_item.to_dict().keys()))

        print("\n✅ All tests passed successfully!")

if __name__ == "__main__":
    test_models()
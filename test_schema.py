#!/usr/bin/env python3
"""
Test script to verify schema.py functionality and display sample data.
"""

from schema import *
from flask import Flask

def test_schema():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        get_database_stats()
        
        # Test some queries
        print('\n🔍 Sample Data Preview:')
        customers = Customer.query.limit(2).all()
        for customer in customers:
            print(f'Customer: {customer.name} ({customer.email})')
        
        categories = ShopItemCategory.query.limit(3).all()
        for category in categories:
            print(f'Category: {category.name} - {category.get_item_count()} items')
        
        orders = Order.query.limit(2).all()
        for order in orders:
            print(f'Order #{order.id}: ${order.total_amount} ({order.status}) - {order.get_item_count()} items')

if __name__ == "__main__":
    test_schema()
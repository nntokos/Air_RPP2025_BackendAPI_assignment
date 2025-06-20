from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from decimal import Decimal
from sqlalchemy import event

db = SQLAlchemy()

# Event listeners for validation
@event.listens_for(db.session, 'before_commit')
def validate_models(session):
    """Validate models before committing to database"""
    for instance in session.new:
        if hasattr(instance, 'validate'):
            if not instance.validate():
                raise ValueError(f"Validation failed for {instance.__class__.__name__}")
    
    for instance in session.dirty:
        if hasattr(instance, 'validate'):
            if not instance.validate():
                raise ValueError(f"Validation failed for {instance.__class__.__name__}")

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.name} ({self.email})>'
    
    def validate_email(self):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, self.email) is not None
    
    def validate_phone(self):
        """Validate phone format (basic validation)"""
        if not self.phone:
            return True  # Phone is optional
        # Remove spaces, dashes, parentheses
        cleaned_phone = re.sub(r'[\s\-\(\)]+', '', self.phone)
        # Check if it contains only digits and optionally starts with +
        return re.match(r'^\+?\d{10,15}$', cleaned_phone) is not None
    
    def get_total_orders(self):
        """Get total number of orders for this customer"""
        return len(self.orders)
    
    def get_total_spent(self):
        """Calculate total amount spent by this customer"""
        return sum(order.total_amount for order in self.orders)
    
    def validate(self):
        """Validate customer data"""
        return (self.name and 
                self.validate_email() and 
                self.validate_phone())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ShopItemCategory(db.Model):
    __tablename__ = 'shop_item_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    shop_items = db.relationship('ShopItem', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<ShopItemCategory {self.name}>'
    
    def get_item_count(self):
        """Get number of items in this category"""
        return len(self.shop_items)
    
    def get_available_items(self):
        """Get items in this category that are available (stock > 0)"""
        return [item for item in self.shop_items if item.stock_quantity > 0]
    
    def validate(self):
        """Validate category data"""
        return bool(self.name)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'item_count': self.get_item_count()
        }

class ShopItem(db.Model):
    __tablename__ = 'shop_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('shop_item_categories.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ShopItem {self.name} (${self.price})>'
    
    def validate_price(self):
        """Validate that price is positive"""
        return self.price > 0
    
    def validate_stock(self):
        """Validate that stock quantity is non-negative"""
        return self.stock_quantity >= 0
    
    def is_available(self):
        """Check if item is available (in stock)"""
        return self.stock_quantity > 0
    
    def can_fulfill_quantity(self, quantity):
        """Check if we have enough stock for the requested quantity"""
        return self.stock_quantity >= quantity
    
    def reduce_stock(self, quantity):
        """Reduce stock by specified quantity"""
        if self.can_fulfill_quantity(quantity):
            self.stock_quantity -= quantity
            return True
        return False
    
    def increase_stock(self, quantity):
        """Increase stock by specified quantity"""
        if quantity > 0:
            self.stock_quantity += quantity
            return True
        return False
    
    def validate(self):
        """Validate shop item data"""
        return (self.name and 
                self.validate_price() and 
                self.validate_stock() and
                self.category_id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock_quantity': self.stock_quantity,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_available': self.is_available()
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    # Valid order statuses
    VALID_STATUSES = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, index=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, confirmed, shipped, delivered, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id} - ${self.total_amount} ({self.status})>'
    
    def validate_status(self):
        """Validate that status is one of the allowed values"""
        return self.status in self.VALID_STATUSES
    
    def validate_total_amount(self):
        """Validate that total amount is positive"""
        return self.total_amount > 0
    
    def calculate_total_from_items(self):
        """Calculate total amount from order items"""
        return sum(item.quantity * item.price_at_time for item in self.order_items)
    
    def update_total_amount(self):
        """Update total amount based on current order items"""
        self.total_amount = self.calculate_total_from_items()
        return self.total_amount
    
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def can_be_shipped(self):
        """Check if order can be shipped"""
        return self.status == 'confirmed'
    
    def can_be_delivered(self):
        """Check if order can be delivered"""
        return self.status == 'shipped'
    
    def get_item_count(self):
        """Get total number of items in this order"""
        return sum(item.quantity for item in self.order_items)
    
    def validate(self):
        """Validate order data"""
        return (self.customer_id and 
                self.validate_status() and 
                self.validate_total_amount())
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'item_count': self.get_item_count(),
            'order_items': [item.to_dict() for item in self.order_items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    shop_item_id = db.Column(db.Integer, db.ForeignKey('shop_items.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Numeric(10, 2), nullable=False)  # Price when order was placed
    
    # Relationship
    shop_item = db.relationship('ShopItem', backref='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.quantity}x {self.shop_item.name if self.shop_item else "Item"} @ ${self.price_at_time}>'
    
    def validate_quantity(self):
        """Validate that quantity is positive"""
        return self.quantity > 0
    
    def validate_price_at_time(self):
        """Validate that price at time is positive"""
        return self.price_at_time > 0
    
    def calculate_subtotal(self):
        """Calculate subtotal for this order item"""
        return self.quantity * self.price_at_time
    
    def validate(self):
        """Validate order item data"""
        return (self.order_id and 
                self.shop_item_id and 
                self.validate_quantity() and 
                self.validate_price_at_time())
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'shop_item_id': self.shop_item_id,
            'shop_item_name': self.shop_item.name if self.shop_item else None,
            'quantity': self.quantity,
            'price_at_time': float(self.price_at_time),
            'subtotal': float(self.calculate_subtotal())
        }
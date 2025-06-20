from flask import request, jsonify
from models import db, Customer, ShopItemCategory, ShopItem, Order, OrderItem

def register_routes(app):
    """Register all API routes with the Flask app"""
    
    @app.route('/customers', methods=['GET', 'POST'])
    def handle_customers():
        if request.method == 'GET':
            customers = Customer.query.all()
            return jsonify([customer.to_dict() for customer in customers])
        elif request.method == 'POST':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                # Check required fields
                if 'name' not in data:
                    return jsonify({'error': 'Missing required field: name'}), 400
                if 'email' not in data:
                    return jsonify({'error': 'Missing required field: email'}), 400
                
                customer = Customer(
                    name=data['name'],
                    email=data['email'],
                    phone=data.get('phone'),
                    address=data.get('address')
                )
                db.session.add(customer)
                db.session.commit()
                return jsonify(customer.to_dict()), 201
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_customer(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        if request.method == 'GET':
            return jsonify(customer.to_dict())
        elif request.method == 'PUT':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                customer.name = data.get('name', customer.name)
                customer.email = data.get('email', customer.email)
                customer.phone = data.get('phone', customer.phone)
                customer.address = data.get('address', customer.address)
                db.session.commit()
                return jsonify(customer.to_dict())
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500
        elif request.method == 'DELETE':
            try:
                db.session.delete(customer)
                db.session.commit()
                return '', 204
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/categories', methods=['GET', 'POST'])
    def handle_categories():
        if request.method == 'GET':
            categories = ShopItemCategory.query.all()
            return jsonify([category.to_dict() for category in categories])
        elif request.method == 'POST':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                # Check required fields
                if 'name' not in data:
                    return jsonify({'error': 'Missing required field: name'}), 400
                
                category = ShopItemCategory(
                    name=data['name'],
                    description=data.get('description')
                )
                db.session.add(category)
                db.session.commit()
                return jsonify(category.to_dict()), 201
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/categories/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_category(category_id):
        category = ShopItemCategory.query.get_or_404(category_id)
        if request.method == 'GET':
            return jsonify(category.to_dict())
        elif request.method == 'PUT':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                category.name = data.get('name', category.name)
                category.description = data.get('description', category.description)
                db.session.commit()
                return jsonify(category.to_dict())
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500
        elif request.method == 'DELETE':
            try:
                db.session.delete(category)
                db.session.commit()
                return '', 204
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/items', methods=['GET', 'POST'])
    def handle_items():
        if request.method == 'GET':
            items = ShopItem.query.all()
            return jsonify([item.to_dict() for item in items])
        elif request.method == 'POST':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                # Check required fields
                required_fields = ['name', 'price', 'stock_quantity', 'category_id']
                for field in required_fields:
                    if field not in data:
                        return jsonify({'error': f'Missing required field: {field}'}), 400
                
                item = ShopItem(
                    name=data['name'],
                    description=data.get('description'),
                    price=data['price'],
                    stock_quantity=data['stock_quantity'],
                    category_id=data['category_id']
                )
                db.session.add(item)
                db.session.commit()
                return jsonify(item.to_dict()), 201
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_item(item_id):
        item = ShopItem.query.get_or_404(item_id)
        if request.method == 'GET':
            return jsonify(item.to_dict())
        elif request.method == 'PUT':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                item.name = data.get('name', item.name)
                item.description = data.get('description', item.description)
                item.price = data.get('price', item.price)
                item.stock_quantity = data.get('stock_quantity', item.stock_quantity)
                item.category_id = data.get('category_id', item.category_id)
                db.session.commit()
                return jsonify(item.to_dict())
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500
        elif request.method == 'DELETE':
            try:
                db.session.delete(item)
                db.session.commit()
                return '', 204
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/orders', methods=['GET', 'POST'])
    def handle_orders():
        if request.method == 'GET':
            orders = Order.query.all()
            return jsonify([order.to_dict() for order in orders])
        elif request.method == 'POST':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                # Check required fields
                if 'customer_id' not in data:
                    return jsonify({'error': 'Missing required field: customer_id'}), 400
                if 'items' not in data:
                    return jsonify({'error': 'Missing required field: items'}), 400
                
                order = Order(
                    customer_id=data['customer_id'],
                    total_amount=0,  # Will be calculated
                    status=data.get('status', 'pending')
                )
                db.session.add(order)
                db.session.flush()  # Get order ID
                
                for item in data['items']:
                    if not all(key in item for key in ['shop_item_id', 'quantity', 'price_at_time']):
                        return jsonify({'error': 'Missing required fields in order item'}), 400
                    order_item = OrderItem(
                        order_id=order.id,
                        shop_item_id=item['shop_item_id'],
                        quantity=item['quantity'],
                        price_at_time=item['price_at_time']
                    )
                    db.session.add(order_item)
                
                order.update_total_amount()
                db.session.commit()
                return jsonify(order.to_dict()), 201
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_order(order_id):
        order = Order.query.get_or_404(order_id)
        if request.method == 'GET':
            return jsonify(order.to_dict())
        elif request.method == 'PUT':
            try:
                data = request.json
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                order.status = data.get('status', order.status)
                db.session.commit()
                return jsonify(order.to_dict())
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': f'Validation error: {str(e)}'}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500
        elif request.method == 'DELETE':
            try:
                db.session.delete(order)
                db.session.commit()
                return '', 204
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500
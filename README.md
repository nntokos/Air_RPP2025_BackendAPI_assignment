# Online Shop Backend API

A Flask-based RESTful API for managing an online shop with customers, categories, items, and orders.

## Features

- **Customer Management**: Create, read, update, and delete customers
- **Category Management**: Manage product categories
- **Item Management**: Handle product inventory with category associations
- **Order Management**: Process orders with multiple items and customer associations
- **SQLite Database**: Lightweight database with automatic initialization
- **Test Data**: Automatic test data population for development
- **Comprehensive Testing**: Full test suite with pytest

## Project Structure

```
Air_RPP2025_BackendAPI_assignment/
├── app.py              # Main Flask application entry point
├── models.py           # SQLAlchemy database models
├── crud.py             # CRUD operations and API routes
├── schema.py           # Database schema and test data initialization
├── requirements.txt    # Python dependencies
├── instance/
│   └── shop.db        # SQLite database file
└── tests/
    ├── test_endpoints.py   # API endpoint tests
    ├── test_models.py      # Database model tests
    └── test_schema.py      # Schema tests
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Air_RPP2025_BackendAPI_assignment
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The database will be automatically initialized when you first run the application. It will create all necessary tables and populate them with test data.

## Running the Application

### Start the Development Server

```bash
python app.py
```

The application will start on `http://localhost:5001`

### Expected Output

```
Initializing database...
Database is empty, adding test data...
✅ Test data added successfully!
🚀 Starting Online Shop Backend API...
📊 API Documentation:
   Customers: GET/POST /customers, GET/PUT/DELETE /customers/<id>
   Categories: GET/POST /categories, GET/PUT/DELETE /categories/<id>
   Items: GET/POST /items, GET/PUT/DELETE /items/<id>
   Orders: GET/POST /orders, GET/PUT/DELETE /orders/<id>
💡 Access the API at: http://localhost:5001
```

## API Endpoints

### Customers
- `GET /customers` - Get all customers
- `POST /customers` - Create a new customer
- `GET /customers/<id>` - Get a specific customer
- `PUT /customers/<id>` - Update a customer
- `DELETE /customers/<id>` - Delete a customer

### Categories
- `GET /categories` - Get all categories
- `POST /categories` - Create a new category
- `GET /categories/<id>` - Get a specific category
- `PUT /categories/<id>` - Update a category
- `DELETE /categories/<id>` - Delete a category

### Items
- `GET /items` - Get all items
- `POST /items` - Create a new item
- `GET /items/<id>` - Get a specific item
- `PUT /items/<id>` - Update an item
- `DELETE /items/<id>` - Delete an item

### Orders
- `GET /orders` - Get all orders
- `POST /orders` - Create a new order
- `GET /orders/<id>` - Get a specific order
- `PUT /orders/<id>` - Update an order
- `DELETE /orders/<id>` - Delete an order

## API Usage Examples (curl)

Here are practical examples of how to interact with the API using curl commands:

### Add a Customer

```bash
curl -X POST http://localhost:5001/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Main St, City, State 12345"
  }'
```

### Add an Item

```bash
curl -X POST http://localhost:5001/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "High-quality Bluetooth wireless headphones",
    "price": 99.99,
    "stock_quantity": 50,
    "category_id": 1
  }'
```

### Get All Customers

```bash
curl -X GET http://localhost:5001/customers
```

### Get a Specific Item

```bash
curl -X GET http://localhost:5001/items/1
```

### Additional Examples

#### Get All Items
```bash
curl -X GET http://localhost:5001/items
```

#### Get All Categories
```bash
curl -X GET http://localhost:5001/categories
```

#### Add a Category (needed before adding items)
```bash
curl -X POST http://localhost:5001/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  }'
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Test API endpoints
pytest test_endpoints.py

# Test database models
pytest test_models.py

# Test database schema
pytest test_schema.py
```

### Run Tests with Verbose Output

```bash
pytest -v
```

## Development

### Activating Virtual Environment

Always activate the virtual environment before working on the project:

```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Database Management

The application uses SQLite database stored in `instance/shop.db`. The database is automatically created and populated with test data on first run.

To reset the database:
1. Stop the application
2. Delete the `instance/shop.db` file
3. Restart the application

### Adding New Dependencies

```bash
# Install new package
pip install <package-name>

# Update requirements.txt
pip freeze > requirements.txt
```

## Configuration

The application can be configured through environment variables:

- `SECRET_KEY`: Flask secret key (defaults to 'dev-secret-key-change-in-production')
- Database URL is configured in `app.py` as SQLite

## Troubleshooting

### Common Issues

1. **Port already in use**: If port 5001 is busy, change the port in `app.py`
2. **Database errors**: Delete `instance/shop.db` to reset the database
3. **Import errors**: Ensure virtual environment is activated and dependencies are installed


## License

This project is part of the Air_RPP2025 assignment.
# Air_RPP2025 Backend API Assignment (branch PyCharm)

A FastAPI backend for managing Customers, Shop Item Categories, Shop Items, and Orders.  
This project demonstrates a simple e-commerce backend with full CRUD operations and automated endpoint tests.

## Prerequisites

- Python 3.8+
- pip

## Project Structure

- `app.py` - Main FastAPI application with all endpoints.
- `crud.py` - CRUD logic for all entities.
- `model.py` - SQLAlchemy models.
- `schema.py` - Database setup and session utilities.
- `schemas.py` - Pydantic schemas for request/response validation.
- `seed.py` - Script to seed the database with initial data.
- `test_endpoints.py` - Automated endpoint tests.
- `test.db` - SQLite database (created after seeding).

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/nntokos/Air_RPP2025_BackendAPI_assignment
    cd Air_RPP2025_BackendAPI_assignment
   git checkout pycharm2025
    ```

2. **Install dependencies:**
    ```sh
    pip install fastapi uvicorn sqlalchemy pydantic pytest
    ```

3. **(Optional) Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

## Database Initialization & Seeding

1. **Initialize and seed the database:**
    ```sh
    python seed.py
    ```
    This will create a SQLite database (`test.db`) and populate it with sample data.

## Running the Application

1. **Start the FastAPI server (default port: 5001):**
    ```sh
    uvicorn app:app --reload --port 5001
    ```
    or:
    ```sh
    python app.py
    ```
    By default, the application runs on port **5001**.  
    If you want to use a different port, change the `--port` argument in the `uvicorn` command above (e.g., `--port 8000`).

2. **Access the API docs:**
    - Open [http://localhost:5001/docs](http://localhost:5001/docs) in your browser for the interactive Swagger UI.

## Running Tests

1. **Run all endpoint tests:**
    ```sh
    pytest test_endpoints.py
    ```

    All CRUD endpoints for Customers, Categories, Items, and Orders are covered.

## Using the API Endpoints

Below are example `curl` commands for common operations.  
**Note:** All commands use port `5001`. If you use a different port, replace `5001` with your chosen port.

### Customers

- **Add a customer:**
    ```sh
    curl -X POST "http://localhost:5001/customers/" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'
    ```
- **Get all customers:**
    ```sh
    curl "http://localhost:5001/customers/"
    ```

### Shop Item Categories

- **Add a category:**
    ```sh
    curl -X POST "http://localhost:5001/categories/" -H "Content-Type: application/json" -d '{"name": "Books"}'
    ```
- **Get all categories:**
    ```sh
    curl "http://localhost:5001/categories/"
    ```

### Shop Items

- **Add an item:**
    ```sh
    curl -X POST "http://localhost:5001/items/" -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 999.99, "category_id": 1}'
    ```
- **Get all items:**
    ```sh
    curl "http://localhost:5001/items/"
    ```

### Orders

- **Add an order for a customer:**
    ```sh
    curl -X POST "http://localhost:5001/orders/" -H "Content-Type: application/json" -d '{"customer_id": 1}'
    ```
- **Get all orders:**
    ```sh
    curl "http://localhost:5001/orders/"
    ```

## Troubleshooting

- If you encounter database errors, try deleting `test.db` and re-running `python seed.py`.
- Ensure all dependencies are installed in your active environment.

## Contributors

- Nikos Ntokos

## License

This project is licensed under the [MIT License](LICENSE.md).

## References & Inspiration

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [awesome-readme](https://github.com/matiassingers/awesome-readme)
- [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)


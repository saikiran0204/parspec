# Order Processing Backend

## Overview
This is a Flask-based order processing system that supports placing orders, tracking order status, and retrieving system metrics. The application uses Flask-SQLAlchemy for database interactions and a background queue for processing orders asynchronously.

---

## Example API Requests & Responses

### 1. Place an Order
**Request:**
```bash
curl -X POST "http://3.84.157.161/orders" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "123e4567-e89b-12d3-a456-426614174000",
           "item_ids": [
               "item-001",
               "item-002"
           ],
           "total_amount": 250.75
        }'
```
**Response:**
```json
{
    "message": "Order placed successfully",
    "order_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Get Order Status
**Request:**
```bash
curl -X GET "http://3.84.157.161/orders/550e8400-e29b-41d4-a716-446655440000"
```
**Response:**
```json
{
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "Processing"
}
```

### 3. Get Metrics
**Request:**
```bash
curl -X GET "http://3.84.157.161/metrics"
```
**Response:**
```json
{
    "average_processing_time": 26,
    "estimated_processing_time": 3976,
    "status_counts": {
        "completed_orders": 12,
        "pending_orders": 1987,
        "processing_orders": 1
    },
    "total_orders": 2000
}
```

---

## Design Decisions & Trade-offs

### 1. **Flask with Flask-SQLAlchemy**
- Used Flask-SQLAlchemy for easy ORM-based database interaction.
- Considered using an async ORM like Tortoise but opted for SQLAlchemy's support for better compatibility.

### 2. **Background Queue for Order Processing**
- Used Python’s built-in `queue.Queue` to process orders asynchronously.
- Considered Celery but avoided it for simplicity and fewer dependencies.

---

## Assumptions
1. Orders are processed on a **First-Come-First-Serve (FCFS)** basis.
2. The queue persists unprocessed orders when the server restarts.
3. The database is lightweight (SQLite) but can be replaced with PostgreSQL or MySQL in production.
4. Processing time for each order is simulated with `time.sleep(2)` but would be replaced by real business logic in production.

---

## Repository Link
[GitHub Repository](https://github.com/saikiran0204/parspec)

## Server Configuration
- Server is hosted on AWS EC2 with t2.micro
- Ip Address: 3.84.157.161
- Port: 80
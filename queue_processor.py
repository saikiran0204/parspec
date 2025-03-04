import threading
import time
from queue import Queue
from database import db
from models import Order
from datetime import datetime

order_queue = Queue()
process_time = 2

def load_pending_orders():
    pending_orders = Order.query.filter(Order.status.in_(["Pending", "Processing"])).all()
    for order in pending_orders:
        order_queue.put(order.order_id)

def process_orders(app):
    time.sleep(1)  # Simulate app startup time
    with app.app_context():
        load_pending_orders()
        while True:
            order_id = order_queue.get()
            order = Order.query.filter_by(order_id=order_id).first()
            if order:
                order.status = "Processing"
                db.session.commit()
                time.sleep(process_time)  # Simulate processing time
                order.status = "Completed"
                order.processed_at = datetime.utcnow()
                db.session.commit()
            order_queue.task_done()
from database import db
import uuid
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, nullable=False)
    item_ids = db.Column(db.String, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)
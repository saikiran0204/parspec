from flask import Blueprint, request, jsonify
from database import db
from models import Order
from schemas import OrderRequest
from queue_processor import order_queue, process_time
import uuid
from sqlalchemy import func

order_blueprint = Blueprint("orders", __name__)

@order_blueprint.route("/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    try:
        validated_data = OrderRequest(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    new_order = Order(
        order_id=str(uuid.uuid4()),
        user_id=validated_data.user_id,
        item_ids=",".join(validated_data.item_ids),
        total_amount=validated_data.total_amount,
        status="Pending"
    )
    db.session.add(new_order)
    db.session.commit()
    order_queue.put(new_order.order_id)
    return jsonify({"message": "Order placed successfully", "order_id": new_order.order_id}), 201

@order_blueprint.route("/orders/<order_id>", methods=["GET"])
def get_order_status(order_id):
    order = Order.query.filter(Order.order_id==order_id).first()
    if order:
        return jsonify({"order_id": order.order_id, "status": order.status})
    return jsonify({"error": "Order not found"}), 404

@order_blueprint.route("/orders/metrics", methods=["GET"])
def get_metrics():
    total_orders = Order.query.count()
    status_counts = db.session.query(Order.status, func.count(Order.status)).group_by(Order.status).all()
    status_dict = {status: count for status, count in status_counts}
    
    avg_processing_time = db.session.query(func.avg((func.julianday(Order.processed_at) - func.julianday(Order.created_at)) * 86400)).filter(Order.status == "Completed").scalar()
    avg_time = avg_processing_time if avg_processing_time else 0

    pending_count = order_queue.qsize()  # Get pending count directly from queue
    processing_count = Order.query.filter(Order.status == 'Processing').count()
    estimated_processing_time = process_time * (pending_count + processing_count)
    
    return jsonify({
        "total_orders": total_orders,
        "status_counts": {
            "completed_orders": status_dict.get("Completed", 0),
            "pending_orders": status_dict.get("Pending", 0),
            "processing_orders": status_dict.get("Processing", 0),
        },
        "average_processing_time": int(avg_time),
        "estimated_processing_time": estimated_processing_time,
    })



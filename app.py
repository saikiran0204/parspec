from flask import Flask
from database import db, init_db
from routes import order_blueprint
import threading
from queue_processor import process_orders

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./orders.db"
    db.init_app(app)
    init_db(app)
    app.register_blueprint(order_blueprint)
    return app

if __name__ == "__main__":
    app = create_app()
    worker_thread = threading.Thread(target=process_orders, args=[app], daemon=True)
    worker_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        worker_thread.join()
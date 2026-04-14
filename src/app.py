from flask import Flask, jsonify, request
import uuid
from src.pricing import calculate_order_total, apply_promo_code, PROMO_CODES

app = Flask(__name__)

orders_db = {}

def reset_db():
    global orders_db
    orders_db = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/orders/simulate', methods=['POST'])
def simulate_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
        
    try:
        items = data.get("items", [])
        distance = data.get("distance", 0)
        weight = data.get("weight", 0)
        promo = data.get("promoCode")
        hour = data.get("hour", 12)
        day = data.get("dayOfWeek", "monday")
        
        result = calculate_order_total(items, distance, weight, promo, hour, day)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
        
    try:
        items = data.get("items", [])
        distance = data.get("distance", 0)
        weight = data.get("weight", 0)
        promo = data.get("promoCode")
        hour = data.get("hour", 12)
        day = data.get("dayOfWeek", "monday")
        
        result = calculate_order_total(items, distance, weight, promo, hour, day)
        
        order_id = str(uuid.uuid4())
        order_record = {
            "id": order_id,
            "items": items,
            "distance": distance,
            "weight": weight,
            "promoCode": promo,
            "hour": hour,
            "dayOfWeek": day,
            "pricing": result
        }
        
        orders_db[order_id] = order_record
        return jsonify(order_record), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    if order_id in orders_db:
        return jsonify(orders_db[order_id]), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/promo/validate', methods=['POST'])
def validate_promo():
    data = request.get_json()
    if not data or "promoCode" not in data or "subtotal" not in data:
        return jsonify({"error": "Missing promoCode or subtotal"}), 400
        
    promo = data.get("promoCode")
    subtotal = data.get("subtotal")
    
    code_obj = next((m for m in PROMO_CODES if m["code"] == promo), None)
    if not code_obj:
        return jsonify({"error": "Promo code not found"}), 404
        
    try:
        discount = apply_promo_code(subtotal, promo, PROMO_CODES)
        new_price = subtotal - discount
        return jsonify({
            "valid": True,
            "discount": discount,
            "new_price": round(new_price, 2)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

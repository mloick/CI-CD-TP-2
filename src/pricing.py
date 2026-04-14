from datetime import datetime

PROMO_CODES = [
    {"code": "BIENVENUE20", "type": "percentage", "value": 20, "minOrder": 15.00, "expiresAt": "2026-12-31"},
    {"code": "FIXED5", "type": "fixed", "value": 5, "minOrder": 10.00, "expiresAt": "2026-12-31"},
    {"code": "EXPIRED", "type": "fixed", "value": 5, "minOrder": 0.00, "expiresAt": "2020-01-01"},
]

def calculate_delivery_fee(distance, weight):
    if distance < 0 or weight < 0:
        raise ValueError("Distance and weight cannot be negative")
    if distance > 10:
        raise ValueError("Delivery refused for distance > 10 km")
    
    base_fee = 2.00
    extra_distance_fee = distance * 0.50 if distance > 0 else 0
    extra_weight_fee = 1.50 if weight > 5 else 0
    
    total = base_fee + extra_distance_fee + extra_weight_fee
    return round(total, 2)

def apply_promo_code(subtotal, promo_code_str, promo_codes_list):
    if not promo_code_str or subtotal <= 0:
        return 0.0
    
    code_obj = next((m for m in promo_codes_list if m["code"] == promo_code_str), None)
    if not code_obj:
        raise ValueError("Promo code not found")
        
    date_format = "%Y-%m-%d"
    today = datetime.now().strftime(date_format)
    # Compare strings or dates. For simplicity, just string comparison.
    if code_obj["expiresAt"] < today:
        raise ValueError("Promo code expired")
        
    if subtotal < code_obj["minOrder"]:
        raise ValueError("Order subtotal is below minimum required")
        
    if code_obj["type"] == "percentage":
        discount = subtotal * (code_obj["value"] / 100.0)
    elif code_obj["type"] == "fixed":
        discount = code_obj["value"]
    else:
        discount = 0.0
        
    return min(subtotal, round(discount, 2))

def calculate_surge(hour, day_of_week):
    if hour < 0 or hour > 23:
        raise ValueError("Invalid hour")
    if hour >= 22 or hour < 10:
        raise ValueError("Restaurant closed")
        
    day_of_week = day_of_week.lower()
    
    is_weekend = day_of_week in ["friday", "saturday", "sunday"]
    
    if is_weekend and 19 <= hour <= 21:
        return 1.8
        
    if 11 <= hour <= 13:
        return 1.3
        
    if 19 <= hour <= 21:
        return 1.5
        
    if day_of_week == "dimanche" or day_of_week == "sunday":
        return 1.2
        
    return 1.0

def calculate_order_total(items, distance, weight, promo_code_str, hour, day_of_week):
    if not items:
        raise ValueError("Cart is empty")
        
    subtotal = 0.0
    for item in items:
        if item["price"] < 0 or item["quantity"] < 0:
            raise ValueError("Invalid item price or quantity")
        if item["quantity"] > 0:
            subtotal += item["price"] * item["quantity"]
            
    if subtotal == 0.0:
        raise ValueError("Subtotal is 0")
        
    discount = apply_promo_code(subtotal, promo_code_str, PROMO_CODES)
        
    delivery_fee = calculate_delivery_fee(distance, weight)
    surge = calculate_surge(hour, day_of_week)
    
    final_delivery_fee = delivery_fee * surge
    
    total = subtotal - discount + final_delivery_fee
    
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "deliveryFee": round(final_delivery_fee, 2),
        "surge": surge,
        "total": round(total, 2)
    }

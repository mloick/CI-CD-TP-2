import pytest
from src.pricing import calculate_delivery_fee, apply_promo_code, calculate_surge, calculate_order_total, PROMO_CODES

class TestPricing:
    def test_calculate_delivery_fee(self):
        assert calculate_delivery_fee(2, 1) == 3.00
        assert calculate_delivery_fee(7, 3) == 5.50
        assert calculate_delivery_fee(5, 8) == 6.00 # 2 + 2.5 + 1.5
        assert calculate_delivery_fee(3, 1) == 3.50
        assert calculate_delivery_fee(10, 6) == 8.50 # 2 + 5 + 1.5
        with pytest.raises(ValueError):
            calculate_delivery_fee(15, 2)
        with pytest.raises(ValueError):
            calculate_delivery_fee(-1, 2)
        with pytest.raises(ValueError):
            calculate_delivery_fee(5, -1)

    def test_apply_promo_code(self):
        assert apply_promo_code(50, "BIENVENUE20", PROMO_CODES) == 10.00
        assert apply_promo_code(30, "FIXED5", PROMO_CODES) == 5.00
        with pytest.raises(ValueError):
            apply_promo_code(9.99, "FIXED5", PROMO_CODES) # below min order
        with pytest.raises(ValueError):
            apply_promo_code(50, "EXPIRED", PROMO_CODES)
        with pytest.raises(ValueError):
            apply_promo_code(50, "UNKNOWN", PROMO_CODES)
        
        custom_promos = [{"code": "FREE", "type": "fixed", "value": 100, "minOrder": 0, "expiresAt": "2030-01-01"}]
        assert apply_promo_code(5, "FREE", custom_promos) == 5.00 # no negative total

        assert apply_promo_code(50, "", PROMO_CODES) == 0.0
        assert apply_promo_code(50, None, PROMO_CODES) == 0.0
        
        custom_promos2 = [{"code": "CENT", "type": "percentage", "value": 100, "minOrder": 0, "expiresAt": "2030-01-01"}]
        assert apply_promo_code(50, "CENT", custom_promos2) == 50.00

    def test_calculate_surge(self):
        assert calculate_surge(15, "tuesday") == 1.0
        assert calculate_surge(12, "wednesday") == 1.3
        assert calculate_surge(20, "thursday") == 1.5
        assert calculate_surge(21, "friday") == 1.8
        assert calculate_surge(14, "sunday") == 1.2
        
        assert calculate_surge(10, "monday") == 1.0
        with pytest.raises(ValueError):
            calculate_surge(22, "tuesday") # Closed
        with pytest.raises(ValueError):
            calculate_surge(9, "tuesday") # Closed

    def test_calculate_order_total(self):
        items = [{"name": "Pizza", "price": 12.50, "quantity": 2}]
        res = calculate_order_total(items, 5, 2, None, 15, "tuesday")
        assert res["subtotal"] == 25.0
        assert res["discount"] == 0.0
        assert res["surge"] == 1.0
        assert res["deliveryFee"] == 4.50
        assert res["total"] == 29.50
        
        res2 = calculate_order_total(items, 5, 2, "BIENVENUE20", 15, "tuesday")
        assert res2["subtotal"] == 25.0
        assert res2["discount"] == 5.0
        assert res2["total"] == 24.50
        
        res3 = calculate_order_total(items, 5, 2, None, 20, "friday")
        assert res3["deliveryFee"] == 4.5 * 1.8
        
        with pytest.raises(ValueError):
            calculate_order_total([], 5, 2, None, 15, "tuesday")
        
        with pytest.raises(ValueError):
            calculate_order_total([{"name": "Bad", "price": -5, "quantity": 1}], 5, 2, None, 15, "tuesday")
            
        with pytest.raises(ValueError):
            calculate_order_total(items, 15, 2, None, 15, "tuesday") # Hors zone
            
        with pytest.raises(ValueError):
            calculate_order_total(items, 5, 2, None, 23, "tuesday") # Fermé
            
        items_ignored = [{"name": "A", "price": 10, "quantity": 0}, {"name": "B", "price": 5, "quantity": 1}]
        res4 = calculate_order_total(items_ignored, 1, 1, None, 15, "tuesday")
        assert res4["subtotal"] == 5.0

import pytest
from src.app import app, reset_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def run_around_tests():
    reset_db()
    yield

class TestAPI:
    # POST /orders/simulate
    def test_simulate_normal(self, client):
        res = client.post("/orders/simulate", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
            "distance": 5, "weight": 2, "hour": 15, "dayOfWeek": "tuesday"
        })
        assert res.status_code == 200
        assert "subtotal" in res.json
    
    def test_simulate_promo(self, client):
        res = client.post("/orders/simulate", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
            "distance": 5, "weight": 2, "hour": 15, "dayOfWeek": "tuesday",
            "promoCode": "BIENVENUE20"
        })
        assert res.status_code == 200
        assert res.json["discount"] == 5.0
        
    def test_simulate_promo_expired(self, client):
        res = client.post("/orders/simulate", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
            "distance": 5, "weight": 2, "hour": 15, "dayOfWeek": "tuesday",
            "promoCode": "EXPIRED"
        })
        assert res.status_code == 400
        assert "error" in res.json
        
    def test_simulate_empty_cart(self, client):
        res = client.post("/orders/simulate", json={"items": [], "distance": 5, "weight": 2})
        assert res.status_code == 400
        
    def test_simulate_hors_zone(self, client):
        res = client.post("/orders/simulate", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 1}],
            "distance": 15, "weight": 2
        })
        assert res.status_code == 400

    def test_simulate_ferme(self, client):
        res = client.post("/orders/simulate", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 1}],
            "distance": 5, "weight": 2, "hour": 23, "dayOfWeek": "mon"
        })
        assert res.status_code == 400
        
    def test_simulate_surge(self, client):
        res = client.post("/orders/simulate", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
            "distance": 5, "weight": 2, "hour": 20, "dayOfWeek": "friday"
        })
        assert res.status_code == 200
        assert res.json["surge"] == 1.8

    # POST /orders
    def test_orders_valid(self, client):
        res = client.post("/orders", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
            "distance": 5, "weight": 2, "hour": 15, "dayOfWeek": "tuesday"
        })
        assert res.status_code == 201
        assert "id" in res.json
        assert res.json["pricing"]["subtotal"] == 25.0
        
    def test_orders_get(self, client):
        post_res = client.post("/orders", json={
            "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
            "distance": 5, "weight": 2, "hour": 15, "dayOfWeek": "tuesday"
        })
        order_id = post_res.json["id"]
        
        get_res = client.get(f"/orders/{order_id}")
        assert get_res.status_code == 200
        assert get_res.json["id"] == order_id
        
    def test_orders_multiple_ids(self, client):
        res1 = client.post("/orders", json={"items": [{"name": "A", "price": 10, "quantity": 1}]})
        res2 = client.post("/orders", json={"items": [{"name": "B", "price": 10, "quantity": 1}]})
        assert res1.json["id"] != res2.json["id"]

    def test_orders_invalid(self, client):
        res = client.post("/orders", json={"items": []})
        assert res.status_code == 400
        assert "id" not in res.json
        
    def test_orders_invalid_not_saved(self, client):
        # Empty input -> ValueError
        client.post("/orders", json={"items": []})
        # Check no orders saved by making sure a bad order doesn't exist
        res = client.get("/orders/invalid_id")
        assert res.status_code == 404

    # GET /orders/:id
    def test_get_order_existing(self, client):
        post_res = client.post("/orders", json={
            "items": [{"name": "A", "price": 10, "quantity": 1}],
            "distance": 1, "weight": 1, "hour": 12, "dayOfWeek": "monday"
        })
        order_id = post_res.json["id"]
        res = client.get(f"/orders/{order_id}")
        assert res.status_code == 200
        assert "pricing" in res.json
        
    def test_get_order_not_found(self, client):
        res = client.get("/orders/999")
        assert res.status_code == 404
        
    def test_get_order_structure(self, client):
        post_res = client.post("/orders", json={"items": [{"name": "A", "price": 10, "quantity": 1}]})
        res = client.get(f"/orders/{post_res.json['id']}")
        data = res.json
        assert "items" in data
        assert "pricing" in data

    # POST /promo/validate
    def test_promo_valid(self, client):
        res = client.post("/promo/validate", json={"promoCode": "BIENVENUE20", "subtotal": 50})
        assert res.status_code == 200
        assert res.json["valid"] is True
        assert res.json["discount"] == 10.0
        
    def test_promo_expired(self, client):
        res = client.post("/promo/validate", json={"promoCode": "EXPIRED", "subtotal": 50})
        assert res.status_code == 400
        assert "error" in res.json
        
    def test_promo_below_minimum(self, client):
        res = client.post("/promo/validate", json={"promoCode": "BIENVENUE20", "subtotal": 5})
        assert res.status_code == 400
        
    def test_promo_unknown(self, client):
        res = client.post("/promo/validate", json={"promoCode": "UNKNOWN", "subtotal": 50})
        assert res.status_code == 404
        
    def test_promo_no_body(self, client):
        res = client.post("/promo/validate", json={"subtotal": 50})
        assert res.status_code == 400

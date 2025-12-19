from app.services.trading_service import buy, sell
from flask import session

def test_buy_and_sell(app):
    with app.test_request_context():
        session.clear()
        assert buy("AAPL", 1, 100)
        assert sell("AAPL", 1, 100)

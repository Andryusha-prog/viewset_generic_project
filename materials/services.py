import stripe
from config.settings import STRIPE_API_KEY
stripe.api_key = STRIPE_API_KEY

def create_stripe_price(price):
    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product_data={"name": "Price unit"},
    )

def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8002/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
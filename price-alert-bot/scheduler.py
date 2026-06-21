from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal
from models import Product, PriceHistory
from scraper import get_price
from bot import notify

def check_prices():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for product in products:
            price = get_price(product.url)
            if price is None:
                print(f"No se pudo obtener precio de {product.url}")
                continue

            history = PriceHistory(product_id=product.id, price=price)
            db.add(history)
            db.commit()

            print(f"{product.name}: {price}€ (objetivo: {product.target_price}€)")

            if price <= product.target_price:
                notify(
                    chat_id=product.chat_id,
                    product_name=product.name,
                    price=price,
                    url=product.url
                )
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_prices, "interval", hours=6)
    scheduler.start()
    return scheduler
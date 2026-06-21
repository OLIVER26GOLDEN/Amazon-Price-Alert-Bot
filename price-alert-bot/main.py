from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, get_db, Base
from models import Product
from scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Alert Bot")

scheduler = start_scheduler()

class ProductCreate(BaseModel):
    url: str
    name: str
    target_price: float
    chat_id: str

@app.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        url=product.url,
        name=product.name,
        target_price=product.target_price,
        chat_id=product.chat_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Producto añadido", "id": db_product.id}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(product)
    db.commit()
    return {"message": "Producto eliminado"}
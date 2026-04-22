from fastapi import APIRouter, Depends
from dependencies import get_session
from models import Product

product_router = APIRouter(tags=['products'])


@product_router.get('/products')
async def get_products(session=Depends(get_session)):
    products = session.query(Product).all()
    return products


from fastapi import FastAPI, HTTPException
import logging

app = FastAPI(
    title="Sylvanian Families - Serwis Produktów",
    description="Katalog produktów Sylvanian Families",
    version="1.0.0"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - PRODUCT SERVICE - %(message)s"
)

logger = logging.getLogger(__name__)

# Katalog produktów
products = {
    1: {
        "id": 1,
        "name": "Rodzina królików Chocolate",
        "price": 129.99,
        "category": "Figurki"
    },
    2: {
        "id": 2,
        "name": "Domek Red Roof Cozy Cottage",
        "price": 249.99,
        "category": "Domki"
    },
    3: {
        "id": 3,
        "name": "Zestaw przedszkole",
        "price": 189.99,
        "category": "Zestawy"
    },
    4: {
        "id": 4,
        "name": "Rodzina jeżyków",
        "price": 99.99,
        "category": "Figurki"
    },
    5: {
        "id": 5,
        "name": "Zestaw mebli",
        "price": 79.99,
        "category": "Akcesoria"
    },
    6: {
        "id": 6,
        "name": "Rodzina kotków",
        "price": 119.99,
        "category": "Figurki"
    }
}


@app.get("/")
async def home():
    return {
        "message": "Witaj w katalogu Sylvanian Families!",
        "service": "Product Service"
    }


@app.get("/products")
async def get_all_products():
    logger.info("Pobrano cały katalog produktów")
    return list(products.values())


@app.get("/products/{product_id}")
async def get_product(product_id: int):

    logger.info(
        f"Otrzymano zapytanie o produkt ID: {product_id}"
    )

    product = products.get(product_id)

    if product is None:
        logger.warning(
            f"Produkt ID {product_id} nie istnieje"
        )

        raise HTTPException(
            status_code=404,
            detail=f"Produkt o ID {product_id} nie istnieje"
        )

    logger.info(
        f"Znaleziono produkt: {product['name']}"
    )

    return product

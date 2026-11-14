
from fastapi import FastAPI, HTTPException
import httpx
import logging

app = FastAPI(
    title="Sylvanian Families - Serwis Magazynowy",
    description="Zarządzanie stanem magazynowym produktów",
    version="1.0.0"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - STOCK SERVICE - %(message)s"
)

logger = logging.getLogger(__name__)

# Adres pierwszego mikroserwisu
PRODUCT_SERVICE_URL = "http://127.0.0.1:8001"

# Stany magazynowe produktów
stock = {
    1: 12,
    2: 5,
    3: 8,
    4: 0,
    5: 20,
    6: 7
}


@app.get("/")
async def home():
    return {
        "message": "Witaj w magazynie Sylvanian Families!",
        "service": "Stock Service"
    }


@app.get("/stock/{product_id}")
async def get_stock(product_id: int):

    logger.info(
        f"Otrzymano zapytanie o produkt ID: {product_id}"
    )

    # Kontakt z Serwisem Produktów
    logger.info(
        f"Wysyłanie zapytania do Product Service: "
        f"/products/{product_id}"
    )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:

            response = await client.get(
                f"{PRODUCT_SERVICE_URL}/products/{product_id}"
            )

        # Produkt nie istnieje
        if response.status_code == 404:

            logger.warning(
                f"Produkt {product_id} nie istnieje "
                f"według Product Service"
            )

            raise HTTPException(
                status_code=404,
                detail=f"Produkt o ID {product_id} nie istnieje"
            )

        response.raise_for_status()

        product = response.json()

    except HTTPException:
        raise

    except httpx.RequestError as error:

        logger.error(
            f"Błąd komunikacji: {error}"
        )

        raise HTTPException(
            status_code=503,
            detail="Serwis Produktów jest niedostępny"
        )

    except httpx.HTTPStatusError as error:

        logger.error(
            f"Błędna odpowiedź Product Service: {error}"
        )

        raise HTTPException(
            status_code=502,
            detail="Błąd odpowiedzi Serwisu Produktów"
        )

    # Pobranie ilości produktu
    quantity = stock.get(product_id, 0)

    logger.info(
        f"Produkt: {product['name']}"
    )

    logger.info(
        f"Ilość w magazynie: {quantity}"
    )

    return {
        "productId": product_id,
        "productName": product["name"],
        "category": product["category"],
        "price": product["price"],
        "quantity": quantity
    }

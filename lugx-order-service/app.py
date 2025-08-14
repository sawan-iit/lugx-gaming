
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "5432")

# DB_HOST = "postgres-lugx.c12ayyuc8016.ap-southeast-1.rds.amazonaws.com"
# DB_USER = "lugxuser"
# DB_PASS = "lugxuser"
# DB_NAME = "postgres"
# DB_PORT = "5432"

# Database connection function
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME,
        port=DB_PORT
    )

# Request model for new order
class Order(BaseModel):
    cart_items: str
    total_price: float

@app.get("/orders")
def get_orders():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"orders": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders")
def add_order(order: Order):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (cart_items, total_price) VALUES (%s, %s)",
            (order.cart_items, order.total_price)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Order saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from typing import List

app = FastAPI()

#DB_HOST = os.getenv("DB_HOST")
#DB_USER = os.getenv("DB_USER")
#DB_PASS = os.getenv("DB_PASS")
#DB_NAME = os.getenv("DB_NAME")
#DB_PORT = os.getenv("DB_PORT", "5432")


DB_HOST = "postgres-lugx.c12ayyuc8016.ap-southeast-1.rds.amazonaws.com"
DB_USER = "lugxuser"
DB_PASS = "lugxuser"
DB_NAME = "postgres"
DB_PORT = "5432"


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME,
        port=DB_PORT
    )


class Game(BaseModel):
    name: str
    category: str
    release_date: str
    price: float


@app.get("/games")
def get_games():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, release_date, price FROM games")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "release_date": str(row[3]),
                "price": float(row[4])
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/games", status_code=201)
def add_game(game: Game):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO games (name, category, release_date, price) VALUES (%s, %s, %s, %s)",
            (game.name, game.category, game.release_date, game.price)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Game added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


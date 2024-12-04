from fastapi import FastAPI
from app.book.router import router as router_book

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Добро пожаловать! Данное приложение осуществляет "
                       "простое управление CRUD операциями по работе с библиотекой книг!"}


app.include_router(router_book)

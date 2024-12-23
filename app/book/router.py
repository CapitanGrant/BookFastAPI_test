import json

import redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.book.dao import BooksDAO
from app.book.schemas import BookFilter, BookID, BookCreate, BookUpdate, BookValues
from app.dao.session_maker import TransactionSessionDep, SessionDep
from app.exceptions import BookAlreadyExistsException, ExistingBookIDException
from app.book.rb import RBBook
from app.book.utils import backup_json, get_redis_client

router = APIRouter(prefix="/book", tags=["Book"])


@router.get("/all_books/", summary="Получить список всех книг")
async def get_all_books(redis_client: redis.Redis = Depends(get_redis_client), session: AsyncSession = SessionDep):
    cache_key: str = "all_books"
    cache = redis_client.get(cache_key)
    if cache:
        print('Serving data from cache')
        return json.loads(cache)
    data = await BooksDAO.find_all(session=session, filters=None)
    serialized_data = json.dumps([book.to_dict() for book in data])
    redis_client.set(cache_key, serialized_data, ex=3600)
    return data


@router.get("/get_book_by_id/", summary="Получить книгу по id")
async def get_book_by_id(id: int, session: AsyncSession = SessionDep,
                         redis_client: redis.Redis = Depends(get_redis_client)):
    cache_key: str = "get_book_by_id"
    cache = redis_client.get(cache_key)
    if cache:
        json_string = json.loads(cache.decode('utf-8'))
        if json_string['id'] == id:
            print('Serving data from cache')
            return json.loads(cache)
    rez = await BooksDAO.find_one_or_none_by_id(session=session, data_id=id)
    serialized_data = json.dumps(rez.to_dict())
    redis_client.set(cache_key, serialized_data, ex=360)
    if rez is None:
        raise ExistingBookIDException
    return rez


@router.post("/create_book/", summary="Создать книгу")
async def create_book(book_data: BookCreate, session: AsyncSession = TransactionSessionDep) -> dict:
    book = await BooksDAO.find_one_or_none(session=session, filters=BookFilter(title=book_data.title))
    if book:
        raise BookAlreadyExistsException
    book_data_dict = book_data.model_dump()
    new_book = await BooksDAO.add(session=session, values=BookCreate(**book_data_dict))
    await backup_json(session)
    return {'message': f'Книга успешно внесена!', 'data': {'id': new_book.id, **book_data_dict}}


@router.post("/find_book/", summary="Найти книгу по определенным параметрам")
async def find_book(book_data: RBBook = Depends(), session: AsyncSession = SessionDep,
                    redis_client: redis.Redis = Depends(get_redis_client)):
    try:
        cache_key: str = "find_book"
        cache = redis_client.get(cache_key)
        print(cache)
        if cache:
            print('Serving data from cache')
            return json.loads(cache)
        rez = await BooksDAO.find_all(session=session, filters=BookFilter(**book_data.to_dict()))
        serialized_data = json.dumps(rez, default=str)
        redis_client.set(cache_key, serialized_data, ex=60)
        if rez is None:
            return {'message': f'Книга с указанными вами параметрами не найдена!'}
        return rez
    except Exception as e:
        print(e)
        return {'message': 'Недостаточно параметров для поиска!'}


@router.put("/update_book/", summary="Обновить сведения о книге")
async def update_book(book_id: BookID, book_data: BookUpdate, session: AsyncSession = TransactionSessionDep):
    rez = await BooksDAO.update(session=session, filters=book_id, values=book_data)
    if rez is None:
        return {'message': f'Не удалось обновить запись!'}
    await backup_json(session)
    return {'message': f'Успешно обновлена {rez} запись!'}


@router.put("/update_book_by_status/", summary="Обновить статус книги")
async def update_book(book_id: BookID, book_data: BookValues, session: AsyncSession = TransactionSessionDep):
    rez = await BooksDAO.update(session=session, filters=book_id, values=book_data)
    if rez is None:
        return {'message': f'Не удалось обновить запись!'}
    await backup_json(session)
    return {'message': f'Успешно обновлена {rez} запись!'}


@router.delete("/delete_book_by_id/", summary="Удалить книгу")
async def delete_book_by_id(book_id: BookID, session: AsyncSession = TransactionSessionDep):
    rez = await BooksDAO.delete(session=session, filters=book_id)
    if rez is None:
        return {'message': f'Вы пытаетесь удалить не существующую книгу!'}
    await backup_json(session)
    return {'message': f'Успешно удалена {rez} запись!'}

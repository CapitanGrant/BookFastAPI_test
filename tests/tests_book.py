import pytest

from tests.test_enpoints.create_book import TestCreateBook
from tests.test_enpoints.delete_book import TestDeleteBook
from tests.test_enpoints.get_all_book import TestGetAllBook
from tests.test_enpoints.find_book import TestFindBook
from tests.test_enpoints.get_book_by_id import TestGetBookByID
from tests.test_enpoints.update_book import TestUpdateBook
from tests.test_enpoints.update_book_status import TestUpdateBookStatus


@pytest.fixture
def book_payload():
    return {
        "title": "Капитал",
        "author": "Карл Маркс",
        "year": 1867,
        "status": True
    }


@pytest.mark.asyncio
async def test_get_all_object():
    '''Тест на получение списка всех книг.'''
    get_obj = TestGetAllBook()
    await get_obj.get_all_book()
    get_obj.check_response_is_200()


@pytest.mark.asyncio
async def test_create_book(book_payload):
    '''Тест на создание книги.'''
    create_obj = TestCreateBook()
    await create_obj.new_book(payload=book_payload)
    create_obj.check_response_is_200()
    create_obj.check_name(book_payload['title'])
    book_id = create_obj.response_json['data']['id']
    delete_obj = TestDeleteBook()
    await delete_obj.delete_book({'id': book_id})
    delete_obj.check_response_is_200()


@pytest.mark.asyncio
async def test_get_book_by_id(obj_id):
    '''Тест на получение книги по ID.'''
    get_obj = TestGetBookByID()
    await get_obj.get_book_by_id(obj_id)
    get_obj.check_response_is_200()
    await get_obj.get_book_by_id(9999)
    get_obj.check_response_is_409()


@pytest.mark.parametrize('params, expected_status', [
    ({"title": "Капитал"}, 200),
    ({"title": "Несуществующая книга"}, 200),
    ({"author": "Карл Маркс"}, 200),
    ({"year": 1867}, 200),
    ({"status": 'true'}, 200),
    ({}, 200),

])
@pytest.mark.asyncio
async def test_find_book(params, expected_status, obj_id):
    '''Тест на поиск книги по заданным параметрам.'''
    find_obj = TestFindBook()
    await find_obj.find_book(obj_id, params)
    assert find_obj.response.status == expected_status


@pytest.mark.asyncio
async def test_update_book_by_status(obj_id):
    '''Тест на обновление статуса книги.'''
    payload_put = {
        "book_id": {
            "id": obj_id
        },
        "book_data": {
            "status": 'false'
        }
    }
    payload_put_exception = {
        "book_id": {
            "id": 9999
        },
        "book_data": {
            "status": 'false'
        }
    }
    update_obj = TestUpdateBookStatus()
    await update_obj.update_book_by_status(payload_put)
    update_obj.check_response_is_200()
    await update_obj.update_book_by_status(payload_put_exception)
    update_obj.check_response_is_200()


@pytest.mark.asyncio
async def test_update_book(obj_id):
    '''Тест на обновление книги по параметрам.'''
    payload_put = {
        "book_id": {
            "id": obj_id
        },
        "book_data": {
            "title": "Основы маркетинга",
            "author": "Филип Котлер",
            "year": 1984,
            "status": 'true'
        }
    }
    payload_put_exception = {
        "book_id": {
            "id": 9999
        },
        "book_data": {
            "title": "Основы маркетинга",
            "author": "Филип Котлер",
            "year": 1984,
            "status": 'true'
        }
    }
    update_obj = TestUpdateBook()
    await update_obj.update_book(payload_put)
    update_obj.check_response_is_200()
    await update_obj.update_book(payload_put_exception)
    update_obj.check_response_is_200()


@pytest.mark.asyncio
async def test_delete_book(book_payload):
    '''Тест на удаление книги.'''
    create_obj = TestCreateBook()
    await create_obj.new_book(payload=book_payload)
    create_obj.check_response_is_200()
    create_obj.check_name(book_payload['title'])
    delete_obj = TestDeleteBook()
    data = create_obj.response_json['data']['id']
    await delete_obj.delete_book({"id": data})
    delete_obj.check_response_is_200()
    get_obj = TestGetBookByID()
    await get_obj.get_book_by_id(data)
    get_obj.check_response_is_409()

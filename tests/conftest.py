import pytest
from tests.test_enpoints.create_book import TestCreateBook
from tests.test_enpoints.delete_book import TestDeleteBook


@pytest.fixture
def create_book():
    return TestCreateBook()


@pytest.fixture
def del_book():
    return TestDeleteBook()


@pytest.fixture
async def obj_id(request, create_book: TestCreateBook, del_book: TestDeleteBook):
    payload = {
        "title": "Капитал",
        "author": "Карл Маркс",
        "year": 1867,
        "status": True
    }
    try:
        await create_book.new_book(payload)
        yield create_book.response_json['data']['id']
    finally:
        if create_book.response_json and "data" in create_book.response_json:
            book_id = create_book.response_json['data']['id']
            await del_book.delete_book({"id": book_id})

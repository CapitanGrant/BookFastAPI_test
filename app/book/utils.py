import json
from app.book.dao import BooksDAO


async def backup_json(session):
    data = await BooksDAO.find_all(session=session, filters=None)
    data = [data.to_dict() for data in data]
    with open('backup_books.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

import json
from app.book.dao import BooksDAO
import redis

from app.config import redis_config


def get_redis_client():
    try:
        client = redis.Redis(host=redis_config.host,
                             port=redis_config.port,
                             )
        client.ping()
        return client
    except redis.exceptions.ConnectionError as e:
        print(f"Redis ошибка подключения: {e}")
        raise


async def backup_json(session):
    data = await BooksDAO.find_all(session=session, filters=None)
    data = [data.to_dict() for data in data]
    with open('backup_books.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

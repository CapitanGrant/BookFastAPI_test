import aiohttp
from tests.test_enpoints.base_endpoint import BaseEndpoint


class TestDeleteBook(BaseEndpoint):
    async def delete_book(self, payload):
        async with aiohttp.ClientSession() as session:
            async with session.delete("http://127.0.0.1:8000/book/delete_book_by_id/", json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()

    def check_name(self, title):
        assert self.response_json['data']['title'] == title

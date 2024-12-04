import aiohttp
from tests.test_enpoints.base_endpoint import BaseEndpoint


class TestUpdateBookStatus(BaseEndpoint):

    async def update_book_by_status(self, payload):
        async with aiohttp.ClientSession() as session:
            async with session.put("http://127.0.0.1:8000/book/update_book_by_status/", json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()

    def check_name(self, title):
        assert self.response_json['data']['title'] == title

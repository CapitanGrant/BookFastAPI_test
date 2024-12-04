import aiohttp
from tests.test_enpoints.base_endpoint import BaseEndpoint


class TestCreateBook(BaseEndpoint):
    async def new_book(self, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:8000/book/create_book/", json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()

    def check_name(self, title):
        assert self.response_json['data']['title'] == title



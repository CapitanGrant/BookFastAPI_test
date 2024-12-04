import aiohttp
from tests.test_enpoints.base_endpoint import BaseEndpoint


class TestUpdateBook(BaseEndpoint):

    async def update_book(self, payload):
        async with aiohttp.ClientSession() as session:
            async with session.put("http://127.0.0.1:8000/book/update_book/", json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()


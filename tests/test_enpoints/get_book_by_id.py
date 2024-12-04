import aiohttp
from tests.test_enpoints.base_endpoint import BaseEndpoint


class TestGetBookByID(BaseEndpoint):

    async def get_book_by_id(self, object_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://127.0.0.1:8000/book/get_book_by_id/?id={object_id}") as response:
                self.response = response
                self.response_json = await self.response.json()

    def check_response_is_409(self):
        assert self.response.status == 409

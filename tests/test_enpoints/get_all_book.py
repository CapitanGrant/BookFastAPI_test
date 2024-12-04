import aiohttp
from tests.test_enpoints.base_endpoint import BaseEndpoint


class TestGetAllBook(BaseEndpoint):

    async def get_all_book(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/book/all_books/") as response:
                self.response = response

    def check_response_is_404(self):
        assert self.response.status == 404

class RBBook:
    def __init__(self, book_id: int | None = None,
                 title: str | None = None,
                 author: str | None = None,
                 year: int | None = None,
                 status: str | None = None):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        return {key: value for key, value in {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }.items() if value is not None}

from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Book(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[bool] = mapped_column(default=True, server_default=text("'true'"))

    def to_dict(self) -> dict:
        return {key: value for key, value in {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }.items() if value is not None}
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=50, description="Название книги")
    author: str | None = Field(None, min_length=2, max_length=50, description="Автор книги")
    year: int | None = Field(None, gt=0, lt=2024, description="Год издания")
    status: bool | None = Field(True, description="Статус книги: True - в наличии, False - выдана")


class BookCreate(BookBase):
    title: str = Field(..., min_length=1, max_length=50, description="Название книги обязательно")
    author: str = Field(..., min_length=2, max_length=50, description="Автор обязателен")
    year: int = Field(..., gt=0, lt=2024, description="Год издания обязателен")


class BookUpdate(BookBase):
    pass


class BookFilter(BookBase):
    pass


class BookID(BaseModel):
    id: int = Field(..., description="ID книги")


class BookValues(BaseModel):
    status: bool = Field(default="true", description="Статус книги: True - в наличии, False - выдана")

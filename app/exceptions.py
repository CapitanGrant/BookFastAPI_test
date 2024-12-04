from fastapi import status, HTTPException

BookAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Книга уже существует!')

ExistingBookIDException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail='Указанный вами id отсутствует!')

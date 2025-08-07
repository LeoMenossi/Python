from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    user: str
    password: str

    class Config:
        from_attributes = True

class QuerySchema(BaseModel):
    query: str
    page_size: int
    page_number: int

    class Config:
        from_attributes = True

class WhereSchema(BaseModel):
    where: list
    group: Optional[str] = None
    order: Optional[str] = None
    page_size: Optional[int] = None
    page_number: Optional[int] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel

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
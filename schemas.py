from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    usuario: str
    senha: str

    class Config:
        from_attributes = True
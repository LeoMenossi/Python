from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import cria_token, existe_usuario, cria_usuario, autentica_usuario
from main import pwd_context
from schemas import UsuarioSchema
from dependencies import valida_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/token")
async def auth(usuario_schema: UsuarioSchema):
    usuario = autentica_usuario(usuario_schema.user, usuario_schema.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    else:
        access_token = cria_token(data={"sub": usuario})
        return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login")
async def login(usuario_schema: OAuth2PasswordRequestForm = Depends()):
    usuario = autentica_usuario(usuario_schema.username, usuario_schema.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    else:
        access_token = cria_token(data={"sub": usuario})
        return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/create")
async def create_account(usuario_schema: UsuarioSchema, valid_token = Depends(valida_token)):
    if valid_token:
        count = existe_usuario(usuario_schema.user)
        if count > 0:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado")
        else:
            senha_criptografada = pwd_context.hash(usuario_schema.password)
            cria_usuario(usuario_schema.user, senha_criptografada)
            return {"mensagem": "Usuário inserido com sucesso"}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")


from fastapi import Depends, HTTPException
from main import oauth2_scheme, SECRET_KEY, ALGORITHM
from auth import existe_usuario
from jose import jwt, JWTError

async def valida_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        count = existe_usuario(usuario)
        if count > 0:
            return True 
        else:
            return False
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado", headers={"WWW-Authenticate": "Bearer"})
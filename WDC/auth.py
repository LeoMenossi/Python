from main import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY,ALGORITHM, connection_db_user
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
import pyodbc

def existe_usuario(usuario):
    try:
        connection = connection_db_user()
        cursor = connection.cursor()
        cursor.execute("SELECT USUARIO FROM apiUser WHERE USUARIO = ?", (usuario))
        count = len(cursor.fetchall())
        return count
    except pyodbc.ProgrammingError as e:
        raise HTTPException(status_code=400, detail=f'Erro no SQL: {str(e)}')
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar query: {str(e)}")
    finally:
        connection.close()

def autentica_usuario(usuario, senha):
    try:
        connection = connection_db_user()
        cursor = connection.cursor()
        cursor.execute("SELECT USUARIO, SENHA FROM apiUser WHERE USUARIO = ?", (usuario))
        row = cursor.fetchone()
        
        if not row:
            return
        else:
            usuario_encontrado = row[0]
            senha_encontrada = row[1]
            if not pwd_context.verify(senha, senha_encontrada):
                return False
            return usuario_encontrado
    except pyodbc.ProgrammingError as e:
        raise HTTPException(status_code=400, detail=f'Erro no SQL: {str(e)}')
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar query: {str(e)}")
    finally:
        connection.close()

def cria_usuario(usuario, senha):
    try:
        connection = connection_db_user()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO apiUser (USUARIO, SENHA) VALUES (?,?)", (usuario, senha))
        connection.commit()
        return 
    except pyodbc.ProgrammingError as e:
        raise HTTPException(status_code=400, detail=f'Erro no SQL: {str(e)}')
    except pyodbc.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao executar query: {str(e)}")
    finally:
        connection.close()

def cria_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
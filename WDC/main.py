from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from passlib.context import CryptContext
import pyodbc
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN"))
DRIVER = os.getenv("DRIVER")
SERVER = os.getenv("SERVER")
SERVER_USER = os.getenv("SERVER_USER")
DATABASE = os.getenv("DATABASE")
DATABASE_USER = os.getenv("DATABASE_USER")
UID = os.getenv("UID")
PWD = os.getenv("PWD")

def connection_db():
    try:
        connection = pyodbc.connect(
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={UID};'
            f'PWD={PWD}'
        )
        return connection
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f'Erro na conexão com o banco: {str(e)}')

def connection_db_user():
    try:
        connection = pyodbc.connect(
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER_USER};'
            f'DATABASE={DATABASE_USER};'
            f'UID={UID};'
            f'PWD={PWD}'
        )
        return connection
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f'Erro na conexão com o banco de usuários: {str(e)}')

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

from auth_routes import auth_router
from query_routes import query_router

app.include_router(auth_router)
app.include_router(query_router)

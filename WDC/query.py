from main import connection_db
from fastapi import HTTPException
import os
import pyodbc

def lista_queries():
    queries = []
    try:
        with os.scandir('queries/') as entradas:
            for entrada in entradas:
                if entrada.is_file():
                    queries.append(entrada.name)
        return queries
    except PermissionError:
        raise HTTPException(status_code=403, detail='Sem permissão a pasta de queries')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Diretório das queries não encontrado')

def get_query(alias: str):
    try:
        with open(f"queries/{alias}.txt", "r") as arquivo:
            query = arquivo.read()

        return query
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de query não encontrado")


def exec_query(query: str, page_size: int, page_number: int):
    offset = (page_number - 1) * page_size
    query = query + f" OFFSET {str(offset)} ROWS FETCH NEXT {str(page_size)} ROWS ONLY"
    try:
        conn = connection_db()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        colunas = [coluna[0] for coluna in cursor.description]
        return [dict(zip(colunas, linha)) for linha in resultado]
    except pyodbc.ProgrammingError as e:
        raise HTTPException(status_code=400, detail=f'Erro no SQL: {str(e)}')
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar query: {str(e)}")
    finally:
        conn.close()

def executa_query(query: str):
    try:
        conn = connection_db()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        colunas = [coluna[0] for coluna in cursor.description]
        return [dict(zip(colunas, linha)) for linha in resultado]
    except pyodbc.ProgrammingError as e:
        raise HTTPException(status_code=400, detail=f'Erro no SQL: {str(e)}')
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar query: {str(e)}")
    finally:
        conn.close()
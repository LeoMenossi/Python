from fastapi import APIRouter, Depends, HTTPException
import query as Query
from dependencies import valida_token

query_router = APIRouter(prefix="/query", tags=["query"])

@query_router.get("/")
async def lista_query(valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela listagem de todas as queries que temos disponíveis em nossa API
    """
    if valid_token:
        queries = Query.lista_queries()
        return {"queries" : queries}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

@query_router.get("/{tabela}")
async def read_query(tabela: str, valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela leitura do arquivo txt para consulta da query do arquivo
    """
    if valid_token:
        query = Query.get_query((tabela.upper()))
        return {"query": query}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

@query_router.get("/consultar/{tabela}")
async def consult_query(tabela: str, valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela consulta da query
    """
    if valid_token:
        query = Query.get_query(tabela.upper())
        resultado = Query.exec_query(query)
        return {"result": resultado}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")


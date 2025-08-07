from fastapi import APIRouter, Depends, HTTPException
import query as Query
from dependencies import valida_token
from schemas import QuerySchema, WhereSchema

query_router = APIRouter(prefix="/query", tags=["query"])

@query_router.get("/list")
async def lista_query(valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela listagem de todas as queries que temos disponíveis em nossa API
    """
    if valid_token:
        queries = Query.lista_queries()
        return {"queries" : queries}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

@query_router.get("/consult/{table}")
async def read_query(table: str, valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela leitura do arquivo txt para consulta da query do arquivo
    """
    if valid_token:
        query = Query.get_query((table.upper()))
        return {"query": query}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

@query_router.get("/execute")
async def consult_query(query_schema: QuerySchema, valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela consulta da query
    """
    if valid_token:
        resultado = Query.exec_query(query_schema.query, query_schema.page_size, query_schema.page_number)
        total = len(Query.executa_query(query_schema.query))
        return {"result": resultado,
                "total": total,
                "page": query_schema.page_number,
                "size": query_schema.page_size,
                "pages": round(total / query_schema.page_size)} 
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

@query_router.get("/execute/{table}")
async def consult_query(table: str, valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela consulta da query
    """
    if valid_token:
        query = Query.get_query(table.upper())
        resultado = Query.executa_query(query)
        return {"result": resultado}
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

@query_router.get("/execute/where/{table}")
async def consult_query(table: str, where_schema: WhereSchema, valid_token = Depends(valida_token)):
    """
    Endpoint responsável pela consulta da query com parâmetros via body
    """
    if valid_token:
        query = Query.get_query(table.upper(), where_schema.where, where_schema.group, where_schema.order)
        if not where_schema.page_size:
            resultado = Query.executa_query(query)
            return {"result": resultado}
        elif where_schema.page_number and where_schema.order:
            resultado = Query.exec_query(query, where_schema.page_size, where_schema.page_number)
            total = len(Query.executa_query(query))
            return {"result": resultado,
                    "total": total,
                    "page": where_schema.page_number,
                    "size": where_schema.page_size,
                    "pages": round(total / where_schema.page_size)} 
        else:
            raise HTTPException(status_code=404, detail="Para usar o recurso de paginação, acrescentar o 'order'")
    else:
        raise HTTPException(status_code=400, detail="Acesso Inválido")

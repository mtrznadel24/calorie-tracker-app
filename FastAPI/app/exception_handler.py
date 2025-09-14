from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import NotFoundError, ConflictError


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(request: Request, exc: NotFoundError):
        return JSONResponse(content={"message": str(exc)}, status_code=404)

    @app.exception_handler(ConflictError)
    async def conflict_exception_handler(request: Request, exc: ConflictError):
        return JSONResponse(content={"message": str(exc)}, status_code=409)
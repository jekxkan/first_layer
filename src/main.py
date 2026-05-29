from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers.router import router
from schemas.base_responses import ErrorDetail, ErrorResponse

app = FastAPI(
    title="Первый слой",
    description="Сервис для получения оптимальных параметров"
                " печати на основе принтера, пластика и геометрии STL-файла",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    status_code_map = {
        404: "RESOURCE_NOT_FOUND",
        400: "BAD_REQUEST",
        422: "VALIDATION_ERROR",
    }
    error_code = status_code_map.get(exc.status_code, "HTTP_ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                code=error_code,
                message=str(exc.detail),
                details={}
            )
        ).model_dump()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Ошибка валидации входных данных",
                details={"errors": exc.errors()}
            )
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="Внутренняя ошибка сервера",
                details={}
            )
        ).model_dump()
    )

@app.get("/health")
def root():
    return {"code": 200}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
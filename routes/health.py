from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def health():
    content = {"health": "OK"}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)

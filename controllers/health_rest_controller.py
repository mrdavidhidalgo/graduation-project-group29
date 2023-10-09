from fastapi import APIRouter

router = APIRouter()
from services import logs
LOGGER = logs.get_logger()
@router.get("/health", status_code=200)
async def health():
    LOGGER.info("health")
    return {"msg": "Up"}
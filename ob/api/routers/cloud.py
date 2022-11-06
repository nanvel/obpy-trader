from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from ob.containers.api import ApiContainer
from ob.api.use_cases import LoadCloudFiles


router = APIRouter()


@router.get("/api/cloud/files")
@inject
async def cloud_files(
    load_cloud_files: LoadCloudFiles = Depends(Provide[ApiContainer.load_cloud_files]),
):
    files = await load_cloud_files.call(exchange_name="binance", symbol_name="BTCUSDT")
    return {"data": files}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.schemas.operating_time_log import OperatingTimeLogCreate, OperatingTimeLogRead, OperatingTimeLogUpdate
from app.crud.operating_time_log import (
    create_operating_time_log,
    get_operating_time_log,
    list_operating_time_logs,
    update_operating_time_log,
    delete_operating_time_log,
)

router = APIRouter(prefix='/operating-time-logs', tags=['operating-time-logs'])

@router.post('', response_model=OperatingTimeLogRead, status_code=status.HTTP_201_CREATED)
async def create_operating_time_log_ep(
    payload: OperatingTimeLogCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    return await create_operating_time_log(session, payload)

@router.get('', response_model=list[OperatingTimeLogRead])
async def list_operating_time_log_ep(
    uav_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await list_operating_time_logs(session, uav_id, limit, offset)

@router.get('/{log_id}', response_model=OperatingTimeLogRead)
async def get_operating_time_log_ep(log_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await get_operating_time_log(session, log_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Operating time log not found')
    return obj

@router.patch('/{log_id}', response_model=OperatingTimeLogRead)
async def update_operating_time_log_ep(
    log_id: int, payload: OperatingTimeLogUpdate, session: AsyncSession = Depends(db_helper.get_session)
):
    obj = await update_operating_time_log(session, log_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail='Operating time log not found')
    return obj

@router.delete('/{log_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_operating_time_log_ep(log_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    ok = await delete_operating_time_log(session, log_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Operating time log not found')

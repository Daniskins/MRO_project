from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.schemas.maintenance_record import MaintenanceRecordCreate, MaintenanceRecordRead, MaintenanceRecordUpdate
from app.crud.maintenance_record import (
    create_maintenance_record,
    get_maintenance_record,
    list_maintenance_records,
    update_maintenance_record,
    delete_maintenance_record,
)

router = APIRouter(prefix='/maintenance-records', tags=['maintenance-records'])

@router.post('', response_model=MaintenanceRecordRead, status_code=status.HTTP_201_CREATED)
async def create_maintenance_record_ep(
    payload: MaintenanceRecordCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    return await create_maintenance_record(session, payload)

@router.get('', response_model=list[MaintenanceRecordRead])
async def list_maintenance_record_ep(
    uav_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await list_maintenance_records(session, uav_id, limit, offset)

@router.get('/{record_id}', response_model=MaintenanceRecordRead)
async def get_maintenance_record_ep(record_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await get_maintenance_record(session, record_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Maintenance record not found')
    return obj

@router.patch('/{record_id}', response_model=MaintenanceRecordRead)
async def update_maintenance_record_ep(
    record_id: int, payload: MaintenanceRecordUpdate, session: AsyncSession = Depends(db_helper.get_session)
):
    obj = await update_maintenance_record(session, record_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail='Maintenance record not found')
    return obj

@router.delete('/{record_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_record_ep(record_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    ok = await delete_maintenance_record(session, record_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Maintenance record not found')

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.schemas.maintenance_type import MaintenanceTypeCreate, MaintenanceTypeRead, MaintenanceTypeUpdate
from app.crud.maintenance_type import (
    create_maintenance_type,
    get_maintenance_type,
    list_maintenance_types,
    update_maintenance_type,
    delete_maintenance_type,
)

router = APIRouter(prefix='/maintenance-types', tags=['maintenance-types'])

@router.post('', response_model=MaintenanceTypeRead, status_code=status.HTTP_201_CREATED)
async def create_maintenance_type_ep(
    payload: MaintenanceTypeCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    return await create_maintenance_type(session, payload)

@router.get('', response_model=list[MaintenanceTypeRead])
async def list_maintenance_type_ep(
    limit: int = 100, offset: int = 0, session: AsyncSession = Depends(db_helper.get_session)
):
    return await list_maintenance_types(session, limit, offset)

@router.get('/{type_id}', response_model=MaintenanceTypeRead)
async def get_maintenance_type_ep(type_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await get_maintenance_type(session, type_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Maintenance type not found')
    return obj

@router.patch('/{type_id}', response_model=MaintenanceTypeRead)
async def update_maintenance_type_ep(
    type_id: int, payload: MaintenanceTypeUpdate, session: AsyncSession = Depends(db_helper.get_session)
):
    obj = await update_maintenance_type(session, type_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail='Maintenance type not found')
    return obj

@router.delete('/{type_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_type_ep(type_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    ok = await delete_maintenance_type(session, type_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Maintenance type not found')

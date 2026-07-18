from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.schemas.uav import UavCreate, UavRead, UavUpdate
from app.crud.uav import (
    create_uav,
    get_uav,
    list_uavs,
    update_uav,
    delete_uav,
    get_uav_maintenance_status,
)

router = APIRouter(prefix='/uavs', tags=['uavs'])

@router.post('', response_model=UavRead, status_code=status.HTTP_201_CREATED)
async def create_uav_ep(payload: UavCreate, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await create_uav(session, payload)
    return obj

@router.get('', response_model=list[UavRead])
async def list_uav_ep(limit: int=100, offset: int=0, session: AsyncSession = Depends(db_helper.get_session)):
    return await list_uavs(session, limit, offset)

@router.get('/{uav_id}', response_model=UavRead)
async def get_uav_ep(uav_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await get_uav(session, uav_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Uav not found')
    return obj

@router.get('/{uav_id}/maintenance-status')
async def get_uav_maintenance_status_ep(uav_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    status_data = await get_uav_maintenance_status(session, uav_id)
    if not status_data:
        raise HTTPException(status_code=404, detail='Uav not found')
    return status_data

@router.patch('/{uav_id}', response_model=UavRead)
async def update_uav_ep(uav_id: int, payload: UavUpdate, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await update_uav(session, uav_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail='Uav not found')
    return obj

@router.delete('/{uav_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_uav_ep(uav_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    obj = await delete_uav(session, uav_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Uav not found')

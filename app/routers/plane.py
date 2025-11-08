from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.db_helper import db_helper
from app.schemas.plane import PlaneBase, PlaneCreate, PlaneRead, PlaneUpdate
from app.crud.plane import create_plane, get_plane, list_planes, update_plane, delete_plane

router = APIRouter(prefix='/planes', tags=['planes'])

async def get_session() -> AsyncSession:
    async with db_helper.session_factor() as session:
        yield session

@router.post('', response_model=PlaneRead, status_code=status.HTTP_201_CREATED)
async def create_plane_ep(payload: PlaneCreate, session: AsyncSession = Depends(get_session)):
    obj = await create_plane(session, payload)
    await session.commit()
    return obj

@router.get('', response_model=list[PlaneRead])
async def list_plane_ep(limit: int=100, offset: int=0, session: AsyncSession = Depends(get_session)):
    return await list_planes(session, limit, offset)

@router.get('/{plane_id}', response_model=PlaneRead)
async def get_plane_ep(plane_id: int, session: AsyncSession = Depends(get_session)):
    obj = get_plane(session, plane_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Plane not found')
    return obj

@router.delete('/{plane_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_plane_ep(plane_id: int, session: AsyncSession = Depends(get_session)):
    obj = await delete_plane(session, plane_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Plane not found')
    await session.commit()
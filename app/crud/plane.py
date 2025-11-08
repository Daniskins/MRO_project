from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.core.models.plane import Plane
from app.schemas.plane import PlaneCreate, PlaneUpdate

async def create_plane(session: AsyncSession, data: PlaneCreate) -> Plane:
    plane_obj = Plane(**data.model_dump())
    session.add(plane_obj)
    await session.flush()
    await session.refresh(plane_obj)
    return plane_obj

async def get_plane(session: AsyncSession, plane_id: int) -> Plane | None:
    result = await session.execute(select(Plane).where(Plane.id == plane_id))
    return result.scalar_one_or_none()

async def list_planes(session: AsyncSession, limit: int=100, offset: int=0) -> list[Plane]:
    result = await session.execute(select(Plane).offset(offset).limit(limit))
    return list(result.scalars().all())

async def update_plane(session: AsyncSession, plane_id: int, data: PlaneUpdate) -> Plane | None:
    payload = {key: value for key, value in data.model_dump(exclude_unset=True).items()}
    if not payload:
        return await get_plane(session, plane_id)
    await session.execute(update(Plane).where(Plane.id==plane_id).values(**payload))
    await session.flush()
    return await get_plane(session, plane_id)

async def delete_plane(session: AsyncSession, plane_id: int) -> bool:
    result = await session.execute(delete(Plane).where(Plane.id==plane_id))
    return result.rowcount > 0

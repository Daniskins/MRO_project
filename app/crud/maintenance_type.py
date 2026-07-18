from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.models.maintenance_type import MaintenanceType
from app.schemas.maintenance_type import MaintenanceTypeCreate, MaintenanceTypeUpdate


async def create_maintenance_type(session: AsyncSession, data: MaintenanceTypeCreate) -> MaintenanceType:
    obj = MaintenanceType(**data.model_dump())
    session.add(obj)
    await session.flush()
    await session.refresh(obj)
    return obj


async def get_maintenance_type(session: AsyncSession, type_id: int) -> MaintenanceType | None:
    result = await session.execute(select(MaintenanceType).where(MaintenanceType.id == type_id))
    return result.scalar_one_or_none()


async def list_maintenance_types(session: AsyncSession, limit: int = 100, offset: int = 0) -> list[MaintenanceType]:
    result = await session.execute(select(MaintenanceType).offset(offset).limit(limit))
    return list(result.scalars().all())


async def update_maintenance_type(
    session: AsyncSession, type_id: int, data: MaintenanceTypeUpdate
) -> MaintenanceType | None:
    payload = {key: value for key, value in data.model_dump(exclude_unset=True).items()}
    if not payload:
        return await get_maintenance_type(session, type_id)
    await session.execute(update(MaintenanceType).where(MaintenanceType.id == type_id).values(**payload))
    await session.flush()
    return await get_maintenance_type(session, type_id)


async def delete_maintenance_type(session: AsyncSession, type_id: int) -> bool:
    result = await session.execute(delete(MaintenanceType).where(MaintenanceType.id == type_id))
    return result.rowcount > 0

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.models.uav import Uav
from app.models.maintenance_record import MaintenanceRecord
from app.schemas.uav import UavCreate, UavUpdate


async def create_uav(session: AsyncSession, data: UavCreate) -> Uav:
    uav_obj = Uav(**data.model_dump())
    session.add(uav_obj)
    await session.flush()
    await session.refresh(uav_obj)
    return uav_obj


async def get_uav(session: AsyncSession, uav_id: int) -> Uav | None:
    result = await session.execute(select(Uav).where(Uav.id == uav_id))
    return result.scalar_one_or_none()


async def list_uavs(session: AsyncSession, limit: int = 100, offset: int = 0) -> list[Uav]:
    result = await session.execute(select(Uav).offset(offset).limit(limit))
    return list(result.scalars().all())


async def update_uav(session: AsyncSession, uav_id: int, data: UavUpdate) -> Uav | None:
    payload = {key: value for key, value in data.model_dump(exclude_unset=True).items()}
    if not payload:
        return await get_uav(session, uav_id)
    await session.execute(update(Uav).where(Uav.id == uav_id).values(**payload))
    await session.flush()
    return await get_uav(session, uav_id)


async def delete_uav(session: AsyncSession, uav_id: int) -> bool:
    result = await session.execute(delete(Uav).where(Uav.id == uav_id))
    return result.rowcount > 0


async def get_uav_maintenance_status(session: AsyncSession, uav_id: int) -> dict | None:
    """Наработка БПЛА относительно следующего планового ТО."""
    uav = await get_uav(session, uav_id)
    if uav is None:
        return None

    result = await session.execute(
        select(MaintenanceRecord)
        .where(MaintenanceRecord.uav_id == uav_id)
        .order_by(MaintenanceRecord.performed_at.desc(), MaintenanceRecord.id.desc())
        .limit(1)
    )
    last_maintenance = result.scalar_one_or_none()

    next_due_operating_time = last_maintenance.next_due_operating_time if last_maintenance else None
    next_due_date = last_maintenance.next_due_date if last_maintenance else None

    overdue_by_hours = None
    if next_due_operating_time is not None:
        overdue_by_hours = uav.total_operating_time - next_due_operating_time

    overdue_by_days = None
    if next_due_date is not None:
        overdue_by_days = (date.today() - next_due_date).days

    is_overdue = bool((overdue_by_hours is not None and overdue_by_hours > 0) or
                       (overdue_by_days is not None and overdue_by_days > 0))

    return {
        "uav_id": uav_id,
        "total_operating_time": uav.total_operating_time,
        "last_maintenance_id": last_maintenance.id if last_maintenance else None,
        "next_due_operating_time": next_due_operating_time,
        "next_due_date": next_due_date,
        "overdue_by_hours": overdue_by_hours,
        "overdue_by_days": overdue_by_days,
        "is_overdue": is_overdue,
    }

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.models.operating_time_log import OperatingTimeLog
from app.models.uav import Uav
from app.schemas.operating_time_log import OperatingTimeLogCreate, OperatingTimeLogUpdate


async def create_operating_time_log(session: AsyncSession, data: OperatingTimeLogCreate) -> OperatingTimeLog:
    log_obj = OperatingTimeLog(**data.model_dump())
    session.add(log_obj)
    # Наработка за вылет пополняет суммарную наработку БПЛА
    await session.execute(
        update(Uav)
        .where(Uav.id == data.uav_id)
        .values(total_operating_time=Uav.total_operating_time + round(data.duration_hours))
    )
    await session.flush()
    await session.refresh(log_obj)
    return log_obj


async def get_operating_time_log(session: AsyncSession, log_id: int) -> OperatingTimeLog | None:
    result = await session.execute(select(OperatingTimeLog).where(OperatingTimeLog.id == log_id))
    return result.scalar_one_or_none()


async def list_operating_time_logs(
    session: AsyncSession, uav_id: int | None = None, limit: int = 100, offset: int = 0
) -> list[OperatingTimeLog]:
    query = select(OperatingTimeLog)
    if uav_id is not None:
        query = query.where(OperatingTimeLog.uav_id == uav_id)
    result = await session.execute(query.order_by(OperatingTimeLog.flight_date.desc()).offset(offset).limit(limit))
    return list(result.scalars().all())


async def update_operating_time_log(
    session: AsyncSession, log_id: int, data: OperatingTimeLogUpdate
) -> OperatingTimeLog | None:
    payload = {key: value for key, value in data.model_dump(exclude_unset=True).items()}
    if not payload:
        return await get_operating_time_log(session, log_id)

    existing = await get_operating_time_log(session, log_id)
    if existing is None:
        return None

    if "duration_hours" in payload:
        delta = round(payload["duration_hours"]) - round(existing.duration_hours)
        if delta:
            await session.execute(
                update(Uav).where(Uav.id == existing.uav_id).values(total_operating_time=Uav.total_operating_time + delta)
            )

    await session.execute(update(OperatingTimeLog).where(OperatingTimeLog.id == log_id).values(**payload))
    await session.flush()
    return await get_operating_time_log(session, log_id)


async def delete_operating_time_log(session: AsyncSession, log_id: int) -> bool:
    existing = await get_operating_time_log(session, log_id)
    if existing is None:
        return False

    await session.execute(
        update(Uav)
        .where(Uav.id == existing.uav_id)
        .values(total_operating_time=Uav.total_operating_time - round(existing.duration_hours))
    )
    result = await session.execute(delete(OperatingTimeLog).where(OperatingTimeLog.id == log_id))
    return result.rowcount > 0

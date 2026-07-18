from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.models.maintenance_record import MaintenanceRecord
from app.models.maintenance_type import MaintenanceType
from app.schemas.maintenance_record import MaintenanceRecordCreate, MaintenanceRecordUpdate


async def create_maintenance_record(session: AsyncSession, data: MaintenanceRecordCreate) -> MaintenanceRecord:
    payload = data.model_dump()

    if payload["maintenance_type_id"] is not None and (
        payload["next_due_operating_time"] is None or payload["next_due_date"] is None
    ):
        result = await session.execute(
            select(MaintenanceType).where(MaintenanceType.id == payload["maintenance_type_id"])
        )
        maintenance_type = result.scalar_one_or_none()
        if maintenance_type is not None:
            if payload["next_due_operating_time"] is None and maintenance_type.interval_hours is not None:
                payload["next_due_operating_time"] = (
                    payload["operating_time_at_maintenance"] + maintenance_type.interval_hours
                )
            if payload["next_due_date"] is None and maintenance_type.interval_days is not None:
                payload["next_due_date"] = payload["performed_at"] + timedelta(days=maintenance_type.interval_days)

    record_obj = MaintenanceRecord(**payload)
    session.add(record_obj)
    await session.flush()
    await session.refresh(record_obj)
    return record_obj


async def get_maintenance_record(session: AsyncSession, record_id: int) -> MaintenanceRecord | None:
    result = await session.execute(select(MaintenanceRecord).where(MaintenanceRecord.id == record_id))
    return result.scalar_one_or_none()


async def list_maintenance_records(
    session: AsyncSession, uav_id: int | None = None, limit: int = 100, offset: int = 0
) -> list[MaintenanceRecord]:
    query = select(MaintenanceRecord)
    if uav_id is not None:
        query = query.where(MaintenanceRecord.uav_id == uav_id)
    result = await session.execute(query.order_by(MaintenanceRecord.performed_at.desc()).offset(offset).limit(limit))
    return list(result.scalars().all())


async def update_maintenance_record(
    session: AsyncSession, record_id: int, data: MaintenanceRecordUpdate
) -> MaintenanceRecord | None:
    payload = {key: value for key, value in data.model_dump(exclude_unset=True).items()}
    if not payload:
        return await get_maintenance_record(session, record_id)
    await session.execute(update(MaintenanceRecord).where(MaintenanceRecord.id == record_id).values(**payload))
    await session.flush()
    return await get_maintenance_record(session, record_id)


async def delete_maintenance_record(session: AsyncSession, record_id: int) -> bool:
    result = await session.execute(delete(MaintenanceRecord).where(MaintenanceRecord.id == record_id))
    return result.rowcount > 0

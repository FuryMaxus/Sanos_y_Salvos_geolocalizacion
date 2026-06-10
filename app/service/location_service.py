import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.location_repository import LocationRepository
from app.model.location import PetLocation

class LocationService:
    def __init__(self, db_session: AsyncSession):
        self.repository = LocationRepository(session=db_session)

    async def upsert_location(
            self,
            pet_id: uuid.UUID,
            latitude: float, 
            longitude: float
        ) -> PetLocation:
        point_wkt = f"POINT({longitude} {latitude})"
        existing_location = await self.repository.get_one_or_none(pet_id=pet_id)
        if existing_location:
            existing_location.coordinate = point_wkt
            return await self.repository.update(existing_location)
        else:
            new_location = PetLocation(pet_id=pet_id, coordinate=point_wkt)
            return await self.repository.add(new_location)

    async def get_location(
            self,
            pet_id: uuid.UUID
        ) -> PetLocation | None:
        return await self.repository.get_one_or_none(pet_id=pet_id)

    async def delete_location(
            self,
            pet_id: uuid.UUID
        ) -> None:
        existing_location = await self.repository.get_one_or_none(pet_id=pet_id)
        if existing_location:
            await self.repository.delete(existing_location.id)
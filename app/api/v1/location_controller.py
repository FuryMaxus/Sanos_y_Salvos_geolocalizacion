import uuid
from typing import cast
from litestar import Controller, post, get, delete
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import to_shape 
from litestar.di import Provide  
from app.service.location_service import LocationService
from app.domain.structs import LocationCreateRequest, LocationResponse, MessageResponse
from shapely.geometry import Point
from app.repository.location_repository import LocationRepository

async def provide_location_service(db_session: AsyncSession) -> LocationService:
    repo = LocationRepository(session=db_session)
    return LocationService(repository=repo)

class LocationController(Controller):
    path = "/locations"

    dependencies = {"location_service": Provide(provide_location_service)}

    @post("/")
    async def save_location(
        self,
        data: LocationCreateRequest,
        location_service: LocationService
    ) -> MessageResponse:
        await location_service.upsert_location(data.pet_id, data.latitude, data.longitude)
        return MessageResponse(message="Location saved successfully")
    
    @get("/{pet_id:uuid}")
    async def get_location(
        self,
        pet_id: uuid.UUID,
        location_service: LocationService
    ) -> LocationResponse:
        location = await location_service.get_location(pet_id)
        
        if not location:
            raise NotFoundException(detail="Location not found for this pet")
            
        point_shape = cast(Point, to_shape(location.coordinate))
        
        return LocationResponse(
            pet_id=location.pet_id, 
            latitude=point_shape.y,  
            longitude=point_shape.x  
        )
    
    @delete("/{pet_id:uuid}")
    async def delete_location(
        self,
        pet_id: uuid.UUID,
        location_service: LocationService
    ) -> None:
        await location_service.delete_location(pet_id)
    
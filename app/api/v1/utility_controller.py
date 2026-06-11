from litestar import Controller, post
from app.service.utility_service import UtilityService
from app.domain.structs import (
    DistanceRequest, DistanceResponse, 
    RadiusRequest, RadiusResponse, PetDistanceItem
)

class UtilityController(Controller):
    path = "/utilities"

    @post("/distance")
    async def calculate_distance(
        self, 
        data: DistanceRequest, 
        utility_service: UtilityService 
    ) -> DistanceResponse:
        
        distance = await utility_service.calculate_distance(
            data.origin_latitude, 
            data.origin_longitude,
            data.target_latitude, 
            data.target_longitude
        )
        
        return DistanceResponse(distance_meters=distance)
    
    @post("/radius")
    async def get_pets_in_radius(
        self, 
        data: RadiusRequest, 
        utility_service: UtilityService
    ) -> RadiusResponse:
        
        pets_data = await utility_service.find_pets_in_radius(
            data.latitude, 
            data.longitude, 
            data.radius_meters
        )
        
        result_items = [
            PetDistanceItem(pet_id=p["pet_id"], distance_meters=p["distance_meters"]) 
            for p in pets_data
        ]
        
        return RadiusResponse(pets=result_items)
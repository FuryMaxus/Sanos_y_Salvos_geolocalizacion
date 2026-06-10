from litestar import Controller, post
from app.domain.structs import DistanceRequest, DistanceResponse
from app.service.utility_service import UtilityService

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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class UtilityService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def calculate_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        query = text("""
            SELECT calculate_distance_sp(:lat1, :lon1, :lat2, :lon2)
        """)
        
        result = await self.db_session.execute(
            query,
            {"lat1": lat1, "lon1": lon1, "lat2": lat2, "lon2": lon2}
        )
        
        return result.scalar() or 0.0
    
    async def find_pets_in_radius(
        self, lat: float, lon: float, radius_meters: float
    ) -> list[dict]:
        query = text("""
            SELECT pet_id, distance 
            FROM get_pets_in_radius_sp(:lat, :lon, :radius)
        """)
        
        result = await self.db_session.execute(
            query,
            {"lat": lat, "lon": lon, "radius": radius_meters}
        )
        
        return [
            {"pet_id": row.pet_id, "distance_meters": row.distance} 
            for row in result.fetchall()
        ]
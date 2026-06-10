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
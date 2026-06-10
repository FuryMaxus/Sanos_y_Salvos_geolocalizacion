from litestar import Litestar
from app.core.db_config import db_plugin
from app.api.v1.location_controller import LocationController
from app.repository.location_repository import LocationRepository
from app.service.location_service import LocationService
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.di import Provide
from app.service.utility_service import UtilityService  
from app.api.v1.utility_controller import UtilityController

async def provide_location_service(db_session: AsyncSession) -> LocationService:
    repo = LocationRepository(session=db_session)
    return LocationService(repository=repo)

async def provide_utility_service(db_session: AsyncSession) -> UtilityService:
    return UtilityService(db_session=db_session)

app = Litestar(
    route_handlers=[
        LocationController,
        UtilityController
    ],
    plugins=[db_plugin],
    dependencies={
        "location_service": Provide(provide_location_service),
        "utility_service": Provide(provide_utility_service)
    },
    debug=True
)
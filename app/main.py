from litestar import Litestar
from app.core.db_config import db_plugin
from app.api.v1.location_controller import LocationController
from app.repository.location_repository import LocationRepository
from app.service.location_service import LocationService
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.di import Provide

async def provide_location_service(db_session: AsyncSession) -> LocationService:
    repo = LocationRepository(session=db_session)
    return LocationService(repository=repo)


app = Litestar(
    route_handlers=[
        LocationController,
    ],
    plugins=[db_plugin],
    dependencies={"location_service": Provide(provide_location_service)},
    debug=True
)
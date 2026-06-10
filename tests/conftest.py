import pytest
from unittest.mock import MagicMock, AsyncMock
from litestar import Litestar
from litestar.testing import AsyncTestClient
from litestar.di import Provide
from app.api.v1.location_controller import LocationController
from app.service.location_service import LocationService
from app.service.utility_service import UtilityService
from app.api.v1.utility_controller import UtilityController

@pytest.fixture(scope="function")
def mock_location_service():
    mock = MagicMock(spec=LocationService)
    mock.upsert_location = AsyncMock()
    mock.delete_location = AsyncMock()
    mock.get_location = AsyncMock()
    return mock

@pytest.fixture(scope="function")
def mock_utility_service():
    mock = MagicMock(spec=UtilityService)
    mock.calculate_distance = AsyncMock()
    return mock

@pytest.fixture(scope="function")
def mock_db_session():
    return AsyncMock()

@pytest.fixture(scope="function")
async def test_client(mock_location_service, mock_utility_service, mock_db_session):
    
    async def provide_location_service() -> LocationService:
        return mock_location_service

    async def provide_util_service() -> UtilityService:
        return mock_utility_service
    
    async def provide_db_session():
        return mock_db_session

    app = Litestar(
        route_handlers=[LocationController, UtilityController],
        dependencies={
            "location_service": Provide(provide_location_service),
            "db_session": Provide(provide_db_session),
            "utility_service": Provide(provide_util_service),
        }
    )

    async with AsyncTestClient(app=app) as client:
        yield client
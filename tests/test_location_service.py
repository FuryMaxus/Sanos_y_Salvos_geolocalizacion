import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.service.location_service import LocationService
from app.repository.location_repository import LocationRepository
from app.model.location import PetLocation


@pytest.fixture
def mock_repository():
    repo = MagicMock(spec=LocationRepository)
    repo.get_one_or_none = AsyncMock()
    repo.add = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo

@pytest.fixture
def location_service(mock_repository):
    return LocationService(repository=mock_repository)


@pytest.mark.asyncio
async def test_upsert_location_creates_new(location_service, mock_repository):
    pet_id = uuid.uuid4()
    mock_repository.get_one_or_none.return_value = None
    
    await location_service.upsert_location(pet_id, -33.4489, -70.6693)
    
    mock_repository.get_one_or_none.assert_called_once_with(pet_id=pet_id)
    mock_repository.add.assert_called_once()
    mock_repository.update.assert_not_called()

@pytest.mark.asyncio
async def test_upsert_location_updates_existing(location_service, mock_repository):
    pet_id = uuid.uuid4()
    existing_location = PetLocation(pet_id=pet_id, coordinate="PUNTO_VIEJO")
    mock_repository.get_one_or_none.return_value = existing_location
    
    await location_service.upsert_location(pet_id, -33.4489, -70.6693)
    
    mock_repository.get_one_or_none.assert_called_once_with(pet_id=pet_id)
    mock_repository.update.assert_called_once_with(existing_location)
    mock_repository.add.assert_not_called()

@pytest.mark.asyncio
async def test_delete_location_existing(location_service, mock_repository):
    pet_id = uuid.uuid4()
    existing_location = PetLocation(pet_id=pet_id, coordinate="PUNTO")
    existing_location.id = uuid.uuid4() 
    mock_repository.get_one_or_none.return_value = existing_location
    
    await location_service.delete_location(pet_id)
    
    mock_repository.delete.assert_called_once_with(existing_location.id)
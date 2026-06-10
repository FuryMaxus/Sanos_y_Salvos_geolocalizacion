import uuid
import pytest
from unittest.mock import patch
from shapely.geometry import Point

@pytest.mark.asyncio
async def test_save_location(test_client, mock_location_service):
    pet_id = str(uuid.uuid4())
    payload = {"pet_id": pet_id, "latitude": -33.4489, "longitude": -70.6693}
    
    response = await test_client.post("/locations/", json=payload)
    
    assert response.status_code == 201
    assert response.json() == {"message": "Location saved successfully"}
    mock_location_service.upsert_location.assert_called_once_with(
        uuid.UUID(pet_id), -33.4489, -70.6693
    )

@pytest.mark.asyncio
@patch("app.api.v1.location_controller.to_shape") 
async def test_get_location_success(mock_to_shape, test_client, mock_location_service):
    pet_id = str(uuid.uuid4())
    
    mock_db_location = mock_location_service.get_location.return_value
    mock_db_location.pet_id = uuid.UUID(pet_id)
    
    mock_to_shape.return_value = Point(-70.6693, -33.4489) 
    
    response = await test_client.get(f"/locations/{pet_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["latitude"] == -33.4489
    assert data["longitude"] == -70.6693

@pytest.mark.asyncio
async def test_get_location_not_found(test_client, mock_location_service):
    pet_id = str(uuid.uuid4())
    mock_location_service.get_location.return_value = None
    
    response = await test_client.get(f"/locations/{pet_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found for this pet"

@pytest.mark.asyncio
async def test_delete_location(test_client, mock_location_service):
    pet_id = str(uuid.uuid4())
    
    response = await test_client.delete(f"/locations/{pet_id}")
    
    assert response.status_code == 204 
    assert response.content == b"" 
    mock_location_service.delete_location.assert_called_once_with(uuid.UUID(pet_id))
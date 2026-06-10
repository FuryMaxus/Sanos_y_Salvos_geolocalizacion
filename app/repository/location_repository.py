from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.model.location import PetLocation

class LocationRepository(SQLAlchemyAsyncRepository[PetLocation]):
    model_type = PetLocation
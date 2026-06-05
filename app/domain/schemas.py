import msgspec
import uuid

class InputCoordinate(msgspec.Struct):
    pet_id: uuid.UUID
    latitude: float
    longitude: float

    def __post_init__(self):
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("La latitud debe estar entre -90 y 90")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("La longitud debe estar entre -180 y 180")
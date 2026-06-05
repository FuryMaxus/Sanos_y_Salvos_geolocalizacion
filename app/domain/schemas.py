import msgspec

class DistanceRequest(msgspec.Struct):
    origin_latitude: float
    origin_longitude: float
    target_latitude: float
    target_longitude: float

    def __post_init__(self):
        if not (-90.0 <= self.origin_latitude <= 90.0) or not (-90.0 <= self.target_latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180.0 <= self.origin_longitude <= 180.0) or not (-180.0 <= self.target_longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
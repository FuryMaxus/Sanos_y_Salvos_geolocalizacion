from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid
from geoalchemy2 import Geometry
from advanced_alchemy.base import UUIDBase
from geoalchemy2.elements import WKBElement
import uuid
class PetLocation(UUIDBase):
    __tablename__ = "pets_locations"

    pet_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True, nullable=False)

    coordinate: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False
    )
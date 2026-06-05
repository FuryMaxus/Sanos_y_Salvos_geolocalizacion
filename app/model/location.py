from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from geoalchemy2 import Geometry
from advanced_alchemy.base import UUIDBase

class petLocation(UUIDBase):
    __tablename__ = "pets_locations"

    pet_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)

    coordinate: Mapped[str] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False
    )
from typing import List
from sqlalchemy import (
    Integer,
    String,
    Float,
    inspect,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db, Base

pokemon_location_area_table = Table(
    "pokemon_location_area_table",
    Base.metadata,
    Column("pokemon_id", ForeignKey("pokemon.id")),
    Column("location_area_id", ForeignKey("location_area.id")),
)


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    api_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    sprite: Mapped[str] = mapped_column(String, nullable=False)
    type_one: Mapped[str] = mapped_column(String, nullable=False)
    type_two: Mapped[str] = mapped_column(String, nullable=True)

    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

    def __repr__(self):
        return f"{self.name}"


class LocationArea(db.Model):
    __tablename__ = "location_area"

    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    api_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    location: Mapped["Location"] = relationship(
        back_populates="location_areas"
    )

    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

    def __repr__(self):
        return f"{self.name}"


class Location(db.Model):
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    api_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=False)
    location_areas: Mapped[List["LocationArea"]] = relationship(
        back_populates="location"
    )

    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

    def __repr__(self):
        return f"{self.name}"

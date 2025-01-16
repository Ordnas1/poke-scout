from typing import List
from sqlalchemy import Integer, String, Float, inspect, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db


class Pokemon(db.Model):
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

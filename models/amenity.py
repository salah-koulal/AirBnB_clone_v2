#!/usr/bin/python3
"""Tthe amenity class data storage"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

class Amenity(BaseModel, Base):
    """This is the class for Amenity
    Attributes:
        name: input name
    """

    """ documment doc """
    __tablename__ = 'amenities'
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place', secondary=place_amenity,
                                    back_populates="amenities")
    else:
        name = ""

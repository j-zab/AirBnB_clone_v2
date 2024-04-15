# models/place.py
#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """The Place class, contains city ID, user ID, name, and description"""
    __tablename__ = "places"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

#        place_amenity = Table('place_amenity', Base.metadata,
 #                     Column('place_id', String(60),
  #                           ForeignKey('places.id'), primary_key=True, nullable=False),
   #                   Column('amenity_id', String(60),
    #                         ForeignKey('amenities.id'), primary_key=True, nullable=False))

        
        # For DBStorage
        user = relationship('User', backref='places', cascade='all, delete-orphan', passive_deletes=True)
        reviews = relationship('Review', backref='place', cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity, viewonly=False)

    # For FileStorage
    @property
    def reviews(self):
        """Getter attribute that returns a list of Review instances
        with place_id equals to the current Place.id"""
        from models import storage
        review_list = []
        for review in storage.all("Review").values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def amenities(self):
        """Getter attribute that returns a list of Amenity instances
        based on the attribute amenity_ids"""
        from models import storage
        amenity_list = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, amenity):
        """Setter attribute that handles append method for adding an Amenity.id
        to the attribute amenity_ids"""
        if isinstance(amenity, Amenity):
            if amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)


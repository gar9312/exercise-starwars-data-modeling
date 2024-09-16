import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine, Table
from eralchemy2 import render_er

Base = declarative_base()

# Association table for many-to-many between User and Character
user_character_favorite = Table('user_character_favorite', Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('character_id', ForeignKey('character.id'), primary_key=True)
)

# Association table for many-to-many between User and Planet
user_planet_favorite = Table('user_planet_favorite', Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('planet_id', ForeignKey('planet.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    subscription_date = Column(String(250), nullable=False)

    # Many-to-many relationship with Character and Planet through association tables
    favorite_characters = relationship('Character', secondary=user_character_favorite, back_populates="favorited_by_users")
    favorite_planets = relationship('Planet', secondary=user_planet_favorite, back_populates="favorited_by_users")

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    species = Column(String(250))
    gender = Column(String(250))
    
    # Many-to-many relationship with User
    favorited_by_users = relationship('User', secondary=user_character_favorite, back_populates="favorite_characters")

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    climate = Column(String(250))
    terrain = Column(String(250))

    # Many-to-many relationship with User
    favorited_by_users = relationship('User', secondary=user_planet_favorite, back_populates="favorite_planets")

class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    planet_id = Column(Integer, ForeignKey('planet.id'))
    character_id = Column(Integer, ForeignKey('character.id'))

    user = relationship('User')
    planet = relationship('Planet')
    character = relationship('Character')

# Generate the ER diagram
render_er(Base, 'diagram.png')

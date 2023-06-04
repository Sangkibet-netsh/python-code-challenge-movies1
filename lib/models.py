import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey, func)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

engine = create_engine('sqlite:///db/movies.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

class Role(Base):
   __tablename__ = 'roles'


   id = Column(Integer, primary_key=True)
   movie_id = Column(Integer, ForeignKey('movies.id'))
   actor_id = Column(Integer, ForeignKey('actors.id'))
   salary = Column(Integer())
   character_name = Column(String())


   movie = relationship("Movie", backref=backref("roles", cascade="all, delete-orphan"))
   actor = relationship("Actor", backref=backref("roles", cascade="all, delete-orphan"))


   def __repr__(self):
       return f'Role: {self.character_name}'
   
   def actor(self):
        return self.actor
   
   def movie(self):
        return self.movie
   
   def credit(self):
        return f"{self.character_name}: Played by {self.actor.name}"



class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String())

    movies = relationship("Movie", secondary="", back_populates="actor")

    def __repr__(self):
        return f'Actor: {self.name}'
    
    def roles(self):
        return self.roles
    
    def movies(self):
        return [role.movie for role in self.roles]
    
    def total_salary(self):
        return sum(role.salary for role in self.roles)
    
    def blockbusters(self):
        return [movie for movie in self.movies if movie.box_office_earnings > 50000000]
    
    @classmethod
    def most_successful(cls):
        return (
            session.query(cls)
            .join(Role)
            .group_by(cls.id)
            .order_by(func.sum(Role.salary).desc())
            .first()
        )


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    box_office_earnings = Column(Integer())

    actors = relationship("Role", back_populates="movie")
    

    
    def __repr__(self):
        return f'Movie: {self.title}'
    
    
    def roles(self):
        return self.roles
    
    
    def actors(self):
        return [role.actor for role in self.roles]
    
    
    def cast_role(self, actor, character_name, salary):
        role = Role(movie=self, actor=actor, character_name=character_name, salary=salary)
        self.roles.append(role)


    def all_credits(self):
        return [role.credit() for role in self.roles]
    
    
    def fire_actor(self, actor):
        role = next((role for role in self.roles if role.actor == actor), None)
        if role:
            self.roles.remove(role)
    


    

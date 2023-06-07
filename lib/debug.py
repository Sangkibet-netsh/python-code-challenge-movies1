#!/usr/bin/env python3
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Movie,Actor
# import ipdb;


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///db/movies.db')
    Session = sessionmaker(bind=engine)
    session = Session()


        # Retrieve all movies
    print("All Movies:")
    movies = session.query(Movie).all()
    for movie in movies:
        print(movie)

    # Retrieve all actors
    print("All Actors:")
    actors = session.query(Actor).all()
    for actor in actors:
        print(actor)

    # Create a new movie
    new_movie = Movie(title="New Movie", box_office_earnings=random.randint(1000000, 10000000))
    session.add(new_movie)
    session.commit()
    print(f"New Movie Created: {new_movie}")

    # Create a new actor
    new_actor = Actor(name="New Actor")
    session.add(new_actor)
    session.commit()
    print(f"New Actor Created: {new_actor}")

    # Cast a role for the new movie
    new_movie.cast_role(new_actor, "New Role", random.randint(100000, 1000000))
    session.commit()
    print(f"New Role Cast: {new_movie.all_credits()}")

    # Retrieve the total salary of an actor
    actor = random.choice(actors)
    total_salary = actor.total_salary()
    print(f"Total Salary for {actor.name}: {total_salary}")

    # Retrieve the most successful actor
    most_successful_actor = Actor.most_successful()
    print(f"Most Successful Actor: {most_successful_actor}")

    # Fire an actor from a movie
    movie = random.choice(movies)
    actor = random.choice(movie.actors())
    movie.fire_actor(actor)
    session.commit()
    print(f"Fired {actor.name} from {movie.title}")
    print(f"Updated Cast: {movie.actors()}")



import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# Running will create a PostgreSQL database for use in program

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)

with server.app.app_context():
    model.db.create_all()

    # Load movie data from movies.JSON file
    with open("data/movies.json") as f:
        movie_data = json.loads(f.read())

    # Create movies, store them in list for use
    movies_in_db = []
    for movie in movie_data:
        title, overview, poster_path = (
            movie["title"],
            movie["overview"],
            movie["poster_path"],
        )
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

        db_movie = crud.create_movie(title, overview, release_date, poster_path)
        movies_in_db.append(db_movie)

    model.db.session.add_all(movies_in_db)
    model.db.session.commit()

    # Create Instance of users
    user_count = 10

    for n in range(user_count):
        email = f"user{n}@test.com" # unique email generator
        password = "test"

        user = crud.create_user(email, password)
        model.db.session.add(user)

        for _ in range(10):
            random_movie = choice(movies_in_db)
            score = randint(1, 5)

            rating = crud.create_rating(user, random_movie, score)
            model.db.session.add(rating)

    model.db.session.commit()

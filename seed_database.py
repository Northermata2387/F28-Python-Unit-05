# SEED_DATABASE.PY

# On execiution will create a PostgreSQL database for use in program

# SETUP
########################################################################

# os > operating systenm connection
import os
# json >
import json
# random > choice > takes in a list and returns a random element in the list
# random > randit > return a random number within a certain range
from random import choice, randint
# datetime > datetime >  turn a string into a Python datetime object.
from datetime import datetime

# Import from crud.py
import crud
# Import from model.py
import model
# Import from server.py
import server

# Database reset
########################################################################

# Drop the database ratings
os.system("dropdb ratings")
# Create the database ratings
os.system("createdb ratings")

# Connect to the model.py > db > and create all the tables outlined in the file
########################################################################

# access the database
model.connect_to_db(server.app)
# create all the tables for PostreSQL
model.db.create_all()

# LOAD
########################################################################

# Load movie data from JSON file
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list for use
# Create stock ratings
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
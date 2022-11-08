# CRUD.PY

# SETUP
########################################################################

# model > multiple options >
from model import db, User, Movie, Rating, connect_to_db


# CREATE
########################################################################

# Instace of User to create and return a new user
def create_user(email, password):

    user = User(email=email, password=password)

    return user

# Instance of Movie to create and return a new movie
def create_movie(title, overview, release_date, poster_path):

    movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path,
    )

    return movie

# Instance of Rating to create and return a new rating
def create_rating(user, movie, score):

    rating = Rating(user=user, movie=movie, score=score)

    return rating

# EXECUTE
########################################################################

# import to server.py and conncet to db
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
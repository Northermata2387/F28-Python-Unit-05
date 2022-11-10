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

# READ
########################################################################

def get_movies():
    """Return all movies."""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return a movie by primary key."""

    return Movie.query.get(movie_id)

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

# EXECUTE
########################################################################

# import to server.py and conncet to db
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    

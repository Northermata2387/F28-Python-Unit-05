# MODEL.PY

# SETUP
########################################################################

# operating system > environ > mapping objects in PostgreSQL
import os

# flask_sqlalchemy > SQLAlchemy >
from flask_sqlalchemy import SQLAlchemy

# rename SQLAlchemy to db to invoke SQLAlchemy and for less typing and space in code
db = SQLAlchemy()

# CLASSES/TABLES
########################################################################

# Class:User / Table:users
class User(db.Model):

    # Override for tablename
    __tablename__ = "users"

    # Instances for SQL db
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects

    # represent the User class's objects as a string
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

# Class:Movie / Table:movies
class Movie(db.Model):

    # Override for tablename
    __tablename__ = "movies"

    # Instances for SQL db
    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    # ratings = a list of Rating objects

    # represent the User class's objects as a string
    def __repr__(self):
        return f"<Movie movie_id={self.movie_id} title={self.title}>"

# Class:Rating / Table:ratings
class Rating(db.Model):

    # Override for tablename
    __tablename__ = "ratings"

    # Instances for SQL db
    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    
    movie = db.relationship("Movie", backref="ratings")
    user = db.relationship("User", backref="ratings")
    
    # represent the User class's objects as a string
    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"
    

# DATABASE CONNECTION
########################################################################
def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

# EXECUTE
########################################################################

# import to server.py and connect to db
if __name__ == "__main__":
    from server import app

    # Use (echo=False) option to silence SQLAlchemy ouput

    connect_to_db(app, echo=False)
# SERVER.PY

# SETUP
########################################################################

# flask > Flask >
from flask import Flask, render_template, request, flash, session, redirect

# model.py > database connection
from model import connect_to_db, db

# crud.py
import crud

# jinja2 > StrictUndefined > disallows all operations beside testing if it’s an undefined object
from jinja2 import StrictUndefined

# define Flask name of this file to app for simple and clean coding
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# ROUTE
########################################################################

# Render homapge.html page
@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

# Render all_movies.html page
@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

# Render movie_details.html page
@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)
# EXECUTE
########################################################################

# run the application
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

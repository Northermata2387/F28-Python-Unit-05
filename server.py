
from flask import Flask, render_template, request, flash, session, redirect
from jinja2 import StrictUndefined

from model import connect_to_db, db
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    
    # view homepage
    return render_template("homepage.html")

@app.route("/movies")
def all_movies():

    # render movies from ratings > movies SQL table
    movies = crud.get_movies()

    # view all_movies and all movie cards
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):

    # render a single movide by its id
    movie = crud.get_movie_by_id(movie_id)

    # View movie_details and inidivual movie card by id
    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def all_users():

    # Define movies as import of get_movie_by_id from crud.py
    users = crud.get_users()

    # View all_users.html
    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Your account already exists. Please login")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

    return "Success"

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")

if __name__ == "__main__":
    connect_to_db(app)
    # host allows access to site from any system with the URL 
    app.run(host="0.0.0.0", debug=True)


from flask import Flask, render_template, request, flash, session, redirect
from jinja2 import StrictUndefined

from model import connect_to_db, db
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")


@app.route("/")
def homepage():
    
    return render_template("homepage.html")

@app.route("/movies")
def all_movies():

    if "user_email" not in session:
        flash("Please login to view all movies")
        return redirect("/login")

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def all_users():
    
    if "user_email" not in session:
        flash("Please login to view profiles")
        return redirect("/login")

    users = crud.get_users()

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

    return redirect("/login")

@app.route("/users/<user_id>")
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/login")
def login():
    
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("The email or password entered was not right, please try again")
        
        return redirect("/login")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        
        return redirect("/movies")

@app.route("/logout")
def logout():
    
    if 'user_email' not in session:
        return redirect("/login")
    
    del session["user_email"]
    flash("logged out")
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

@app.route("/register")
def register():
    
    return render_template("register.html")

# @app.route("/register")
# def register():
    
#     redirect("/login")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

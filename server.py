from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud
import model

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('authentication.html')

@app.route('/movies')
def movies():
    movies = crud.get_all_movies()
    return render_template('movies.html', movies=movies)

@app.route('/movie/<movie_id>')
def movie(movie_id):
    movie = crud.get_movie(movie_id)
    return render_template('movie.html', movie=movie)

@app.route('/users')
def users():
    users = crud.get_all_users()
    return render_template('users.html', users=users)

@app.route('/user/<user_id>')
def user(user_id):
    user = crud.get_user(user_id)
    return render_template('user.html', user=user)

@app.route('/register', methods=['POST'])
def register():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return render_template('authentication.html')

@app.route('/login', methods=['POST'])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        return redirect('/movies')

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
        movie = crud.get_movie(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movie/{movie_id}")

@app.errorhandler(404)
def error_404(e): 
   return render_template("404.html") 

        
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

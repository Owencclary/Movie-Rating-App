from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    user = User(email=email, password=password)
    return user

def create_movie(title, overview, release_date, poster_path):
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    return movie

def create_rating(user, movie, score):
    rating = Rating(user=user, movie=movie, score=score)
    return rating

def get_all_movies():
    return Movie.query.all()

def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        raise ValueError(f"Movie with ID {movie_id} not found.")
    return movie

def get_all_users():
    users = User.query.all()
    return users

def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")
    return user

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

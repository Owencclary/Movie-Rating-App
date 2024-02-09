import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# connects the database to the server then creates all the data tables
app = server.app
model.connect_to_db(app)

# Load movie data from JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'movies.json')
with open(json_file_path) as f:
    movie_data = json.loads(f.read())

# gets all the movies from the json file and adds them to a list
movies_in_db = []

with app.app_context():
    for movie in movie_data:
        title = movie['title']
        overview = movie['overview']
        poster_path = movie['poster_path']
        release_date_str = movie['release_date']

        # Convert the release_date string to a datetime object
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d")

        movie_obj = crud.create_movie(title, overview, release_date, poster_path)
        movies_in_db.append(movie_obj)

    # Adds all the movies from the movies list to the database
    model.db.session.add_all(movies_in_db)
    model.db.session.commit()

# creates 10 users with a unique id for each user
with app.app_context():
    for n in range(10):
        email = f'user{n}@test.com'  
        password = 'test'

        # adds user to the db
        user = crud.create_user(email, password)
        model.db.session.add(user)

        # creates 10 ratings for each user
        for _ in range(10):
            random_movie = choice(movies_in_db) # picks a random movie from the movies list
            score = randint(1, 5) # picks a rating between 1-5

            # adds rating to the db with the user and the random movie 
            rating = crud.create_rating(user, random_movie, score)
            model.db.session.add(rating)
            model.db.session.commit() # commits changes

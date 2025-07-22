from models.Cinema import Cinema
from models.Movie import Movie
from models.Screening import Screening
from datetime import datetime

class AdminManager:
    def __init__(self, cinema):
        self.cinema = cinema
        self.next_movie_id = cinema.get_newest_screening_id() + 1
        self.next_screening_id = cinema.get_newest_screening_id() + 1
    
    def add_movie(self, title, duration, rating, description):
        movie = Movie(
            self.next_movie_id,
            title,
            duration,
            rating,
            description
        )
        self.next_movie_id += 1
        self.cinema.add_movie(movie)
        return movie
    
    def add_screening(self, movie_id, room_id, start_time, price):
        screening = Screening(
            self.next_screening_id,
            movie_id,
            room_id,
            start_time,
            price
        )
        self.next_screening_id += 1
        self.cinema.add_screening(screening)
        return screening
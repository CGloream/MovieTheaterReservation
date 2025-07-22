from models.Movie import Movie
from models.ScreeningRoom import ScreeningRoom
from models.Screening import Screening
from models.Reservation import Reservation
from models.Cinema import Cinema

import json
import os
from datetime import datetime

class DataStorage:
    def __init__(self, filename):
        self.filename = filename
    
    def save_data(self, cinema):
        data = {
            "name": cinema.name,
            "movies": [{"id": m.id, "title": m.title, "duration": m.duration, "rating": m.rating, "description": m.description} for m in cinema.movies],
            "screening_rooms": [{"id": r.id, "name": r.name, "rows": r.rows, "cols": r.cols} for r in cinema.screening_rooms],
            "screenings": [{"id": s.id, "movie_id": s.movie_id, "room_id": s.room_id, "start_time": s.start_time.strftime("%Y-%m-%d %H:%M"), "price": s.price, "reserved_seats": list(s.reserved_seats)} for s in cinema.screenings],
            "reservations": [{"id": r.id, "screening_id": r.screening_id, "customer_name": r.customer_name, "customer_email": r.customer_email, "seats": r.seats, "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for r in cinema.reservations]
        }

        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
    
    # return None if error, return cinema if data is True
    def load_data(self):
        if not os.path.exists(self.filename):
            return None
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            cinema = Cinema(data["name"])
             # Load movies
            for movie_data in data.get("movies", []):
                movie = Movie(
                    movie_data["id"],
                    movie_data["title"],
                    movie_data["duration"],
                    movie_data["rating"],
                    movie_data["description"]
                )
                cinema.add_movie(movie)
            
            # Load screening rooms
            for room_data in data.get("screening_rooms", []):
                room = ScreeningRoom(
                    room_data["id"],
                    room_data["name"],
                    room_data["rows"],
                    room_data["cols"]
                )
                cinema.add_screening_room(room)
            
            # Load screenings
            for screening_data in data.get("screenings", []):
                screening = Screening(
                    screening_data["id"],
                    screening_data["movie_id"],
                    screening_data["room_id"],
                    datetime.strptime(screening_data["start_time"], "%Y-%m-%d %H:%M"),
                    screening_data["price"]
                )
                screening.reserved_seats = set(tuple(seat) for seat in screening_data.get("reserved_seats", []))
                cinema.add_screening(screening)
            
            # Load reservations
            for reservation_data in data.get("reservations", []):
                reservation = Reservation(
                    reservation_data["id"],
                    reservation_data["screening_id"],
                    reservation_data["customer_name"],
                    reservation_data["customer_email"],
                    [tuple(seat) for seat in reservation_data["seats"]]
                )
                reservation.timestamp = datetime.strptime(reservation_data["timestamp"], "%Y-%m-%d %H:%M:%S")
                cinema.add_reservation(reservation)
            
            return cinema
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
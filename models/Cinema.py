from models.Movie import Movie
from models.ScreeningRoom import ScreeningRoom
from models.Screening import Screening
from models.Reservation import Reservation

class Cinema:
    def __init__(self, name):
        self.name = name
        self.movies = []
        self.screening_rooms = []
        self.screenings = []
        self.reservations = []
    
    def add_movie(self, movie):
        self.movies.append(movie)
    
    def add_screening_room(self, room):
        self.screening_rooms.append(room)
    
    def add_screening(self, screening):
        self.screenings.append(screening)
    
    def add_reservation(self, reservation):
        self.reservations.append(reservation)

        # look for the screening
        screening = next((s for s in self.screenings if s.id == reservation.screening_id), None)
        if screening:
            screening.reserve_seats(reservation.seats)
    


    def get_movies(self):
        return self.movies
    
    def get_screening_rooms(self):
        return self.screening_rooms
    
    def get_screenings_by_movie(self, movie_id):
        return [s for s in self.screenings if s.movie_id == movie_id]
    
    def get_screening_by_id(self, screening_id):
        return next((s for s in self.screenings if s.id == screening_id), None)
    
    def get_reservations_by_screening(self, screening_id):
        return [r for r in self.reservations if r.screening_id == screening_id]

    def get_screening_by_id(self, screening_id):
        return next((s for s in self.screenings if s.id == screening_id), None)



    def get_newest_reservation_id(self):
        # the reseration id will increment by 1 always
        if self.reservations==[]:
            return 0
        else:
            return max([r.id for r in self.reservations])
    
    def get_newest_screening_id(self):
        # the screening id will increment by 1 always
        if self.screenings==[]:
            return 0
        else:
            return max([s.id for s in self.screenings])
    
    def get_newest_movie_id(self):
    # the movie id will increment by 1 always
        if self.movies==[]:
            return 0
        else:
            return max([m.id for m in self.movies])
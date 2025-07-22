from models.Cinema import Cinema
from models.Reservation import Reservation

from datetime import datetime

class ReservationManager:

    def __init__(self, cinema):
        self.cinema = cinema
        self.next_reservation_id = cinema.get_newest_reservation_id() + 1

    def make_reservation(self, screening_id, customer_name, customer_email, seats):
        screening = self.cinema.get_screening_by_id(screening_id)

        if not screening:
            return False, "The screening doesn't exist"

        for seat in seats:
            if not screening.is_seat_available(seat):
                return False, f"Seat {seat} is not available"

        reservation = Reservation(
            self.next_reservation_id,
            screening_id,
            customer_name,
            customer_email,
            seats
        )

        self.next_reservation_id += 1
        self.cinema.add_reservation(reservation)
        return True, reservation
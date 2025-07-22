class Screening:

    def __init__(self, id, movie_id, room_id, start_time, price):
        self.id = id
        self.movie_id = movie_id
        self.room_id = room_id
        self.start_time = start_time
        self.price = price
        self.reserved_seats = set() # seats which have been reserved

    # seat in (row, col)
    def is_seat_available(self, seat):
        return seat not in self.reserved_seats

    # reserve seats, return True if it's available
    def reserve_seats(self, seats):
        for seat in seats:
            if self.is_seat_available(seat):
                self.reserved_seats.add(seat)
                return True
        return False
    
    def get_available_seats(self, room):
        all_seats = [(row, col) for row in range(1, room.rows + 1) for col in range(1, room.cols + 1)]
        return [seat for seat in all_seats if seat not in self.reserved_seats]
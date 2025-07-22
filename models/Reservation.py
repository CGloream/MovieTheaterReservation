from datetime import datetime

class Reservation:

    def __init__(self, id, screening_id, customer_name, customer_email, seats):
        
        self.id = id
        self.screening_id = screening_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.seats = seats
        self.timestamp = datetime.now()
        
    def get_total_price(self, screening):
        return len(self.seats) * screening.price
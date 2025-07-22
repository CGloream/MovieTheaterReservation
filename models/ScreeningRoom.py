'''
Screening Room
'''
class ScreeningRoom:
    def __init__(self, id, name, rows, cols):
        self.id = id
        self.name = name
        self.rows = rows
        self.cols = cols
    
    def get_total_seats(self):
        return self.rows * self.cols
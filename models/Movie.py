
class Movie:
    
    def __init__(self, id, title, duration, rating, description):
        self.id = id
        self.title = title
        self.duration = duration # in minutes
        self.rating = rating
        self.description = description
    
    def __str__(self):
        return f"{self.title} ({self.rating}) - {self.duration} min"
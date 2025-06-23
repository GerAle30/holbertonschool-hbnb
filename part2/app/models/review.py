from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, user=None, place=None, rating=0, comment=""):
        super().__init__()
        self.user = user # ref user who wrote the review
        self.place = place # ref place being reviewed
        self.rating = rating
        self.comment = comment

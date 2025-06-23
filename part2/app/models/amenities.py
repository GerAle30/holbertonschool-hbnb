from .base_models import BaseModel


class Amenity(BaseModel):
    def __init__(self, name=""):
        super().__init__()
        self.name = name

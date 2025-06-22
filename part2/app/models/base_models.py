# app/models/base.py

import uuid
from datetime import datetime


class baseModel:
    def __init__(self):
        self.id = str(uuid.uuid4()))
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        def save(self):
            """Update the time stamp whenever the object"""
            self.updated_at = date time.now()

            def update(self, data):
                """Update using a dictionary"""
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                        self.save() 

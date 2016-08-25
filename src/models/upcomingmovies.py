from src.common.database import Database

__author__ = 'Akshay_Rahar'


class Upmovies(object):


    def __init__(self, poster, title, release_date):
        self.poster = poster
        self.title = title
        self.release_date = release_date

    def json(self):
        return {
            "poster": self.poster,
            "title": self.title,
            "release_date": self.release_date,
        }

    def save_to_mongo(self, genre):
        Database.insert(genre, self.json())

    @classmethod
    def from_mongo(cls, genre, id):
        data=Database.find(genre, {"_id":id})
        return cls(**data)




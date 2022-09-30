"""Creating table models"""
from . import db
from sqlalchemy.dialects.postgresql import JSONB

class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    names = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    

    def __repr__(self):
        return "<User {}>".format(self.username)

class Mood(db.Model):
    """Data model for moods"""

    __tablename__ = "Mood"
    userid = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(64), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return "<User {}>".format(self.userid)

class CollectiveMood(db.Model):
    """Data model for all moods"""

    __tablename__ = "CollectiveMood"
    userid = db.Column(db.Integer, primary_key=True)
    allmood = db.Column(db.Text, nullable=False) #Column(JSONB)
    
    def __repr__(self):
        return "<User {}>".format(self.userid)
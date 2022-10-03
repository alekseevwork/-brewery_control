from datetime import datetime
from email.policy import default
from sqlalchemy.orm import relationship

from webapp.db import db
from webapp.tank.enums import TitleBeer


class Tank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer(), nullable=False, unique=True)
    title = db.Column(db.Enum(TitleBeer), nullable=False)
    yeast = db.Column(db.String(50), nullable=False, default=0)
    actual_volume = db.Column(db.Integer, default=0)
    beer_grooving = db.Column(db.Boolean, default=False)
    cooling = db.Column(db.Boolean, default=False)


    def __repr__(self) -> str:
        return f'#{self.number} - {self.title}'


class Measuring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    density = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False, default=0)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    comment = db.Column(db.String(300))
    tank_id = db.Column(
        db.Integer,
        db.ForeignKey('tank.id', ondelete='CASCADE'), index=True)
    tank = relationship('Tank', backref='measurings')

    def __repr__(self) -> str:
        return f'Измерение ЦКТ {self.tank} за {self.create_at}'

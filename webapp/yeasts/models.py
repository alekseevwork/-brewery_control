from webapp.db import db

class Yeasts(db.Model):
    __tablename__ = "yeasts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    cycles = db.Column(db.Integer, default=0, nullable=False)
    #когда будет добавлена модель с цистерной, необходимо добавить связь один ко многим

    def __repr__(self):
        return f"Yeasts id: {self.id}, name: {self.name}"
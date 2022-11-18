from webapp.db import db
from webapp.stock.enums import ProductType


class Stock(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(100), nullable=False, unique=True)
    type_product = db.Column(db.Enum(ProductType), nullable=False)
    amount_product = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f'{self.name_product} - {self.amount_product}кг.'


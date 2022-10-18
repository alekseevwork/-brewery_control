from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from webapp.yeasts.enums import TypeOfYeast
from wtforms.validators import DataRequired

class YeastsForm(FlaskForm):
    yeasts_name = SelectField(
        'Сорт дрожжей:',
        choices=TypeOfYeast.list_names(),
        render_kw={'class': 'form-select'}
        )
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
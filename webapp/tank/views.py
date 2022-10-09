from flask import Blueprint ,flash, render_template, redirect, url_for

from webapp.db import db
from webapp.tank.forms import CreateTankForm, MeasuringForm
from webapp.tank.models import Tank, Measuring
from webapp.tank.utils import number_of_brews_for_full_tank, planned_expected_volume, cooling_beer_check, beer_grooving_check
from webapp.user.decorators import brewer_required

blueprint = Blueprint('tank', __name__, url_prefix='/tank')




@blueprint.route('/create-tank')
@brewer_required
def create_tank():
    page_title = 'Добавить ЦКТ'
    create_form = CreateTankForm()

    return render_template('tank/create_tank.html', title=page_title, form=create_form)

@blueprint.route('/process-create_tank', methods=['POST'])
@brewer_required
def process_create_tank():
    form = CreateTankForm()

    if form.validate_on_submit:
        if Tank.query.filter(Tank.number == form.number.data).count():
            flash('Данный ЦКТ уже занят')
            return redirect(url_for('tank.create_tank'))
        if not Tank.query.get(1):
            previous_brew_number = 1
        else:
            previous_brew_number = Tank.query.order_by(Tank.id.desc()).first().brew_number_last
        numbers_brew = number_of_brews_for_full_tank(form.number.data)

        new_tank = Tank(
            number=form.number.data,
            title=form.title.data,
            expected_volume= numbers_brew * planned_expected_volume(form.number.data),
            brew_number_first = previous_brew_number + 1,
            brew_number_last = previous_brew_number + numbers_brew,
            )   
        db.session.add(new_tank)
        db.session.commit()
        flash('ЦКТ добавлен')

    return redirect(url_for('user.home_page'))


@blueprint.route('/measuring')
def measuring_tank():
        page_title = 'Внести измерения'
        create_form = MeasuringForm()

        return render_template('tank/measuring.html', title=page_title, form=create_form)


@blueprint.route('/process-measuring', methods=['POST'])
def process_measuring():
    form = MeasuringForm()
    print(form.pressure.data)
    if form.validate_on_submit():
        new_measuring = Measuring(
            temperature = form.temperature.data,
            density = form.density.data,
            pressure = form.pressure.data,
            comment = form.comment.data,
            tank_id = form.tank_id.data
        )
        tank = Tank.query.get(new_measuring.tank_id)
        title_tank = tank.title.name
        if not tank.cooling:
            if not tank.beer_grooving:
                tank.beer_grooving = beer_grooving_check(title_tank, new_measuring.density)
            tank.cooling = cooling_beer_check(title_tank, new_measuring.density)
            
        db.session.add(new_measuring)
        db.session.commit()
        flash('Данные успешно заполнены')
        return redirect(url_for('tank.measuring_tank'))
    
    for field, error in form.errors:
        flash(field, error)
    return redirect(url_for('tank.measuring_tank'))

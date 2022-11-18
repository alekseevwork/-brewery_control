import json
from flask import Blueprint ,flash, render_template, redirect, url_for, request, jsonify
from flask_login import login_required

from webapp.db import db
from webapp.tank.forms import CreateTankForm, MeasuringForm, PourBeerForm
from webapp.tank.models import Tank, Measuring
from webapp.tank.utils import (
    create_diagrams_for_tanks,
    number_of_brews_for_full_tank,
    planned_expected_volume,
    is_beer_need_cooling,
    is_beer_need_grooving,
    show_error_message,
    )
from webapp.stock.models import Stock
from webapp.stock.utils import get_needs_materials_for_brew_in_stock, is_stock_products, is_amount_yasts_in_stock
from webapp.yeasts.models import Yeasts
from webapp.yeasts.utils import get_the_right_yeasts, get_list_of_suitable_tanks, get_id_now_yeast, get_need_yasts
from webapp.user.decorators import brewer_required

blueprint = Blueprint('tank', __name__, url_prefix='/tank')


@blueprint.route('/<int:tank_id>')
@login_required
def view_tank_info(tank_id):
    tank = Tank.query.filter(Tank.id == tank_id).first()
    yeats = Yeasts.query.filter(Yeasts.id == tank.yeasts_id).first()
    measuring = Measuring.query.order_by(Measuring.create_at.asc()).filter(Measuring.tank_id == tank_id).all()
    page_title = 'Информация по ЦКТ'
    
    return render_template('tank/tank_info.html', title=page_title, tank=tank, measuring=measuring, yeats=yeats)

@blueprint.route('/delete/<int:tank_id>')
@login_required
def delete_tank(tank_id):
    tank = Tank.query.get(tank_id)
    db.session.delete(tank)
    db.session.commit()
    flash('ЦКТ удален')

    return redirect(url_for('main.view_tanks'))


@blueprint.route('/create-tank')
@brewer_required
def create_tank():
    page_title = 'Добавление ЦКТ'
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
        if not Tank.query.count():
            previous_brew_number = 0
        else:
            previous_brew_number = Tank.query.order_by(Tank.id.desc()).first().brew_number_last
        numbers_brew = number_of_brews_for_full_tank(form.number.data)
        
        materials_for_brew = get_needs_materials_for_brew_in_stock(form.title.data, numbers_brew, form.number.data)
        errors = []
        for material in materials_for_brew.keys():
            try:
                in_stock_product = Stock.query.filter(Stock.name_product == material).first().amount_product
            except AttributeError:
                in_stock_product = 0
            is_product, count = is_stock_products(in_stock_product, materials_for_brew[material])
            if is_product:
                errors.append(f'Не хватает {count}кг {material}')
 
        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('stock.append_in_stock'))
        else:
            for material in materials_for_brew:
                Stock.query.filter(Stock.name_product==material).\
                    update({Stock.amount_product:Stock.amount_product - float(materials_for_brew[material])}, synchronize_session = False)
                db.session.commit()
        now_id, generation = get_id_now_yeast(form.yeasts.data)
        name_yasts = get_the_right_yeasts(form.title.data)
        if now_id <= 0:
            generation = 0
            add_generation = 1
            amount_yasts = get_need_yasts(name_yasts, numbers_brew)
            if is_amount_yasts_in_stock(amount_yasts, name_yasts.stock_name()):
                if Stock.query.filter(Stock.name_product==name_yasts.stock_name()).count():
                    Stock.query.filter(Stock.name_product==name_yasts.stock_name()).\
                            update({Stock.amount_product:Stock.amount_product - float(amount_yasts)}, synchronize_session = False)
                    flash('Нет подходящих дрожжей. Нужно использовать сухие')
                    add_generation = 0
            else:
                flash(f'Не хватает {amount_yasts}кг {name_yasts.stock_name()}')
                return redirect(url_for('stock.append_in_stock'))
        new_yeast = Yeasts(
            name = name_yasts,
            cycles = generation + add_generation
        )
        db.session.add(new_yeast)
        db.session.commit()

        new_tank = Tank(
            number=form.number.data,
            title=form.title.data,
            yeasts_id = new_yeast.id,
            expected_volume= numbers_brew * planned_expected_volume(form.number.data),
            brew_number_first = previous_brew_number + 1,
            brew_number_last = previous_brew_number + numbers_brew,
            ) 
        db.session.add(new_tank)
        db.session.commit()
        flash('ЦКТ добавлен')
    return redirect(url_for('tank.view_tank_info', tank_id = new_tank.id))


@blueprint.route('/measuring')
def measuring_tank():
        page_title = 'Внесение измерения'
        create_form = MeasuringForm()

        return render_template('tank/measuring.html', title=page_title, form=create_form)


@blueprint.route('/process-measuring', methods=['POST'])
def process_measuring():
    form = MeasuringForm()
    if form.validate_on_submit():
        new_measuring = Measuring(
            temperature = form.temperature.data,
            density = form.density.data,
            pressure = form.pressure.data,
            comment = form.comment.data,
            tank_id = form.tank_id.data
        )
        tank = Tank.query.get(new_measuring.tank_id)
        title_tank = tank.title
        if not tank.cooling:
            if not tank.beer_grooving:
                tank.beer_grooving = is_beer_need_grooving(title_tank, new_measuring.density)
            tank.cooling = is_beer_need_cooling(title_tank, new_measuring.density)
            
        db.session.add(new_measuring)
        db.session.commit()
        flash('Данные успешно заполнены')
        return redirect(url_for('tank.measuring_tank'))
    
    show_error_message(form.errors.items())
    return redirect(url_for('tank.measuring_tank'))


@blueprint.route('/yeast-request-processing', methods=['GET', 'POST'])
def get_choise_suitable_tanks():

    if request.method == 'POST':
        choise_title_beer = str(request.data)[2:-1]
        yeast = get_the_right_yeasts(choise_title_beer)
        list_tanks = get_list_of_suitable_tanks(yeast)
        if not list_tanks:
            return ['Нет подходящих дрожжей']
        else:
            jsonList = json.dumps(list_tanks)
            return jsonList
    return redirect(url_for('tank.create_tank'))


@blueprint.route('/pour-beer')
@login_required
def pour_beer():
    page_title = 'Разлив пива из ЦКТ'
    form = PourBeerForm()

    return render_template('tank/pour_beer.html', title=page_title, form=form)


@blueprint.route('/process-pour-beer', methods=['POST'])
@login_required
def process_pour_beer():
    form = PourBeerForm()
    if form.validate_on_submit():
        volume_of_bottled_beer = form.kegs.data * form.volume.data
        tank = Tank.query.filter(Tank.id == form.tank_id.data).first()
        if tank:
            tank.actual_volume += volume_of_bottled_beer
            db.session.commit()
            flash('Данные успешно внесены')
        else:
            flash('Выбранная ЦКТ не обнаружена.')
    else:
        show_error_message(form.errors.items())
    return redirect(url_for('tank.pour_beer'))

@blueprint.route('/tanks-view', methods=['GET'])
def view_tanks():
    diagrams = create_diagrams_for_tanks()
    return jsonify({
            'diagrams': diagrams
        })


@blueprint.route('/tanks-info', methods=['GET'])
def view_info():
    args = request.args
    tank_measuring = []
    tank = Tank.query.filter(Tank.id == args['tank_id']).first()
    yeats = Yeasts.query.filter(Yeasts.id == tank.yeasts_id).first()
    for measuring in Measuring.query.order_by(Measuring.create_at.asc()).filter(Measuring.tank_id == tank.id).all():
        tank_measuring.append(dict(
            temperature=measuring.temperature,
            density=measuring.density,
            pressure=measuring.pressure,
            comment=measuring.comment,
            create_at=measuring.create_at.strftime("%d-%m-%Y, %H:%M")
        ))
    return jsonify({
        'tank_number': tank.number,
        'tank_title_value': tank.title.value,
        'yeats': yeats.name.value,
        'tank_beer_grooving': 'Да' if tank.beer_grooving else 'Нет',
        'tank_cooling': 'Да' if tank.cooling else 'Нет',
        'tank_expected_volume': tank.expected_volume,
        'tank_actual_volume': tank.actual_volume,
        'measuring': tank_measuring
    })

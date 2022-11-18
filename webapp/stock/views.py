import json
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError, DataError

from webapp.db import db
from webapp.stock.form import AppendProductForm
from webapp.stock.models import Stock
from webapp.stock.utils import get_the_right_product
    

blueprint = Blueprint('stock', __name__, url_prefix='/stock')

@blueprint.route('/append-in-stock')
@login_required
def append_in_stock():
    page_title = 'Внести сырье на склад'
    create_form = AppendProductForm()

    return render_template('stock/append_in_stock.html', title=page_title, form=create_form)


@blueprint.route('/process-append', methods=['POST'])
@login_required
def process_append_in_stock():
    form = json.loads(request.data)
    for index in range(len(form["type_product"])):
        if form["type_product"][index] == 'None':
            flash(f'Ошибка ввода')
        else:
            try:
                new_product = Stock(
                    type_product = form["type_product"][index],
                    name_product = form["name_product"][index],
                    amount_product = float(form["amount_product"][index])
                )

                db.session.add(new_product)
                db.session.commit()
                flash('Добавлено')

            except IntegrityError:
                db.session.rollback()
                Stock.query.filter(Stock.name_product==form["name_product"][index]).\
                    update({Stock.amount_product:float(form["amount_product"][index]) + Stock.amount_product}, synchronize_session = False)
                db.session.commit()
                flash('Обновлено')

            except DataError:
                flash('Ошибка ввода')
    
    return redirect(url_for('stock.append_in_stock'))


@blueprint.route('/process-request-append', methods=['GET', 'POST'])
def get_choise_suitable_product():

    if request.method == 'POST':
        choise_type_product = str(request.data)[2:-1]
        product = get_the_right_product(choise_type_product)
        list_product = product
        jsonList = json.dumps(list_product)
        return jsonList
    return redirect(url_for('tank.create_tank'))


@blueprint.route('/stock-view')
def stock_view():
    
    page_title = 'Склад'
    content = Stock.query.order_by(Stock.type_product).all()

    return render_template('stock/stock_view.html', title=page_title, content=content)

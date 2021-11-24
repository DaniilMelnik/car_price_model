from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
import flask
import pandas as pd
import urllib.request
from urllib.error import URLError
import json


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='fhfgfahhkmhjrtyrsthfgvcnvb',
)


def get_prediction(model, brand, year, transmission, mileage, fuel_type, tax, mpg, engineSize):
    body = {
        "brand": brand,
        "model": model,
        "year": year,
        "transmission": transmission,
        "mileage": mileage,
        "fuelType": fuel_type,
        "tax": tax,
        "mpg": mpg,
        "engineSize": engineSize,
    }

    myurl = "http://192.168.0.106:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    json_data = json.dumps(body)
    json_data_as_bytes = json_data.encode('utf-8')
    req.add_header('Content-Length', len(json_data_as_bytes))
    response = urllib.request.urlopen(req, json_data_as_bytes)
    return json.loads(response.read())['predictions']


train_data = pd.read_csv('data/X_train.csv')

page_data = {
    'menu': ['Главная страница', 'О сайте']
}

allowed_data = {
    'car_models': train_data.groupby('brand')['model'].apply(set),
    'transmissions': train_data['transmission'].unique(),
    'fuel_types': train_data['fuelType'].unique(),
}


def check_parameter(value, type_func, allowed_values: tuple, name):
    try:
        value = type_func(value)
    except ValueError:
        flash(f'{name} должен иметь тип {type_func.__name__}', category='error')
    else:
        if value < allowed_values[0] or value > allowed_values[1]:
            flash(f'Введите значения {name} в диапазоне от {allowed_values[0]} до {allowed_values[1]}',
                  category='error')


@app.route("/", methods=['GET', 'POST'])
def index():
    page_data.update(allowed_data)
    if request.method == 'POST':
        model, brand = flask.request.form.get('Модель').split(' - ')
        year = flask.request.form.get('year')
        transmission = flask.request.form.get('Коробка передач')
        mileage = flask.request.form.get('mileage')
        fuel_type = flask.request.form.get('Тип топлива')
        tax = flask.request.form.get('tax')
        mpg = flask.request.form.get('mpg')
        engineSize = flask.request.form.get('engineSize')

        check_parameter(year, int, (1997, 2020), 'Год')
        check_parameter(mileage, int, (0, 260000), 'Пробег')
        check_parameter(tax, int, (0, 600), 'Налог')
        check_parameter(mpg, int, (2, 480), 'Расход')
        check_parameter(engineSize, float, (0, 6.6), 'Обхем двигателя')

        if not get_flashed_messages():
            flash(f'Данные отправлены', category='success')
            try:
                response = get_prediction(model, brand, year, transmission, mileage, fuel_type, tax, mpg, engineSize)
                print(response)
            except ConnectionError:
                response = json.dumps({"error": "ConnectionError"})
            except URLError:
                response = json.dumps({"error": "URLError"})
            return redirect(url_for('predicted', response=response))

    return render_template('index.html', **page_data)


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    return render_template('predicted.html', response=response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)

import pandas as pd

from flask import Flask, escape, request
from joblib import load

app = Flask(__name__)

reg = None

class Predictor:
    __reg = None
    __scaler = None

    @classmethod
    def _load_regressor(cls):
        cls.__reg = load('regressor.joblib')

    @classmethod
    def _load_scaler(cls):
        cls.__scaler = load('scaler.joblib')

    @classmethod
    def get_prediction(
        cls,
        location,
        product,
        date,
        temp_mean,
        temp_min,
        temp_max,
        sun,
        is_special_event,
        price,
    ):
        if cls.__reg is None:
            cls._load_regressor()
        
        if cls.__scaler is None:
            cls._load_scaler()

        date = pd.to_datetime(date)
        df = pd.DataFrame(data={
            'location': [int(location)],
            'product': [int(product)],
            'temp_mean': [float(temp_mean)],
            'temp_min': [float(temp_min)],
            'temp_max': [float(temp_max)],
            'sunshine_quant': [float(sun)],
            'price': [float(price)],
            'is_special_event': [float(is_special_event)],
            'weekday': [date.weekday()],
            'day_of_year': [(date.month - 1)*32 + (date.day - 1)]
        })

        print(df)
        df = cls.__scaler.transform(df)

        prediction = cls.__reg.predict(df)

        return prediction[0]

@app.route('/')
def predictSales():
    location = request.args.get("location")
    date = request.args.get("date")
    product = request.args.get("product")
    temp_mean = request.args.get("temp_mean")
    temp_min = request.args.get("temp_min")
    temp_max = request.args.get("temp_max")
    sun = request.args.get("sun")
    is_special_event = request.args.get("is_special_event")
    price = request.args.get("price")

    prediction = Predictor.get_prediction(
        location,
        product,
        date,
        temp_mean,
        temp_min,
        temp_max,
        sun,
        is_special_event,
        price,
    )

    return {'prediction': prediction}
import numpy as np
import pandas as pd

from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
from joblib import load

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

reg = None

class Predictor:
    __reg = None
    __scaler = None
    __outlier_clf = None
    __no_temp_reg = None
    __outlier_reg = None

    @classmethod
    def predict(cls, df):
        if cls.__reg is None:
            cls.__reg = load('../models/regressor.joblib')

        if cls.__scaler is None:
            cls.__scaler = load('../models/scaler.joblib')

        if cls.__outlier_clf is None:
            cls.__outlier_clf = load('../models/outlier_classifier.joblib')

        if cls.__no_temp_reg is None:
            cls.__no_temp_reg = load('../models/no_temp_reg.joblib')

        if cls.__outlier_reg is None:
            cls.__outlier_reg = load('../models/outlier_reg.joblib')

        prediction = 0.0

        has_no_temp = np.any(np.isnan(df['temp_mean']))
        df = df.drop(columns=['temp_mean'])
        if has_no_temp:
            df = df.drop(columns=['temp_max', 'temp_min', 'sunshine_quant'])
            df = cls.__scaler.transform(df)
            prediction = cls.__no_temp_reg.predict(df)
        else:
            df = cls.__scaler.transform(df)
            is_outlier = cls.__outlier_clf.predict(df)
            if is_outlier[0] == 0:
                prediction = cls.__reg.predict(df)
            else:
                prediction = cls.__outlier_reg.predict(df)
        
        return prediction[0]

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

        prediction = cls.predict(df)

        return prediction

@app.route('/')
@cross_origin()
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

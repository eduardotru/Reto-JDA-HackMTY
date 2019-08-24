import pandas as pd
import numpy as np

data = pd.read_csv('../input_data_train.csv')

# We do not care of the type of the event since we have the data, we only care
# if it's special or not
print('Transforming: Is special event')
data['is_special_event'] = data['event'].notna().astype(float)

# We transform the date into the weekday as weekends may influence the sale
# of beer
print('Transforming: Date')
data['date'] = pd.to_datetime(data['date'])

print('Transforming: Weekday')
data['weekday'] = data['date'].dt.weekday

# We care of the day of year (month * 32) + day
print('Transforming: Day of year')
data['day_of_year'] = (data['date'].dt.month - 1)* 32 + (data['date'].dt.day - 1)

# The price which are null will be filled with the average price of the beer
# by location and product
print('Transforming: Filling empty prices')
data['price'] = data.groupby(['product', 'location'])['price'].transform(lambda x: x.fillna(x.mean()))

# This are the columns we care about now
important_columns = [
    'location',
    'product',
    'sa_quantity',
    'temp_mean',
    'temp_max',
    'temp_min',
    'sunshine_quant',
    'price',
    'is_special_event',
    'weekday',
    'day_of_year'
]

print('Transforming: Getting important columns')
data = data[important_columns]

# We may need to train 2 models, one with temperatures and one without
print('Transforming: Separating info without temperature')
data_with_temp = data[data['temp_mean'].notna()]
data_no_temp = data[data['temp_mean'].isna()]

print('Transforming: Saving information')
data_with_temp.to_csv(path_or_buf='../data_with_temp_processed.csv')
data_no_temp.to_csv(path_or_buf='../data_no_temp_processed.csv')

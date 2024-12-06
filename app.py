import streamlit as st
import datetime
import requests
import pandas as pd

st.markdown('''
# Welcome to BaronBarK's TaxiFareModel 🚕

This wonderfully simple website will let you use the Taxifare API to predict a the price of a taxi ride

*Note : This model has been trained with New York taxi data and, as such, will work better with NY adresses*


''')

st.markdown('''

## Please enter the desired ride infos below
''')

date = st.date_input(
    "Ride date (YYYY/MM/DD)",
    datetime.date(2019, 1, 1))

time = st.time_input('Ride time (HH:MM)',
                     datetime.time(12,0))

pickup_long = st.number_input('Input the pick-up longitude', value=-73.977295)

pickup_lat = st.number_input('Input the pick-up latitude', value=40.752655)

dropoff_long = st.number_input('Input the drop-off longitude', value=-73.780968)

dropoff_lat = st.number_input('Input the drop-off latitude', value=40.641766)

passenger_count = st.number_input('How many passengers ?', value=1)

button = st.button("Compute taxi fare 💲")

df= pd.DataFrame({'lat':[pickup_lat, dropoff_lat], 'lon':[pickup_long, dropoff_long], 'color':["#008000", "#ff0000"]})

url = 'https://taxifare.lewagon.ai/predict'
params={
    "pickup_datetime":f"{date} {time}",
    "pickup_longitude":pickup_long,
    "pickup_latitude":pickup_lat,
    "dropoff_longitude":dropoff_long,
    "dropoff_latitude":dropoff_lat,
    "passenger_count":passenger_count
}

if button:
    if pickup_long and pickup_lat and dropoff_long and dropoff_lat and passenger_count:
        apiresponse = requests.get(url, params=params)
        fare = apiresponse.json()["fare"]
        response = f'''
        ## The taxi fare would be : {round(fare,2)}$
        '''
    else:
        response = f'''
        ## Waiting for inputs
        Some information is missing to compute a taxi fare, please check your inputs in the fields above.'''
    response

    st.map(df, color="color", size=10)
    '''*Legend: Pick_location in GREEN, Drop_off location in RED*'''

import streamlit as st
import datetime
import requests
import pandas as pd
import urllib.parse

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

pickup_address = st.text_input('Pick-up location adress', value="Grand Central Terminal")

# getting pick-up location latitude and longitude
pickup_url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(pickup_address) +'&format=json'
pickup = requests.get(pickup_url, headers={'User-Agent':'taxifare_baronbark'}).json()
pickup_long = float(pickup[0]["lon"])
pickup_lat = float(pickup[0]["lat"])

dropoff_address = st.text_input('Drop-off location adress', value="JFK Airport")

# getting drop-off location latitude and longitude
dropoff_url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(dropoff_address) +'&format=json'
dropoff = requests.get(dropoff_url, headers={'User-Agent':'taxifare_baronbark'}).json()
dropoff_long = float(dropoff[0]["lon"])
dropoff_lat = float(dropoff[0]["lat"])

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

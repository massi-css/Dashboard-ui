import random
from pymongo import MongoClient 
import streamlit as st
import yaml 
from yaml.loader import SafeLoader
import requests
from json import JSONDecodeError
import pyperclip




# initialize the config
with open('config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# retieve the uri, database name from the config file
uri = config['mongodb']['uri']
database_name = config['mongodb']['database']
server_uri = config['server']['uri']
api_key = config['APIKEY']['key']
user_id = config['USERID']['id']


# connect to mongo db
def connect_to_db(uri, database_name, collection_name):
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]
    return collection

# get the authenfication status
def get_authentication_status():
    authentication = connect_to_db(uri, database_name, "authentication")
    status = authentication.find_one().get('status')
    return status

def set_authentication_status(status):
    authentication = connect_to_db(uri, database_name, "authentication")
    authentication.update_one({}, {"$set": {"status": status}})
    return status

# create a user
def create_user(collection, username, password, email, name):
    # hashed_password = stauth.Hasher([password]).generate()
    user = {
        'username': username,
        'password': password,
        'email': email,
        'name': name
    }
    try:
        if collection.find_one({"username": username}):
            return False
        if collection.insert_one(user):
            return True
    except Exception as e:
        print(f"An error occurred: {e}")

# authenticate user
def authenticate_user(collection, username, password):
    # hashed_password = stauth.Hasher([password]).generate()
    user = collection.find_one({"username": username, "password":password})
    if user:
        return True
    else:
        return False

def logout():
    st.session_state.authenticated = set_authentication_status(False)
    st.rerun()

# get all devices
def get_devices():
    try:
        response = requests.get(f"{server_uri}/devices")
        devices = response.json()
        return devices
    except JSONDecodeError:
        print("Empty response received from the server")
        return []

# get device by id 
def get_device_by_id(device_id):
    try:
        response = requests.get(f"{server_uri}/devices/{device_id}")
        device = response.json()
        return device
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}

# create a device
def create_device(device):
    try:
        response = requests.post(f"{server_uri}/devices", json=device)
        device = response.json()
        return device
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}

# update a device
def update_device(device_id, device):
    try:
        response = requests.put(f"{server_uri}/devices/{device_id}", json=device)
        device = response.json()
        return device
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}

# delete a device
def delete_device(device_id):
    try:
        response = requests.delete(f"{server_uri}/devices/{device_id}")
        device = response.json()
        return device
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}

# delete all devices 
def delete_all_devices():
    try:
        response = requests.delete(f"{server_uri}/devices")
        devices = response.json()
        return devices
    except JSONDecodeError:
        print("Empty response received from the server")
        return []
    
# get device data
def get_device_data(device_id):
    try:
        response = requests.get(f"{server_uri}/data/{device_id}")
        data = response.json()
        return data
    except JSONDecodeError:
        print("Empty response received from the server")
        return []

# get latest device data
def get_latest_device_data(device_id):
    try:
        response = requests.get(f"{server_uri}/data/latest/{device_id}")
        data = response.json()
        return data
    except JSONDecodeError:
        print("Empty response received from the server")
        return []

# reset device data
def reset_device_data(device_id):
    try:
        response = requests.delete(f"{server_uri}/devices/data/{device_id}")
        data = response.json()
        return data
    except JSONDecodeError:
        print("Empty response received from the server")
        return []
    
# get all notifications
def get_notifications():
    try:
        response = requests.get(f"{server_uri}/notifications")
        notifications = response.json()
        return notifications
    except JSONDecodeError:
        print("Empty response received from the server")
        return []

# while we have only one user its not nessesary to have a user_id parameter so defined it as a global variable
def get_user_by_Id():
    try:
        response = requests.get(f"{server_uri}/users/{user_id}")
        user = response.json()
        return user
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}

def update_user(user):
    try:
        response = requests.put(f"{server_uri}/users/{user_id}", json=user)
        user = response.json()
        return user
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}
def update_notification(user):
    try:
        response = requests.put(f"{server_uri}/users/{user_id}/notifications", json=user)
        user = response.json()
        return user
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}
    
# calculates the water quality index
def calculate_wqi(ph, turbidity, conductivity, temperature):
    """
    Calculate Water Quality Index (WQI) based on specified parameters.
    
    Args:
    ph: pH value of the water sample.
    turbidity: Turbidity value in NTU (Nephelometric Turbidity Units).
    conductivity: Conductivity value in μS/cm (microsiemens per centimeter).
    temperature: Water temperature in Celsius.
    
    Returns:
    Water Quality Index (WQI) value.
    """
    
    # Weightage factors for each parameter
    ph_weight = 0.25
    turbidity_weight = 0.25
    conductivity_weight = 0.25
    temperature_weight = 0.25
    
    # Normalize parameters
    ph_norm = (ph - 6) / (8.5 - 6) * 100
    turbidity_norm = (turbidity / 5) * 100  # Assuming maximum acceptable turbidity is 5 NTU
    conductivity_norm = (conductivity / 1500) * 100  # Assuming maximum acceptable conductivity is 1500 μS/cm
    temperature_norm = (temperature - 0) / (30 - 0) * 100  # Assuming temperature range from 0 to 30 Celsius
    
    # Calculate sub-indices
    ph_index = ph_norm * ph_weight
    turbidity_index = turbidity_norm * turbidity_weight
    conductivity_index = conductivity_norm * conductivity_weight
    temperature_index = temperature_norm * temperature_weight
    
    # Calculate WQI
    wqi = ph_index + turbidity_index + conductivity_index + temperature_index
    
    return wqi

def copy_to_clipboard(text):
    pyperclip.copy(text)
# get latest 10 rows of forcasted data
async def get_latest_forcasted_data(deviceId):
    try:
        response = await requests.get(f"{server_uri}/forcast/{deviceId}/all")
        data = response.json()
        return data
    except JSONDecodeError:
        print("Empty response received from the server")
        return {}

# get latest line of forcasted data

async def get_last_forcasted_data(deviceId):
    try:
        response = await requests.get(f"{server_uri}/forcast/{deviceId}")
        data = response.json()
        return data
    except JSONDecodeError :
        print("Empty response received from the server")
        return {}
    
async def forcast_next_day(deviceId,data):
    try:
        response = await requests.post(f"{server_uri}/forcast/{deviceId}",json=data)
        data = response.json()
        return data
    except JSONDecodeError :
        print("Empty response received from the server")
        return {} 
    
def generate_random_lat_long(min_lat, max_lat, min_long, max_long):
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_long, max_long)
    return latitude, longitude
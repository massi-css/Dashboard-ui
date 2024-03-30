from pymongo import MongoClient 
import streamlit as st
import yaml 
from yaml.loader import SafeLoader
import requests
from json import JSONDecodeError




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


    

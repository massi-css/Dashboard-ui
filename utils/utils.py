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


def getLatestTemperature():
    response = requests.get('http://localhost:5000/data/temperature/latest')
    try:
        data = response.json()
        return data
    except JSONDecodeError:
        print("Empty response received from the server")
        return None

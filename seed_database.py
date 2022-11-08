# SEED_DATABASE.PY

# SETUP
########################################################################

# os > operating systenm connection
import os
# json >
import json
# random > choice > takes in a list and returns a random element in the list
# random > randit > return a random number within a certain range
from random import choice, randint
# datetime > datetime >  turn a string into a Python datetime object.
from datetime import datetime

# Import from crud.py
import crud
# Import from model.py
import model
# Import from server.py
import server

# Database reset
########################################################################

# Drop the database ratings
os.system("dropdb ratings")
# Create the database ratings
os.system("createdb ratings")

# Connect to the model.py > db > and create all the tables outlined in the file
########################################################################

# access the database
model.connect_to_db(server.app)
# create all the tables for PostreSQL
model.db.create_all()

# EXECUTE
########################################################################
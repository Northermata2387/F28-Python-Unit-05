# CRUD.PY

# SETUP
########################################################################

from model import db, User, Movie, Rating, connect_to_db


# EXECUTE
########################################################################

# import to server.py and conncet to db
if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
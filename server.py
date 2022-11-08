# SERVER.PY

# SETUP
########################################################################

# flask > Flask >
from flask import Flask

# define Flask name of this file to app for simple and clean coding
app = Flask(__name__)


# Replace this with routes and view functions!


# EXECUTE
########################################################################

# run the application
if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)

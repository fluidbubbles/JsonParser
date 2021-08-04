from flask import Flask
from flask_restful import Api

import auth
from api import resources
# from config import API_PREFIX


app = Flask(__name__)
api = Api(app)

# Register api resources
api.add_resource(resources.Parser, '/parse')

# Register auth verification handlers
auth.auth.verify_password(auth.authenticate)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

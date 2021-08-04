from flask_httpauth import HTTPBasicAuth
from config import AUTH

auth = HTTPBasicAuth()


def authenticate(username, password):
    """Verify username and password """
    if not (username and password):
        return False
    return AUTH.get(username) == password


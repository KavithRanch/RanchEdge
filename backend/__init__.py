import os
from flask import Flask
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')


from backend import routes
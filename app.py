import os
from flask import Flask, jsonify, request, flash
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from services.users import register_user, login_user, forgot_password, change_password, edit_profile, get_user_detail
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
CORS(app)
bcrypt = Bcrypt(app)

MONGODB_URI = os.environ.get('MONGODB_URI_PART1') # add db url
client = MongoClient(MONGODB_URI + '&w=majority')
database = client.rentalvista

@app.route("/users/signup", methods=["POST"])
def signup():
    user = database.user
    data = request.json
    print(data)
    return register_user(data["name"], data["email"], data["password"], data["contact"], user, bcrypt)

@app.route("/users/login", methods=["POST"])
def login():
    user = database.user
    data = request.json
    return login_user(data["email"], data["password"], user, bcrypt)

@app.route("/users/forgot", methods=["POST"])
def forgot():
    user = database.user
    data = request.json
    return forgot_password(data['email'], user, mail, bcrypt)

@app.route("/users/change", methods=["POST"])
def change():
    token = request.headers['Authorization']
    user = database.user
    data = request.json
    return change_password(token, data['password'], data['new_password'], user, bcrypt)

@app.route("/users/user", methods=["POST"])
def user_detail():
    token = request.headers['Authorization']
    user = database.user
    return get_user_detail(token, user)

@app.route("/users/edit", methods=["POST"])
def edit():
    token = request.headers['Authorization']
    user = database.user
    data = request.json
    return edit_profile(token, data['name'], data['contact'], user)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
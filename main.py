# -*- coding: utf-8 -*-
import os
import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
from src.objects.Application import Application
app = Flask(__name__)
app.config['DEBUG'] = True

# load the environment variables
load_dotenv('.env')

@app.route("/")
def homepage():
    return render_template("user_form.html")

@app.route('/addDetails', methods=['POST'])
def addDetails(payload):
    # Instantiate the Application object and execute required method.
    obj = Application(payload)
    # Insert data
    obj.add_details()
    return render_template('user_form_response.html')

@app.route('/get_data', methods=['GET'])
def data():
    data = get_data()
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete(payload):
    Application(None).delete(payload)



if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)

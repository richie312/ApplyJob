# -*- coding: utf-8 -*-
import os
import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
from flask_restx import Api
from src.objects.Application import Application


app = Flask(__name__)
app.config['DEBUG'] = True
# api = Api(app, version='1.0', title='Common Database API',
#                 description='Common Database for all my application.')

# load the environment variables
load_dotenv('.env')

@app.route("/")
def homepage():
    return render_template("user_form.html")

@app.route('/addDetails', methods=['POST'])
#@api.doc(params={'columns': []})
def addDetails(payload):
    # Instantiate the Application object and execute required method.
    obj = Application(payload["TableName"],payload)
    # Insert data
    obj.add_details()
    return render_template('user_form_response.html')

@app.route('/get_data', methods=['GET'])
def data(payload):
    data = Application(payload["TableName"]).get_data()
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete(payload):
    Application(payload["TableName"]).delete(payload)



if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)

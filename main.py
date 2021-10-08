# -*- coding: utf-8 -*-
import os
import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
from flask_restx import Api
from src.objects.Application import Application


app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app, version='1.0', title='Common Database API',
                description='Common Database for all my application.')

# load the environment variables
load_dotenv('.env')

@app.route("/")
def homepage():
    return render_template("user_form.html")

@app.route('/addDetails', methods=['POST'])
def addDetails(payload):
    # Instantiate the Application object and execute required method.
    obj = Application(payload["TableName"],payload)
    # Insert data
    obj.add_details()
    return render_template('user_form_response.html')

@app.route('/get_data', methods=['GET'])
def data():
    payload = request.args
    print(payload)
    data = Application(payload).get_data()
    return jsonify(data)

@app.route('/delete', methods=['POST'])
@api.doc(params={'TableName': "Target Table name",
                 "Column":"ColumnName",
                 "Value": "value to be deleted from the column."})
def delete():
    payload = request.get_json()
    Application(payload["TableName"]).delete(payload)
    return {"Operation": "Successful"}



if __name__ == '__main__':
    app.run(host = '127.0.0.1',debug=True,port=5001)

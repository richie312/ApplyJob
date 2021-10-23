# -*- coding: utf-8 -*-
from flask import Flask, request, json,render_template,redirect,url_for,jsonify
from dotenv import load_dotenv
from flask_restx import Api, Resource, fields
from src.objects.Application import Application


app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app, version='1.0', title='Common Database API',
                description='Common Database for all my application.')

# load the environment variables
load_dotenv('.env')
@api.route('/get_data/', methods=["GET"])
@api.doc(params={'TableName': 'mission_half_marathon'})
class MyResource(Resource):
    def get(self):
        t = request.args
        data = Application(t).get_data()
        return jsonify(str(data))

@api.route('/add_details', methods=["POST"])
class MyResource(Resource):
    def post(self):
        t = request.get_json()
        print(t)
        data = Application(t).add_details()
        response = {"Response": "Successfully! added the details in the {table} table.".format(table=t["TableName"])}
        return jsonify(response)


@app.route('/delete', methods=['POST'])
@api.doc(params={'TableName': "Target Table name",
                 "Column":"ColumnName",
                 "Value": "value to be deleted from the column."})
def delete():
    payload = request.get_json()
    Application(payload).delete()
    return {"Operation": "Successful"}



if __name__ == '__main__':
    app.run(host = '127.0.0.1',debug=True,port=5001)

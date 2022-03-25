from flask import Flask, request, jsonify, make_response, render_template
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask_restx import Api, Resource, fields
from src.server.flask_server import app, db
from src.Auth.Authentication import token_required
from src.sql.sqlite import User
from src.objects.Application import Application
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}
api = Api(app,
          version='1.0',
          title='Common Database API',
          authorizations=authorizations,
          security='apikey',
          description='Common Database for all my application.')


@app.route("/docs", methods = ['GET'])       
def docs():
    return render_template("api_docs.html")

@api.route('/user', endpoint='user')
@api.doc(params={})
class MyResource(Resource):
    @api.doc(responses={201: 'Authorization Successful'})
    @token_required
    def get(self,current_user):
        # querying the database
        # for all the entries in it
        users = User.query.all()
        # converting the query objects
        # to list of jsons
        output = []
        for user in users:
            # appending the user data json
            # to the response list
            output.append({
                'public_id': user.public_id,
                'name': user.name,
                'email': user.email
            })

        return jsonify({'users': output})

# route for logging user in
@api.route('/login', endpoint='login')
@api.doc(params={'email': "youremailid@domain.com",
                 "password": "yourpassword@123",
                 "session_time": "Accept in days; optional argument. By default the token is valid for 30 days."})
class MyResource(Resource):
    @api.doc(responses={201: 'Authorization Successful'})
    def post(self):
        # creates dictionary of form data
        auth = request.args if request.args else request.form
        session_time = auth.get("session_time") if auth.get("session_time") != None else 30
        if not auth or not auth.get('email') or not auth.get('password'):
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )
        user = User.query \
            .filter_by(email=auth.get('email')) \
            .first()
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )
        if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(days=session_time)
            }, app.config['SECRET_KEY'])

            return make_response(jsonify({'token': token.decode('UTF-8')}), 201)

        # returns 403 if password is wrong
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )


# signup route

@api.route('/signup', endpoint='signup')
@api.doc(params={'name': 'yourusername',
                 "password": "yourpassword@123",
                 "email": "youremailid@domain.com"})
class MyResource(Resource):
    @api.doc(responses={403: 'Not Authorized'})
    def post(self):
        # creates a dictionary of the form data
        data = request.args if request.args else request.form
        print(data)
        # gets name, email and password
        name, email = data.get('name'), data.get('email')
        password = data.get('password')
        print(password)
        # checking for existing user
        user = User.query \
            .filter_by(email=email) \
            .first()
        if not user:
            # database ORM object
            # generate the password and keep track of it.
            password_user = generate_password_hash(password)
            user = User(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                password= password_user,
                created = datetime.now()
            )
            # insert user
            db.session.add(user)
            db.session.commit()
            return make_response('Successfully registered.', 201)
        else:
            # returns 202 if user already exists
            return make_response('User already exists. Please Log in.', 202)


@api.route('/get_data/', methods=["GET"])
class MyResource(Resource):
    @api.doc(params={'TableName': 'mission_half_marathon'}, security='apikey')
    @token_required
    def get(self,current_user):
        t = request.args
        data = Application(t).get_data()
        return jsonify(str(data))

@api.route('/add_details', methods=["POST"])
class MyResource(Resource):
    @token_required
    def post(self,current_user):
        payload = request.get_json()
        print(payload)
        data = Application(payload).add_details()
        response = {"Response": "Successfully! added the details in the {table} table.".format(table=payload["TableName"])}
        return jsonify(response)


if __name__ == "__main__":
    app.run(host = '0.0.0.0',debug=True,port=5001)
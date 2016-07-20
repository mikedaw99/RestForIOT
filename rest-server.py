#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
import json
import sqlite3
import datetime

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

DB_FILE='temp_readings.sqlite'

@auth.get_password
def get_password(username):
    if username == 'dawsonm':
        return 'Lf0oTS4M'
    return None
    
def update_log(dlog,temp):
    #
    db=sqlite3.connect(DB_FILE)
    cursor=db.cursor()
    cursor.execute('''insert into temp_log(dlog,temp) VALUES(?,?)''',(dlog,temp))
    db.commit()

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/api/v1.0/readings', methods = ['POST'])
@auth.login_required
def create_reading():
    #curl -u dawsonm:Lf0oTS4M -i http://localhost:5000/api/v1.0/readings
    post_data=request.get_json(force=True)
    print post_data
    if not post_data or not 'temp' in post_data:
        abort(400)

    post_dict=json.loads(post_data)

    dlog=post_dict["dlog"]
    temp=post_dict['temp']
    
    print dlog
    print temp
    
    # Update temp_log table
    update_log(dlog,temp)
    return make_response(jsonify( { 'Updated': 'True' } ), 201)

@app.route('/')
def hello_world():
    return 'Hello EC2 from Flask '+str(datetime.datetime.now())
    
if __name__ == '__main__':
    app.run(debug = True)

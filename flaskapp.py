#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask.ext.httpauth import HTTPBasicAuth
import json
import sqlite3
import datetime

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

DB_FILE='/var/www/html/flaskapp/freezer.sqlite'
#DB_FILE='freezer.sqlite'

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
    db.close()
    
def update_weather(datetime_logged,pressure,temperature):
    #
    db=sqlite3.connect(DB_FILE)
    cursor=db.cursor()
    cursor.execute('''insert into weather(`datetime_logged`,`pressure`,`temperature`) VALUES(?,?,?)''',(datetime_logged,pressure,temperature))
    db.commit()
    db.close()

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
    #print post_data
    if not post_data or not 'temp' in post_data:
        abort(400)

    post_dict=json.loads(post_data)

    dlog=post_dict["dlog"]
    temp=post_dict['temp']
    
    #print dlog
    #print temp
    
    # Update temp_log table
    update_log(dlog,temp)
    return make_response(jsonify( { 'temperature updated': 'True' } ), 201)
    
    
@app.route('/api/v1.0/weather', methods = ['POST'])
@auth.login_required
def create_weather():
    #curl -u dawsonm:Lf0oTS4M -i http://localhost:5000/api/v1.0/readings
    post_data=request.get_json(force=True)
    #print post_data
    if not post_data or not 'pressure' in post_data:
        abort(400)

    post_dict=json.loads(post_data)

    datetime_logged=post_dict["datetime_logged"]
    pressure=post_dict["pressure"]
    temperature=post_dict['temperature']
    
    #print dlog
    #print temp
    
    # Update weather table
    update_weather(datetime_logged,pressure,temperature)
    return make_response(jsonify( { 'weather updated': 'True' } ), 201)

@app.route('/')
def hello_world():
    return 'Hello EC2 from Flask '+str(datetime.datetime.now())
    
@app.route("/index")
def index():
    return render_template("index2.html")   
    
@app.route("/simple.png")
def simple():
    import datetime
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
    
@app.route("/home")
def home():
    return render_template("index2.html")

@app.route("/about")
def about():
    return render_template("index2.html")
    
@app.route("/contact")
def contact():
    return render_template("index2.html")
    
if __name__ == '__main__':
    app.run(debug = True)

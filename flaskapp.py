#!flask/bin/python

import json
import sqlite3
#import datetime type
from datetime import datetime
#import timedelta type
from datetime import timedelta
from flask import Flask, jsonify, abort, request
from flask import make_response, url_for, render_template
from flask.ext.httpauth import HTTPBasicAuth
import appconfig

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

#DB_FILE = '/var/www/html/flaskapp/freezer.sqlite'
# DB_FILE = 'freezer.sqlite'
DB_FILE = appconfig.DB_FILE


@auth.get_password
def get_password(username):
    """
    get password for user
    """
    if username == 'dawsonm':
        return 'Lf0oTS4M'
    return None


def update_log(dlog, temp):
    """
    update tabl2
    """
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute(
        '''insert into temp_log(dlog,temp) VALUES(?,?)''', (dlog, temp))
    db.commit()
    db.close()


def update_weather(datetime_logged, pressure, temperature):
    """
    update tabl2
    """
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute(
        '''insert into weather
           (`datetime_logged`,`pressure`,`temperature`)
            VALUES(?,?,?)''',
        (datetime_logged,
         pressure,
         temperature))
    db.commit()
    db.close()


def scan_weather():
    """
    Scan weather for gif
    """

    from matplotlib.dates import date2num

    x = []
    y = []
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # --------- date calculation -----------
    today = datetime.today()
    offset = timedelta(days=5)
    five_days_ago = str(today - offset)
    #parameters must be in a tuple
    cursor.execute(
                   """select * from weather where datetime_logged > ?""",
                   (five_days_ago,)
                   )
    for row in cursor.fetchall():
        id, date, mb, temp = row
        date_dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        x.append(date2num(date_dt))
        y.append(mb)
    return (x, y)


@auth.error_handler
def unauthorized():
    """
    Return 403 error
    """
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the
    # default auth dialog


@app.errorhandler(400)
def not_found(error):
    """
    Return 400 error
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    """
    Return 404 error
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1.0/readings', methods=['POST'])
@auth.login_required
def create_reading():
    """
    endpoint for temperature readinggs
    curl -u dawsonm:Lf0oTS4M -i http://localhost:5000/api/v1.0/readings
    """
    post_data = request.get_json(force=True)
    # print post_data
    if not post_data or 'temp' not in post_data:
        abort(400)

    post_dict = json.loads(post_data)

    dlog = post_dict["dlog"]
    temp = post_dict['temp']

    # Update temp_log table
    update_log(dlog, temp)
    return make_response(jsonify({'temperature updated': 'True'}), 201)


@app.route('/api/v1.0/weather', methods=['POST'])
@auth.login_required
def create_weather():
    """
    endpoint for weather readinggs
    curl -u dawsonm:Lf0oTS4M -i http://localhost:5000/api/v1.0/readings
    """
    post_data = request.get_json(force=True)
    # print post_data
    if not post_data or 'pressure'not in post_data:
        abort(400)

    post_dict = json.loads(post_data)

    datetime_logged = post_dict["datetime_logged"]
    pressure = post_dict["pressure"]
    temperature = post_dict['temperature']

    # Update weather table
    update_weather(datetime_logged, pressure, temperature)
    return make_response(jsonify({'weather updated': 'True'}), 201)


@app.route('/')
def hello_world():
    """
    Show Flask is working!
    """
    return 'Hello EC2 from Flask ' + str(datetime.now())


@app.route("/index")
def index():
    """
    show the matplotlib image via jinja template
    """
    return render_template("index2.html")


@app.route("/simple.png")
def simple():
    """
    Display png pf a matplotlib graph
    """
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig = Figure()
    ax = fig.add_subplot(111)
    x, y = scan_weather()
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route("/home")
def home():
    """
    place holder
    """
    return render_template("index2.html")


@app.route("/about")
def about():
    """
    place holder
    """
    return render_template("index2.html")


@app.route("/contact")
def contact():
    """
    place holder
    """
    return render_template("index2.html")

if __name__ == '__main__':
    app.run(debug=True)

# Libraries
import json
import csv
from random import random
from datetime import datetime, timedelta
from io import StringIO
from flask import Flask, redirect, url_for, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from HAR.classification import init_model, predict
import tensorflow as tf
from sqlalchemy import desc
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__, template_folder='template')

# connecting to the MySQL database
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:L5CB49ijM00Q@localhost/database_getsmart"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# initialize machine learning algorithm
x = np.zeros((1, 200, 6))
k = 0

Model = init_model('fcn_reg_50Hz_4seconds')


# initialize a table called datatab, _id is prime key, set automatically by order of entry, do not refer it
class db1(db.Model):
    __tablename__ = "datatab"

    _id = db.Column(db.Integer, primary_key=True)
    _timestamp = db.Column(db.String(100))
    _user = db.Column(db.String(100))
    _acceX = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    _acceY = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    _acceZ = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    _gyroX = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    _gyroY = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    _gyroZ = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    _bpm = db.Column(db.String(100))
    _initTime = db.Column(db.String(100))
    _label = db.Column(db.String(100))
    _pred_label = db.Column(db.String(100))


# home screen, go to see all data, plot or enter a term and go to search
@app.route('/')
def hello():
    return redirect(url_for('home'))


@app.route('/home', methods=['POST', 'GET'])
def home():
    # renders the home page in index.html in folder 'template'
    SessionData = db1.query.order_by(desc(db1._timestamp)).group_by(db1._initTime).distinct()

    if request.method == 'POST':
        if request.form['submit'] == 'Search':
            username = request.form['data1']
            return redirect(url_for('usersessions', username=username))
        elif request.form['submit'] == 'direct_select':
            username = request.form['username']
            token = request.form['timestamp']
            return redirect(url_for('sessiondata', username=username, token=token))
        elif request.form['submit'] == 'download':
            username = request.form['username']
            token = request.form['timestamp']
            return redirect(url_for('download', username=username, token=token))
        elif request.form['submit'] == 'viewUser':
            username = request.form['uniqueUserId']
            return redirect(url_for('usersessions', username=username))
        else:
            token = request.form['timestamp']
            db1.query.filter_by(_initTime=token).delete()
            db.session.commit()
            now = datetime.now()
            past = now + timedelta(hours=0) - timedelta(minutes=1)
            # past = now
            past_time = past.strftime('%Y-%m-%d:%H:%M:%S.%f')
            chopped_time = past_time[:-3]
            selectedData = db1.query.filter(db1._timestamp >= chopped_time).group_by(db1._user).distinct().all()

            uniqueUsers = db1.query.order_by(db1._timestamp).group_by(db1._user).distinct()
            pred = db1.query.order_by(db1._timestamp)
            return render_template('index.html', selectedData=selectedData, SessionData=SessionData,
                                   uniqueUsers=uniqueUsers, pred=pred)

    else:
        now = datetime.now()
        past = now + timedelta(hours=0) - timedelta(minutes=1)

        past_time = past.strftime('%Y-%m-%d:%H:%M:%S.%f')
        chopped_time = past_time[:-3]

        selectedData = db1.query.filter(db1._timestamp >= chopped_time).group_by(db1._user).distinct().all()

        uniqueUsers = db1.query.order_by(db1._timestamp).group_by(db1._user).distinct()
        return render_template('index.html', selectedData=selectedData, SessionData=SessionData,
                               uniqueUsers=uniqueUsers)


# shows all distinct session tokens of the selected user
@app.route('/usersessions', methods=['POST', 'GET'])
def usersessions():
    username = request.args.get('username')
    selectedData = db1.query.order_by(desc(db1._timestamp)).filter_by(_user=username).group_by(db1._initTime).distinct()
    if request.method == 'POST':
        token = request.form['timestamp']
        if request.form['submit'] == 'direct_select':
            return redirect(url_for('sessiondata', username=username, token=token))
        elif request.form['submit'] == 'download':
            return redirect(url_for('download', username=username, token=token))
        else:
            db1.query.filter_by(_user=username, _initTime=token).delete()
            db.session.commit()
            return render_template('usersessions.html', selectedData=selectedData)
    else:
        return render_template('usersessions.html', selectedData=selectedData)


# shows the search result, with a button that redirects to download
@app.route('/sessiondata', methods=['POST', 'GET'])
def sessiondata():
    # Request username and token of recording
    username = request.args.get('username')
    token = request.args.get('token')

    # download data if POST request, else show data
    if request.method == 'POST':
        return redirect(url_for('download', username=username, token=token))
    else:
        if token != '' and username != '':
            content = db1.query.order_by(desc(db1._timestamp)).filter_by(_user=username).filter_by(_initTime=token)
        elif token == '' and username != '':
            content = db1.query.order_by(desc(db1._timestamp)).filter_by(_user=username)
        elif token != '' and username == '':
            content = db1.query.order_by(desc(db1._timestamp)).filter_by(_initTime=token)
        else:
            content = db1.query.order_by(desc(db1._timestamp))

        return render_template('sessiondata.html', content=content)


# # Json post
@app.route('/json/post', methods=['POST'])
def json_post():
    global x, k, sat_counter, Model, prediction
    # check if the post is json, if true store the data in database
    if request.is_json:
        req = request.get_json()

        # start of a for-loop
        for anything in range(len(req)):
            _timestamp = req[anything]['timestamp']
            _user = req[anything]['user']
            _acceX = req[anything]['acceX']
            _acceY = req[anything]['acceY']
            _acceZ = req[anything]['acceZ']
            _gyroX = req[anything]['gyroX']
            _gyroY = req[anything]['gyroY']
            _gyroZ = req[anything]['gyroZ']
            _bpm = req[anything]['bpm']
            _initTime = req[anything]['token']
            _label = req[anything]['label']

            # # if no existing row is found make a new one
            # prediction part
            x = np.roll(x, -1, axis=1)
            x[0, -1, :] = [_acceX, _acceY, _acceZ, _gyroX, _gyroY, _gyroZ]
            k += 1
            if k == 50:
                prediction = predict(Model, x)
                k = 0

            Package = db1(_timestamp=_timestamp, _user=_user,
                          _acceX=_acceX, _acceY=_acceY, _acceZ=_acceZ,
                          _gyroX=_gyroX, _gyroY=_gyroY, _gyroZ=_gyroZ,
                          _bpm=_bpm, _initTime=_initTime, _label=_label, _pred_label=prediction)
            db.session.add(Package)
            db.session.commit()
            # print(_user, prediction, _user + prediction)
        return 'Json received', 200

    # if not json, return not received
    else:
        return 'Not received', 400


# download the recording sorted by timestamp as a csv file
@app.route('/download', methods=["GET"])
def download():
    # Request username and token of recording
    username = request.args.get('username')
    token = request.args.get('token')

    # generate CSV file from recording
    def generate(username, token):
        # get selected data and write them in a list grouped by parenthesis
        if token != '' and username != '':
            selectedData = db1.query.order_by(db1._timestamp).filter_by(_user=username).filter_by(_initTime=token)
        elif token == '' and username != '':
            selectedData = db1.query.order_by(db1._timestamp).filter_by(_user=username)
        elif token != '' and username == '':
            selectedData = db1.query.order_by(db1._timestamp).filter_by(_initTime=token)
        else:
            selectedData = db1.query.order_by(db1._timestamp)

        log = []
        for i in selectedData:
            log.append((i._timestamp, i._user, i._acceX, i._acceY, i._acceZ,
                        i._gyroX, i._gyroY, i._gyroZ, i._bpm, i._initTime, i._label, i._pred_label))

        data = StringIO()
        w = csv.writer(data)

        # write header of CSV
        w.writerow(('Timestamp', 'User', 'Accel_X', 'Accel_Y', 'Accel_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Heart_rate',
                    'Token', 'Label', 'Prediction'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for item in log:
            w.writerow((
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5],
                item[6],
                item[7],
                item[8],
                item[9],
                item[10],
                item[11]
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # stream the response as the data is generated
    response = Response(generate(username, token), mimetype='text/csv')

    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename=token + ".csv")
    return response


# Run website on port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

# ---------------------------------------------------------------------------
# Json post old version
# @app.route('/json/post', methods = ['POST'])
# def json_post():
#     # check if the post is json, if true store the data in database
#     if request.is_json:
#         req = request.get_json()
#         # turns json into python data/dictionary
#         _timestamp = req.get("timestamp")
#         _user = req.get("user")
#         _acceX = req.get("acceX")
#         _acceY = req.get("acceY")
#         _acceZ = req.get("acceZ")
#         _gyroX = req.get("gyroX")
#         _gyroY = req.get("gyroY")
#         _gyroZ = req.get("gyroZ")
#         _bpm = req.get("bpm")
#         _initTime = req.get("token")
#         _label = req.get("label")

#         Package = db1(_timestamp=_timestamp, _user=_user,
#         _acceX=_acceX, _acceY=_acceY, _acceZ=_acceZ,         _gyroX=_gyroX, _gyroY=_gyroY, _gyroZ=_gyroZ,
#         _bpm=_bpm, _initTime=_initTime, _label=_label, _pred_label = prediction)
#         db.session.add(Package)
#         db.session.commit()
#         return 'Json received', 200

#     # if not json, return not received
#     else:
#         return 'Not received', 400

# shows all data in the table
# @app.route('/posted')
# def posted():
#     allData = db1.query.order_by(desc(db1._timestamp))
#     return render_template('posted.html', allData = allData)

# shows which users have been sending data in the last minute
# @app.route('/online')
# def online():
#     now = datetime.now()
#     past = now + timedelta(hours = 0) - timedelta(minutes=1)

#     past_time = past.strftime('%Y-%m-%d:%H:%M:%S.%f')
#     chopped_time = past_time[:-3]

#     selectedData = db1.query.filter(db1._timestamp>=chopped_time).group_by(db1._user).distinct().all()
#     return render_template('plot.html', selectedData = selectedData)

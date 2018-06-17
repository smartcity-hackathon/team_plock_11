from flask import Flask, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_compress import Compress
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackaton.db'
app.secret_key = b'a7dy9813hoieniasa7dy9813hoienias'
db = SQLAlchemy(app)

admin = Admin(app, name='plock', template_mode='bootstrap3')


class MapData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True, nullable=False, default=db.func.current_timestamp())
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    quality = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    CO = db.Column(db.Float)
    C6H6 = db.Column(db.Float)
    O3 = db.Column(db.Float)
    PM2 = db.Column(db.Float)
    PM10 = db.Column(db.Float)

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in ret.keys():
            if isinstance(ret[key], datetime.date):
                ret[key] = int(ret[key].timestamp())
        return ret

    def as_dict_lite(self):
        return (int(self.date.timestamp()), (self.station_id, self.quality))


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    notify = db.Column(db.Integer, default=0)
    expiration = db.Column(db.DateTime)

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in ret.keys():
            if isinstance(ret[key], datetime.date):
                ret[key] = int(ret[key].timestamp())
        return ret


class Wind(db.Model):
    date = db.Column(db.DateTime, primary_key=True, default=db.func.current_timestamp())
    direction = db.Column(db.Integer, default=0)

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in ret.keys():
            if isinstance(ret[key], datetime.date):
                ret[key] = int(ret[key].timestamp())
        return ret


class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def as_dict_lite(self):
        return (int(self.date.timestamp()), (self.latitude, self.longitude))


def get_air():
    data = {}
    for map_data in MapData.query.order_by(MapData.date.desc()).all():
        v = map_data.as_dict_lite()
        date = v[0]
        data.setdefault(date, []).append(v[1])

    return data


def get_air_now():
    return MapData.query.filter(MapData.quality <= 70).order_by(MapData.date.desc()).first().as_dict()


def get_stations():
    data = {}
    for map_data in MapData.query.group_by(MapData.station_id).all():
        data[map_data.station_id] = (map_data.latitude, map_data.longitude)

    return data


def get_info():
    data = []
    for info in Info.query.order_by(Info.date.desc()).all():
        data.append(info.as_dict())

    return data


def get_wind():
    data = {}
    for wind in Wind.query.order_by(Wind.date.desc()).all():
        data[int(wind.date.timestamp())] = wind.direction

    return data


def get_tracker():
    data = {}
    for tracker in Tracker.query.order_by(Tracker.date.desc()).all():
        data.setdefault(int(tracker.date.timestamp()), []).append((tracker.latitude, tracker.longitude))

    return data

@app.route('/api/status', methods=['GET', 'POST'])
def status():
    return jsonify(status_data)

@app.route('/api/tracker', methods=['GET', 'POST'])
def tracker():
    return jsonify(tracker_data)


if __name__ == '__main__':
    db.create_all()

    admin.add_view(ModelView(Info, db.session))
    admin.add_view(ModelView(MapData, db.session))
    admin.add_view(ModelView(Wind, db.session))

    Compress(app)
    status_data = {'air': get_air(), 'air_now': get_air_now(), 'stations': get_stations(), 'wind': get_wind(), 'info': get_info()}
    tracker_data = get_tracker()
    app.run(host='0.0.0.0', port='8000')

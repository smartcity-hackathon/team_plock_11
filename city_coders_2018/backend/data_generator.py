from main import app, db, MapData, Wind, Info, Tracker
import datetime
import random
import math

manual_stations = [
    (52.54383915, 19.61841689),
    (52.53130977, 19.67884169),
    (52.51668765, 19.69806777),
    (52.50665823, 19.71454726),
    (52.48910125, 19.74269972),
    (52.45647681, 19.73857985),
    (52.49119173, 19.65274916),
    (52.46066079, 19.66373549),
    (52.57890239, 19.63008986),
    (52.56137428, 19.66098891),
    (52.55177258, 19.67334853),
    (52.54550947, 19.68914137),
    (52.54175117, 19.70150099),
    (52.53715726, 19.71111403),
    (52.53172748, 19.71798048),
    (52.52755026, 19.73514662),
    (52.51877682, 19.75505934),
    (52.49286405, 19.81548415),
    (52.50415052, 19.83608351),
    (52.52337265, 19.8147975),
    (52.53339825, 19.77909194),
    (52.53966309, 19.75025282),
    (52.54592704, 19.71729384),
    (52.55302509, 19.69875441),
    (52.560122, 19.68364821),
    (52.57931965, 19.65961562),
    (52.59396963, 19.63121521),
    (52.60835754, 19.65078461),
    (52.6073151, 19.67962372),
    (52.61190166, 19.56220734),
    (52.64128596, 19.63808166),
    (52.62482485, 19.68134033),
    (52.6139863, 19.72871887),
    (52.64399416, 19.74107849),
    (52.62232388, 19.78914368),
    (52.59876613, 19.79463684),
    (52.57269189, 19.80802643),
    (52.5610056, 19.7774707),
    (52.5787425, 19.74382507),
    (52.56225786, 19.73352539),
    (52.56851858, 19.84716522),
    (52.54514066, 19.83343231),
    (52.5062891, 19.83686554),
    (52.58896403, 19.85059845),
    (52.55265635, 19.872285),
    (52.585291, 19.683431),
    (52.595738, 19.766393),
    (52.539737, 19.730168),
    (52.591726, 19.555392),
    (52.645666, 19.610663),
    (52.649145, 19.751867),
    (52.609135, 19.854521),
    (52.576587, 19.899774),
    (52.509192, 19.911791),
    (52.464566, 19.827333),
    (52.483388, 19.673868),
    (52.505127, 19.582201)
]

stations_start = (52.20, 18.80)
stations_end = (52.90, 20.70)

emission_zones = [
    (52.539341, 19.717627, 3.0),
    (52.586645, 19.673912, 10.0)
]

dist_multiplier = 50
wind_divider = 40


def get_emission_multiplier(station, wind):
    angle = math.pi * wind / 180
    wind = [(math.cos(angle) - math.sin(angle)) / wind_divider, (math.sin(angle) + math.cos(angle)) / wind_divider]
    emission_zones_with_wind = emission_zones[:]
    for emission_zone in emission_zones:
        emission_zones_with_wind.append((emission_zone[0]+wind[0], emission_zone[1]+wind[1], emission_zone[2]))
        emission_zones_with_wind.append((emission_zone[0]+wind[0] * 5, emission_zone[1]+wind[1] * 5, emission_zone[2]))
        emission_zones_with_wind.append((emission_zone[0]+wind[0] * 10, emission_zone[1]+wind[1] * 10, emission_zone[2]))
        emission_zones_with_wind.append((emission_zone[0]+wind[0] * 15, emission_zone[1]+wind[1] * 15, emission_zone[2]))

    multiplier = 1
    for emission_zone in emission_zones_with_wind:
        dist = math.sqrt((emission_zone[0]-station[0]) ** 2 + (emission_zone[1]-station[1]) ** 2)
        dist *= dist_multiplier
        dist = max(1.0, dist)
        multiplier += (1 / (math.sqrt(dist))) * emission_zone[2]
    return multiplier


def add_station_log(date, station_id, station, base_values, wind):
    multiplier = get_emission_multiplier(station, wind)
    SO2 = round(base_values[0] * random.uniform(0.8, 1.2) * multiplier, 2)
    NO2 = round(base_values[1] * random.uniform(0.8, 1.2) * multiplier, 2)
    CO = round(base_values[2] * random.uniform(0.8, 1.2) * multiplier, 2)
    C6H6 = round(base_values[3] * random.uniform(0.8, 1.2) * multiplier, 2)
    O3 = round(base_values[4] * random.uniform(0.8, 1.2) * multiplier, 2)
    PM2 = round(base_values[5] * random.uniform(0.8, 1.2) * multiplier, 2)
    PM10 = round(base_values[6] * random.uniform(0.8, 1.2) * multiplier, 2)
    quality = round(sum([SO2, NO2, CO, C6H6, O3, PM2, PM10]) / len(base_values), 2)
    map_data = MapData(station_id=station_id, date=date, latitude=station[0], longitude=station[1], quality=quality, SO2=SO2, NO2=NO2,
                       CO=CO, C6H6=C6H6, O3=O3, PM2=PM2, PM10=PM10)
    db.session.add(map_data)


def generate_air_data():
    stations = []
    lat = stations_start[0]
    iter = 0
    while lat < stations_end[0]:
        lng = stations_start[1] + (0.02 if iter % 2 == 0 else 0)
        while lng < stations_end[1]:
            stations.append((round(lat, 5), round(lng, 5)))
            lng += 0.04
        lat += 0.02
        iter += 1

    iter_time = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(minute=0, second=0, microsecond=0)
    wind = 180
    base_values = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
    while iter_time < datetime.datetime.now():
        for station_id in range(len(stations)):
            add_station_log(iter_time, station_id, stations[station_id], base_values, wind)
        db.session.add(Wind(date=iter_time, direction=wind))
        iter_time += datetime.timedelta(hours=1)
        wind = (wind + random.randint(-40, 40)) % 360
        for i in range(len(base_values)):
            base_values[i] = min(0.25, max(0.15, base_values[i] * random.uniform(0.9, 1.1)))


def add_info(info_type, info_date, info_title, info_text, info_expiration=None):
    db.session.add(Info(type=info_type, date=info_date, title=info_title, text=info_text, expiration=info_expiration))

def generate_info_data():
    with open('sample_infos.txt', 'r') as f:
        for line in f:
            params = line.strip().split(';')
            if len(params) < 4:
                continue
            try:
                info_type = int(params[0])
                info_date = datetime.datetime.strptime(params[1], "%H:%M %d/%m/%y")
                info_title = params[2]
                info_text = params[3]
                add_info(info_type, info_date, info_title, info_text)
            except ValueError:
                continue


track_start = (52.48533812, 19.62596999)
track_end = (52.57556425, 19.73995314)


def generate_tracking_data():
    walkers = []
    for i in range(500):
        walkers.append([random.uniform(track_start[0], track_end[0]), random.uniform(track_start[1], track_end[1])])

    iter_time = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(minute=0, second=0, microsecond=0)
    while iter_time < datetime.datetime.now():
        for i in range(len(walkers)):
            db.session.add(Tracker(date=iter_time, latitude=walkers[i][0], longitude=walkers[i][1]))
            walkers[i][0] = min(track_end[0], max(track_start[0], walkers[i][0] + random.uniform(-0.001, 0.001)))
            walkers[i][1] = min(track_end[1], max(track_start[1], walkers[i][0] + random.uniform(-0.001, 0.001)))
        iter_time += datetime.timedelta(minutes=2)



if __name__ == '__main__':
    db.create_all()
    generate_air_data()
    generate_info_data()
    generate_tracking_data()
    db.session.commit()

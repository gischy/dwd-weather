import json
import psycopg2
from flask import Flask
from flask import request
import collections
import os
import datetime

user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
host=os.getenv("POSTGRES_HOST")
port=os.getenv("POSTGRES_PORT")

print(f'host: {host} port: {port} database: {database} user: {user} password: {password}')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/temperature/all")
def get_all():
    try:
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from TEMPERATUREN;"
        cursor.execute(postgreSQL_select_Query)
        results = cursor.fetchall()
        objects_list = []
        for row in results:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["datum"] = row[1]
            d["temperatur"] = row[2]
            objects_list.append(d)
        j = json.dumps(objects_list, indent=4, sort_keys=True, default=str)
        print(j)
        return j  
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return "fehler"

@app.route("/temperature/date")
def get_all_temperatures_for_date():
    try:
        date = request.args.get('date')
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = f"select * from TEMPERATUREN where DATUM='{date}'"
        cursor.execute(postgreSQL_select_Query)
        results = cursor.fetchall()
        objects_list = []
        for row in results:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["datum"] = row[1]
            d["temperatur"] = row[2]
            objects_list.append(d)
        j = json.dumps(objects_list, indent=4, sort_keys=True, default=str)
        print(j)
        return j  
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return "fehler"

@app.route("/temperature/plz")
def get_temperature_for_plz_for_today():
    try:
        plz = request.args.get('plz')
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = f"select ST_centroid(geom) from plz_5 where plz = '{plz}';"
        cursor.execute(postgreSQL_select_Query)
        results = cursor.fetchall()
        center_point = results[0][0];
        print(f"center point {center_point}")
        # query = f"SELECT *, ST_Transform(s.geom, 4326), s.geom <-> 'SRID=4326;{center_point}'::geometry AS dist FROM stationen s ORDER BY dist LIMIT 3;"
        query = f"SELECT s.id, s.geom <-> 'SRID=4326;{center_point}'::geometry AS dist FROM stationen s left join temperaturen t on t.id = s.id where t.datum = '2021-11-18' ORDER BY dist LIMIT 1;"
        cursor.execute(query)
        results2 = cursor.fetchall()
        nearest_station = results2[0][0]
        print(f"nearest station id {nearest_station}")
        today = datetime.date.today()
        the_date = today - datetime.timedelta(days=1)
        temp_query = f"select * from TEMPERATUREN where ID='{nearest_station}' AND DATUM='{the_date}';"
        print(temp_query)
        cursor.execute(temp_query)
        results = cursor.fetchall()
        objects_list = []
        for row in results:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["datum"] = row[1]
            d["temperatur"] = row[2]
            objects_list.append(d)
        j = json.dumps(objects_list, indent=4, sort_keys=True, default=str)
        print(j)
        return j
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return "fehler"

@app.route("/stations/plz")
def list_stations_for_plz():
    try:
        plz = request.args.get('plz')
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = f"select ST_centroid(geom) from plz_5 where plz = '{plz}';"
        cursor.execute(postgreSQL_select_Query)
        results = cursor.fetchall()
        center_point = results[0][0];
        print(f"center point {center_point}")
        query = f"SELECT *, ST_Transform(s.geom, 4326), s.geom <-> 'SRID=4326;{center_point}'::geometry AS dist FROM stationen s ORDER BY dist LIMIT 3;"
        cursor.execute(query)
        results = cursor.fetchall()
        objects_list = []
        for row in results:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["start_datum"] = row[1]
            d["end_datum"] = row[2]
            d["hoehe"] = row[3]
            d["lat"] = row[4]
            d["lon"] = row[5]
            d["stadt"] = row[6]
            d["bundesland"] = row[7]
            objects_list.append(d)
        j = json.dumps(objects_list, indent=4, sort_keys=True, default=str)
        print(j)
        return j
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return "fehler"

if __name__ == "__main__":
    app.run("0.0.0.0")


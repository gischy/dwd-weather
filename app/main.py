import requests
import datetime
import pandas as pd
import psycopg2
import os

user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
host=os.getenv("POSTGRES_HOST")
port=os.getenv("POSTGRES_PORT")

print(f'host: {host} port: {port} database: {database} user: {user} password: {password}')

date_format = "%Y-%m-%d"
today = datetime.date.today()
# DB

print("hello powercloud-weather")

def fetch_new_data():
    the_date = today - datetime.timedelta(days=1)
    the_date_string = the_date.strftime(date_format)
    print(f"fetching data for {the_date_string}")
    etl_wether_data_for_date(the_date_string)

def fetch_historic_data(days=365):
    for i in range(days):
        the_date = today - datetime.timedelta(days=i)
        the_date_string = the_date.strftime(date_format)
        print(f"fetching data for {the_date_string}")
        etl_wether_data_for_date(the_date_string)

def etl_wether_data_for_date(date):
    """
    function extracts data from dwd and loads specified columns to db

    date: date in format "%Y-%m-%d", example --> 2021-12-24
    """
    weather_data = extract_weather_data(date)
    sqls = transform_weather_data(weather_data)
    status = load_weather_data(sqls)

    if status:
        print(f"data was loaded to db for {date}")
    else:
        print(f"data could not be loaded to db for {date}")

def extract_weather_data(date_request_string):
    url = 'https://cdc.dwd.de/geoserver/ows'
    payload = f'<GetFeature xmlns="http://www.opengis.net/wfs" service="WFS" version="1.1.0" outputFormat="json" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"><Query typeName="CDC:OBS_DEU_P1D_T2M" srsName="EPSG:4326" xmlns:CDC="CDC"><Filter xmlns="http://www.opengis.net/ogc"><And><PropertyIsEqualTo><PropertyName>ZEITSTEMPEL</PropertyName><Literal>{date_request_string}T00:00:00.000Z/P0Y0M0DT23H59M</Literal></PropertyIsEqualTo><BBOX><PropertyName>SDO_GEOM</PropertyName><Envelope xmlns="http://www.opengis.net/gml" srsName="EPSG:4326"><lowerCorner>-10.64435 44.871480499352316</lowerCorner><upperCorner>31.54315 56.70453485493249</upperCorner></Envelope></BBOX></And></Filter></Query></GetFeature>'
    response = requests.post(url, data = payload)
    return response.json()["features"]

def transform_weather_data(weather_data_dict: dict):
    df = pd.DataFrame.from_dict(data=weather_data_dict)
    sqls = []
    for id, row in df.iterrows():
        geometry = row["geometry"]
        properties_var = row["properties"]
        sdo_code = properties_var["SDO_CODE"]
        wert = properties_var["WERT"]
        zeitstempel = properties_var["ZEITSTEMPEL"]
        sql = f"""INSERT INTO public.temperaturen (id, datum, wert) VALUES ({sdo_code}, '{zeitstempel}', {wert}) ON CONFLICT(id, datum) DO UPDATE SET wert = {wert};"""
        sqls.append(sql)
    return sqls

def load_weather_data(sqls: list):
    success = False
    try:
        # TODO: use env
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cursor = connection.cursor()
        for sql in sqls:
            cursor.execute(sql)
        connection.commit()
        success = True
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return success

def get_amount_rows():
    amt_rows = 0  # this should be changed
    try:
        # TODO: use env
        sql = "SELECT count(*) FROM temperaturen;"
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cursor = connection.cursor()
        cursor.execute(sql)
        amt_rows = cursor.fetchall()[0][0]
        success = True
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return amt_rows

if __name__ == "__main__":
    print("Hey guys!")
    print
    amt_rows = get_amount_rows()
    print(f"there are {amt_rows} rows in db")
    if amt_rows == 0:
        fetch_historic_data(days=10)
        print("hi")
    else:
        print("hi")
        fetch_new_data()

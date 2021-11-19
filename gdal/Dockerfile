FROM osgeo/gdal

COPY PLZ_2.geojson .

CMD ["ogr2ogr", "-f", "PostgreSQL", "PG:host=db dbname=powercloud_db user=powercloud password=powercloud", "PLZ_2.geojson"]

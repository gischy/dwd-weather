FROM postgis/postgis

COPY 11-create_statements.sql /docker-entrypoint-initdb.d/11-create_statements.sql
COPY stationen.csv .
COPY 12-PLZ_1.sql /docker-entrypoint-initdb.d/12-PLZ_1.sql
COPY 13-PLZ_2.sql /docker-entrypoint-initdb.d/13_PLZ_2.sql
COPY 14-PLZ_3.sql /docker-entrypoint-initdb.d/14_PLZ_3.sql
COPY 15-PLZ_4.sql /docker-entrypoint-initdb.d/15_PLZ_4.sql
COPY 16-PLZ_5.sql /docker-entrypoint-initdb.d/15_PLZ_5.sql
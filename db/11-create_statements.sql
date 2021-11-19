CREATE TABLE STATIONEN (
    ID integer PRIMARY KEY,
    START_DATUM date not null,
    END_DATUM date not null,
    HOEHE decimal not null,
    LAT decimal not null,
    LON decimal not null,
    STADT varchar not null,
    BUNDESLAND varchar not null
);

COPY STATIONEN(ID, START_DATUM, END_DATUM, HOEHE, LAT, LON, STADT, BUNDESLAND) FROM '/stationen.csv' DELIMITER ';' CSV HEADER;

ALTER TABLE STATIONEN ADD COLUMN GEOM geometry(Point, 4326);
UPDATE STATIONEN SET GEOM = ST_SetSRID(ST_MakePoint(LON, LAT), 4326);

CREATE TABLE TEMPERATUREN (
    ID integer,
    DATUM date NOT NULL,
    WERT decimal NOT NULL,
    PRIMARY KEY(ID, DATUM),
    CONSTRAINT FK_TEMPERATUREN
      FOREIGN KEY(ID)
	  REFERENCES STATIONEN(ID)
);


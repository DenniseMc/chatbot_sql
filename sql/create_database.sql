CREATE DATABASE cpsc_final_exam;

CREATE TABLE fraud_data (
    id 	                SERIAL PRIMARY KEY,
    transdatetranstime  TIMESTAMP,
    merchant            VARCHAR(255),
    category            VARCHAR(255),
    amt                 FLOAT,
    city                VARCHAR(255),
    state               VARCHAR(255),
    lat                 FLOAT,
    long                FLOAT,
    citypop             INT,
    job                 VARCHAR(255),
    dob                 DATE,
    transnum            VARCHAR(255),
    merchlat            FLOAT,
    merchlong           FLOAT,
    isfraud             BOOLEAN
);

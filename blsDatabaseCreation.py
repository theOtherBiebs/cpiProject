
# This script contains the code necessary to create a database of BLS Average Price and Consumer Universe time series data related to BLS surveys of consumer prices. Please note areas where variables need to be filled in by the user. You will also need the .txt files listed in the project readme. 
# 
# Please note that if you were running this on a server with external access to the internet (e.g. remote server), additional security measures might be warranted.
# 
# Ultimately this script is meant to be an example of how to create a database from an external source. I wrote it in Python for readability; however in the 'real world' I'd probably do most of this in SQL directly on the server; while it would be less readable it would probably run faster. Note that for large data sets I had to chunk the queries to get this to run within a couple minutes. 

# %%
###import necessary libraries

import pandas as pd
import psycopg2
import math
import json
import requests


# %%
##### function definitions

### function to clean extraneous spaces and weird null values out of raw bls data

def clean_bls_df(df):

    df_out=df

    columns_list=df_out.columns

    new_list=list()

    for item in columns_list:
        item = str(item).replace(" ","")
        new_list.append(item)

    df_out.columns = new_list

    df_out.loc[:, ~df_out.columns.isin(['series_title'])] = df_out.loc[:, ~df_out.columns.isin(['series_title'])].replace(r'\s+', '', regex=True)

    df_out.loc[:, df_out.columns.isin(['series_title'])]=df_out.loc[:, df_out.columns.isin(['series_title'])].replace(r'\'', '', regex=True)

    df_out.loc[:, df_out.columns.isin(['footnote_codes'])]=df_out.loc[:, df_out.columns.isin(['footnote_codes'])].fillna('none')

    df_out.loc[:, df_out.columns.isin(['footnotes'])]=df_out.loc[:, df_out.columns.isin(['footnotes'])].fillna('none')

    return df_out;

### function to wrap redundant function calls into one to make the db queries more readable

def insert_data_into_db(query, database=None, host={host_here}, port={port_here}, user={user_here}, password={password_here}):

    conn_params = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
    }

    if database is not None:
         conn_params['database'] = database

    conn = psycopg2.connect(**conn_params)

    conn.autocommit = True

    cursor = conn.cursor()

    cursor.execute(query)

    cursor.close()

    conn.close()

    return;

### function to create a query string from a dataframe of BLS data values for INSERT INTO queries
    
def create_query_string_from_df(df):

    values_list = [tuple(row) for row in df.values]

    values_string = str()

    for item in values_list:
        if values_string=='':
            values_string=str(item)
        else:
            values_string = values_string+', '+str(item)

    return values_string;


# %%

#### import and parse text files from bls.gov/cpi/data.htm . these files cannot be automatically retrieved by a bot due to bls restrictions. 

avg_price_series_df = pd.read_csv({string filepath to avg price series doc}, delimiter='\t', header=0)

avg_price_current_df= pd.read_csv({string filepath to avg price current doc}, delimiter='\t', header=0)

cu_series_df = pd.read_csv({string filepath to current universe series doc}, delimiter='\t', header=0)

cu_current_df = pd.read_csv({string filepath to current universe current doc}, delimiter='\t', header=0, dtype=str)

#### clean text file data to get rid of troublesome whitespace and escape characters

avg_price_current_df=clean_bls_df(avg_price_current_df)

avg_price_series_df = clean_bls_df(avg_price_series_df)

cu_series_df = clean_bls_df(cu_series_df)

cu_current_df = clean_bls_df(cu_current_df)


# %%
### create database for BLS data

drop_if_exists_query = '''DROP DATABASE IF EXISTS "BLSdata";'''

insert_data_into_db(query=drop_if_exists_query)


create_db_query = '''

CREATE DATABASE "BLSdata"
  WITH
   OWNER = '''{your user here}'''
   ENCODING = 'UTF8'
   LC_COLLATE = 'English_United States.1252'
   LC_CTYPE = 'English_United States.1252'
   TABLESPACE = pg_default
   CONNECTION LIMIT = -1
   IS_TEMPLATE = False;'''

insert_data_into_db(query=create_db_query)

##### create tables for data and insert data from dataframes

database = 'BLSdata'

table_name = "averagePriceTimeSeriesData" #### defines table name

ap_data_query = '''DROP TABLE IF EXISTS public.\"%s\";
CREATE TABLE IF NOT EXISTS public.\"%s\"  
(
    series_id character varying COLLATE pg_catalog."default" NOT NULL,
    year integer NOT NULL,
    period character varying COLLATE pg_catalog."default",
    value character varying,
    footnote_codes character varying COLLATE pg_catalog."default",
    CONSTRAINT "%s_pkey" PRIMARY KEY (series_id, year, period)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."%s"
    OWNER to '''{your user here}''';''' %(table_name,table_name,table_name,table_name)

insert_data_into_db(query=ap_data_query, database=database)

values_string=create_query_string_from_df(avg_price_current_df)

insert_query = '''
    INSERT INTO \"%s\" (\"series_id\", \"year\", \"period\", \"value\", \"footnote_codes\")
    VALUES %s
''' % (table_name, values_string)

insert_data_into_db(query=insert_query, database=database)


# %%
table_name = "averagePriceSeriesLabels" #### defines table name

ap_labels_query = '''DROP TABLE IF EXISTS public."averagePriceSeriesLabels";
CREATE TABLE IF NOT EXISTS public."averagePriceSeriesLabels"
(
    series_id character varying NOT NULL,
    area_code character varying,
    item_code character varying,
    series_title character varying,
    footnote_codes character varying,
    begin_year bigint,
    begin_period character varying,
    end_year bigint,
    end_period character varying,
    PRIMARY KEY (series_id)
);

ALTER TABLE IF EXISTS public."averagePriceSeriesLabels"
    OWNER to '''{your user here}''';'''  

insert_data_into_db(query=ap_labels_query, database=database)

values_string=create_query_string_from_df(avg_price_series_df)

insert_query = '''
    INSERT INTO \"%s\" (\"series_id\", \"area_code\", \"item_code\", \"series_title\", \"footnote_codes\", \"begin_year\", \"begin_period\"
    , \"end_year\", \"end_period\")
    VALUES %s
''' % (table_name, values_string)

insert_data_into_db(query=insert_query, database=database)


# %%
table_name = "consumerUniverseSeriesLabels" #### defines table name

cu_labels_query = '''DROP TABLE IF EXISTS public."consumerUniverseSeriesLabels";
CREATE TABLE IF NOT EXISTS public."consumerUniverseSeriesLabels"
(
    series_id character varying,
    area_code character varying,
    item_code character varying,
    seasonal character varying,
    periodicity_code character varying,
    base_code character varying,
    base_period character varying,
    series_title character varying,
    footnote_codes character varying,
    begin_year character varying,
    begin_period character varying,
    end_year character varying,
    end_period character varying,
    PRIMARY KEY (series_id)
);

ALTER TABLE IF EXISTS public."consumerUniverseSeriesLabels"
    OWNER to '''{your user here}''';'''  

insert_data_into_db(query=cu_labels_query, database=database)

values_string=create_query_string_from_df(avg_price_series_df)

insert_query = '''
    INSERT INTO \"%s\" (\"series_id\", \"area_code\", \"item_code\", \"series_title\", \"footnote_codes\", \"begin_year\", \"begin_period\"
    , \"end_year\", \"end_period\")
    VALUES %s
''' % (table_name, values_string)

insert_data_into_db(query=insert_query, database=database)


# %%
table_name = "consumerUniverseTimeSeriesData" #### defines table name

cu_current_query = '''DROP TABLE IF EXISTS public."consumerUniverseTimeSeriesData";
CREATE TABLE IF NOT EXISTS public."consumerUniverseTimeSeriesData"  
(
    series_id character varying COLLATE pg_catalog."default" NOT NULL,
    year integer NOT NULL,
    period character varying COLLATE pg_catalog."default",
    value character varying,
    footnote_codes character varying COLLATE pg_catalog."default",
    CONSTRAINT "consumerUniverseTimeSeriesData_pkey" PRIMARY KEY (series_id, year, period)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."consumerUniverseTimeSeriesData"
    OWNER to '''{your user here}''';'''   #### the above is a create if not exists that ensures the script will run even if the db has errors

insert_data_into_db(query=cu_current_query, database=database)

values_string=create_query_string_from_df(cu_current_df)

insert_query = '''
    INSERT INTO \"%s\" (\"series_id\", \"year\", \"period\", \"value\", \"footnote_codes\")
    VALUES %s
''' % (table_name, values_string)

insert_data_into_db(query=insert_query, database=database)



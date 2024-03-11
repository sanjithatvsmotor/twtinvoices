#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pypyodbc as pyodbc
from datetime import datetime


# In[2]:


# drivers = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.121.2.218;DATABASE=Vision_System;uid=AIML;pwd=I0TaiML123#;Pooling=false;Connect Timeout=2000;Max Pool Size=200;"
drivers = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.121.212.43;DATABASE=Vision_System;uid=ssluser;pwd=ssluser;Pooling=true;Connect Timeout=2000;Max Pool Size=200;"
driverssaphr = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.121.212.43;DATABASE=saphr;uid=ssluser;pwd=ssluser;Pooling=true;Connect Timeout=2000;Max Pool Size=200;"
# driverazure = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=prod-tvsm-ib-sqlserver.database.windows.net;DATABASE=prod-tvsm-letexport-db;uid=letexport_writer;pwd=Cw$xUm>7%wKu#2s/;"


# In[3]:


def DB_Read(query,drivers):
    try:
        sql_conn = pyodbc.connect(drivers, autocommit=False)
        pyodbc.pooling = True
        pd.set_option( 'display.max_colwidth', 255 )
        df = pd.read_sql(query, sql_conn)
        sql_conn.close()
        return df
    except Exception as ee:
        print("Data Read error:",str(ee))


# In[4]:


def DB_Insert(query,drivers):
    try:
        # global drivers
        sql_conn = pyodbc.connect(drivers, autocommit=False)
        pyodbc.pooling = True
        mycursor = sql_conn.cursor()
        mycursor.execute(query)
        mycursor.commit()
        sql_conn.close()
        print("Data updated")
        #df = pd.read_sql(query, sql_conn)
    except Exception as ee:
        print("Data updation error:",str(ee))


# In[5]:


def xstr(s):
    try:
        if s == None or s == 'None' or s == 'NULL' or 'None' in s:
            return ''
        else:
            return s
    except Exception as eee:
        print("xstr issue:",str(eee))
        return ''
    #return '' if s is None else str(s) 


# In[6]:


def xint(s):
    try:
        if s == None or s == 'None' or s == 'NULL' or 'None' in s:
            return 0
        else:
            return int(s)
    except Exception as eee:
        print("xint issue:",str(eee))
        return 0
    #return '' if s is None else str(s)


# In[7]:


def checkFloat(kps):
    try:
        mkp = 0.0
        mkp = float(kps.strip())
    except Exception as eee:
        mkp = 0.0
    return mkp


# In[ ]:





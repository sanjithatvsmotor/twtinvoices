#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pypyodbc as pyodbc
import pandas as pd
import Config


# In[2]:


def mssql_read_data(sql,driver):
    try:
        # print(Config.drivers)
        conn = pyodbc.connect(driver, autocommit=True)
        pyodbc.pooling = False
        df = pd.read_sql(sql, conn)
        #print("Data read from mssql done")
        return df
    except Exception as ee:
        print( str( ee ) )
    finally:
        conn.close()


# In[3]:


def DB_Read(query,drivers):
    try:
        print("query, drivers",query,drivers)
        sql_conn = pyodbc.connect(drivers, autocommit=True)
        pd.set_option( 'display.max_colwidth', 255 )
        df = pd.read_sql(query, sql_conn)
        sql_conn.close()
        return df
    except Exception as ee:
        print("Data Read error:",str(ee))


# In[4]:


def mssql_insert_data(_sql,drivers):
    try:
        # global drivers
        sql_conn = pyodbc.connect(drivers, autocommit=False)
        pyodbc.pooling = False
        mycursor = sql_conn.cursor()
        mycursor.execute(_sql)
        mycursor.commit()
        mycursor.close()
        #sql_conn.close()
        print("Data inserted in DB")
    except Exception as ee:
        print("Data insertion error:",str(ee))
    finally:
        sql_conn.close()



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


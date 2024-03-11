#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import base64
import re
import pandas as pd
import Config


# In[2]:


def api_call(inputJson):
  url = ""
  headers = ""
  PException = ""
  Config.SAPConnectivity = "PRD"
  # print("ID Config.SAPConnectivity: ",Config.SAPConnectivity)

  if Config.SAPConnectivity == "DVS":
      url = "http://thshdevsrvr.hosur.tvsmotor.co.in:8000/sap/bc/zmm_inv_digi/invoice?sap-client=400" # DVS 400
    
      #DEV 400
      headers = {
          'X-CSRF-TOKEN': 'fetch',
          'Authorization': 'Basic dC52aW1hbHJhajpzYXNoYSo0Ng==',
          'Content-Type': 'application/json'
      }
      response = requests.request( "GET", url, headers=headers, data=inputJson )
      
      Session_id = "SAP_SESSIONID_DVS_400"
      token_generated = response.headers["x-csrf-token"]
      sap_usercontext = response.cookies["sap-usercontext"]
      SAP_SESSIONID = response.cookies[Session_id]
      cookies = 'sap-usercontext=' + sap_usercontext + ';' + Session_id + '=' + SAP_SESSIONID
    
      headers = {
          'X-CSRF-TOKEN': token_generated,
          'Authorization': 'Basic dC52aW1hbHJhajpzYXNoYSo0Ng==', #DVS 400
          'Content-Type': 'application/json',
          'Cookie': cookies
      }
  
  elif Config.SAPConnectivity == "PRD":
      url = "https://tvsmits.tvsmotor.co.in/sap/bc/zmm_inv_digi/invoice?sap-client=777"  # PRD 777
      # #PRD
      headers = {
          'X-CSRF-TOKEN': 'fetch',
          'Authorization': 'Basic RElHSS1JTlY6RDFnMTNuVnM3Iw==',
          'Content-Type': 'application/json'
      }
      # print("headers:",headers)
      response = requests.request( "GET", url, headers=headers, data=inputJson )
    
      Session_id = "SAP_SESSIONID_PRD_777"
      token_generated = response.headers["x-csrf-token"]
      sap_usercontext = response.cookies["sap-usercontext"]
      SAP_SESSIONID = response.cookies[Session_id]
      cookies = 'sap-usercontext=' + sap_usercontext + ';' + Session_id + '=' + SAP_SESSIONID
    
      headers = {
          'X-CSRF-TOKEN': token_generated,
          'Authorization': 'Basic RElHSS1JTlY6RDFnMTNuVnM3Iw==',  # PRD
          'Content-Type': 'application/json',
          'Cookie': cookies
      }
  
  response = requests.request( "POST", url, headers=headers, data=inputJson )
  # print("\n" + response.text)
  # print(response.content)
  text = response.text
  z = json.loads( text )
  # print(type(z),z)
  Overall_output = z["MESSAGE"]

  listL = []
  x = z["IT_FINAL"]
  for dict in x:
      # print( dict["REMARKS"] )
      listL.append(dict["REMARKS"])
  df = pd.DataFrame( {'REMARKS': listL} )
  # print("-------API Output------")
  # print(Overall_output,df)
  return Overall_output,df



# In[ ]:





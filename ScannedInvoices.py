#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cProfile
import os
VisionDriver = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.121.2.220;DATABASE=CORPFINANCE;uid=DIGITALFINANCE;pwd=F!n@N(3d!g397*;Pooling=true;Connect Timeout=2000;Max Pool Size=200;"
import Config
import logging
from datetime import datetime
from Config import serverFileBackupPath_mysore
from shutil import copyfile
import re
import sql_con
from time import sleep
import glob
import time
import json
import SendMails
from dateutil.parser import parse
import datetime
from pathlib import Path
import glob
import decimal
from pandas import DataFrame
import CustGet_ModelID
import Ecopy_CustModel
import concurrent.futures
import threading
from PyPDF2 import PdfFileWriter, PdfFileReader
import schedule
from ID_pdf_plum import Invoice_Extract
from Config import *
 


# In[3]:


class RecognizeCustomForms(object):
    def recognize_custom_forms(self, path_to_sample_forms, mappings_M, modelIdDf, locationPO, validations, processingType, vendorCode):
        try:
            print(f"Processing file: {path_to_sample_forms}")
            #pdb.set_trace() 
 
            if processingType == "Scanned":
                _, vendorCode = CustGet_ModelID.getModelID(path_to_sample_forms, modelIdDf)
 
            if vendorCode != "":
                Ecopy_CustModel.RecognizeCustomForms().recognize_custom_forms(
                    path_to_sample_forms, mappings_M, "", locationPO,
                    processingType, validations, vendorCode
                )
                print("File : ", path_to_sample_forms, " got processed!")
            else:
                print("Model ID / PO NO / Vendor code not found!")
                maa = datetime.datetime.now()
                sm = str(maa)[0:19]
                sm = sm.replace(':', '_').replace(' ', '_').replace('-', '_')
                sm = "Exception_config_" + sm
                copyfile(path_to_sample_forms, Config.destination + sm + ".pdf")
                SendMails.sendMailCustom.main1(
                    path_to_sample_forms,
                    "Model ID / PO NO / Vendor code not found - Configuration required OR Scanned PDF is blank.",
                    sm, Config.serverFileBackupPath_mysore,
                    'HOSUR', "PO / Vendor code configuration required OR Blank Scan",
                    'Scanned', vendorCode, "", "", "", ""
                )
                os.remove(path_to_sample_forms)
        except Exception as ex:
            print("Exception!!!", ex)


# In[4]:


def recognize_custom_forms(path_to_sample_forms, mappings_M, modelIdDf, locationPO, validations, processingType):
    try:
        vendorCode = ""
        print("recognize_custom_forms")
        if Path(path_to_sample_forms).stat().st_size > 0:
            vendorCodeArr = path_to_sample_forms.rsplit('\\', 1)
            vc = vendorCodeArr[1].split('_')
            vendorCode = vc[0]

            if vendorCode != "" and processingType == "PortalInvoices":
                df = modelIdDf.loc[(modelIdDf['vendorcode'].str.strip() == str(vendorCode))]
                df = df.reset_index(drop=True)
                if not df.empty:
                    Model_id_ob = df['modelid'][0]
                else:
                    Model_id_ob = ""

            if processingType == "Scanned":
                _, vendorCode = CustGet_ModelID.getModelID(path_to_sample_forms, modelIdDf)

            if vendorCode != "":
                Ecopy_CustModel.RecognizeCustomForms().recognize_custom_forms(
                    path_to_sample_forms, mappings_M, "", "", locationPO,
                    processingType, vendorCode
                )
                print("File : ", path_to_sample_forms, " got processed!!")
            else:
                print("Model ID / PO NO / Vendor code not found")
                maa = datetime.datetime.now()
                sm = str(maa)[0:19]
                sm = sm.replace(':', '_').replace(' ', '_').replace('-', '_')
                sm = str(vendorCode) + '_' + sm
                copyfile(path_to_sample_forms, Config.destination + sm + ".pdf")
                sql_comand = "set dateformat dmy;exec RPA_FI_InvoiceDetails @typeCateg='Invoice_extractedData',@querytype='2',@UniqueId='" + str(sm) + "',@InvoiceNo='0',@PoNo='0',@VendorCode='" + str(vendorCode) + "',@ProcessingTime='0',@SAPOutput='E',@processingType='PortalInvoices',@DataRowType='Header',@Pages='0',@Filesize='0';"
                sql_con.mssql_insert_data(sql_comand, VisionDriver)
                os.remove(path_to_sample_forms)
        else:
            try:
                print("Found file size 0.")
                os.remove(path_to_sample_forms)
                maa = datetime.now()
                sm = str(maa)[0:19]
                sm = sm.replace(':', '_').replace(' ', '_').replace('-', '_')
                SendMails.sendMailCustom.main1(
                    path_to_sample_forms, "Found file size 0.", sm,
                    Config.serverFileBackupPath_mysore, 'HOSUR',
                    "File size found 0.", "PortalInvoices", "", "", "", "", ""
                )
            except Exception as ex:
                print("Exception scannedinvoices page!!!")
                if "Permission denied" not in str(ex) and "access denied" not in str(ex) and "being used" not in str(ex) and "cannot access" not in str(ex) and "JPEG, PNG, BMP, PDF" not in str(ex):
                    print("ScannedInvoices Page (PortalInvoices) - Exception : ", ex)
                time.sleep(10)
    except Exception as ex:
        print("Exception!!!", ex)



# In[5]:


def scannedInvoices():
    global mappings_M
    global modelIdDf
    global locationPO
    global validations
 
    while True:
        start = time.perf_counter()
        files = []
        List_Threads = []
        Folderpath = Config.ShareDrivePath_mysore
 
        for filename in os.listdir(Folderpath):
            if filename.lower().__contains__(".pdf"):
                file = Folderpath + "\\" + filename
                print(file)
                List_Threads.append(threading.Thread(
                    target=RecognizeCustomForms().recognize_custom_forms,
                    args=[file, mappings_M, modelIdDf, locationPO, validations, "Scanned"]
                ))
 
        for x in List_Threads:
            x.start()
 
        for x in List_Threads:
            x.join()



# In[6]:


def PortalInvoices():
    global mappings_M
    global modelIdDf
    global locationPO
    global validations
    
    while True:
        start = time.perf_counter()
        files = []
        List_Threads = []
        Folderpath = Config.ShareDrivePath_PortalInvoices
        for filename in os.listdir(Folderpath):
            print(filename)
            if filename.lower().__contains__(".pdf"):
                file = Folderpath + "\\" + filename
                #print(file)
                processingType = "PortalInvoices"
                vendorCode = "123456"  
                modelIdDf = ""  
                locationPO = "123"
                validations = ""
                
                List_Threads.append(threading.Thread(
                    target=RecognizeCustomForms().recognize_custom_forms,
                    args=[file, mappings_M, modelIdDf, locationPO, validations, processingType, vendorCode]
                ))
 
        for x in List_Threads:
            x.start()
 
        for x in List_Threads:
            x.join()


# In[ ]:


if __name__ == '__main__':
    
    sample = RecognizeCustomForms()
    mappings_M = None  
    mappings_E = None  
 
    #pdb.set_trace()  

    t22 = threading.Thread(target=PortalInvoices)
    t22.start()
 
    try:
        while True:
            schedule.run_pending()
    except Exception as ee:
        print("Exception in main:", ee)


# In[ ]:





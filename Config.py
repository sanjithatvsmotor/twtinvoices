#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


os_name = str(os.name)
# print(os_name)
driver = ""
if os_name == "nt":
    driver = "13"
else:
    driver = "17"
    
SAPConnectivity = "PRD"


# In[3]:


#drivers = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.121.2.43;DATABASE=NEWPROJECTS;uid=ssluser;pwd=ssluser;"
NewProjectsdriver = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.121.2.43;DATABASE=NEWPROJECTS;uid=ssluser;pwd=ssluser;"
# drivers = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.121.212.43;DATABASE=SAPHR;uid=ssluser;pwd=ssluser;"
#driversVision = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.121.212.43;DATABASE=Vision_System;uid=ssluser;pwd=ssluser;Pooling=false;Connect Timeout=2000;Max Pool Size=200;"
# VisionDriver = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.121.212.43;DATABASE=Vision_System;uid=ssluser;pwd=ssluser;Pooling=false;Connect Timeout=2000;Max Pool Size=200;"
endpoint = "https://formrecogfinance.cognitiveservices.azure.com/" #"https://centralindia.api.cognitive.microsoft.com/"
key = "a242a5848d224bbdb47f43150fd47649"
VisionDriver = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.121.2.220;DATABASE=CORPFINANCE;uid=DIGITALFINANCE;pwd=F!n@N(3d!g397*;Pooling=true;Connect Timeout=2000;Max Pool Size=200;"


# In[5]:


model_id_hosur = "5806caf7-0dca-456d-ad36-2ab6178dcdc4" #"ff974163-4d09-46d8-9dde-080b83384f31"#"b8983b4f-b643-4dcf-9b94-a04efc546566"#"d15c0e80-7188-41ff-a6a2-6d8aa6ce55d4"#"ca05127e-cd53-41a6-86e1-27e9c7195f33"#"f2d9a2d6-4eaa-40e1-97ac-e47824c8a39e"
ShareDrivePath_hosur = r"\\D:\invoice\from" # Hosur

#ShareDrivePath_mysore = "\\\\THSWINFLSRVR1\ScannedInvoices$\scannedinvoices" # Mysore
ShareDrivePath_mysore = r"\\D:\invoice\fromm" #mysore

#ShareDrivePath_PortalInvoices = "\\\\THSWINFLSRVR1\ScannedInvoicesHosur$\VendorPortalInvoices\invoice_common"

ShareDrivePath_PortalInvoices = r'D:\invoice\from'
model_id_mysore = "064c80e7-86f4-4ae9-8017-223b4f5d1a63"
#serverFileBackupPath_mysore = "http://10.121.3.197/InvoiceBackups/"
serverFileBackupPath_mysore = r"\\D:\invoice\to_copies"

destination = r"D:\invoice\to" #"C:\\Python automation\\Invoice Digitization\\Invoice Backup\\"

vCodeModelId = "d33b70b8-34c4-43ab-8d7c-1ff77e1971fe"#"fce0c3fc-6907-40ff-8c82-fff269a5a2fe"

emailattachmentextensions = ['pdf', 'zip', 'rar']


# In[ ]:





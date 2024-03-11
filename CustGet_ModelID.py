#!/usr/bin/env python
# coding: utf-8

# In[1]:


import Config
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
import re
import sql_con


# In[2]:


def getModelID(path_to_sample_forms,modelIdDf):

    form_recognizer_client = FormRecognizerClient(
        endpoint=Config.endpoint, credential=AzureKeyCredential( Config.key )
    )
    # with open( path_to_sample_forms, "rb" ) as f:
    #     poller = form_recognizer_client.begin_recognize_custom_forms(
    #         model_id=Config.vCodeModelId, form=f
    #     )     # vendor code extraction model
    with open( path_to_sample_forms, "rb" ) as f:
        poller = form_recognizer_client.begin_recognize_custom_forms(
            model_id=Config.vCodeModelId, form=f    #vPONOModelId
        )  # PO base extraction model
    forms = poller.result()

    for idx, form in enumerate( forms ):
        print( "--------Recognizing Form #{}--------".format( idx + 1 ) )
        for name, field in form.fields.items():
            if field.value is None:
                field.value = ""
            else:
                if field.value.count( ":" ):
                    d = field.value.split( ":" )
                    field.value = d[1]
                print(name)
                if "VendorCodeOnly" in name or "PONO" in name: #list to be mainatined
                    if field.value.__contains__( "/" ):
                        d = field.value.split( "/" )
                        field.value = d[0]
                field.value = re.sub( "[^0123456789]", "",field.value )#re.sub( r"[-()\"#/@;:,<>{}`+=~|!?%]", "", field.value )

    vendorCode = field.value
    # print(modelIdDf)
    # df = sql_con.mssql_read_data("select modelId from Invoice_ModelIDMapping where dflag='A' and vendorcode='" + vendorCode+"';")
    df = modelIdDf.loc[(modelIdDf['vendorcode'].str.strip() == str(vendorCode))]
    df = df.reset_index(drop=True)
    # df = modelIdDf.loc[modelIdDf["vendorcode"] == vendorCode]
    print(df)
    modelID = ""
    if not df.empty:
        modelID = df['modelid'][0]
    else:
        modelID = ""
    print(modelID,vendorCode)

    return modelID,vendorCode


# In[ ]:





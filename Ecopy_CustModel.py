import pypdfium2 as pdfium
import pyodbc
import sys
from io import BytesIO
import numpy as np
import cv2
import zxingcpp
import jwt
import json
import PyPDF2
#import fitz
import os
import shutil 
from shutil import copyfile
import Config
import time
from datetime import datetime
from dateutil.parser import parse
import sql_con
import CustAPIFormReco
import json
import SendMails
from SendMails import sendMailCustom
import os
import shutil
from datetime import datetime
from datetime import date
from Config import serverFileBackupPath_mysore
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from shutil import copyfile
from PyPDF2 import PdfFileWriter, PdfFileReader
import Config
import re
import sql_con
from time import sleep
import glob
import time
import CustAPIFormReco, json
import SendMails
from dateutil.parser import parse
import datetime
from pathlib import Path
import pandas as pd
import pdfplumber
import requests
import base64

class RecognizeCustomForms():
    def recognize_custom_forms(self, filepath, email, emailsubject, mailReceivedOn, locationPO, processingType, vendorCode):
        inv_total = ""
        seller_gst = ""
        buyer_gst = ""
        inv_no = ""
        inv_dt = ""
        hsn = ""
        irn = ""
        data_dict = {}
        Overall_output = ""
        exceptionWE_g = ""
        location = ""
        

        maa = datetime.datetime.now()
        sm = str(maa)[0:19]
        sm = sm.replace(':', '_').replace(' ', '_').replace('-', '_')

        destination = Config.destination
        ProgramRemarks = ""
        start_time = time.time()

        #filenameNom = "D:\\invoice\\to\\" + "0_" + Path(filepath).name
        filenameNom = os.path.join(Config.serverFileBackupPath_mysore, "0_" + Path(filepath).name)
        shutil.copyfile(filepath, filenameNom)
        
        try:
            with open(filepath, 'rb') as f:
                pdf_bytes = BytesIO(f.read())
                pdf_all_pages = pdfium.PdfDocument(pdf_bytes)

                for page_number, this_pg in enumerate(pdf_all_pages):
                    decoded_list = []
                    for scale_value in range(1, 6, 1):
                        pil_image = this_pg.render(scale=scale_value).to_pil()
                        np_arr_img = np.array(pil_image)
                        cpp_result = zxingcpp.read_barcodes(np_arr_img)

                        if len(cpp_result) > 0:
                            decoded_list = [str(d_str.text) for d_str in cpp_result]
                            print(f"Decoded list (Page {page_number + 1}, Scale {scale_value}) for PDF: {filepath}")

                            for items in decoded_list:
                                try:
                                    decoded_token = jwt.decode(items.strip(), algorithms=["RS256"],
                                                              options={"verify_signature": False})
                                    data = decoded_token["data"]
                                    data_dict = json.loads(data)
                                    print("Decoded successfully")
                                    #print("Output result: ", data_dict)

                                except jwt.ExpiredSignatureError:
                                    print("Expired token")
                                except jwt.InvalidTokenError as e:
                                    print(f"Invalid token: {e}")
                                except Exception as ee:
                                    print("Not able to decode:", ee)

                            break

                    if data_dict:
                        break

                if data_dict is None:
                    print("No QR code found in the PDF.")

        except Exception as ex:
            print("Exception handled:", ex)
            
        if len(data_dict)>0:
            inv_total = data_dict['TotInvVal']
            seller_gst = data_dict['SellerGstin']
            buyer_gst = data_dict['BuyerGstin']
            inv_no = data_dict['DocNo']
            inv_dt = data_dict['DocDt']
            hsn = data_dict['MainHsnCode']
            irn = data_dict['Irn']

            inv_dt = parse(inv_dt, fuzzy=True, dayfirst=True)

            UniqueId = str(vendorCode) + "_" + str(inv_no) + "_" + str(inv_dt.strftime('%Y%m%d'))
            UniqueId = UniqueId.replace('/', '-')

            sqlCheckDuplicate = "set dateformat dmy;exec RPA_FI_InvoiceDetails @querytype= '3', @invoiceno='" + inv_no + "',@invoicedate='" + str(
                inv_dt) + "',@VendorName='" + vendorCode + "',@typeCateg='Invoice_extractedData'"

            dupl = sql_con.mssql_read_data(sqlCheckDuplicate, Config.VisionDriver)
            Overall_output = ""
            print("Output result: ", data_dict)
        if len(data_dict) <= 0:
             print("No QR code found in the PDF, storing data in RPA_FI_Invoice_Exceptions.")
             SendMails.sendMailCustom.main1(filepath, exceptionWE_g, sm, Config.serverFileBackupPath_mysore, location, 
                                            "QR Code Not Readable / Not Found",processingType,vendorCode,inv_no,inv_dt,
                                            str('0'),str('0'))
             sys.exit(1)
                
        if dupl.empty:
            #digital sign validation, pdf as input to e-mudra api in B64 format, checking whether sign is valid/invalid
            #if valid then push data to SAP and SQL, else create exception "Sign not valid"

            '''try:
                pdf_data = None
                with open(filepath, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')
                digital_signature_b64 = extract_digital_signature(pdf_data_base64)

                api_endpoint = 'http://10.121.4.251:8080/emas2/services/dsverifyWS'
                #api_key = 'your_api_key'

                headers = {
                    #'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                }

                payload = {
                    'digital_signature': digital_signature_b64,
                }

                response = requests.post(api_endpoint, json=payload, headers=headers)

                if response.status_code == 200:
                    verification_response = response.text
                else:
                    raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

            except Exception as ex:
                print(f"Exception during digital signature validation and data pushing: {ex}")


            #print("process invoice further - unique combination")

            ######sap api payload format to be done #############
'''
            nested_dict=[
                            {
                                "INV_NO": str(inv_no),
                                "INV_DATE": str(inv_dt),
                                "SUP_GSTNO": str(seller_gst),
                                "INV_TOTAL": str(inv_total),
                                "TOT_BASE_VAL": "0.00",
                                "TOT_TAXABLE": "0.00",
                                "TOT_CGST_RATE": "0.00",
                                "TOT_SGST_RATE": "0.00",
                                "TOT_IGST_RATE": "0.00",
                                "TOT_TCS": "0.00",
                                "TOT_TCS_RATE": "0.00"
                            }
                        ]

            inputJson = {"T_FINAL": nested_dict}
            #print(inputJson)
            r = json.dumps( inputJson )

            try:
                print( "------SAP API start --------" )
                try:
                     Overall_output, ddc = CustAPIFormReco.api_call( r )
                except Exception as ex:
                     print( "Exception SAP1: ", ex )
                     Overall_output = ""
                     if str(ex).lower().__contains__("x-csrf-token"):
                         ProgramRemarks ="SAP user id and password not working. Please get the working password and send it to IT co-ordinator to use in script"
                     else:
                         ProgramRemarks = "SAP API Error : " + ex
                         print( "------SAP API End -------" )

            except Exception as ex:
                print( "Exception SAP2: ", ex )
                ProgramRemarks = ex

            if str(Overall_output) != "":
                    Overall_output = "SAP Output : " + str(Overall_output)
                    print("OVERALL OUTPUT : ", Overall_output)
            if ProgramRemarks != "":
                ProgramRemarks = str(Overall_output) + "Program Exception : " + str(ProgramRemarks)

            print( "Total time taken to process the File : ", time.time() - start_time )

            proPara = ""
            if ProgramRemarks == "":
                print("before insertion")
                proPara="set dateformat dmy;exec RPA_FI_InvoiceDetails @typeCateg='Invoice_extractedData',@querytype='2', @InvoiceNo='"+str(inv_no)+"',@InvoiceDate='"+str(inv_dt)+"',@VendorCode='"+str(vendorCode)+"',@IRNNo='"+str(irn)+"',@SupGSTINNo='"+str(seller_gst)+"',@HSNCode='"+str(hsn)+"',@InvoiceTotal='"+str(inv_total)+"',@BillToGSTINNo='"+str(buyer_gst)+"',@UniqueId='" + str(UniqueId) + "',@loc='"+ str(location)+"',@SAPOutput='" +  str(Overall_output) + "',@processingTime='" + str(time.time() - start_time ) + "',@processingType='"+str(processingType)+"',@email='"+str(email)+"',@mailSubject='"+str(emailsubject)+"',@mailReceivedOn='"+ str(mailReceivedOn)+"',@DataRowType='Header'; "

                sql_con.mssql_insert_data( proPara,Config.VisionDriver )
            else:
                print( "Exception captured by program" )
                print( "duplicate present in database so skipped push to SAP as well as DB!" )
            


        #print( "-----------------------------------" )
            # only fisrt page will be processed and sent to db and sap


            try:
                if ProgramRemarks != "":  # if sap posting issues
                    # sm = "Exception_SAPPosting_" + sm
                     # copyfile( filepath, destination + sm + ".pdf" )
                    copyfile(filepath, destination + UniqueId + ".pdf")
                    
                else:
                    # print(filepath,destination)
                    if (filepath and destination) and dupl.empty:
                        # print( filepath, UniqueId )
                        copyfile( filepath, destination + UniqueId + ".pdf" )
                    else:
                            # sm = "Exception_duplicate_" + sm
                            # copyfile( filepath, destination + sm + ".pdf" )
                        print("here in duplicate")
                        copyfile(filepath, destination + UniqueId + ".pdf")
                        SendMails.sendMailCustom.main1(filepath,
                                                        "Duplicate invoice found! Obtained combinations :  " + str(
                                                            UniqueId), UniqueId, Config.serverFileBackupPath_mysore,
                                                        location, "Duplicate Found", processingType, vendorCode, inv_no,
                                                        '',str('0'),str('0'))
                        try:
                            # print("in try", filepath)
                            os.remove(filepath)
                        except Exception as ex:
                            # print("in exception", filepath)
                            print( "We were not able to remove the file from folder" )
                            print("Exception: ",ex)
            except Exception as ex:
                print( "Exception : ", ex )
                # sm = "Exception_unhandled_" + sm
                # copyfile( filepath, destination + sm + ".pdf" )
                copyfile(filepath, destination + UniqueId + ".pdf")
                SendMails.sendMailCustom.main1(filepath, ex, UniqueId, Config.serverFileBackupPath_mysore, location,
                                                "Exception handled", processingType, vendorCode, inv_no, inv_dt,str('0'),str('0'))
                # SendMails.sendMailCustom.main1( filepath, ex, sm,Config.serverFileBackupPath_mysore, location,"Exception handled",processingType,vendorCode,InNo,InDate)
                os.remove( filepath )

                print( "Total time taken to process the File : ", time.time() - start_time )
                print( "===========================================================" )

            except Exception as ex:
                print("Exception at Ecopy_Custmodel",ex)

            try:
                print( "Exception at ecopy_custmodel!!!" )
                if "Permission denied" not in str( ex ) and "access denied" not in str(
                     ex ) and "being used" not in str( ex ) and "cannot access" not in str(
                     ex ) and "JPEG, PNG, BMP, PDF" not in str( ex ):
                    print( "Ecopy_CustModel Page - Exception : ", ex )
                    exceptionWE = "Ecopy_CustModel Page - Exception : " + str( ex )
                    exceptionWE_g=exceptionWE
                         # filepath_g=filepath
                         # sm_g=sm
                    #destination_g=destination
                         # location_g=location
                         # invno_g=invno
                         # invdate_g=invdate
                    copyfile( filepath, destination + sm + ".pdf" )
                    print("inside exceptions")
                    SendMails.sendMailCustom.main1( filepath,
                             exceptionWE_g, sm, Config.serverFileBackupPath_mysore, location, "QR Code Not Readable / Not Found",processingType,vendorCode,inv_no,inv_dt,str('0'),str('0'))
                    os.remove( filepath )

                return data_dict

            except Exception as ex:

                 #print( "Exception backup taken!" )
                 print( "Exception inside exception: handled" )

    # if __name__=="__main__":
    #     RecognizeCustomForms.recognize_custom_forms()

if __name__ == "__main__":
    #custom_form_recognizer = RecognizeCustomForms()

    filepath = "D:\\invoice\\from\\Invoice-35.pdf"
    email = "sanjitha.rajesh@tvsmotor.com"
    emailsubject = "QR Invoice"
    mailReceivedOn = "2024-03-06"  
    locationPO = None  
    processingType = "PortalInvoices"
    vendorCode = "1234"
    
    custom_form_recognizer = RecognizeCustomForms()

    
    result = custom_form_recognizer.recognize_custom_forms(filepath, email, emailsubject, mailReceivedOn, locationPO, processingType, vendorCode)
    
    
    #print("Output Result:", result)

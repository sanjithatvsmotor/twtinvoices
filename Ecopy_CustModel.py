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
#from azure.core.credentials import AzureKeyCredential
#from azure.ai.formrecognizer import FormRecognizerClient
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
        dupl = pd.DataFrame()
        UniqueId = ""
        
        #Date modified: 25/02/24, 
        #Purpose: To generate QR code information from any page of a PDF, 
        #Modified by: sanjitha.rajesh@tvsmotor.com, 
        #Lines: 64-150
        
        maa = datetime.datetime.now()
        sm = str(maa)[0:19]
        sm = sm.replace(':', '_').replace(' ', '_').replace('-', '_')
        destination = Config.destination
        ProgramRemarks = ""
        start_time = time.time()
        
        try:
            with open(filepath, 'rb') as f:
                pdf_bytes = BytesIO(f.read())
                pdf_all_pages = pdfium.PdfDocument(pdf_bytes)
                for page_number, this_pg in enumerate(pdf_all_pages):
                    print(page_number)
                    decoded_list = []
                    for scale_value in range(1, 8, 1):
                        pil_image = this_pg.render(scale=scale_value).to_pil()
                        np_arr_img = np.array(pil_image)
                        cpp_result = zxingcpp.read_barcodes(np_arr_img)
                        print(len(cpp_result))
                        if len(cpp_result) > 0:
                            decoded_list = [str(d_str.text) for d_str in cpp_result]
                            print(f"Decoded list (Page {page_number + 1}, Scale {scale_value}) for PDF: {filepath}")
                            print(len(decoded_list))
                            for items in decoded_list:
                                try:
                                    decoded_token = jwt.decode(items.strip(), algorithms=["RS256"],
                                                              options={"verify_signature": False})
                                    data = decoded_token["data"]
                                    data_dict = json.loads(data)
                                    print("Decoded successfully")
                                    print("Output result: ", data_dict)

                                except jwt.ExpiredSignatureError:
                                    print("Expired token")
                                except jwt.InvalidTokenError as e:
                                    print(f"Invalid token: {e}")
                                except Exception as ee:
                                    print("Not able to decode:", ee)
                                    
                            print("data_dict here",data_dict)
                            print("-----------------------",len(data_dict),"---------------------------------")
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
                                #vendorCode = ""
                                print("Printing in Ecopy_CustModel: ", vendorCode)
                                if UniqueId != "":
                                    sqlCheckDuplicate = "set dateformat dmy;exec RPA_FI_InvoiceDetails @querytype= '3', @invoiceno='" + inv_no + "',@invoicedate='" + str(inv_dt) + "',@VendorName='" + vendorCode + "',@typeCateg='Invoice_extractedData'"
                                    dupl = sql_con.mssql_read_data(sqlCheckDuplicate, Config.VisionDriver)
                                    Overall_output = ""
                                    print("Output result: ", data_dict)
                                    
                                    
                                #checking whether any duplicate is there of PDF via stored procedure RPA_FI_Invoice_Details
                                
                            
                            #if len(data_dict) <= 0
                    try:
                        if len(data_dict) == 0:
                            print("No QR code found in the PDF, storing data in RPA_FI_Invoice_Exceptions.")
                            sqlCheckDuplicateException = "SELECT COUNT(*) FROM RPA_FI_Invoice_Exceptions WHERE invoiceno = '{}' AND InvoiceDate = '{}'".format(inv_no, inv_dt)
                            duplicate_count = sql_con.mssql_read_data(sqlCheckDuplicateException, Config.VisionDriver)
                            if duplicate_count.iloc[0, 0] == 0:  # If no duplicates found
                  
                                SendMails.sendMailCustom.main1(filepath, exceptionWE_g, sm, Config.serverFileBackupPath_mysore, location, 
                                                                "QR Code Not Readable / Not Found",processingType,vendorCode,inv_no,inv_dt,
                                                                str('0'),str('0'))

                                filenameNom = os.path.join("D:\\", destination, "0_" + Path(filepath).name)

                                shutil.move(filepath, filenameNom)
                                sys.exit(1)
                            else:
                                print("Duplicate exception found in the database, skipping...")
                                

                    except Exception as e:
                        print( e )
                    #break

                    #if data_dict:
                        #break

                if data_dict is None:
                    print("No QR code found in the PDF.")
                    

        except Exception as ex:
            print("Exception handled:", ex)
            
        filenameNom = os.path.join("D:\\", destination, "0_" + Path(filepath).name)
        shutil.move(filepath, filenameNom)

        if dupl is not None and dupl.empty:
            
            #digital sign validation, pdf as input to e-mudra api in B64 format, checking whether sign is valid/invalid
            #if valid then push data to SAP and SQL, else create exception "Sign not valid"
            
        #Modified Date: Before 16/02/24, Modified by: Piyush Chandra, (Initial code)
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

            #Purpose of code: Storing QR data in SAP and sending mails, Lines: 179-293
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
                
                
                print("storing data_1")
                print("Unique ID here",UniqueId)   
                if UniqueId != "" :
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

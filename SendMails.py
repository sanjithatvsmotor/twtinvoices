#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import argparse
import numpy as np
import threading
import os
# from config import mail_server
# =======================================================
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
import sql_con
import re
import Config


# In[5]:


class sendMailCustom():
    def main1( file, exceptionMessage, filename, filepath, loc, exceptionShort, processingType,vendorcode,invoiceno,invoicedate,Pages,Filesize):
        try:
            print(invoiceno,invoicedate)
            exceptionMessage = re.sub( r"[']", "", exceptionMessage )
            # sql = "set dateformat dmy;insert into RPA_FI_invoice_exceptions (filename,ExceptionDescription,filepath,moddate,loc,exceptionType,processingType,vendorcode,invoiceno,invoicedate) values ('"+filename+"','"+exceptionMessage+"','"+filepath+"',getdate(),'"+loc+"','"+exceptionShort+"','"+processingType+"','"+vendorcode+"','"+invoiceno+"','"+invoicedate+"');"
            # print(sql)
            # sql_con.mssql_insert_data( sql )
            sql =  "set dateformat dmy;insert into RPA_FI_invoice_exceptions (filename,ExceptionDescription,filepath,moddate,loc,exceptionType,processingType,vendorcode,invoiceno,invoicedate,project,Pages,Filesize) values ('" + filename + "','" + exceptionMessage + "','" + filepath + "',getdate(),'" + loc + "','" + exceptionShort + "','" + processingType + "','" + vendorcode + "','" + invoiceno + "','" + invoicedate + "','ID','"+Pages+"','"+Filesize+"');"
            print(sql)
            sql_con.mssql_insert_data(sql,Config.VisionDriver)
            print("Inserted exception details in database.")
            if (exceptionShort!="Duplicate Found"):
                #server = "10.121.2.222"
                #server = "tvsmsmtp.tvsmotor.com"
                server = "smtp.sendgrid.net"
                smtp_port = 25
                smtp_username= "apikey"
                smtp_password = "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"
                print( "Sending mail..." )
                # assert isinstance(send_to, list)

                #send_from = "ID_BOT_DoNotReply@tvsmotor.com"
                send_from = "sanjitha.rajesh@tvsmotor.com"

                subject1 = "Invoice Digitization Automation Exception : " + str(exceptionShort) + " " + str(loc) + " - "+ str(processingType)
                body1 = '<p style=COLOR: blue;FONT-WEIGHT: bold;><b style=FONT-WEIGHT: bold; TEXT-TRANSFORM: capitalize; COLOR: blue; FONT-STYLE: italic; ><font color=blue >Dear Team,<br>This is to inform you that while processing scanned invoice an automated system has encountered exception for vendor code '+vendorcode+'. The exception is as follows: <br/><br/>'+ exceptionMessage + '<br/><br/>Same file can be accessed through server using path: '+ filepath + filename+'.pdf <br/><br/>Kindly make sure invoice is properly scanned, please contact patil.samiksha@tvsmotor.com for any sort of clarification.<br/><br/><b>Regards,</b><br/>Team ID Automation<br/>DO NOT REPLY!</p>'
                #send_to = 'Patil.Samiksha@tvsmotor.com,Prakash.Patil@tvsmotor.com,D.Preethi@tvsmotor.com;Abirami.Chithra@tvsmotor.com;Vasanthkumar.k@tvsmotor.com;Muniraju.v@tvsmotor.com;'
                send_to = "sanjitha.rajesh@tvsmotor.com, anwesh.sahoo@tvsmotor.com"
                # print(body1)
                #send_to = "patil.samiksha@tvsmotor.com"

                msg = MIMEMultipart()
                msg['From'] = send_from
                # msg['To'] = COMMASPACE.join(send_to)
                msg['To'] = send_to
                # print(COMMASPACE.join(send_to))
                # msg['Date'] = formatdate(localtime=True)
                msg['Subject'] = subject1
                # attach the body with the msg instance
                msg.attach( MIMEText( body1, 'html' ) )

                # attachment = file
                # print( attachment )
                # file_name = M_date_time + '.xlsx'
                print("Send mail file : ",file)
                if  file != '':
                    part = MIMEBase( 'application', "octet-stream" )
                    part.set_payload( open( file, "rb" ).read() )
                    encoders.encode_base64( part )
                    part.add_header( 'Content-Disposition', 'attachment; filename=ExceptionInvoice.pdf' )
                    msg.attach( part )

                 #part.set_payload( (attachment).read() )
                encoders.encode_base64( part )
                #part.add_header( 'Content-Disposition', 'attachment; filename=2W_IB_PERFORMANCE.pptx' )
                msg.attach( part )
 
                smtp = smtplib.SMTP( server , smtp_port )
                smtp.starttls()
                smtp.login(smtp_username, smtp_password)
                smtp.sendmail( send_from, send_to.split( ',' ), msg.as_string() )
                smtp.close()
                #smtp = smtplib.SMTP( server )
                #smtp.sendmail( send_from, send_to.split( ',' ), msg.as_string() )
                #smtp.close()

                # if os.path.exists( filename ):
                #     os.remove( filename )
                print("Mail sent!")
        except Exception as ee:
            print( "SendMail Exception : ", str( ee ) )


# In[ ]:




import cv2
import argparse
import numpy as np
import threading
import os
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
import sql_con
import re
import Config

class sendMailCustom():
    def main1(file, exceptionMessage, filename, filepath, loc, exceptionShort, processingType, vendorcode, invoiceno,
             invoicedate, Pages, Filesize):
        try:
            print(invoiceno, invoicedate)
            exceptionMessage = re.sub(r"[']", "", exceptionMessage)
            sql = "set dateformat dmy;insert into RPA_FI_Invoice_Exceptions (filename,ExceptionDescription,filepath,moddate,loc,exceptionType,processingType,vendorcode,invoiceno,invoicedate,project,Pages,Filesize) values ('" + filename + "','" + exceptionMessage + "','" + filepath + "',getdate(),'" + loc + "','" + exceptionShort + "','" + processingType + "','" + vendorcode + "','" + invoiceno + "','" + invoicedate + "','ID','" + Pages + "','" + Filesize + "');"

            sql_con.mssql_insert_data(sql, Config.VisionDriver)

            if (exceptionShort != "Duplicate Found"):
                server = "smtp.sendgrid.net"
                smtp_port = 25
                smtp_username = "apikey"
                smtp_password = "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"

                send_from = "sanjitha.rajesh@tvsmotor.com"

                subject1 = "Invoice Digitization Automation Exception : " + str(
                    exceptionShort) + " " + str(loc) + " - " + str(processingType)
                body1 = '<p style=COLOR: blue;FONT-WEIGHT: bold;><b style=FONT-WEIGHT: bold; TEXT-TRANSFORM: capitalize; COLOR: blue; FONT-STYLE: italic; ><font color=blue >Dear Team,<br>This is to inform you that while processing scanned invoice an automated system has encountered exception for vendor code ' + vendorcode + '. The exception is as follows: <br/><br/>' + exceptionMessage + '<br/><br/>Same file can be accessed through the server using path: ' + filepath + filename + '.pdf <br/><br/>Kindly make sure the invoice is properly scanned, please contact patil.samiksha@tvsmotor.com for any sort of clarification.<br/><br/><b>Regards,</b><br/>Team ID Automation<br/>DO NOT REPLY!</p>'
                send_to = "sanjitha.rajesh@tvsmotor.com, anwesh.sahoo@tvsmotor.com"

                msg = MIMEMultipart()
                msg['From'] = send_from
                msg['To'] = send_to
                msg['Subject'] = subject1
                msg.attach(MIMEText(body1, 'html'))

                print("Send mail file : ", file)
                if file != '':
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(file, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename=ExceptionInvoice.pdf')
                    msg.attach(part)

                smtp = smtplib.SMTP(server, smtp_port)
                smtp.starttls()
                smtp.login(smtp_username, smtp_password)
                smtp.sendmail(send_from, send_to.split(','), msg.as_string())
                smtp.close()
                print("Mail sent!")
        except Exception as ee:
            print("SendMail Exception : ", str(ee))

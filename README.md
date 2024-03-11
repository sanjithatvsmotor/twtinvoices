# twtinvoices
Contains the code for the Trade with TVS portal, wherein members of the team can see and access the code for QR generation/extraction and digital signature verification.

Main components of the repo:

1. ScannedInvoices.ipynb: This is the entry point for the application. It imports the SQL Driver which needs to be used for storage of the invoice details, defines the paths for upload and copying, and creates threads for running the invoices and finds out whether QR codes are present or not. This code also calls another notebook, Ecopy_CustModel.ipynb.
2. Ecopy_CustModel.ipynb: This is another primary notebook where the code for extracting QR code and digital signature is present. It defines a class and function called RecognizeCustomForms (recognize_custom_forms) which is in charge of all the invoice related operations. It reads the PDF as input, extracts the QR information such as SellerGST, TotalInvoiceValue, ItemCount etc using the zxingcpp library and pushes it into the SQL database. There are two tables, RPA_FI_Invoice_MainData, which is where the successfully decoded invoices are pushed, and RPA_FI_Invoice_Exceptions, where the invoices which could not be decoded properly are pushed.
Subsequently, there is also a component of the code that takes the PDF as input in base64 format, then calls the EMudhra API which is in charge of extracting the digital signature from the PDF.

Other files needed for the code to run:
1. Config.ipynb
2. CustAPIFormReco.ipynb
3. CustGetModelID.ipynb
4. sql_con.ipynb
5. SendMails.ipynb
6. DB.ipynb

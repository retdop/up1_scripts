# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:51:21 2016

@author: gchenard
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:26:30 2016
@author: gchenard
"""
import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import getpass
import openpyxl


#update necessaire: mettre plusieurs addresses mails dans le champs "to"

def email_login(server):
    #login to the email server    
    server.ehlo()
    server.starttls()
    server.ehlo()
    username=input('What is your Gmail username? ')
    password=getpass.getpass()
    server.login(username, password)

def quit_server(server):
    server.quit()

def send_email (server,frm, to, message, subject):    
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['FROM'] = frm
    bodyStr = message
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()
    msg['To'] = to    #for sending the email to multiple people, just write the email adresses seprated with a ','
    _attach = MIMEText(bodyStr.encode('utf-8'), 'html', 'UTF-8')        

    msg.attach(_attach)
    server.sendmail(frm, to, msg.as_string())
    
    print ('Email sent to ', to)


def load_excel_file(excel_file_name):
    # load excel file and get to the first sheet
    # excel file has to be in the repository    
    wb = openpyxl.load_workbook(excel_file_name)
    type(wb)
    sheet = wb.get_sheet_by_name('Feuil1')
    return sheet        


def email_paramter_with_excel(sheet,i):       
    #i is the number of the line in the excel sheet where you get your data from
<<<<<<< 933fa756c3f0a7d905dcfd1ce4e00a78cff6a157:up1/email_from_excel_sender.py
    to =(sheet[('C'+str(i))].value)    #Put the column of mail adresses. For sending the email to multiple people, just write the email adresses seprated with a ','
    
    message = str(                    # Write message here. each <br> sets a new line
    "Dear " + sheet[('A'+str(i))].value + '<br>' +   
    "" + '<br>' +
    "I hope everything is fine for you at " + sheet[('D'+str(i))].value + '<br>' +
    "If you ever have to do a painful computer related task, just ask Bob" + '<br>' +
    "He is available at this adress : https://retdop.github.io" + '<br>' +
    "See you soon," + '<br>' +
    "" + '<br>' +
    "Gautier, Edouard et Gabi" + '<br>' +
    "" + '<br>' +
    "Ps: this gif is you before and after using bob : http://i.imgur.com/ZgrSBBc.gifv" 
    )

    subject=("Urgent message for the founders of " + sheet[('D'+str(i))].value)
=======
    to =(sheet[('E'+str(i))].value)    #Put the column of mail adresses. For sending the email to multiple people, just write the email adresses seprated with a ','
    type(to)
    message = str("Dear " + sheet[('B'+str(i))].value+ ',<br><br>' + sheet[('F'+str(i))].value + '<br>' +
    "I hope everything is doing well at " + sheet[('D'+str(i))].value +  '<br><br>Cheers,<br>Gabriel')

    subject=("Salut " + sheet[('B'+str(i))].value)
>>>>>>> for mac os test:Email sender.py
        
    frm=('gabriel.bstd@gmail.com')
    
    return (frm, to, message, subject)
    
    
def number_of_rows_in_excel(sheet) :
    row_count = sheet.max_row
    return row_count


def send_multiples_emails(server,excel_file_name):   
    email_login(server)
    sheet=load_excel_file(excel_file_name)
    count=number_of_rows_in_excel(sheet)  
    i=2    #i the the first line you get the data from on the excel (do not count the header)
    while i <= count:    # go through each line of the excel
        (frm, to, message, subject) = email_paramter_with_excel(sheet,i)
        
        #If you want to ask the user for mail paramters :         
        #frm=input('From:')
        #to=input("To:")
        #message=input("Message:")
        #subject=input("Subject:")
        
        send_email(server,frm, to, message, subject)
        i+=1
    quit_server(server)

if '__name__' == '__main__':
    
    server = SMTP('smtp.gmail.com:587')
                # Find your SMTP server name : http://www.serversmtp.com/en/what-is-my-smtp
    excel_file_name='../dumps/L2L_contacts_for_Bob.xlsx'
                
    send_multiples_emails(server, excel_file_name)

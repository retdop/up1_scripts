# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:48:50 2016

@author: gchenard
"""
import smtplib
from smtplib import SMTP
import os
os.chdir('/Users/gchenard/up1_scripts/')
os.getcwd()

import up1.email_from_excel_sender as email


server = SMTP('smtp.gmail.com:587')   # Find your SMTP server name : http://www.serversmtp.com/en/what-is-my-smtp
excel_file_name='dumps/L2L_contacts_for_Bob.xlsx'

email.send_multiples_emails(server, excel_file_name)
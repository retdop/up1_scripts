from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import getpass
import openpyxl


#remplace le for i in range par un while do qui se desincrement de 1 a chaque fois.
#permettre connection de tous les servers


def email_login(server, username, password):
    #login to the email server
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)

def quit_server(server):
    server.quit()

def send_email (frm, to, message, subject):
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['FROM'] = frm
    msg['CC'] = 'hassanbenjell@gmail.com'
    bodyStr = message
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()
    msg['To'] = to    #for sending the email to multiple people, just write the email adresses seprated with a ','
    _attach = MIMEText(bodyStr.encode('utf-8'), 'html', 'UTF-8')

    msg.attach(_attach)
    cc = 'hassanbenjell@gmail.com'
    server.sendmail(frm, [to, cc], msg.as_string())

    print ('Email sent to', to, cc)


def load_excel_file(excel_file_name):
    # load excel file and get to the first sheet
    # excel file has to be in the repository
    wb = openpyxl.load_workbook(excel_file_name)
    type(wb)
    sheet = wb.get_sheet_by_name('Feuil1')
    return sheet


def email_paramter_with_excel(sheet, i, username):
    #i is the number of the line in the excel sheet where you get your data from
    to =(sheet[('C'+str(i))].value)    #Put the column of mail adresses. For sending the email to multiple people, just write the email adresses seprated with a ','
    type(to)
    message = "Hi " + sheet[('A'+str(i))].value + ",<br><br>" + "My name is Hassan, I am a grad student at UC Berkeley, currently working on a social project on volunteering."+" Next week, on Monday 7/11, and in this period of political excitement, we invite professionals in SF to revive their civic spirit around the concept : "+"<b>Volunteering for the community, alongside likeminded people</b>.<br>"+"More precisely, we have reached out to several companies in SF, to have teams from different companies volunteer at the same event, and we would love to have " + sheet[('B'+str(i))].value + " participate!<br>"+"To see and subscribe to the events, here is the link to our website: <a href='www.karmaclub.club'>www.karmaclub.club</a><br><br>"+"As we have spent a lot of time organizing these events, we would feel incredibly rewarded if you could talk about this opportunity to your coworkers.<br>"+"If you have any inquiry, I would love to have a quick chat about it, you can reach me at any time on my mobile phone: (631) 408-1384 (Anytime, really...)<br><br>"+"Thank you so much,<br><br>"+"Best,<br><br>"+"Hassan" 

    subject=("Karma Club")

    frm=(username)

    return (frm, to, message, subject)


def number_of_rows_in_excel(sheet) :
    row_count = sheet.max_row
    return row_count


def send_multiples_emails(server,excel_file_name):
    username=input('What is your username? ')
    password=getpass.getpass()
    email_login(server, username, password)
    sheet=load_excel_file(excel_file_name)
    count=number_of_rows_in_excel(sheet)
    i=2    #i the the line you get the datat from on the excel
    while i <= count:    # go through each line of the excel
        (frm, to, message, subject) = email_paramter_with_excel(sheet, i, username)


        send_email(frm, to, message, subject)
        i+=1
    quit_server(server)

    

if __name__ == '__main__':
    server = SMTP('smtp.gmail.com:587')
            # Find your SMTP server name : http://www.serversmtp.com/en/what-is-my-smtp
    excel_file_name='Liste mailing .xlsx'
    send_multiples_emails(server, excel_file_name)

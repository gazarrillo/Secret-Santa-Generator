import random

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def getNamesList(filename):
    """This function reads a file and creates a list with its contents"""
    participants = []
    emails = []
    filename = open(filename, 'r')
    for line in filename:
        line = line.rstrip('\n')
        sline = line.split()
        participants.append(sline[0] + ' ' + sline[1])
        emails.append(sline[2])
    filename.close()
    return participants, emails


def read_template(filename):
    """This function reads a file as the template for the message
    you're going to send"""
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


nameFile = 'participants.txt'
MY_ADDRESS = input('Enter your gmail address: ')
PASSWORD = input('Enter your gmail password: ')
subject = input('Enter subject for the email: ')

participants, emails = getNamesList(nameFile)
message_template = read_template('message.txt')

partners = participants[:]

# Checking if anyone is matched with themselves

same = True

while same is True:
    same = False
    random.shuffle(partners)
    for i in range(len(participants)):
        if participants[i] == partners[i]:
            same = True

for i in range(len(participants)):
    print(participants[i], '------>', partners[i])

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)

for partners, email in zip(partners, emails):
    msg = MIMEMultipart()
    message = message_template.substitute(PERSON_NAME=partners.title())
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    del msg

s.quit()

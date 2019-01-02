import tkinter as tk

import random

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SSS_GUI:

    def __init__(self):

        self.title_frame = tk.Frame()
        self.top_frame = tk.Frame()
        self.mid_frame = tk.Frame()
        self.mid_frame2 = tk.Frame()
        self.mid_frame3 = tk.Frame()
        self.bottom_frame = tk.Frame()

        self.tile_label = tk.Label(self.title_frame, font=('none', 20),
                                   text='Secret Santa Generator')
        self.prompt_label1 = tk.Label(self.top_frame,
                                      text='Enter your gmail address:')
        self.prompt_label2 = tk.Label(self.mid_frame,
                                      text='Enter your gmail password:')
        self.prompt_label3 = tk.Label(self.mid_frame2,
                                      text='Enter the subject for your email:')

        self.email_entry = tk.Entry(self.top_frame, width=10)
        self.password_entry = tk.Entry(self.mid_frame, width=10)
        self.subject_entry = tk.Entry(self.mid_frame2, width=10)

        self.tile_label.pack(side='top')
        self.prompt_label1.pack(side='left')
        self.prompt_label2.pack(side='left')
        self.prompt_label3.pack(side='left')

        self.email_entry.pack(side='left')
        self.password_entry.pack(side='left')
        self.subject_entry.pack(side='left')

        self.calc_button = tk.Button(self.bottom_frame,
                                     text='Generate',
                                     command=self.main)

        self.calc_button.pack(side='left')

        self.value = tk.StringVar()
        self.descr_label = tk.Label(self.mid_frame3,
                                    textvariable=self.value, fg='green')

        self.descr_label.pack()

        self.title_frame.pack()
        self.top_frame.pack()
        self.mid_frame.pack()
        self.mid_frame2.pack()
        self.mid_frame3.pack()
        self.bottom_frame.pack()

    def main(self):

        self.value.set('')

        def getNamesList(filename):
            """This function reads a file and creates a list
            with its contents"""
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
        MY_ADDRESS = self.email_entry.get()
        PASSWORD = self.password_entry.get()
        subject = self.subject_entry.get()

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

        self.value.set('Success')


root = tk.Tk()
root.title('Secret Santa Generator')
SSS_GUI()
root.mainloop()

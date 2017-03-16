#!/usr/bin/python
import Tkinter as tk, tkSimpleDialog, tkMessageBox
import time
from random import random

emails = ['elena@utilityapi.com', 'krishna@tynker.com', 'aisling@synack.com', 'laurenk@hackerone.com', 'mathilde@frontapp.com', 'farm.cp@gmail.com', 'gleb@nylas.com', 'sohail@equidateinc.com', 'matthew@polleverywhere.com', 'sgreenberg@doctorondemand.com', 'shanlian@goshippo.com', 'gavan@altvr.com', 'will@sketchdeck.com', 'nick.sullivan@airbnb.com', 'donnaz2015@gmail.com', 'david@honeybook.com', 'andy@roadster.com', 'ned@joinbreeze.com', 'tristan@tryzen99.com', 'quentin@wittycircle.com', 'lsarafan@homecareassistance.com', 'yong@wonolo.com', 'christopher@betable.com', 'michael@nylas.com']

class MyDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        self.geometry("350x100")
        self.text = tk.StringVar()
        tk.Label(master, text="Please enter your email address:").grid(row=0)
        tk.Label(master, text="Please enter your password:").grid(row=1)
        self.label1 = tk.Label(master, text = "", textvariable = self.text)
        self.label1.grid(row=3)
        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2 = tk.Entry(master, show='*')
        self.e2.grid(row=1, column=1)
        return self # initial focus


    def validate(self):
        self.email, self.pwd = self.e1.get(), self.e2.get()
        i = 0
        self.text.set("Connection to SMTP server.")
        self.label1.update_idletasks()
        time.sleep(random())
        self.text.set("Connection to SMTP server..")
        self.label1.update_idletasks()
        time.sleep(random())
        self.text.set("Connection to SMTP server...")
        self.label1.update_idletasks()
        time.sleep(random())
        for email in emails:
            i += 1
            self.text.set(str(i) + "/" + str(len(emails)) + " email sent")
            self.label1.update_idletasks()
            time.sleep(random())
        return self

    def apply(self):
        pass



if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    test = MyDialog(root, "Password")

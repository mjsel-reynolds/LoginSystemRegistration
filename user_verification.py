from tkinter import *
from tkinter import messagebox #Use all tkinter modules for GUI
from PIL import ImageTk #Use to upload jpg files in place of png files
import pymysql #Use to connect mySQL database to Python
import pyotp #Use to generate random verification code
import time #Use to help generate time based 30 sec code


# Functionality

def verify_user():
    # Generate Verification Code
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key)
    print(totp.now())
    verify_code = totp.now() #Makes key based on current time, regenerates every 30 secs

    # Verify code
    input_code = input('Enter 2FA Code:')
    print(totp.verify(input_code))

    # Send verification code to user
    # Connect to database
    mydata=pymysql.connect(host='localhost',user='root',password='Classynotsassy1!')
    mycursor=mydata.cursor()

    # Check if fields are empty
    #if codeEntry.get()=='':
        #messagebox.showerror('Error', 'All Fields Are Required')
    #else:
        # Connect to database



root=Tk()

# TITLE SCREEN
root.title('User Verification')
verify_bg = PhotoImage(file='user_verify.png')
verify_bgLabel = Label(root,image=verify_bg)
verify_bgLabel.place(x=0,y=0)
root.geometry('1174x660+50+50')
root.resizable(False, False)


header = Label(root, text='User Verification', font=('Sanchez', 36), bg='white', fg='#595651')
header.place(x=425,y=145)


# Verification Code

code = Label(root, text='Verification Code', font=('Sanchez', 11), bg='#F8F8F8', fg='#595651')
code.place(x=455, y=230)
codeEntry = Entry(root, width=15, font=('Source Serif Pro', 26), bd=0, fg='#595651', bg='#F8F8F8')
codeEntry.place(x=455,y=260)

# OTP Buttons
submit_code = Button(root, text='SUBMIT', bd=0, bg='#738664', activebackground='#738664',
               cursor='hand2', font=('Open Sauce', 19), fg='white', activeforeground='white', width=20, height=2)
submit_code.place(x=448,y=400)
resend_code = Button(root, text='RESEND CODE', bd=0, bg='#738664', activebackground='#738664',
                     cursor='hand2', font=('Open Sauce', 15), fg='white', activeforeground='white', width=21,
                     height=1)
resend_code.place(x=482,y=500)


messagebox.showinfo('User Verification', 'A Verification Code has been sent to your email.\n'
                                         'Enter the code within 30 seconds to access your account')


root.mainloop()
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk #Use to upload jpg files in place of png files
import pymysql #Use to connect mySQL database to Python

# Functionality


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

# Generate key to send to user via the given email corresponding to their account in the database
# Generate key to send to user, used as a one-time password
#key = pyotp.random_base32()
#print(key)

# Time based key will generate a new random key every 30 secs, display message that
# countdowns from 30 secs after login button was pressed
#totp = pyotp.TOTP(key)

#print(totp.now())


root.mainloop()
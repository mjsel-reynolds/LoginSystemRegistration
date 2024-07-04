from tkinter import *#import all classes, functions, etc. from tkinter module
from tkinter import messagebox
import pymysql
import pyotp
import smtplib
from email.message import EmailMessage

#Functionality
def email_msg(subject, body, address):
    message = EmailMessage()
    message.set_content(body)
    message['subject']=subject
    message['to']=address

    user = 'pylogin.system@gmail.com'
    message['from'] = user
    password = 'cyez msqk dzco pdnf'

    server= smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(message)

    server.quit()


def enter_user(event):
    if userEntry.get()=='enter username':
        userEntry.delete(0,END)


def enter_password(event):
    if passwordEntry.get()=='enter password':
        passwordEntry.delete(0,END)


def hide_pw():
    open_eye.config(file='hide_password.png')
    if passwordEntry.get()!='enter password':
        passwordEntry.config(show='*')

    eyeButton.config(command=show_pw)


def show_pw():
    open_eye.config(file='show_password.png')
    passwordEntry.config(show='')

    # If button is pressed again, hide password
    eyeButton.config(command=hide_pw)


def signup_page():
    # login page window destroyed
    login_root.destroy()
    import sign_up


def forgot_pw():
    login_root.destroy()
    import new_password


def user_verification():
    # Generate Verification Code
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key)
    print(totp.now())
    verify_code = totp.now()  # Makes key based on current time, regenerates every 30 secs

    # Check database for an email matching username and send verification code
    # Connect to database with userdata
    try:
        mydata = pymysql.connect(host='localhost', user='root', password='Classynotsassy1!')
        mycursor = mydata.cursor()
    except:
        messagebox.showerror('Error', 'Database Connection Issue. Please Try Again')
        return

    query = 'use userdata'
    mycursor.execute(query)

    # Find email inside the database
    query = 'select email from data where username=%s'
    mycursor.execute(query, userEntry.get())

    userTaken = mycursor.fetchone()
    userEmail = ''
    for r in userTaken:
        userEmail += r
    print(userEmail)

    # send email to user
    email_msg('Login Project Verification Code',
              'Login Registration Verification Code\n'
              'Below is the verification code. Please insert the code as '
              'directed on the Login Project verification page.\n' 
              'This code will expire in 30 seconds:\n' + verify_code,
              userEmail)

    mycursor.close()
    mydata.close()

    # Generate User Verification GUI
    login_root.destroy()

    root = Tk()

    # TITLE SCREEN
    root.title('User Verification')
    verify_bg = PhotoImage(file='user_verify.png')
    verify_bgLabel = Label(root, image=verify_bg)
    verify_bgLabel.place(x=0, y=0)
    root.geometry('1174x660+50+50')
    root.resizable(False, False)

    header = Label(root, text='User Verification', font=('Sanchez', 36), bg='white', fg='#595651')
    header.place(x=425, y=145)

    # Verification Code Interface
    code = Label(root, text='Verification Code', font=('Sanchez', 11), bg='#F8F8F8', fg='#595651')
    code.place(x=455, y=230)
    codeEntry = Entry(root, width=15, font=('Source Serif Pro', 26), bd=0, fg='#595651', bg='#F8F8F8')
    codeEntry.place(x=455, y=260)

    submit_code = Button(root, text='SUBMIT', bd=0, bg='#738664', activebackground='#738664', cursor='hand2',
                         font=('Open Sauce', 19), fg='white', activeforeground='white', width=20, height=2)
    submit_code.place(x=448, y=400)
    resend_code = Button(root, text='RESEND CODE', bd=0, bg='#738664', activebackground='#738664', cursor='hand2',
                         font=('Open Sauce', 15), fg='white', activeforeground='white', width=21, height=1)
    resend_code.place(x=482, y=500)

    messagebox.showinfo('User Verification', 'A Verification Code has been sent to your email.\n'
                                             'Enter the code within 30 seconds to access your account.')

    # Verify Code
    # input_code = input('Enter 2FA Code:')
    # print(totp.verify(input_code))
    if totp.verify(codeEntry.get()):
        messagebox.showinfo('Success', 'User Verified\nAccount Access Granted.')
    else:
        messagebox.showerror('Error', 'Code Does Not Match')

    # Resend Code If Button Pressed

    root.mainloop()


def login_user():
    # Check if entry fields are empty
    if userEntry.get()=='enter username' or passwordEntry.get()=='enter password' or userEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error', 'All Fields Are Required')
    else:
        # Connect to database with userdata
        try:
            # All fields properly filled out, connect to database
            # Use a variable to commit changes to the database
            mydata=pymysql.connect(host='localhost',user='root',password='Classynotsassy1!')
            mycursor=mydata.cursor() # Use to execute commands from the database server
        except:
            messagebox.showerror('Error', 'Database Connection Issue. Please Try Again')
            return

        # Check database for matching login data
        query='use userdata'
        mycursor.execute(query)

        # Find table inside the database
        query='select * from data where username=%s and password=%s'
        mycursor.execute(query, (userEntry.get(), passwordEntry.get()))

        userTaken=mycursor.fetchone()

        if userTaken==None: #Corresponding username not found in database
            messagebox.showerror('Error', 'Invalid Username or Password')
        else:
            # Use Email Authentication based on Email in Database
            user_verification()
            messagebox.showinfo('Welcome', 'Welcome Back!')


login_root = Tk()

# TITLE SCREEN
login_root.title("Welcome Page")
login_root.geometry('1174x660+50+50')
login_root.resizable(False, False)

# set background
bgImage=PhotoImage(file='background.png')
bgLabel=Label(login_root, image=bgImage)
bgLabel.place(x=0,y=0)


# title
header=Label(login_root, text='Sign In', font=('Sanchez', 26), bg='white', fg='#595651')
header.place(x=278,y=135)

# Username
username=Label(login_root, text='Username', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
username.place(x=190,y=205)
userEntry=Entry(login_root, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
userEntry.place(x=192,y=225)
userEntry.insert(0,'enter username')
userEntry.bind('<FocusIn>',enter_user)

# user picture
userImage=PhotoImage(file='pfp.png')
userLabel=Label(login_root, image=userImage, bd=0, bg='#F8F8F8')
userLabel.place(x=474,y=223)

# Password
password=Label(login_root, text='Password', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
password.place(x=190,y=280)
passwordEntry=Entry(login_root, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
passwordEntry.place(x=192,y=300)
passwordEntry.insert(0,'enter password')
passwordEntry.bind('<FocusIn>',enter_password)

# Eye Button
open_eye=PhotoImage(file='show_password.png')
eyeButton=Button(login_root, image=open_eye, bd=0, bg='#F8F8F8', activebackground='#F8F8F8', cursor='hand2', command=hide_pw)
eyeButton.place(x=470,y=298)

# Forget Password
forget_pw=Button(login_root, text='Forget Password?', bd=0, bg='white', activebackground='white',
                 cursor='hand2', font=('Sanchez',9, 'bold'), fg='#595651', activeforeground='#595651', command=forgot_pw)
forget_pw.place(x=400,y=348)

# Login Buttons
login=Button(login_root, text='LOGIN', bd=0, bg='#738664', activebackground='#738664',
             cursor='hand2', font=('Open Sauce',18), fg='white', activeforeground='white', width=20, height=1,
             command=login_user)
login.place(x=200,y=380)
otherLogin=Label(login_root, text='Or Sign In With', font=('Sanchez', 9), bg='white', fg='#595651')
otherLogin.place(x=300,y=438)
Frame(login_root, width=85, height=3, bg='#595651').place(x=200, y=445)
Frame(login_root, width=85, height=3, bg='#595651').place(x=400, y=445)

twitter=PhotoImage(file='twitter.png')
twitterButton=Button(login_root, image=twitter, bd=0, bg='white', activebackground='white', cursor='hand2',
                     activeforeground='#595651')
twitterButton.place(x=245,y=470)


gmail=PhotoImage(file='google.png')
gmailButton=Button(login_root, image=gmail, bd=0, bg='white', activebackground='white', cursor='hand2',
                   activeforeground='#595651')
gmailButton.place(x=325,y=470)

facebook=PhotoImage(file='facebook.png')
facebookButton=Button(login_root, image=facebook, bd=0, bg='white', activebackground='white', cursor='hand2',
                      activeforeground='#595651')
facebookButton.place(x=405,y=470)

# Sign Up Option
signupLabel=Label(login_root, text='Not a Member?', font=('Sanchez', 9, 'bold'), bg='white', fg='#595651')
signupLabel.place(x=240,y=520)
newAccount=Button(login_root, text='Create an Account', bd=0, bg='white', activebackground='white',
                  cursor='hand2', font=('Sanchez',9, 'bold underline'), fg='blue', activeforeground='blue',
                  command=signup_page)
newAccount.place(x=330,y=520)


login_root.mainloop()
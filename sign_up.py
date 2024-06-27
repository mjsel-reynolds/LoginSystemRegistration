from tkinter import *
from tkinter import messagebox
from PIL import ImageTk #Use to upload jpg files in place of png files
import pymysql #Use to connect mySQL database to Python


# Functionality
def clear_entries():
    emailEntry.delete(0,END)
    userEntry.delete(0,END)
    passwordEntry.delete(0,END)
    confirmPasswordEntry.delete(0,END)
    checked.set(False)


def redirect():
    signup_root.destroy()
    import login_page


def connect_database():
    # Entry Error Cases
    if emailEntry.get()=='' or userEntry.get()=='' or passwordEntry.get()=='' or confirmPasswordEntry.get()=='':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif passwordEntry.get() != confirmPasswordEntry.get():
        messagebox.showerror('Error', 'Password Entries Must Match')
    # Condition Error Case
    elif checked==False:
        messagebox.showerror('Error', 'Must Accept Terms & Conditions')
    else:
        try:
            mydata=pymysql.connect(host='localhost',user='root',password='Classynotsassy1!')
            mycursor=mydata.cursor()
        except:
            messagebox.showerror('Error','Database Connection Issue. Please Try Again')
            return

        try:
            # If database DNE, create database using new user information
            query='create database userdata'
            mycursor.execute(query)
            query='use userdata'
            mycursor.execute(query)

            # Create table inside the database
            query='create table data(user_id int auto_increment primary key not null, email varchar(50), username varchar(20), password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')

        # Check if username already exists in database, if username DNE, register
        query='select * from data where username=%s'
        mycursor.execute(query, (userEntry.get()))

        # If a row where the username already exists, tell that it is taken
        userTaken = mycursor.fetchone()

        if userTaken!=None:
            messagebox.showerror('Error', 'Username Already Exists')
        else:
            # insert values from entry boxes into their corresponding columns
            query='insert into data(email, username, password) values (%s,%s,%s)'
            mycursor.execute(query, (emailEntry.get(), userEntry.get(), passwordEntry.get()))
            # Commit changes to table
            mydata.commit()
            mydata.close()
            messagebox.showinfo('Success', 'Registration Complete!')

            # Clear Entry Boxes after Registration & Redirect to Login Page
            clear_entries()
            redirect()


def login_page():
    signup_root.destroy()
    import login_page

signup_root=Tk()

# TITLE SCREEN
signup_root.title('Sign Up Page')
signup_root.geometry('1174x660+50+50')
signup_root.resizable(False, False)

# set background
signup_bg=PhotoImage(file='signup.png')
signup_bgLabel=Label(signup_root, image=signup_bg)
signup_bgLabel.place(x=0,y=0)

# title
frame=Frame(signup_root, bg='white')
frame.place(x=185,y=125)

header=Label(frame, text='Create An Account', font=('Sanchez', 26), bg='white', fg='#595651')
header.grid(row=0,column=0, padx=10)

# Email
frame1=Frame(signup_root, bg='#F8F8F8')
frame1.place(x=187,y=185)

email=Label(frame1, text='Email', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
email.grid(row=1,column=0, sticky='w', padx=15)
emailEntry=Entry(frame1, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
emailEntry.grid(row=2,column=0, sticky='w', padx=15)

# email picture
mailImage=PhotoImage(file='email.png')
mailLabel=Label(signup_root, image=mailImage, bd=0, bg='#F8F8F8')
mailLabel.place(x=466,y=198)

# Username
frame2=Frame(signup_root, bg='#F8F8F8')
frame2.place(x=187,y=250)

user=Label(frame2, text='Username', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
user.grid(row=1,column=0, sticky='w', padx=15)
userEntry=Entry(frame2, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
userEntry.grid(row=2,column=0, sticky='w', padx=15)


# user picture
userImage=PhotoImage(file='pfp.png')
userLabel=Label(signup_root, image=userImage, bd=0, bg='#F8F8F8')
userLabel.place(x=467,y=260)

# Password
frame3=Frame(signup_root, bg='#F8F8F8')
frame3.place(x=187,y=315)

password=Label(frame3, text='Password', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
password.grid(row=1,column=0, sticky='w', padx=15)
passwordEntry=Entry(frame3, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
passwordEntry.grid(row=2,column=0, sticky='w', padx=15)

# lock picture
lockImage=PhotoImage(file='lock.png')
lockLabel=Label(signup_root, image=lockImage, bd=0, bg='#F8F8F8')
lockLabel.place(x=467,y=327)

# Confirm Password
frame4=Frame(signup_root, bg='#F8F8F8')
frame4.place(x=187,y=380)

confirmPassword=Label(frame4, text='Confirm Password', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
confirmPassword.grid(row=1,column=0, sticky='w', padx=15)
confirmPasswordEntry=Entry(frame4, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
confirmPasswordEntry.grid(row=2,column=0, sticky='w', padx=15)

# Conditions Confirmation
checked=BooleanVar()
conditions=Checkbutton(signup_root, text='I agree to the Terms & Conditions', bd=0, bg='white', activebackground='white',
                       cursor='hand2', font=('Sanchez',10), fg='#595651', activeforeground='#595651', variable=checked)
conditions.place(x=225,y=440)

# SignUp Button / Once pressed, user information gets added to the database
signUp=Button(signup_root, text='SIGN UP', bd=0, bg='#738664', activebackground='#738664',
              cursor='hand2', font=('Open Sauce',18), fg='white', activeforeground='white', width=20, height=1,
              command=connect_database)
signUp.place(x=200,y=480)

# Login Option
loginLabel=Label(signup_root, text='Already Have an Account?', font=('Sanchez', 9, 'bold'), bg='white', fg='#595651')
loginLabel.place(x=240, y=530)
login=Button(signup_root, text='Log In', bd=0, bg='white', activebackground='white',
             cursor='hand2', font=('Sanchez',9, 'bold underline'), fg='blue', activeforeground='blue',
             command=login_page)
login.place(x=390,y=530)

signup_root.mainloop()
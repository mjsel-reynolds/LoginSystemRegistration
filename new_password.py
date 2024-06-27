from tkinter import *
from tkinter import messagebox
from PIL import ImageTk #Use to upload jpg files in place of png files
import pymysql #Use to connect mySQL database to Python

#Functionality
def clear_entries():
    userEntry.delete(0,END)
    newPasswordEntry.delete(0,END)
    confirmNewPasswordEntry.delete(0,END)


def redirect():
    new_pw_root.destroy()
    import login_page


def update_database():
    # Entry Error Cases
    if userEntry.get()=='' or newPasswordEntry.get()=='' or confirmNewPasswordEntry.get()=='':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif newPasswordEntry.get() != confirmNewPasswordEntry.get():
        messagebox.showerror('Error', 'Password Entries Must Match')
    else:
        try:
            mydata=pymysql.connect(host='localhost',user='root',password='Classynotsassy1!')
            mycursor=mydata.cursor()
        except:
            messagebox.showerror('Error','Database Connection Issue. Please Try Again')
            return

        mycursor.execute('use userdata')

        # Check if username exists in database, if username DNE, invalid
        query='select * from data where username=%s'
        mycursor.execute(query, (userEntry.get()))
        userTaken = mycursor.fetchone()

        if userTaken==None:
            messagebox.showerror('Error', 'Invalid Username')
        else:
            # update password at that row
            query='update data set password=%s where username=%s'
            mycursor.execute(query, (newPasswordEntry.get(), userEntry.get()))
            # Commit changes to table
            mydata.commit()
            mydata.close()
            messagebox.showinfo('Success', 'Password Updated!')

            # Clear Entry Boxes after Registration & Redirect to Login Page
            clear_entries()
            redirect()


new_pw_root=Tk()

# TITLE SCREEN
new_pw_root.title('Reset Password Page')
new_pw_root.geometry('1174x660+50+50')
new_pw_root.resizable(False, False)

# set background
resetPassword_bg=PhotoImage(file='newPassword.png')
resetPassword_bgLabel=Label(new_pw_root, image=resetPassword_bg)
resetPassword_bgLabel.place(x=0,y=0)

# title
frame=Frame(new_pw_root, bg='white')
frame.place(x=185,y=130)

header=Label(frame, text='Reset Password', font=('Sanchez', 26), bg='white', fg='#595651')
header.grid(row=0,column=0, padx=30)

# Username
frame1=Frame(new_pw_root, bg='#F8F8F8')
frame1.place(x=187,y=200)

username=Label(frame1, text='Username', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
username.grid(row=3,column=0, sticky='w', padx=10)
userEntry=Entry(frame1, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
userEntry.grid(row=10,column=0, sticky='w', padx=10)

# user picture
userImage=PhotoImage(file='pfp.png')
userLabel=Label(new_pw_root, image=userImage, bd=0, bg='#F8F8F8')
userLabel.place(x=467,y=220)

# Password
frame2=Frame(new_pw_root, bg='#F8F8F8')
frame2.place(x=187,y=300)

newPassword=Label(frame2, text='Password', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
newPassword.grid(row=3,column=0, sticky='w', padx=10)
newPasswordEntry=Entry(frame2, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
newPasswordEntry.grid(row=10,column=0, sticky='w', padx=10)

# lock picture
lockImage=PhotoImage(file='lock.png')
lockLabel=Label(new_pw_root, image=lockImage, bd=0, bg='#F8F8F8')
lockLabel.place(x=467,y=320)

# Confirm Password
frame3=Frame(new_pw_root, bg='#F8F8F8')
frame3.place(x=187,y=400)

confirmNewPassword=Label(frame3, text='Confirm Password', font=('Sanchez', 9), bg='#F8F8F8', fg='#595651')
confirmNewPassword.grid(row=3,column=0, sticky='w', padx=10)
confirmNewPasswordEntry=Entry(frame3, width=27, font=('Source Serif Pro', 13), bd=0, fg='#595651', bg='#F8F8F8')
confirmNewPasswordEntry.grid(row=10,column=0, sticky='w', padx=10)

# Submit Reset Password Request
submitPassword=Button(new_pw_root, text='SUBMIT', bd=0, bg='#738664', activebackground='#738664',
                      cursor='hand2', font=('Open Sauce',18), fg='white', activeforeground='white', width=20, height=1,
                      command=update_database)
submitPassword.place(x=200,y=490)



new_pw_root.mainloop()
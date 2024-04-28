from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd

def get_details(email):
    global name, location, gen, clicid
    q = f'select CName,CLocation,CGender,CID from mydb.client where CEmail="{email}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()

    name = d[0][0]
    location = d[0][1]
    gen = d[0][2]
    clicid = d[0][3]


def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)


# ---------------------------------------------Apply a Job---------------------------------------------------
def apply(table):
    # fetch cid,jid from treeview that is in available jobs function
    # code
    selectedindex = table.focus()     # that will return number index
    # that will return list of values with columns=['JID','JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification','MinExp', 'Salary']
    selectedvalues = table.item(selectedindex, 'values')
    ajid = selectedvalues[0]
    chkquery = f'SELECT * from mydb.application where cid={clicid} and jid={ajid}'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(chkquery)
    tempbuff = cur.fetchall()
    mycon.close()
    if(tempbuff):
        messagebox.showinfo(
            'Oops', 'It seems like you have already applied to this job')
    else:
        queryapplyjob = f'Insert into application values(NULL,(select rid from mydb.job where job.jid={ajid}),{ajid},{clicid})'
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(queryapplyjob)
        mycon.commit()
        mycon.close()
        messagebox.showinfo('Thanks', 'Your application has been submitted !')

# ----------------------------------------------Delete A Job -----------------------------------


def delet(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    aaid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'delete from mydb.application where aid={aaid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Thanks', 'Your application has been Deleted')
    myapp()


# -------------------------------------------- Sort Queries --------------------------------------------------------
def sort_alljobs(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        a=f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid order by {criteria}'
        b=f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid order by {criteria} desc'
        if(criteria=="Salary"):
            cur.execute(b)
        else:
            cur.execute(a)
        jobs = cur.fetchall()
        mycon.close()
        i = 0
        for r in jobs:
            table.insert('', i, text="", values=(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
            i += 1


def sort_myapplications(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(
            f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid} order by {criteria}')
        jobs = cur.fetchall()
        mycon.close()
        i = 0
        for r in jobs:
            table.insert('', i, text="", values=(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
            i += 1

# ----------------------------------------------Show all Jobs-----------------------------------------------


def showalljobs(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid')
    jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in jobs:
        table.insert('', i, text="", values=(
            r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
        i += 1

# ----------------------------------------------Show my Applications-----------------------------------------------------


def show_myapplications(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid}')
    applications = cur.fetchall()
    mycon.close()
    print(applications)
    i = 0
    for x in applications:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
        i += 1


# ----------------------------------------------Available Jobs----------------------------------------------------

def available():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=(
        'Times', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'JobType', 'CompanyLocation', 'Salary')
    search_d.current(0)
    search_d.grid(row=0, column=3, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sort_alljobs(table))
    search.grid(row=0, column=4, padx=10, pady=10, ipadx=15)

    apl = Button(rt, text="Apply", font=('Times', 12, 'bold'),
                 bg="#ffd700", fg="#000000", command=lambda: apply(table))
    apl.grid(row=0, column=5, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JID', 'JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JID")
    table.heading("JobRole", text="JobRole")
    table.heading("JobType", text="JobType")
    table.heading("CompanyName", text='CompanyName')
    table.heading("CompanyLocation", text="CompanyLocation")
    table.heading("Qualification", text='Qualification')
    table.heading("MinExp", text='MinExp')
    table.heading("Salary", text="Salary")

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=100)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("CompanyName", width=150)
    table.column("CompanyLocation", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=100)
    table.column("Salary", width=150)
    showalljobs(table)
    table.pack(fill="both", expand=1)
    mycon.close()


# -----------------------------------------My Applictions----------------------------------------------------------------
def myapp():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=('Times', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'JobType', 'CompanyLocation')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="#00b9ed",
                    fg="#ffffff", command=lambda: sort_myapplications(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    dlt = Button(rt, text="Delete", font=('Times', 12, 'bold'),
                 bg="#b32e2e", fg="#ffffff", command=lambda: delet(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('AID', 'JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("AID", text="AID")
    table.heading("JobRole", text="JobRole")
    table.heading("JobType", text="JobType")
    table.heading("CompanyName", text='CompanyName')
    table.heading("CompanyLocation", text="CompanyLocation")
    table.heading("Qualification", text='Qualification')
    table.heading("MinExp", text='MinExp')
    table.heading("Salary", text="Salary")
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("AID", width=50)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("CompanyName", width=150)
    table.column("CompanyLocation", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=100)
    table.column("Salary", width=150)
    show_myapplications(table)
    table.pack(fill="both", expand=1)
    mycon.close()


# ---------------------------------------------------------------------------------------------------------------------------
def change_done(root):
    if opwd1 and pwd1 and cpwd1:
        exe = f'update mydb.users set password="{pwd1}" where email="{email}"'
        try:
            mycon = sql.connect(host='localhost', user='root',
                                passwd=user_pwd, database='mydb')
            cur = mycon.cursor()
            cur.execute(exe)
            mycon.commit()
            mycon.close()
            messagebox.showinfo('SUCCESS!', 'Password Changed Successfully !\nLogin Again With New Password.')
            logi(root)
            opwd1.delete(0, END)
            pwd1.delete(0, END)
            cpwd1.delete(0, END)
        except:
            pass

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')


def password_check(root):
    global opwd1, pwd1, cpwd1
    opwd1 = opwd.get()
    pwd1 = pwd.get()
    cpwd1 = cpwd.get()
    print(opwd1, pwd1, cpwd1)
    if opwd1 and pwd1 and cpwd1:
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(f'select password from users where email="{email}"')
        old = cur.fetchall()
        oldp = old[0][0]
        mycon.close()

        if oldp!=opwd1:
            messagebox.showinfo('ALERT!', 'INVALID Old Password !')
            opwd.delete(0, END)

        else:
            if pwd1 == cpwd1:
                if pwd1==opwd1:
                    messagebox.showinfo('ALERT!', "NEW Password CAN'T be SAME as OLD Password.")
                    opwd.delete(0, END)
                    pwd.delete(0, END)
                    cpwd.delete(0, END)
                else:
                    change_done(root)
            else:
                messagebox.showinfo('ALERT!', 'NEW PASSWORDS DO NOT MATCH !')
                pwd.delete(0, END)
                cpwd.delete(0, END)

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')

def change(root, email):
    global opwd, pwd, cpwd
    print("Change Password")
    bg.destroy()
    r2 = Frame(root, height=700, width=1050)
    r2.place(x=0, y=0)
    r2.render = PhotoImage(file="elements/cp_bg.png")
    img = Label(r2, image=r2.render)
    img.place(x=0, y=0)
    # name_l = Label(r2, text="Name : ", bg='#FFFFFF', fg="#000000",
    #                font=('Times', 20, 'bold'))
    # name_l.place(x=100, y=250)
    # name = Entry(r2, placeholder='Enter Your Full Name...', width=20)
    # name.place(x=290, y=250)

    # email_l = Label(r2, text="Email : ", bg='#FFFFFF', fg="#000000",
    #                 font=('Times', 20, 'bold'))
    # email_l.place(x=100, y=300)
    # email = Entry(r2, placeholder='Email', width=20)
    # email.place(x=290, y=300)

    pwd_0 = Label(r2, text="Old Password : ", bg='#FFFFFF', fg="#000000",
                  font=('Times', 19, 'bold'))
    pwd_0.place(x=100, y=250)
    opwd = Entry(r2, placeholder='Enter Your Old Password', show="•", width=20)
    opwd.place(x=290, y=250)

    pwd_l = Label(r2, text="New Password : ", bg='#FFFFFF', fg="#000000",
                  font=('Times', 19, 'bold'))
    pwd_l.place(x=100, y=325)
    pwd = Entry(r2, placeholder='Enter New Password', show="*", width=20)
    pwd.place(x=290, y=325)

    con_pwd_l = Label(r2, text="Please Confirm : ", bg='#FFFFFF', fg="#000000",
                      font=('Times', 19, 'bold'))
    con_pwd_l.place(x=100, y=400)
    cpwd = Entry(r2, placeholder='Confirm Password', show="*", width=20)
    cpwd.place(x=290, y=400)

    r2.bn = PhotoImage(file="elements\\next1.png")
    btn = Button(r2, image=r2.bn, bg='#FFFFFF', bd=0,
                 activebackground="#ffffff", command=lambda: password_check(root))
    btn.place(x=320, y=475)
    
    # up = Button(root, text="Done ✔️", font=(
    #     'HoneyBee', 14, 'bold'), bg="#00bfff", border=0, fg="#ffffff", command=lambda: )
    # up.place(x=320, y=450)

    r2.back = PhotoImage(file="elements\\back.png")
    btn2 = Button(r2, image=r2.back, bg='#FFFFFF', bd=0,
                  activebackground="#ffffff", command=lambda: cli(root,email))
    btn2.place(x=120, y=475)

def cli(root, email1):
    global email, bg
    email = email1
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    get_details(email)

    bg.load = PhotoImage(file=f'elements\\bg{gen}.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    # Navbar
    nm = Label(root, text=f'{name}', font=(
        'normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{location}', font=(
        'normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="LOGOUT", font=('Lucida Console', 20, 'bold'),
                bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)
    up = Button(root, text="🔒🗝", font=(
        'HoneyBee', 14, 'bold'), bg="#00bfff", border=0, fg="#ffffff", command=lambda: change(root,email))
    up.place(x=1000, y=3)

    # Left
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=240)
    pj = Button(lf, text="Available Jobs", font=(
        'Times', 20), bg="#32cd32", fg="#000000", command=available)
    pj.grid(row=0, column=0, padx=60, pady=70)
    ap = Button(lf, text="My Applications", font=(
        'Times', 20), bg="#00bfff", fg="#000000", command=myapp)
    ap.grid(row=1, column=0, padx=60, pady=70)

    # Right
    global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)

# root = Tk()
# root.geometry("1050x700")
# root.title("Client")
# root.resizable(0, 0)
# cli()
# root.mainloop()

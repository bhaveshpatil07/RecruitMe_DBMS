from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd
from _hashlib import new
import email

# def get_details(email):
#     global name, location, gen, clicid
#     q = f'select CName,CLocation,CGender,CID from mydb.client where CEmail="{email}"'
#     mycon = sql.connect(host='localhost', user='root',
#                         passwd=user_pwd, database='mydb')
#     cur = mycon.cursor()
#     cur.execute(q)
#     d = cur.fetchall()
#     mycon.close()
#
#     name = d[0][0]
#     location = d[0][1]
#     gen = d[0][2]
#     clicid = d[0][3]


def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)


# # ---------------------------------------------Apply a Job---------------------------------------------------
# def apply(table):
#     # fetch cid,jid from treeview that is in available jobs function
#     # code
#     selectedindex = table.focus()     # that will return number index
#     # that will return list of values with columns=['JID','JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification','MinExp', 'Salary']
#     selectedvalues = table.item(selectedindex, 'values')
#     ajid = selectedvalues[0]
#     chkquery = f'SELECT * from mydb.application where cid={clicid} and jid={ajid}'
#     mycon = sql.connect(host='localhost', user='root',
#                         passwd=user_pwd, database='mydb')
#     cur = mycon.cursor()
#     cur.execute(chkquery)
#     tempbuff = cur.fetchall()
#     mycon.close()
#     if(tempbuff):
#         messagebox.showinfo(
#             'Oops', 'It seems like you have already applied to this job')
#     else:
#         queryapplyjob = f'Insert into application values(NULL,(select rid from mydb.job where job.jid={ajid}),{ajid},{clicid})'
#         mycon = sql.connect(host='localhost', user='root',
#                             passwd=user_pwd, database='mydb')
#         cur = mycon.cursor()
#         cur.execute(queryapplyjob)
#         mycon.commit()
#         mycon.close()
#         messagebox.showinfo('Thanks', 'Your application has been submitted !')
#
# # ----------------------------------------------Delete A Job -----------------------------------
#
#
# def delet(table):
#     selectedindex = table.focus()
#     selectedvalues = table.item(selectedindex, 'values')
#     aaid = selectedvalues[0]
#     mycon = sql.connect(host='localhost', user='root',
#                         passwd=user_pwd, database='mydb')
#     cur = mycon.cursor()
#     cur.execute(
#         f'delete from mydb.application where aid={aaid}')
#     mycon.commit()
#     mycon.close()
#     messagebox.showinfo('Thanks', 'Your application has been Deleted')
#     myapp()


# -------------------------------------------- Sort Queries --------------------------------------------------------
# def sort_alljobs(table):
#     criteria = search_d.get()
#     if(criteria == "Select"):
#         pass
#     else:
#         table.delete(*table.get_children())
#         mycon = sql.connect(host='localhost', user='root',
#                             passwd=user_pwd, database='mydb')
#         cur = mycon.cursor()
#         cur.execute(
#             f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid order by {criteria}')
#         jobs = cur.fetchall()
#         mycon.close()
#         i = 0
#         for r in jobs:
#             table.insert('', i, text="", values=(
#                 r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
#             i += 1
#
#
# def sort_myapplications(table):
#     criteria = search_d.get()
#     if(criteria == "Select"):
#         pass
#     else:
#         table.delete(*table.get_children())
#         mycon = sql.connect(host='localhost', user='root',
#                             passwd=user_pwd, database='mydb')
#         cur = mycon.cursor()
#         cur.execute(
#             f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid} order by {criteria}')
#         jobs = cur.fetchall()
#         mycon.close()
#         i = 0
#         for r in jobs:
#             table.insert('', i, text="", values=(
#                 r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
#             i += 1
#
# # ----------------------------------------------Show all Jobs-----------------------------------------------


def showdeljobs(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select *from mydb.deljob order by deleted_at desc')
    jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in jobs:
        table.insert('', i, text="", values=(
            r[0], r[1], r[2], r[3]))
        i += 1

# ----------------------------------------------Show my Applications-----------------------------------------------------


def showdelapp(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT *FROM mydb.delapp order by deleted_at desc')
    applications = cur.fetchall()
    mycon.close()
    print(applications)
    i = 0
    for x in applications:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2]))
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

    cp = Label(r, text="Deleted Jobs", font=(
        'Comic Sans MS', 18, 'bold'), bg="#ffffff", fg="#0A3D62")
    cp.place(x=630, y=213)
    # search_l = Label(rt, text="Deleted Jobs", font=(
    #     'Comic Sans MS', 18, 'bold'), bg="#00ffff", fg="#ff4500")
    # search_l.grid(row=2, column=0, padx=175, pady=0)
    # global search_d
    # search_d = ttk.Combobox(rt, width=12, font=(
    #     'normal', 18), state='readonly')
    # search_d['values'] = ('Select', 'JobRole', 'JobType', 'CompanyLocation')
    # search_d.current(0)
    # search_d.grid(row=0, column=2, padx=0, pady=10)
    # search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
    #                 bg="#00b9ed", fg="#ffffff", command=lambda: sort_alljobs(table))
    # search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)
    #
    # apl = Button(rt, text="Apply", font=('Times', 12, 'bold'),
    #              bg="#ffd700", fg="#000000", command=lambda: apply(table))
    # apl.grid(row=0, column=4, padx=10, pady=10, ipadx=5)
    #
    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JID', 'RID', 'JobRole', 'Deleted At'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JID")
    table.heading("RID", text="RID")
    table.heading("JobRole", text="JobRole")
    table.heading("Deleted At", text="Deleted At")

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=75,anchor=CENTER)
    table.column("RID", width=75,anchor=CENTER)
    table.column("JobRole", width=150,anchor=CENTER)
    table.column("Deleted At", width=150,anchor=CENTER)
    showdeljobs(table)
    table.pack(fill="both", expand=1)
    mycon.close()
    myapp()

#
# # -----------------------------------------My Applictions----------------------------------------------------------------
def myapp():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    # for widget in rt.winfo_children():
    #     widget.destroy()
    for widget in tab1.winfo_children():
        widget.destroy()
    bgr.destroy()

    cp = Label(r, text="Deleted Applications", font=(
        'Comic Sans MS', 18, 'bold'), bg="#ffffff", fg="#0A3D62")
    cp.place(x=590, y=430)
    # search_l = Label(rt, text="Deleted Applications", font=(
    #     'Comic Sans MS', 18, 'bold'), bg="#00ffff", fg="#ff4500")
    # search_l.grid(row=0, column=0, padx=125, pady=0)
    # global search_d
    # search_d = ttk.Combobox(rt, width=12, font=(
    #     'normal', 18), state='readonly')
    # search_d['values'] = ('Select', 'JobRole', 'JobType', 'CompanyLocation')
    # search_d.current(0)
    # search_d.grid(row=0, column=2, padx=0, pady=10)
    # search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="#00b9ed",
    #                 fg="#ffffff", command=lambda: sort_myapplications(table))
    # search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)
    #
    # dlt = Button(rt, text="Delete", font=('Times', 12, 'bold'),
    #              bg="#b32e2e", fg="#ffffff", command=lambda: delet(table))
    # dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab1, orient="horizontal")
    scy = Scrollbar(tab1, orient="vertical")

    table = ttk.Treeview(tab1, columns=('CID', 'JID', 'Deleted At'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("CID", text="CID")
    table.heading("JID", text="JID")
    table.heading("Deleted At", text="Deleted At")
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("CID", width=100,anchor=CENTER)
    table.column("JID", width=100,anchor=CENTER)
    table.column("Deleted At", width=150,anchor=CENTER)
    showdelapp(table)
    table.pack(fill="both", expand=1)
    mycon.close()


# ---------------------------------------------------------------------------------------------------------------------------
def alljobs():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'CALL no_of_job()')
    d = cur.fetchall()
    mycon.close()
    jobs = d[0][0]
    c = Label(r, text=f': {jobs}', font=(
        'honeybee', 21, 'bold'), bg="#ffffff", fg="#0A3D62")
    c.place(x=315, y=269)

def allapps():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'CALL no_of_app()')
    d = cur.fetchall()
    mycon.close()
    apps = d[0][0]
    c = Label(r, text=f': {apps}', font=(
        'honeybee', 21, 'bold'), bg="#ffffff", fg="#0A3D62")
    c.place(x=345, y=367)

def newapp0(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT *FROM mydb.newapp order by created_at desc')
    new = cur.fetchall()
    mycon.close()
    print(new)
    i = 0
    for x in new:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2]))
        i += 1

def newapp():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    
    for widget in tab1.winfo_children():
        widget.destroy()
    bgr.destroy()
    
    cp = Label(r, text="Created Applications", font=(
        'Comic Sans MS', 18, 'bold'), bg="#ffffff", fg="#0A3D62")
    cp.place(x=590, y=430)
    
    scx = Scrollbar(tab1, orient="horizontal")
    scy = Scrollbar(tab1, orient="vertical")

    table = ttk.Treeview(tab1, columns=('CID', 'JID', 'Created At'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("CID", text="CID")
    table.heading("JID", text="JID")
    table.heading("Created At", text='Created At')
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("CID", width=100,anchor=CENTER)
    table.column("JID", width=100,anchor=CENTER)
    table.column("Created At", width=150,anchor=CENTER)
    newapp0(table)
    table.pack(fill="both", expand=1)
    mycon.close()

def created0(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select *from mydb.newjob order by created_at desc')
    newjobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in newjobs:
        table.insert('', i, text="", values=(
            r[0], r[1], r[2], r[3]))
        i += 1

def created():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()
    
    
    cp = Label(r, text="Created Jobs", font=(
        'Comic Sans MS', 18, 'bold'), bg="#ffffff", fg="#0A3D62")
    cp.place(x=630, y=213)
    
    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JID', 'RID', 'JobRole', 'Created At'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JID")
    table.heading("RID", text="RID")
    table.heading("JobRole", text="JobRole")
    table.heading("Created At", text='Created At')

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=75,anchor=CENTER)
    table.column("RID", width=75,anchor=CENTER)
    table.column("JobRole", width=150,anchor=CENTER)
    table.column("Created At", width=150,anchor=CENTER)
    created0(table)
    table.pack(fill="both", expand=1)
    mycon.close()
    newapp()

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
                  activebackground="#ffffff", command=lambda: admin(root))
    btn2.place(x=120, y=475)

def admin(root):
    global r,bg,email
    email="ADMIN"
    r=root
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    # get_details(email)

    bg.load = PhotoImage(file=f'elements\\bgAdmin.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    # Navbar
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'CALL no_of_users()')
    d = cur.fetchall()
    mycon.close()
    count = d[0][0]
    
    nm = Label(root, text=f'Total Users : {count-1}', font=(
        'Comic Sans MS', 16, 'bold'), bg="#ffffff", fg="#000000")
    nm.place(x=805, y=145)
    cp = Label(root, text="B2 Grp2", font=(
        'honeybee', 24, 'bold'), bg="#ffffff", fg="#0A3D62")
    cp.place(x=309, y=139)
    bn = Button(root, text="LOGOUT", font=('Lucida Console', 20, 'bold'),
                bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)
    up = Button(root, text="🔒🗝", font=(
        'HoneyBee', 14, 'bold'), bg="#00bfff", border=0, fg="#ffffff", command=lambda: change(root,email))
    up.place(x=1000, y=3)

    # Left
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=240)
    nj = Button(lf, text="NO OF Jobs", font=(
        'Times', 18), bg="#ffa500", fg="#000000", command=alljobs)
    nj.grid(row=0, column=0, padx=25, pady=25)
    nj = Button(lf, text="NO OF Applications", font=(
        'Times', 18), bg="#ffd700", fg="#000000", command=allapps)
    nj.grid(row=1, column=0, padx=25, pady=25)
    pj = Button(lf, text="Deleted Jobs&Applications", font=(
        'Times', 18), bg="#32cd32", fg="#000000", command=available)
    pj.grid(row=2, column=0, padx=25, pady=25)
    ap = Button(lf, text="Inserted Jobs&Applications", font=(
        'Times', 18), bg="#00bfff", fg="#000000", command=created)
    ap.grid(row=3, column=0, padx=25, pady=25)
    

    # Right
    global rt, tab, tab1, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=254, width=520, height=178)
    tab1 = Frame(root, bg="#FFFFFF")
    tab1.place(x=460, y=476, width=520, height=180)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgAdm.png")
    bgrf.load = PhotoImage.zoom(bgrf.load, 100, 1)
    bgrf.load = PhotoImage.subsample(bgrf.load, 98, 1)
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)

# root = Tk()
# root.geometry("1050x700")
# root.title("Client")
# root.resizable(0, 0)
# cli()
# root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd

def get_details(email):
    global name, company, gen, recid
    q = f'select RName,CompanyName,RGender,RID from mydb.recruiter where REmail="{email}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()

    name = d[0][0]
    company = d[0][1]
    gen = d[0][2]
    recid = d[0][3]


def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)


def submit_job():
    global role1, jtype1, qual1, exp1, sal1
    role1 = role.get()
    jtype1 = jtype.get()
    qual1 = qual.get()
    exp1 = exp.get()
    sal1 = sal.get()
    print(role1, jtype1, qual1, exp1, sal1)
    if role1 and jtype1 and qual1 and exp1 and sal1:
        if jtype1 == "Select":
            messagebox.showinfo('ALERT!', 'Please provide Job Type')
        else:
            exe1 = f'INSERT INTO mydb.Job(RID, JID, JobRole, JobType, Qualification, MinExp, Salary) VALUES({recid}, NULL, "{role1}", "{jtype1}", "{qual1}", {exp1}, {sal1})'
            try:
                mycon = sql.connect(host='localhost', user='root',
                                    passwd=user_pwd, database='mydb')
                cur = mycon.cursor()
                cur.execute(exe1)
                role.delete(0, END)
                jtype.delete(0, END)
                qual.delete(0, END)
                exp.delete(0, END)
                sal.delete(0, END)
                mycon.commit()
                mycon.close()
                messagebox.showinfo('SUCCESS!', 'You have successfully created a Job !')
            except:
                pass
    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')


# -------------------------------------------- Sort Queries --------------------------------------------------------
def sort_all(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')

        cur = mycon.cursor()
        a=f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid} order by {criteria}'
        b=f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid} order by {criteria} desc'
        if(criteria=="Salary"):
            cur.execute(b)
        else:
            cur.execute(a)
        all_jobs = cur.fetchall()
        mycon.close()
    i = 0
    for r in all_jobs:
        table.insert('', i, text="", values=(
            r[1], r[2], r[3], r[4], r[5], r[6]))
        i += 1


def sort_applicants(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')

        cur = mycon.cursor()
        cur.execute(
            f'SELECT job.JobRole, client.CName, client.CEmail, client.CAge, client.CLocation, client.CGender, client.CExp, client.CSkills, client.CQualification FROM application JOIN client ON application.cid=client.CID JOIN job ON job.jid=application.jid where job.rid={recid} order by {criteria}')
        applicats = cur.fetchall()
        mycon.close()
        print(applicats)
        i = 0
        for x in applicats:
            table.insert('', i, text="", values=(
                x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
            i += 1
# ----------------------------------------------Posted jobs Query-----------------------------------------------


def show_all(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid}')
    all_jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in all_jobs:
        table.insert('', i, text="", values=(
            r[1], r[2], r[3], r[4], r[5], r[6]))
        i += 1

# ----------------------------------------------Applicants-----------------------------------------------------


def show_applicants(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT job.JobRole, client.CName, client.CEmail, client.CAge, client.CLocation, client.CGender, client.CExp, client.CSkills, client.CQualification FROM application JOIN client ON application.cid=client.CID JOIN job ON job.jid=application.jid where job.rid={recid}')
    applicats = cur.fetchall()
    mycon.close()
    print(applicats)
    i = 0
    for x in applicats:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
        i += 1


# ---------------------------------------------Post a Job---------------------------------------------------
def create():
    global role, jtype, qual, exp, sal
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    # Create Form
    f1 = Frame(rt, width=520)
    f1.load = PhotoImage(file="elements\\create.png")
    img = Label(rt, image=f1.load, bg="#FFFFFF")
    img.grid(row=0, column=1, padx=150, pady=10)

    # Form
    # Labels
    role_l = Label(tab, text="Role :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    role_l.grid(row=0, column=0, pady=10, padx=10)
    type_l = Label(tab, text="Type :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    type_l.grid(row=1, column=0, pady=10, padx=10)
    qual_l = Label(tab, text="Qualification :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    qual_l.grid(row=2, column=0, pady=10, padx=10)
    exp_l = Label(tab, text="Experience :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    exp_l.grid(row=3, column=0, pady=10, padx=10)
    sal_l = Label(tab, text="Salary :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    sal_l.grid(row=4, column=0, pady=10, padx=10)

    # Entries
    style = ttk.Style(tab)
    style.configure("TCombobox", background="white",
                    foreground="#696969")

    role = Entry(tab, placeholder="Enter Job Role")
    role.grid(row=0, column=1, pady=10, padx=10)
    jtype = ttk.Combobox(tab, font=("normal", 18),
                         width=23, state='readonly')
    jtype['values'] = ('Select', 'FullTime', 'PartTime', 'Intern')
    jtype.current(0)
    jtype.grid(row=1, column=1, pady=10, padx=10)
    qual = Entry(tab, placeholder="Enter Job Qualifications")
    qual.grid(row=2, column=1, pady=10, padx=10)
    exp = Entry(tab, placeholder="Enter Minimum Experience")
    exp.grid(row=3, column=1, pady=10, padx=10)
    sal = Entry(tab, placeholder="Enter Expected salary")
    sal.grid(row=4, column=1, pady=10, padx=10)

    btn = Button(tab, text="Submit", font=(20), bg="#45CE30",
                 fg="#FFFFFF", command=submit_job)
    btn.grid(row=5, column=1, pady=15)

# -------------------------------------------------Delete A Posted Job----------------------------------------------------------


def deletjob(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    ajid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(f'delete from mydb.application where jid={ajid}')
    cur.execute(f'delete from mydb.job where jid={ajid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Thanks', 'Your Job has been Deleted')
    posted()

# ----------------------------------------------Posted Jobs by Recruiter----------------------------------------------------


def posted():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=(
        'normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'JobType', 'Salary')
    search_d.current(0)
    search_d.grid(row=0, column=3, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sort_all(table))
    search.grid(row=0, column=4, padx=10, pady=10, ipadx=15)
    dlt = Button(rt, text="Delete", font=('normal', 12, 'bold'),
                 bg="#b32e2e", fg="#ffffff", command=lambda: deletjob(table))
    dlt.grid(row=0, column=5, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JID', 'JobRole', 'JobType', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JobID")
    table.heading("JobRole", text="Role")
    table.heading("JobType", text='Type')
    table.heading("Qualification", text='Qualification')
    table.heading("MinExp", text='MinExp')
    table.heading("Salary", text="Salary")

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=100)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=100)
    table.column("Salary", width=150)
    show_all(table)
    table.pack(fill="both", expand=1)


# -----------------------------------------Applications on your recruiters posted jobs----------------------------------------------------------------
def app():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'CName', 'CLocation')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=10, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sort_applicants(table))
    search.grid(row=0, column=3, padx=45, pady=10, ipadx=30)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JobRole', 'CName', 'CEmail', 'CAge', 'CLocation', 'CGender', 'CExp', 'CSkills', 'CQualification'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")

    table.heading("JobRole", text="Job Role")
    table.heading("CName", text='Applicants Name')
    table.heading("CEmail", text='Email')
    table.heading("CAge", text='Age')
    table.heading("CLocation", text='Location')
    table.heading("CGender", text='Gender')
    table.heading("CExp", text='Experience')
    table.heading("CSkills", text='Skills')
    table.heading("CQualification", text='Qualification')

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JobRole", width=150)
    table.column("CName", width=200)
    table.column("CEmail", width=100)
    table.column("CAge", width=50)
    table.column("CLocation", width=150)
    table.column("CGender", width=100)
    table.column("CExp", width=100)
    table.column("CSkills", width=200)
    table.column("CQualification", width=150)
    show_applicants(table)
    table.pack(fill="both", expand=1)


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
                  activebackground="#ffffff", command=lambda: rec(root,email))
    btn2.place(x=120, y=475)


# ---------------------------------------------------------------------------------------------------------------------------
def rec(root, email1):
    global email,bg
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
    cp = Label(root, text=f'{company}', font=(
        'normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="LOGOUT", font=(
        'Lucida Console', 20, 'bold'), bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)
    up = Button(root, text="🔒🗝", font=(
        'HoneyBee', 14, 'bold'), bg="#00bfff", border=0, fg="#ffffff", command=lambda: change(root,email))
    up.place(x=1000, y=3)

    # Left
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=220)
    cj = Button(lf, text="Post a Job", font=(
        'Times', 20), bg="#32CD32", fg="#000000", command=create)
    cj.grid(row=0, column=0, padx=80, pady=40)
    pj = Button(lf, text="Posted Jobs", font=(
        'Times', 20), bg="#00Bfff", fg="#000000", command=posted)
    pj.grid(row=1, column=0, padx=80, pady=40)
    ap = Button(lf, text="Applications", font=(
        'Times', 20), bg="#ffD700", fg="#000000", command=app)
    ap.grid(row=2, column=0, padx=80, pady=40)

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

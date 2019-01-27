import tkinter as tk
from tkinter import messagebox

from DB_manager import *

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.db = DatabaseUtility("testDB.db")
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x600+500+300")
        self.title("Main Menu")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.loggedInUser = ""

        self.frames = {}

        for F in [Menu, Login, PeopleForm, PeopleList]:

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def successfulLogin(self,username):
        self.loggedInUser = username
        print("Logged in as", username)
        self.show_frame(Menu)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.loadUp()

class Menu(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        tk.Frame.__init__(self,parent)
        TitleLabel = tk.Label(self,text="Welcome to the Activities Database")
        TitleLabel.grid(row=0, column=0, columnspan=3, sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))
        loggedin = tk.StringVar()
        loggedin.set(controller.loggedInUser)
        self.usernameLabel = tk.Label(self,text = "Logged in as" + loggedin.get(), font=("Arial",8), fg="blue")
        self.usernameLabel.grid(row=10,column=2,sticky="E")

        spacer1 = tk.Label(self,text=" ")
        spacer1.grid(row=1,column=0)
        b1 = tk.Button(self,text="View/Edit People", command=lambda: controller.show_frame(PeopleForm))
        b1.grid(row=2,column = 0)
        
        spacer2 = tk.Label(self,text=" ")
        spacer2.grid(row=3,column=0)
        b2 = tk.Button(self,text="View/Edit Activities")
        b2.grid(row=4,column = 0)
        
        self.columnconfigure(0, weight=1)

    def loadUp(self):
        self.usernameLabel.config(text="Logged in as: " + self.controller.loggedInUser)


class Login(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        tk.Frame.__init__(self, parent)

        self.controller.bind("<Return>", self.keypressed)
        TitleLabel = tk.Label(self, text="Welcome to the Activities Database")
        TitleLabel.grid(row=0, column=0, columnspan=3, sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))

        spacer1 = tk.Label(self, text=" ")
        spacer1.grid(row=1, column=0)
        l1 = tk.Label(self,text="Username", font=("Arial", 12))
        l1.grid(row=2, column=0)
        self.unamebox = tk.Entry(self,width=20, font=("Arial", 12))
        self.unamebox.grid(row=2,column=1)

        spacer2 = tk.Label(self, text=" ")
        spacer2.grid(row=3, column=0)
        l2 = tk.Label(self,text="Password", font=("Arial", 12))
        l2.grid(row=4, column=0)
        self.passbox = tk.Entry(self,width=20, show="*", font=("Arial", 12))
        self.passbox.grid(row=4,column=1 )


        spacer3 = tk.Label(self, text=" ")
        spacer3.grid(row=5, column=0)
        b2 = tk.Button(self, text="Submit", command=self.loginSubmitted)
        b2.grid(row=6, column=0)
        spacer4 = tk.Label(self, text=" ")
        spacer4.grid(row=7, column=0)

        self.feedbacklabel = tk.Label(self, "", foreground="red")
        self.feedbacklabel.grid(row=8, column=0)
        self.columnconfigure(2, weight=1)

    def keypressed(self,event):
        # they pressed return. have they entered a username yet?
        if len(self.unamebox.get())>0:
            self.loginSubmitted()

    def loadUp(self):
        print("loaded Login")
        # print("Bypassed login")
        # self.controller.successfulLogin("asmith")

    def loginSubmitted(self):
        results = self.db.RunCommand("SELECT * from tblUsers WHERE username = ?", [self.unamebox.get()])
        for line in results:
            if line[1] == self.passbox.get():
                self.controller.successfulLogin(self.unamebox.get())
                return True
            else:
                self.feedbacklabel.config(text="Wrong Password")
                return False
        self.feedbacklabel.config(text="No such user")
        return False


class PeopleList(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        self.data = []
        self.databoxes = []

        tk.Frame.__init__(self, parent)
        back = tk.Button(self, text="Main Menu", command=lambda: self.controller.show_frame(Menu))
        back.grid(row=0, column=0, sticky="W")
        self.rowconfigure(1,minsize=20)
        self.columnconfigure(1, weight=1)

        TitleLabel = tk.Label(self, text="View or Edit People - List View")
        TitleLabel.grid(row=2, column=0, columnspan=3, sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))

        formView = tk.Button(self, text="Form View", command = lambda: self.controller.show_frame(PeopleForm))
        formView.grid(row=0,column=2, sticky="E")
        self.datagrid = tk.Frame(self)
        self.datagrid.grid(row=4,column=0,sticky="NSEW",columnspan=3)
        self.delbtn = tk.Button(self, text="Del", command=self.deleteChecked)
        self.delbtn.grid(row=5, column=2, sticky="E")
        self.columnconfigure(2,weight=1)

        saveBtn = tk.Button(self,text="Save Changes", command = self.saveData)
        saveBtn.grid(row=5, column=1, sticky="E")

    def saveData(self):
        for row in self.databoxes:
            self.db.RunCommand("UPDATE tblPeople  SET FirstName = ?, Surname = ?, Form = ? WHERE personID = ?",
                               [row[1][0].get(),row[2][0].get(),row[3][0].get(),row[0][0].get()] )


    def updateDatagrid(self):
        #clear the old grid
        for row in self.databoxes:
            for item in row:
                item[1].destroy()
        self.databoxes=[]
        for rownum in range(len(self.data)):
            self.databoxes.append([])
            for fieldNum in range(len(self.data[rownum])):
                self.databoxes[-1].append([tk.StringVar()])
                self.databoxes[-1][-1][0].set(str(self.data[rownum][fieldNum]))
                self.databoxes[-1][-1].append(tk.Entry(self.datagrid, textvariable=self.databoxes[-1][-1][0]))
                self.databoxes[-1][-1][1].grid(row=rownum, column=fieldNum, padx=5, pady=2)
            self.databoxes[-1][0][1].config(state="disabled") # This makes this column read only
            self.databoxes[-1].append([tk.IntVar()])
            self.databoxes[-1][-1].append(tk.Checkbutton(self.datagrid, variable=self.databoxes[-1][-1][0]))
            self.databoxes[-1][-1][1].grid(row=rownum, column=fieldNum+1,padx=5)


    def refreshData(self):
        result = self.db.RunCommand("SELECT * from tblPeople")
        self.data = result.fetchall()

    def deleteChecked(self):
        numChecked = 0
        for row in self.databoxes:
            if row[-1][0].get()==1:
                numChecked+=1
        if numChecked>0:
            OK = messagebox.askokcancel("Warning", str(numChecked) + " row(s) to delete.\nAre you sure?")
            if OK:
                for row in self.databoxes:
                    if row[-1][0].get() == 1:
                        print("deleting", row[0][0].get(), row[1][0].get())
                        self.db.RunCommand("DELETE FROM tblPeople WHERE personID = ?", [row[0][0].get()])
        self.refreshData()
        self.updateDatagrid()

    def loadUp(self):
        print("loaded People List")
        self.refreshData()
        self.updateDatagrid()


class PeopleForm(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        self.recNum = 0

        tk.Frame.__init__(self, parent)
        self.columnconfigure(1,weight=1)
        back = tk.Button(self, text="Main Menu", command = lambda: self.controller.show_frame(Menu))
        back.grid(row=0,column=0, sticky="W")

        listView = tk.Button(self, text="List View", command = lambda: self.controller.show_frame(PeopleList))
        listView.grid(row=0,column=2, sticky="E")
        self.rowconfigure(1,minsize=20)
        TitleLabel = tk.Label(self, text="View or Edit People - Form View")
        TitleLabel.grid(row=2, column=0, columnspan=3,sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))

        self.rowconfigure(3, minsize=30)
        ul = tk.Label(self, text="ID:")
        ul.grid(row=4, column=0)
        self.ID = tk.StringVar()
        self.IDBox = tk.Entry(self, textvariable = self.ID)
        self.IDBox.grid(row=4, column=1)

        self.IDFeedback = tk.Label(self, text="", fg="red")
        self.IDFeedback.grid(row=4, column=2)

        fn = tk.Label(self, text="First name:")
        fn.grid(row=5, column=0)
        self.firstname = tk.StringVar()
        self.firstnameBox = tk.Entry(self, textvariable = self.firstname)
        self.firstnameBox.grid(row=5, column=1)

        sn = tk.Label(self, text="Surname:")
        sn.grid(row=6, column=0)
        self.surname = tk.StringVar()
        self.surnameBox = tk.Entry(self, textvariable = self.surname)
        self.surnameBox.grid(row=6, column=1)

        fm = tk.Label(self, text="Form Group:")
        fm.grid(row=7, column=0)
        self.form = tk.StringVar()
        self.formBox = tk.Entry(self, textvariable = self.form)
        self.formBox.grid(row=7, column=1)
        self.rowconfigure(8,minsize=50)
        bottomButtons = tk.Frame(self)
        bottomButtons.grid(row=9,column=0, columnspan=2, sticky="NSEW")
        prevBtn = tk.Button(bottomButtons, text="<< Previous", command = lambda: self.changeRec(-1))
        prevBtn.grid(row=0,column=0)

        nextBtn = tk.Button(bottomButtons, text="Next >>", command=lambda: self.changeRec(1))
        nextBtn.grid(row=0, column=4)

        self.newBtn = tk.Button(bottomButtons, text="Create New", command=self.newPerson)
        self.newBtn.grid(row=0, column=1)

        self.delBtn = tk.Button(bottomButtons, text="Delete", command=self.delete)
        self.delBtn.grid(row=0, column=3)

        saveBtn = tk.Button(bottomButtons, text="Save Changes", command=self.saveData)
        saveBtn.grid(row=0, column=2)

        bottomButtons.columnconfigure(0,weight=1)
        bottomButtons.columnconfigure(1,weight= 1)
        bottomButtons.columnconfigure(2, weight=1)
        bottomButtons.columnconfigure(3, weight=1)
        bottomButtons.columnconfigure(4, weight=1)

    def saveData(self):
        if self.recNum == -1:
            # this is a new person
            if self.ID.get() in [str(person[0]) for person in self.data]:
                self.IDFeedback.config(text="This ID already exists")
                return
            else:
                self.IDFeedback.config(text="")
                self.db.RunCommand("INSERT INTO tblPeople VALUES (?,?,?,?)", [self.ID.get(), self.firstname.get(), self.surname.get(), self.form.get()])
                self.recNum = len(self.data)
                self.refreshData()

        else:
            self.db.RunCommand("UPDATE tblPeople SET personID = ?, FirstName = ?, Surname = ?, Form = ? WHERE personID = ?",
                               [self.ID.get(), self.firstname.get(), self.surname.get(), self.form.get(), self.data[self.recNum][0]])
        self.refreshData()


    def newPerson(self):
        self.recNum = -1
        self.ID.set("")
        self.firstname.set("")
        self.surname.set("")
        self.form.set("")
        self.IDBox.focus()

    def delete(self):
        OK = messagebox.askokcancel("Warning", "Are you sure you want to delete this?")
        if OK:
            self.db.RunCommand("DELETE from tblPeople where personID = ?", [self.ID.get()])
            self.recNum = 0
            self.refreshData()


    def changeRec(self, val):
        self.recNum = (self.recNum + val) % len(self.data)
        if self.recNum<0:
            self.recNum = 0
        self.refreshData()

    def changeUserDisplayed(self):
        self.ID.set(self.data[self.recNum][0])
        self.firstname.set(self.data[self.recNum][1])
        self.surname.set(self.data[self.recNum][2])
        self.form.set(self.data[self.recNum][3])
        print("updated")

    def refreshData(self):
        result = self.db.RunCommand("SELECT * from tblPeople")
        self.data = result.fetchall()
        self.changeUserDisplayed()

    def loadUp(self):
        print("loaded People")
        self.refreshData()


def createDemoData():
    db = DatabaseUtility("testDB.db")
    db.RunCommand("DELETE * from tblPeople")
    db.RunCommand("INSERT INTO tblPeople VALUES (?,?,?,?)", [1, 'Steve', 'Nallon', '7SAP'])
    db.RunCommand("INSERT INTO tblPeople VALUES (?,?,?,?)", [2, 'Mike', 'Yarwood', '8JML'])
    db.RunCommand("INSERT INTO tblPeople VALUES (?,?,?,?)", [3, 'Jon', 'Culshaw', '8JML'])
    db.RunCommand("INSERT INTO tblPeople VALUES (?,?,?,?)", [4, 'Rory', 'Bremner', '7SAP'])
    db.RunCommand("INSERT INTO tblPeople VALUES (?,?,?,?)", [5, 'Steve', 'Coogan', '7SAP'])

createDemoData()
app = Main()
app.mainloop()
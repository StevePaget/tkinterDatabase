import tkinter as tk


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x600+500+300")
        self.title("Main Menu")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [Menu]:

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        TitleLabel = tk.Label(self,text="Welcome to the Activities Database")
        TitleLabel.grid(row=0,column=0,sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))
        
        spacer1 = tk.Label(self,text=" ")
        spacer1.grid(row=1,column=0)
        b1 = tk.Button(self,text="View/Edit People")
        b1.grid(row=2,column = 0)
        
        spacer2 = tk.Label(self,text=" ")
        spacer2.grid(row=3,column=0)
        b2 = tk.Button(self,text="View/Edit Activities")
        b2.grid(row=4,column = 0)
        
        self.columnconfigure(0, weight=1)



app = Main()
app.mainloop()
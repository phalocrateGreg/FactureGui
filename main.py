from tkinter import *
from tkinter import simpledialog
# from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

from Screen.ClientSCreen import ClientSCreen
from Screen.CalendarScreen import CalendarScreen
from Command.logger import bcolors as pp


import traceback




def showCalendarSCreen(event):
    pp.printGreen("Drawing calendar")
    screen=CalendarScreen(event.widget.master.master)
    screen.drawScreen()

def showClientScreen(event):
    pp.printGreen("Drawing Client")
    screen=ClientSCreen(event.widget.master.master)
    screen.drawScreen()

def showOtherSCreen (event):
    print ("hello")



    master=event.widget.master.master
    for widget in master.grid_slaves() :
        widget.destroy()

    w = Spinbox(master, from_=0, to=10)
    w.pack()


##################
# Main code
#####################
root = Tk()
root.title("Mine")

toplevel = root.winfo_toplevel()
#toplevel.wm_state('zoomed')

#print ("maxX="+str(root.winfo_screenwidth())+" "+str(root.winfo_screenheight()))


try :
    #Menu bar
    rowIndex=0
    separator = Frame(bd=1, relief=SUNKEN)
    separator.grid(row=rowIndex,columnspan=2,sticky=W+E)

    photo01 = PhotoImage(file="Ressources/calendar_tpdk-casimir_software.gif")
    nP01=photo01.subsample(6,6)
    w01 = Label(separator, image=nP01, compound="top")
    w01.bind("<Button-1>",showCalendarSCreen )
    w01.grid(row=rowIndex,column=0)

    photo0 = PhotoImage(file="Ressources/Client.gif")
    nP0=photo0.subsample(6,6)
    w0 = Label(separator, image=nP0, compound="top")
    w0.bind("<Button-1>", showClientScreen)
    #w.pack(fill=BOTH,expand="true")
    w0.grid(row=rowIndex,column=1)

    photo00 = PhotoImage(file="Ressources/30143-xsara54-Parametres.gif")
    nP00=photo00.subsample(6,6)
    w00 = Label(separator, image=nP00, compound="top")
    w00.bind("<Button-1>", showOtherSCreen)
    w00.grid(row=rowIndex,column=2)



    #Screen Clients
    pp.printGreen("OK")
    #myScreen=ClientSCreen(root)
    # listPhoto=myScreen.drawScreen()
    mySCreen=CalendarScreen(root)
    mySCreen.drawScreen()
    root.mainloop()

    #root.destroy()  # optional; see description below
except Exception as e :
    pp.printError("I have fail")
    pp.printError(e)
    pp.printError(traceback.format_exc())
    messagebox.showerror("Erreur", str(e))
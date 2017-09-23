from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
# from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import collections

from Screen.ClientSCreen import ClientSCreen
from Screen.CalendarScreen import CalendarScreen
from Screen.GenerationScreen import GenerationScreen

from Command.logger import bcolors as pp
from Bom.Client import Client

import os
import sys
import traceback
import configparser

global configFile
global clientList

def loadConfigFile():
    pp.printGreen("Loading config file ...")
    config = configparser.ConfigParser(defaults=None, dict_type=collections.OrderedDict
                                       , allow_no_value=True)
    config.read('Config\\config.dat')
    for section in config.sections():
        print("["+section+"]")
        for key in config[section]:
            print("   "+key+":"+str(config[section][key]))
    pp.printGreen("Done")
    return config

def loadClientInfo(clientName):
    try:
        config = configparser.ConfigParser()
        config.read('Config\\'+clientName+'.dat')
        aClient = Client(config["info"]["name"],
                         config["info"]["adress"],
                         config["info"]["period"],
                         config["info"]["mail"],
                         config["info"]["zipcode"],
                         config["info"]["amount"])
        return aClient
    except Exception:
        pp.printError("Unable to open config file for  "+clientName)
        pp.printError(traceback.format_exc())

def saveBeforeDestroy():
    global configFile
    global clientList
    try:
        os.remove("./Config/config.old")
    except:
        print("No old config file to rm")
    try:
        os.rename("./Config/config.dat", "./Config/config.old")
    except:
        print("No config file to backup")

    with open('./Config/config.dat', 'w') as configfile:
        configFile.write(configfile)
    pp.printGreen("Config file save")

    
    for client in clientList:
        print("Saving Client "+client)
        clientList[client].toConfig(True)
        #with open("./Config/"+client+".dat.bu","w") as clientFile:
        #    clientFile.write(clientList[client].toString())
    pp.printGreen("Clients file save")


    toplevel.destroy()


def showCalendarSCreen(event):
    pp.printGreen("Drawing calendar")
    global clientList
    screen = CalendarScreen(event.widget.master.master, configFile, clientList)
    screen.drawScreen()

def showClientScreen(event):
    pp.printGreen("Drawing Client")
    global clientList
    screen = ClientSCreen(event.widget.master.master, configFile, clientList)
    screen.drawScreen()

def showGenerationScreen(event):
    pp.printGreen("Drawing Generation screen")
    global clientList
    screen = GenerationScreen(event.widget.master.master, configFile, clientList)
    screen.drawScreen()


##################
# Main code
#####################
sys.path.insert(0, os.path.realpath(__file__))

#Load data
global configFile
configFile = loadConfigFile()

global clientList 
clientList = {}
for client in configFile["clientsDB"]:
    print("New client to load ... "+client)
    aClient = loadClientInfo(client)
    aClient.loadConfig()
    clientList[aClient.name] = aClient
#####################################################


root = Tk()
root.title("Mine")

toplevel = root.winfo_toplevel()
toplevel.protocol("WM_DELETE_WINDOW", saveBeforeDestroy)
#toplevel.wm_state('zoomed')

#print ("maxX="+str(root.winfo_screenwidth())+" "+str(root.winfo_screenheight()))


try :
    #Menu bar
    rowIndex = 0
    separator = Frame(bd=1, relief=SUNKEN)
    separator.grid(row=rowIndex, columnspan=2, sticky=W+E)

    photo01 = PhotoImage(file="Ressources/calendar_tpdk-casimir_software.gif")
    nP01 = photo01.subsample(6, 6)
    w01 = Label(separator, image=nP01, compound="top")
    w01.bind("<Button-1>", showCalendarSCreen )
    w01.grid(row=rowIndex, column=0)

    photo0 = PhotoImage(file="Ressources/Client.gif")
    nP0 = photo0.subsample(6, 6)
    w0 = Label(separator, image=nP0, compound="top")
    w0.bind("<Button-1>", showClientScreen)
    #w.pack(fill=BOTH,expand="true")
    w0.grid(row=rowIndex, column=1)

    photo00 = PhotoImage(file="Ressources/30143-xsara54-Parametres.gif")
    nP00 = photo00.subsample(6 , 6)
    w00 = Label(separator, image=nP00, compound="top")
    w00.bind("<Button-1>", showGenerationScreen)
    w00.grid(row=rowIndex, column=2)



    #myScreen = ClientSCreen(root, configFile, clientList)
    myScreen = CalendarScreen(root,configFile,clientList)
    myScreen.drawScreen()
    root.mainloop()

    #root.destroy()  # optional; see description below
except Exception as e:
    pp.printError("I have fail")
    pp.printError(e)
    pp.printError(traceback.format_exc())
    messagebox.showerror("Erreur", str(e))

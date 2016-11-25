import traceback
import configparser
import os

from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog


from Command.logger import bcolors as pp
from Command.FactureWritter import FactureWritter
from Bom.Client import Client



global theSelectedClient


class ClientSCreen:
    def __init__(self,master,config):
        self.master=master
        self.config=config
        self.clientList = {}
        self.textList = []
        self.listPhoto = []

        for widget in master.grid_slaves():
            #Don't touch the menu bar !
            if widget.widgetName !="frame":
                widget.destroy()

        for ix in range (0,7) :
            self.textList.append(StringVar())


        for client in config["clientsDB"]:
            print ("New client to load ... "+client)
            aClient=self.loadClientInfo(client)
            self.clientList[aClient.name] = aClient

        pp.printGreen("Load of  client DB OK")
        #Initialize the first item in the list as the details
        try :
            theFirstClient=str(list(self.clientList.keys())[0])
            theInfo=self.clientList[theFirstClient].toList()
            for ix in range (0,len(theInfo)-1):
                self.textList[ix].set(theInfo[ix])
        except Exception as e:
            pp.printError ("Unbale to init the field")
            pp.printError(traceback.format_exc())


    def loadClientInfo(self,clientName):
        try:
            config = configparser.ConfigParser()
            config.read('Config\\'+clientName+'.dat')
            aClient=Client(config["info"]["name"],config["info"]["adress"],config["info"]["period"],config["info"]["mail"],config["info"]["zipcode"],config["info"]["amount"])
            return aClient
        except :
            pp.printError("Unable to open config file for  "+clientName)
            pp.printError(traceback.format_exc())

    def drawScreen (self) :


        # Toolbar
        rowIndex =  1
        photo = PhotoImage(file="Ressources/newClient.gif")
        nP = photo.subsample(4, 4)
        w = Label(self.master, image=nP, text="Add client", compound="top")
        w.bind("<Button-1>", self.callbackAdd)
        w.photo = photo
        w.grid(row=rowIndex)
        rowIndex = rowIndex + 1
        photo2 = PhotoImage(file="Ressources/rmClient.gif")
        nP2 = photo2.subsample(4, 4)
        w2 = Label(self.master, image=nP2, text="Remove client", compound="top")
        w2.bind("<Button-1>", self.callbackRm)
        w2.photo = photo2
        w2.grid(row=rowIndex, padx=20)
        rowIndex = rowIndex + 1
        photo4= PhotoImage(file="Ressources/edit.gif")
        nP4 = photo4.subsample(4, 4)
        w4 = Label(self.master, image=nP4, text="edit client ", compound="top")
        w4.bind("<Button-1>", self.callbackEdit)
        w4.photo = photo2
        w4.grid(row=rowIndex, padx=20)
        rowIndex = rowIndex + 1
        photo3 = PhotoImage(file="Ressources/30143-xsara54-Parametres.gif")
        nP3 = photo3.subsample(4, 4)
        w3 = Label(self.master, image=nP3, text="Générer facture", compound="top")
        w3.bind("<Button-1>", self.callbackGen)
        w3.photo = photo2
        w3.grid(row=rowIndex, padx=20)



        titleLB = Label(self.master,name="titleLB",text="Liste des clients",anchor=S,padx=0,pady=0)
        titleLB.grid(row=1,column=1)
        listbox = Listbox(self.master, name="maListe")
        listbox.bind("<Double-Button-1>", self.refreshClientDetails)
        listbox.grid(row=2, column=1, rowspan=3, sticky=N + S)
        for client in self.clientList:
            print(">1 " + client)
            listbox.insert(END, client)

        #Avoid photo to be destroy by garbage collector
        self.listPhoto.append(photo)
        self.listPhoto.append(photo2)
        self.listPhoto.append(photo3)
        self.listPhoto.append(photo4)
        self.listPhoto.append(nP)
        self.listPhoto.append(nP2)
        self.listPhoto.append(nP3)
        self.listPhoto.append(nP4)

        #Client details
        try :
            theRow=2
            clientName = Label(self.master,name="clientName",textvariable=self.textList[0], anchor=S, padx=0, pady=0).grid(row=theRow,column=2, sticky=N + S)
            theRow=theRow+1
            clientAdress = Label(self.master,name="clientAdress",textvariable=self.textList[1], anchor=S, padx=0, pady=0).grid(row=theRow,column=2, sticky=N + S)

            theRow = theRow + 1
            clientZip=Label(self.master,name="clientZip",textvariable=self.textList[3], anchor=S, padx=0, pady=0).grid(row=theRow,column=2, sticky=N + S)

            theRow = theRow + 1
            clientCity = Label(self.master, name="clientCity", textvariable=self.textList[2], anchor=S, padx=0,pady=0).grid(row=theRow, column=2, sticky=N + S)

            theRow = theRow + 1
            clientType =  Label(self.master,name="clientType",textvariable=self.textList[6], anchor=S, padx=0, pady=0).grid(row=theRow,column=2, sticky=N + S)

            theRow = theRow + 1
            clientMail = Label(self.master, name="clientMail", textvariable=self.textList[4], anchor=S, padx=0,
                               pady=0).grid(row=theRow, column=2, sticky=N + S)
        except Exception as e :
            pp.printError ("Unable to draw CLient details")
            pp.printError(e)
            pp.printError(traceback.format_exc())
        return self.listPhoto

    def callbackAdd (self,event) :
        test = MyDialog(event.widget)

        if test.client is not None :
            print (test.client.name)

            print ("refresssssssssssssssssssssh")
            self.clientList[test.client.name]=test.client
            theList=event.widget.master.nametowidget(".maListe")
            theList.insert(END, test.client.name)
            # theList.delete(0, END)
            # for client in self.clientList:
            #     print(")>" + client)
            #     theList.insert(END, client)
            self.config["clientsDB"][test.client.name]=""
        else :
            print ("Nothing return ... Do not refresh")


    def callbackRm (self,event) :
        theList =event.widget.master.nametowidget(".maListe")
        print ("Item to rm=>"+theList.get(ACTIVE))
        print("Rmmmmmmmmmmmmmmmmmmm")


        #Now remove the items
        #Rm client config file
        os.remove("Config\\"+theList.get(ACTIVE)+".dat")
        #Rm client from config
        del self.config["clientsDB"][theList.get(ACTIVE)]

        del self.clientList[theList.get(ACTIVE)]
        theList.delete(0, END)
        for client in self.clientList:
           # print(")>" + client)
            theList.insert(END, client)

    def callbackEdit(self,event):
        #Not elegant way to transmit client info to class MyDialog
        event.widget.client=self.clientList[event.widget.master.nametowidget(".maListe").get(ACTIVE)]
        oldClientName=self.clientList[event.widget.master.nametowidget(".maListe").get(ACTIVE)].name
        global theSelectedClient
        theSelectedClient = self.clientList[event.widget.master.nametowidget(".maListe").get(ACTIVE)]

        test = MyDialog(event.widget)
        if test.client is not None:
            del self.clientList[oldClientName]
            self.clientList[test.client.name] = test.client
            theList = event.widget.master.nametowidget(".maListe")
            theList.insert(END, test.client.name)
            theList.delete(0, END)
            for client in self.clientList:
                 print(")>" + client)
                 theList.insert(END, client)
        else:
            print("Nothing return ... Do not refresh")


    def refreshClientDetails(self,event):
        try :
            theList = self.master.nametowidget(".maListe")
            theListInfo=self.clientList[theList.get(ACTIVE)].toList()
            index=0
            for ix in theListInfo:
                print (ix)
                self.textList[index].set(ix)
                index=index+1


        except Exception as e :
            pp.printError ("error !!!!!")
            pp.printError (e)
            pp.printError(traceback.format_exc())

    def callbackGen(self,event):
            theClient=event.widget.master.nametowidget(".maListe").get(ACTIVE)
            print("Generating the doc ")
            event.widget.master.config(cursor="watch")

            try:
                aWritter = FactureWritter(self.clientList[theClient])
                gentime = aWritter.printFacture()

            except Exception as e:
                pp.printError("I have fail")
                pp.printError(e)
                messagebox.showerror("Erreur", str(e))
                event.widget.master.config(cursor="arrow")
                return




            event.widget.master.config(cursor="arrow")
            messagebox.showinfo("Info","Facture créé avec succés (en "+str(gentime)+")")
            pp.printGreen("Generating the doc : OK!")

class MyDialog(simpledialog.Dialog):

    def body(self, master):
        self.title("Add client")

        Label(master, text="Nom du Client:").grid(row=0)
        Label(master, text="Adresse:").grid(row=1)
        Label(master, text="Code postal:").grid(row=2)
        Label(master, text="Ville:").grid(row=3)
        Label(master, text="Mail:").grid(row=4)
        Label(master, text="Montant:").grid(row=5)
        Label(master, text="Periode:").grid(row=6)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)
        self.e7 = Spinbox(master, values=("Mensuel", "Hebdomadaire", "Journalier"))
        #self.e7 = Entry(master)
        global theSelectedClient

        try :
            print ("Pushing "+theSelectedClient.name+"|")
            self.e1.insert(0, theSelectedClient.name)
            self.e2.insert(0, theSelectedClient.adress)
            self.e3.insert(0, theSelectedClient.zipcode)
            self.e4.insert(0, theSelectedClient.city)
            self.e5.insert(0, theSelectedClient.mail)
            self.e6.insert(0, theSelectedClient.amount)
        except :
            print ("New Client")




        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)
        self.e7.grid(row=6, column=1)


        self.client = None
        return self.e1 # initial focus

    def apply(self):
        name = str(self.e1.get())
        adress = str(self.e2.get())
        zipcode=str(self.e3.get())
        city=str(self.e4.get())
        mail=str(self.e5.get())
        amount=str(self.e6.get())
        period = str(self.e7.get())

        self.client = Client(name,adress,period,mail,city,zipcode,amount)
        self.client.toConfig(True)
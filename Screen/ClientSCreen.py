import traceback
import configparser
import os

from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from tkinter import font as tkFont

from Command.logger import bcolors as pp
from Command.FactureWritter import FactureWritter
from Bom.Client import Client



global theSelectedClient


class ClientSCreen:
    def __init__(self,master,config,clientList):
        self.master=master
        self.config=config
        self.clientList = clientList
        self.textList = []
        self.listPhoto = []
        self.activeClient = ""
        self.activeFacture = ""
        self.listFactures = []

        for widget in master.grid_slaves():
            #Don't touch the menu bar !
            if widget.widgetName !="frame" :
                widget.destroy()
        for ix in range (0,7) :
            self.textList.append(StringVar())

        #Initialize the first item in the list as the details
        try :
            theFirstClient=str(list(self.clientList.keys())[0])
            self.activeClient=theFirstClient
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
        rowIndex = rowIndex + 1
        photo5 = PhotoImage(file="Ressources/tickAction.gif")
        nP5 = photo5.subsample(4, 4)
        w5 = Label(self.master, image=nP5, text="Payé", compound="top")
        w5.bind("<Button-1>", self.switchPaidStatus)
        w5.photo = photo4
        w5.grid(row=rowIndex, padx=20)
        #Avoid photo to be destroy by garbage collector
        self.listPhoto.append(photo)
        self.listPhoto.append(photo2)
        self.listPhoto.append(photo3)
        self.listPhoto.append(photo4)
        self.listPhoto.append(photo5)
        self.listPhoto.append(nP)
        self.listPhoto.append(nP2)
        self.listPhoto.append(nP3)
        self.listPhoto.append(nP4)
        self.listPhoto.append(nP5)


        aFakeLabel = Label(self.master, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)


        
        placeHolder = Frame(self.master, name="placeHolder", bd=1, relief=SUNKEN,bg="white")
        placeHolder.grid(row=1,column=1,rowspan=5,columnspan=5, sticky=N)

        titleLB = Label(placeHolder,name="titleLB",text="Liste des clients",anchor=S,padx=0,pady=0,font=myFont)
        titleLB.grid(row=1,column=1)
        listbox = Listbox(placeHolder, name="maListe")
        listbox.bind("<Double-Button-1>", self.refreshClientDetails)
        listbox.grid(row=2, column=1, rowspan=5, sticky=N + S)
        for client in self.clientList:
            listbox.insert(END, client)
            
        #activate the first element of the list
        ix=0
        for client in listbox.get(0, END):            
            if client == self.activeClient:
                listbox.activate(ix)
                listbox.select_set(ix)
                break            
            ix = ix + 1
            
            
        #Client details

        titleClientDetails = Label(placeHolder,name="titleCD",text="Détails client",anchor=S,padx=0,pady=0,font=myFont)
        titleClientDetails.grid(row=1,column=2,columnspan=2)
        try :
            theRow=2
            clientName = Label(placeHolder,name="clientName",textvariable=self.textList[0]).grid(row=theRow,column=2, sticky=N,columnspan=2 )
            theRow=theRow+1
            clientAdress = Label(placeHolder,name="clientAdress",textvariable=self.textList[1]).grid(row=theRow,column=2, sticky=N ,columnspan=2)

            theRow = theRow + 1
            clientZip=Label(placeHolder,name="clientZip",textvariable=self.textList[3]).grid(row=theRow,column=2, sticky=N,columnspan=2)

            theRow = theRow + 1
            clientCity = Label(placeHolder, name="clientCity", textvariable=self.textList[2], anchor=S, padx=0,pady=0).grid(row=theRow, column=2, sticky=N,columnspan=2 )

            theRow = theRow + 1
            clientType =  Label(placeHolder,name="clientType",textvariable=self.textList[6]).grid(row=theRow,column=2, sticky=N,columnspan=2 )

            theRow = theRow + 1
            clientMail = Label(placeHolder, name="clientMail", textvariable=self.textList[4]).grid(row=theRow, column=2, sticky=N ,columnspan=2)

            theRow = theRow + 1
            #List des factures
            ###################
            titleLBfacture = Label(placeHolder,name="titleLB2",text="Factures Client",anchor=S,padx=0,pady=0,font=myFont)
            titleLBfacture.grid(row=theRow,column=1,columnspan=2)
            #Facture details
            ###################
            titleLBfactureDetails = Label(placeHolder,name="titleFacDetails",text="Détails facture",anchor=S,padx=0,pady=0,font=myFont)
            titleLBfactureDetails.bind("<Double-Button-1>", self.refreshFactureDetails)
            titleLBfactureDetails.grid(row=theRow,column=2,columnspan=2)

            theRow = theRow + 1

            self.listFactures.clear
            scrollbar = Scrollbar(placeHolder, orient=VERTICAL)

            listboxFact = Listbox(placeHolder, name="maListeFac",listvariable=self.listFactures, yscrollcommand=scrollbar.set)
            listboxFact.bind("<Double-Button-1>", self.refreshFactureDetails)
            listboxFact.grid(row=theRow, column=1, sticky=N + S,rowspan=5)

            scrollbar.config(command=listboxFact.yview)
            scrollbar.grid(row=theRow, column=2, sticky=N + S,rowspan=5)
            
            for aFact in self.clientList[self.activeClient].factureList:
               listboxFact.insert(END, aFact.numberId+"-"+aFact.editionDate)
            

            listboxFactDetailsName = Listbox(placeHolder)            
            listboxFactDetailsName.insert(END, "N°")
            listboxFactDetailsName.insert(END, "Fait le")
            listboxFactDetailsName.insert(END, "Échéance")
            listboxFactDetailsName.insert(END, "Montant")
            listboxFactDetailsName.insert(END, "Payé")
            listboxFactDetailsName.grid(row=theRow, column=3, sticky=N + S,rowspan=5)
            theRow = theRow + 1
            listboxFactDetails = Listbox(placeHolder, name="maListeFacDetails")
            listboxFactDetails.grid(row=theRow, column=4, sticky=N + S,rowspan=5)

           

        except Exception as e :
            pp.printError ("Unable to draw CLient details")
            pp.printError(e)
            pp.printError(traceback.format_exc())

        return self.listPhoto

    def switchPaidStatus(self,event):
        print("Switch paid status")
        theClient=event.widget.master.nametowidget(".placeHolder.maListe").get(ACTIVE)
        print ( "theClient="+theClient)
        print( "selectedFact"+self.activeFacture)
        for facture in self.clientList[theClient].factureList:
            if str(facture.numberId+"-"+facture.editionDate) == self.activeFacture:
                facture.isPaid = not facture.isPaid
                self.refreshFactureDetails(None)
                print (" Facture updated")

    def callbackAdd (self,event) :
        test = MyDialog(event.widget)

        if test.client is not None :
            self.clientList[test.client.name]=test.client
            theList=event.widget.master.nametowidget(".placeHolder.maListe")
            theList.insert(END, test.client.name)
            self.config["clientsDB"][test.client.name]=""
        else :
            print ("Nothing return ... Do not refresh")


    def callbackRm (self,event) :
        theList =event.widget.master.nametowidget(".placeHolder.maListe")
        print ("Item to rm=>"+theList.get(ACTIVE))

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
        event.widget.client=self.clientList[event.widget.master.nametowidget(".placeHolder.maListe").get(ACTIVE)]
        oldClientName=self.clientList[event.widget.master.nametowidget(".placeHolder.maListe").get(ACTIVE)].name
        global theSelectedClient
        theSelectedClient = self.clientList[event.widget.master.nametowidget(".placeHolder.maListe").get(ACTIVE)]

        test = MyDialog(event.widget)
        if test.client is not None:
            del self.clientList[oldClientName]
            self.clientList[test.client.name] = test.client
            theList = event.widget.master.nametowidget(".placeHolder.maListe")
            theList.insert(END, test.client.name)
            theList.delete(0, END)
            for client in self.clientList:
                 print(")>" + client)
                 theList.insert(END, client)
        else:
            print("Nothing return ... Do not refresh")

    def refreshFactureDetails(self,event):
        pp.printGreen("Refresh facture details")
        if event :
            self.activeFacture=event.widget.get(ACTIVE)
        theList= self.master.nametowidget(".placeHolder.maListeFacDetails")
        for aFact in self.clientList[self.activeClient].factureList:
            if str(aFact.numberId+"-"+aFact.editionDate) == self.activeFacture:
                theList.delete(0,END)
                theList.insert(END, aFact.numberId)
                theList.insert(END, aFact.editionDate)
                theList.insert(END, aFact.dueDate)
                theList.insert(END, aFact.amount)
                if aFact.isPaid:
                    theList.insert(END,"V")
                else :
                    theList.insert(END,"X")
                break


    def refreshClientDetails(self,event):
        try :
            theList= self.master.nametowidget(".placeHolder.maListe")
            theListInfo=self.clientList[theList.get(ACTIVE)].toList()
            global theSelectedClient
            self.activeClient=theList.get(ACTIVE)
            index=0
            for ix in theListInfo:
                print (ix)
                self.textList[index].set(ix)
                index=index+1

            listboxFact = self.master.nametowidget(".placeHolder.maListeFac")
            listboxFact.delete(0, END) 
            for aFact in self.clientList[self.activeClient].factureList:
               # print(">2 " + aFact.numberId)
               listboxFact.insert(END, aFact.numberId+"-"+aFact.editionDate)


        except Exception as e :
            pp.printError ("error !!!!!")
            pp.printError (e)
            pp.printError(traceback.format_exc())
            
    def callbackGen(self,event):
            theClient=event.widget.master.nametowidget(".placeHolder.maListe").get(ACTIVE)
            print("Generating the doc ")
            event.widget.master.config(cursor="watch")

            try:
                aWritter = FactureWritter(self.clientList[theClient])
                gentime = aWritter.printFacture()

            except Exception as e:
                pp.printError("I have fail")
                pp.printError(e)
                pp.printError(traceback.format_exc())
                messagebox.showerror("Erreur", str(e))
                event.widget.master.config(cursor="arrow")
                return

            for aFac in self.clientList[theClient].factureList:
                print (aFac.toString())
            pp.printGreen("Generating the doc : OK!")
            event.widget.master.config(cursor="arrow")
            messagebox.showinfo("Info","Facture créé avec succés (en "+str(gentime)+")")
            self.clientList[theClient].toConfig(True)


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
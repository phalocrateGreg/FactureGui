import traceback

from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog

from Command.FactureWritter import FactureWritter
from Bom.Client import Client

class ClientSCreen:
    def __init__(self,master):
        self.master=master
        self.clientList = {}
        self.textList = []
        for ix in range (0,7) :
            self.textList.append(StringVar())

        f = open('workfile.dat', 'r')
        for line in f:
            print(line)
            clientInfo = line.split(";")
            if(len(clientInfo)>5):
                aClient=Client(clientInfo[0], clientInfo[1],clientInfo[6], clientInfo[4],clientInfo[2],clientInfo[3],clientInfo[5])
                self.clientList[aClient.name] = aClient
        f.close()

        #Initialize the first item in the list as the details
        try :
            theFirstClient=str(list(self.clientList.keys())[0])
            theInfo=self.clientList[theFirstClient].toList()
            for ix in range (0,len(theInfo)-1):
                self.textList[ix].set(theInfo[ix])
        except Exception as e:
            print ("Unbale to init the field")


    def drawScreen (self) :
        listPhoto= []
        # Toolbar
        rowIndex =  1
        photo = PhotoImage(file="newClient.gif")
        nP = photo.subsample(4, 4)
        w = Label(self.master, image=nP, text="Add client", compound="top")
        w.bind("<Button-1>", self.callbackAdd)
        w.photo = photo
        w.grid(row=rowIndex)

        rowIndex = rowIndex + 1
        photo2 = PhotoImage(file="rmClient.gif")
        nP2 = photo2.subsample(4, 4)
        w2 = Label(self.master, image=nP2, text="Remove client", compound="top")
        w2.bind("<Button-1>", self.callbackRm)
        w2.photo = photo2
        w2.grid(row=rowIndex, padx=20)

        rowIndex = rowIndex + 1
        photo3 = PhotoImage(file="30143-xsara54-Parametres.gif")
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
        listPhoto.append(photo)
        listPhoto.append(photo2)
        listPhoto.append(photo3)
        listPhoto.append(nP)
        listPhoto.append(nP2)
        listPhoto.append(nP3)

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
            print ("Unable to draw CLient details")
            print(e)
            print(traceback.format_exc())
        return listPhoto

    def callbackAdd (self,event) :
        print ("Click"+str(event))
        test = MyDialog(event.widget)

        if test.client is not None :
            print (test.client.name)

            print ("refresssssssssssssssssssssh")
            self.clientList[test.client.name]=test.client
            theList=event.widget.master.nametowidget(".maListe")
            theList.delete(0, END)
            for client in self.clientList:
                print(")>" + client)
                theList.insert(END, client)
        else :
            print ("Nothing return ... Do not refresh")


    def callbackRm (self,event) :
        print ("Click2"+str(event))
        theList =event.widget.master.nametowidget(".maListe")
        print ("Item to rm=>"+theList.get(ACTIVE))
        print("Rmmmmmmmmmmmmmmmmmmm")


        #Now remove the items
        f = open('workfile.dat', 'w')
        newClientList = {}
        del self.clientList[theList.get(ACTIVE)]
        for client in self.clientList:
            print ("# "+client+" "+theList.get(ACTIVE))
            if client != theList.get(ACTIVE):
                f.write( client + ";" + self.clientList[client].adress + ";" + self.clientList[client].period+"\n")
            else :
                print ("Skip this item =>"+theList.get(ACTIVE))

        f.close()


        theList.delete(0, END)
        for client in self.clientList:
            print(")>" + client)
            theList.insert(END, client)


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
            print ("error !!!!!")
            print (e)
            print(traceback.format_exc())

    def callbackGen(self,event):
            print("Click3" + str(event))
            theClient=event.widget.master.nametowidget(".maListe").get(ACTIVE)
            print("Generating the doc ")
            event.widget.master.config(cursor="watch")

            try :
                aWritter = FactureWritter(self.clientList[theClient])
                gentime=aWritter.printFacture()
            except Exception as e :
                print ("I have fail")
                print (e)
                messagebox.showerror("Erreur", str(e))
                event.widget.master.config(cursor="arrow")
                return

            event.widget.master.config(cursor="arrow")
            messagebox.showinfo("Info","Facture créé avec succés (en "+str(gentime)+")")
            print("Generating the doc : OK!")

class MyDialog(simpledialog.Dialog):

    def body(self, master):
        self.title("Add client")

        Label(master, text="Nom du Client:").grid(row=0)
        Label(master, text="Adresse:").grid(row=1)
        Label(master, text="Code postal:").grid(row=2)
        Label(master, text="Ville:").grid(row=3)
        Label(master, text="Mail:").grid(row=4)
        Label(master, text="Periode:").grid(row=5)
        Spinbox(master,values=("Mensuel", "Hebdomadaire", "Journalier")).grid(row=6)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)
        #self.e7 = Entry(master)


        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)
        self.client = None
        return self.e1 # initial focus

    def apply(self):
        name = str(self.e1.get())
        adress = str(self.e2.get())
        zipcode=str(self.e3.get())
        city=str(self.e4.get())
        mail=str(self.e5.get())
        period = str(self.e6.get())

        self.client = Client(name,adress,period,mail,city,zipcode)
        f = open('workfile.dat', 'a')
        f.write("\n"+self.client.toString())
        f.close()
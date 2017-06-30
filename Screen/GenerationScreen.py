import traceback
from Command.logger import bcolors as pp
from tkinter import *
from tkinter import font as tkFont
from datetime import datetime, date, time,timedelta
import calendar
from Bom.Client import Client
from Command.FactureWritter import FactureWritter

class GenerationScreen:
    def __init__(self,master,config,clientList):
        self.master=master
        self.config=config
        self.clientList = clientList
        self.clientListVar = {}
        self.listCheckBox = []
        self.shouldActivateAll = False
        self.listPhoto = []
        self.progressGen =IntVar(0)
        self.maxProgress = IntVar()
        self.maxProgress.set(len(clientList))
        self.progresBar = None
        for widget in master.grid_slaves():
            #Don't touch the menu bar !
            if widget.widgetName !="frame":
                widget.destroy()
        self.master.nametowidget(".placeHolder").destroy()

    def drawScreen(self):
        # Toolbar
        rowIndex =  1
        photo1 = PhotoImage(file="Ressources/30143-xsara54-Parametres.gif")
        nP1 = photo1.subsample(4, 4)
        w1 = Label(self.master, image=nP1, text="Générer facture", compound="top")
        w1.bind("<Button-1>", self.callbackGen)
        w1.photo = photo1
        w1.grid(row=rowIndex, padx=20)
        rowIndex = rowIndex + 1


        photo2 = PhotoImage(file="Ressources/tickAction.gif")
        nP2 = photo2.subsample(4, 4)
        w2 = Label(self.master, image=nP2, text="(dé)selectioner tous", compound="top")
        w2.bind("<Button-1>", self.switchAll)
        w2.photo = photo2
        w2.grid(row=rowIndex, padx=20)
    
        #Avoid photo to be destroy by garbage collector
        self.listPhoto.append(nP1)
        self.listPhoto.append(nP2)
        
        aFakeLabel = Label(self.master, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)

        titleClientList = Label(self.master, name="titleClientList", text="Liste des clients", anchor=S, padx=50, pady=0,font=myFont).grid(row=1,column=1)
        titleTickBox = Label(self.master, name="titleTickBox", text="Generation des factures", anchor=S, padx=50, pady=0,font=myFont).grid(row=1,column=2)
       
        rowIndex = 1
        for ix in self.clientList:
            pp.printGreen(ix)
            self.clientListVar[ix] = IntVar(0)
            label = Label(self.master, name="client_"+str(ix), text = self.clientList[ix].name).grid(row = rowIndex+1,column = 1)
            c = Checkbutton(
                self.master, name="clientCheckbox_"+str(ix),
                text="",
                variable=self.clientListVar[ix])
            c.select()
            self.listCheckBox.append(c)
            c.grid(row=rowIndex+1,column=2)
            rowIndex = rowIndex +1

        self.progresBar = ttk.Progressbar(orient=HORIZONTAL, length=150, mode='determinate',variable = self.progressGen,maximum=self.maxProgress.get())
        self.progressGen.set(0)
        self.progresBar.grid(row=rowIndex+1,column = 1)
        self.progresBar.grid_remove()




    def switchAll(self,event):
        for widget in self.listCheckBox:
            if  self.shouldActivateAll :
                widget.select()
            else :
                widget.deselect()
        self.shouldActivateAll = not self.shouldActivateAll
           
    def callbackGen(self, event):
            isError = False
            pp.printGreen("Generating the doc ")
            event.widget.master.config(cursor="watch")
            numberOfClient  = len(self.clientListVar)
            self.progresBar.grid()
            for aClient in self.clientListVar:
                self.progressGen.set(self.progressGen.get()+1)
                if self.clientListVar[aClient].get():
                    try:
                        pp.printGreen("  "+aClient)
                        aWritter = FactureWritter(self.clientList[aClient])
                        gentime = aWritter.printFacture()

                    except Exception as e:
                        pp.printError("I have fail")
                        pp.printError(e)
                        pp.printError(traceback.format_exc())
                        messagebox.showerror("Erreur", str(e))
                        event.widget.master.config(cursor="arrow")
                        self.progressGen.set(self.progressGen.get()+1)
                        isError = True                        
                        continue

                    #for aFac in self.clientList[aClient].factureList:
                    #    print (aFac.toString())
                    # pp.printGreen("Generating the doc : OK!")
                    
                    #messagebox.showinfo("Info","Facture créé avec succés (en "+str(gentime)+")")
                    self.clientList[aClient].toConfig(True)
                    self.progressGen.set(self.progressGen.get()+1)
                else :
                    self.progressGen.set(self.progressGen.get()+1)

            event.widget.master.config(cursor="arrow")
            if isError:
                pp.printWarning(" Erreur durant la génération")
                messagebox.showerror("Warning","Probléme durant laa génération des factures")
            else :
                messagebox.showinfo("Info","Facture créé avec success")
            self.progresBar.grid_remove()


class DialogProgressBar(simpledialog.Dialog):

    def body(self, master):
        self.title("Génération des factures ")

        Label(master, text="Nom du Client:").grid(row=0)
        '''progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate',variable = progressStatus,maximum=100)
        progressStatus.set(0)'''

    def buttonbox(self):
         pass

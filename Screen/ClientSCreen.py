from tkinter import *
from tkinter import simpledialog

from pylatex import Document, Section, Itemize, Enumerate, Description,  Command, NoEscape

import os
import sys

class ClientSCreen:
    def __init__(self,master):
        self.master=master
        self.clientList = {}
        f = open('workfile.dat', 'r')
        for line in f:
            print(line)
            clientInfo = line.split(";")
            aList = []
            for j in clientInfo:
                print(j)
                aList.append(j)
            self.clientList[clientInfo[0]] = aList
        f.close()
        for client in self.clientList:
            print(">" + client)

    def drawScreen (self) :
        listPhoto= []
        # Toolbar
        rowIndex =  1
        photo = PhotoImage(file="newClient.gif")
        nP = photo.subsample(4, 4)
        w = Label(self.master, image=nP, text="Add client", compound="top")
        w.bind("<Button-1>", self.callbackAdd)
        w.photo = photo
        # w.pack(fill=BOTH,expand="true")
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

        # test = MyDialog(root)

        # for i in myContainer1.pack_slaves():
        #    print (str(i))




        listbox = Listbox(self.master, name="maListe")
        listbox.grid(row=1, column=1, rowspan=3, sticky=N + S)
        for client in self.clientList:
            print(">1 " + client)
            listbox.insert(END, client)

        #AVoid photo to be destroy by garbage collector
        listPhoto.append(photo)
        listPhoto.append(photo2)
        listPhoto.append(photo3)
        listPhoto.append(nP)
        listPhoto.append(nP2)
        listPhoto.append(nP3)
        return listPhoto

    def callbackAdd (self,event) :
        print ("Click"+str(event))
        test = MyDialog(event.widget)
        #refreshClientList(event.widget.master)
        print ("refresssssssssssssssssssssh")
        clientList = {}
        f = open('workfile.dat', 'r')
        for line in f:
            clientInfo = line.split(";")
            aList = []
            for j in clientInfo:
                aList.append(j)
            clientList[clientInfo[0]] = aList
        f.close()
        theList=event.widget.master.nametowidget(".maListe")
        theList.delete(0, END)
        for client in clientList:
            print(")>" + client)
            theList.insert(END, client)


    def callbackRm (self,event) :
        print ("Click2"+str(event))
        theList =event.widget.master.nametowidget(".maListe")
        print ("Item to rm=>"+theList.get(ACTIVE))
        print("Rmmmmmmmmmmmmmmmmmmm")

        #First read the file
        clientList = {}
        f = open('workfile.dat', 'r')
        for line in f:
            clientInfo = line.split(";")
            aList = []
            for j in clientInfo:
                aList.append(j)
            clientList[clientInfo[0]] = aList
        f.close()

        #Now remove the items
        f = open('workfile.dat', 'w')
        newClientList = {}
        for client in clientList:
            print ("# "+client+" "+theList.get(ACTIVE))
            if client != theList.get(ACTIVE):
                f.write("\n" + client + ";" + clientList[client][0] + ";" + clientList[client][1])
                aList = []
                clientInfo=clientList[client]
                for j in clientInfo:
                    aList.append(j)
                newClientList[clientInfo[0]] = aList
            else :
                print ("Skip this item =>"+theList.get(ACTIVE))
        f.close()


        theList.delete(0, END)
        for client in newClientList:
            print(")>" + client)
            theList.insert(END, client)


    def refreshClientList(self) :
        print ("refresssssssssssssssssssssh")
        clientList = {}
        f = open('workfile.dat', 'r')
        for line in f:
            clientInfo = line.split(";")
            aList = []
            for j in clientInfo:
                aList.append(j)
            clientList[clientInfo[0]] = aList
        f.close()
        theList=self.master.nametowidget(".maListe")
        theList.delete(0, END)
        for client in clientList:
            print(")>" + client)
            theList.insert(END, client)

    def callbackGen(self,event):
            print("Click3" + str(event))
            #do(event.widget.master.nametowidget(".maListe").get(ACTIVE))
            theClient=event.widget.master.nametowidget(".maListe").get(ACTIVE)
            doc = Document()
            doc.append(Command("title{TiLuNet}"))
            doc.append(Command("maketitle"))
            with doc.create(Section(theClient)):
             with doc.create(Itemize()) as itemize:
                     itemize.add_item("the first item")
                     itemize.add_item("the second item")
                     itemize.add_item("the third etc")
                     # you can append to existing items
                     itemize.append(Command("ldots"))


            # create a bulleted "itemize" list like the below:
            # \begin{itemize}
            #   \item The first item
            #   \item The second item
            #   \item The third etc \ldots
            # \end{itemize}

            # with doc.create(Section(theClient)):
            #     with doc.create(Itemize()) as itemize:
            #         itemize.add_item("the first item")
            #         itemize.add_item("the second item")
            #         itemize.add_item("the third etc")
            #         # you can append to existing items
            #         itemize.append(Command("ldots"))

            # create a numbered "enumerate" list like the below:
            # \begin{enumerate}
            #   \item The first item
            #   \item The second item
            #   \item The third etc \ldots
            # \end{enumerate}

            # with doc.create(Section('"Enumerate" list')):
            #     with doc.create(Enumerate()) as enum:
            #         enum.add_item("the first item")
            #         enum.add_item("the second item")
            #         enum.add_item(NoEscape("the third etc \\ldots"))

            # create a labelled "description" list like the below:
            # \begin{description}
            #   \item[First] The first item
            #   \item[Second] The second item
            #   \item[Third] The third etc \ldots
            # \end{description}

            # with doc.create(Section('"Description" list')):
            #     with doc.create(Description()) as desc:
            #         desc.add_item("First", "The first item")
            #         desc.add_item("Second", "The second item")
            #         desc.add_item("Third", NoEscape("The third etc \\ldots"))
            # doc.generate_tex('MyDoclists2')
            doc.generate_pdf('MyDoclists', clean=True, clean_tex=False,
                             compiler="pdflatex", compiler_args=None, silent=True)

    def do (theClient) :

        doc = Document()
        doc.append(Command("title{TiLuNet}"))
        doc.append(Command("maketitle"))
        with doc.create(Section(theClient)):
         with doc.create(Itemize()) as itemize:
                 itemize.add_item("the first item")
                 itemize.add_item("the second item")
                 itemize.add_item("the third etc")
                 # you can append to existing items
                 itemize.append(Command("ldots"))


        # create a bulleted "itemize" list like the below:
        # \begin{itemize}
        #   \item The first item
        #   \item The second item
        #   \item The third etc \ldots
        # \end{itemize}

        # with doc.create(Section(theClient)):
        #     with doc.create(Itemize()) as itemize:
        #         itemize.add_item("the first item")
        #         itemize.add_item("the second item")
        #         itemize.add_item("the third etc")
        #         # you can append to existing items
        #         itemize.append(Command("ldots"))

        # create a numbered "enumerate" list like the below:
        # \begin{enumerate}
        #   \item The first item
        #   \item The second item
        #   \item The third etc \ldots
        # \end{enumerate}

        # with doc.create(Section('"Enumerate" list')):
        #     with doc.create(Enumerate()) as enum:
        #         enum.add_item("the first item")
        #         enum.add_item("the second item")
        #         enum.add_item(NoEscape("the third etc \\ldots"))

        # create a labelled "description" list like the below:
        # \begin{description}
        #   \item[First] The first item
        #   \item[Second] The second item
        #   \item[Third] The third etc \ldots
        # \end{description}

        # with doc.create(Section('"Description" list')):
        #     with doc.create(Description()) as desc:
        #         desc.add_item("First", "The first item")
        #         desc.add_item("Second", "The second item")
        #         desc.add_item("Third", NoEscape("The third etc \\ldots"))
        # doc.generate_tex('MyDoclists2')
        doc.generate_pdf('MyDoclists', clean=True, clean_tex=False,
                         compiler="pdflatex", compiler_args=None, silent=True)

class MyDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Add client")

        Label(master, text="Nom du Client:").grid(row=0)
        Label(master, text="Adresse:").grid(row=1)
        Label(master, text="Periode:").grid(row=2)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        return self.e1 # initial focus

    def apply(self):
        first = str(self.e1.get())
        second = str(self.e2.get())
        third = str(self.e3.get())
        f = open('workfile.dat', 'a')
        f.write("\n"+first+";"+second+";"+third)
        f.close()

        print ( first, second,third) # or something
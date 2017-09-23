import traceback
from Command.logger import bcolors as pp
from tkinter import *
from tkinter import font as tkFont
from datetime import datetime, date, time,timedelta
import calendar
from Bom.Client import Client


class CalendarScreen:
    def __init__(self,master,config,clientList):
        self.master=master
        self.config=config
        self.clientList = clientList
        self.listOfDueDate = {}
        self.listOfLateFact = {}
        self.listOfIncomingFact = {}
        self.buildListOfDueDate()
        self.yearMonth = ""
        self.calendarDate = datetime.now().date()
        self.detaislLabel = StringVar()
        self.activeDate=""
        self.clickDate=""
        self.clickWidget=None
        self.listPhoto = []
        self.activeFacture=None
        for widget in master.grid_slaves():
            #Don't touch the menu bar !
            if widget.widgetName !="frame":
                widget.destroy()
        try :
            self.master.nametowidget(".placeHolder").destroy()
        except Exception:
            pp.printWarning("Unable to delete placeholder ")

    def buildListOfDueDate (self) :
        today=datetime.now()
        todayDate = today.date()
        for aClient in self.clientList:
            for aFact in self.clientList[aClient].factureList:
                aDueDate=aFact.dueDate
                aDate=datetime.strptime(aDueDate, '%Y-%m-%d')
                if aDate.date() < todayDate:
                    if aDueDate in self.listOfLateFact:                    
                        self.listOfLateFact[aDueDate] = self.listOfLateFact[aDueDate]+";"+aClient
                    else :
                        self.listOfLateFact[aDueDate]=aClient
                if aDueDate in self.listOfDueDate:                    
                    self.listOfDueDate[aDueDate] = self.listOfDueDate[aDueDate]+aClient
                else :
                    self.listOfDueDate[aDueDate]=aClient

    def highlightMe(self,event):
        event.widget["bg"]="light blue"

    def hideMe(self, event):
        if event.widget.config("text")[4] != self.clickDate:
           event.widget["bg"] = "SystemWindow"

    def showDetails(self,event):
        if self.clickWidget:
            self.clickWidget["bg"] = "SystemWindow"
        self.clickDate=event.widget.config("text")[4]
        self.clickWidget=event.widget

        event.widget["bg"]="light blue"

        if len(self.clickDate)<2:
            self.clickDate=self.clickDate
        theKey=self.yearMonth+self.clickDate
        if theKey in self.listOfDueDate:
            self.detaislLabel.set(theKey+" "+self.listOfDueDate[theKey])
        else :
            self.detaislLabel.set(theKey)
        

    def drawCalendar(self,master) :
        aFakeLabel = Label(self.master, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)
        day_list = ["Er", "Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
        
        daysInCurrentMonth = calendar.monthrange(self.calendarDate.year, self.calendarDate.month)[1] + 1
        shiftValue=datetime(self.calendarDate.year, self.calendarDate.month, 1).date().weekday()

        self.yearMonth=str(self.calendarDate.year)+"-"
        month=str(self.calendarDate.month)
        if len(month) < 2:
           month="0" +month
        self.yearMonth=self.yearMonth+month+"-"
        currentWeek=int(datetime.strftime(self.calendarDate,'%W'))
        currentWeek-=1
        master.config(text= self.calendarDate.strftime('%B'))


        #Comptue number of displayable week
        maxWeek= ((daysInCurrentMonth+shiftValue)/7)
        if maxWeek>5.0:
            maxWeek=6
        maxWeek+=1
        aLabelPrevious = Label(master, text="<prec",font=myFont)
        aLabelPrevious.grid(row=0,column=0)
        aLabelPrevious.bind("<Button-1>", self.previousMonth)

        aLabelNext = Label(master, text="suiv>",font=myFont)
        aLabelNext.grid(row=0,column=1)
        aLabelNext.bind("<Button-1>", self.nextMonth)
        #Header print of calendar
        for aDay in range(1, 8):
            aLabel = Label(master, text=str(day_list[aDay]),font=myFont).grid(row=1,column=aDay)
        for aWeek in range(1,int(maxWeek)):
                aLabel=Label(master, text="w"+str(aWeek+currentWeek),font=myFont)
                aLabel.grid(row=aWeek+1,column=0)

        #Print calendar
        column = 1+shiftValue
        row = 2
        for aDay in range (1,daysInCurrentMonth):
            aLabel = Label(master, text=str(aDay),name=str(aDay))
            fullDay=str(aDay)
            if len(fullDay) < 2:
                fullDay="0"+fullDay
            fullDay=self.yearMonth+fullDay
            if aDay == self.calendarDate.day:
                aLabel = Label(master, text=str(aDay),fg="blue",font=myFont,name=str(aDay))
            elif fullDay in self.listOfDueDate:
                pp.printWarning("Find a due date "+str(aDay))
                aLabel = Label(master, text=str(aDay),fg="red",font=myFont,name=str(aDay))

            if column >7 :
                row+=1
                column=1
            aLabel.grid(row=row, column=column )
            aLabel.bind("<Button-1>", self.showDetails)
            aLabel.bind("<Enter>", self.highlightMe)
            aLabel.bind("<Leave>", self.hideMe)
            column+=1

    def previousMonth(self,event) :
        pp.printGreen("Previous")
        self.calendarDate = self.calendarDate - timedelta(days=self.calendarDate.day+1)
        self.calendarDate = self.calendarDate -timedelta(days=self.calendarDate.day-1 )
        self.drawCalendar(event.widget.master)

    def nextMonth(self,event) :
        pp.printGreen("Next")
        dayInCurrentMonth=calendar.monthrange(self.calendarDate.year, self.calendarDate.month)[1] + 1
        shiftDays=dayInCurrentMonth-self.calendarDate.day
        self.calendarDate = self.calendarDate + timedelta(shiftDays+1)
        self.drawCalendar(event.widget.master)

    def switchPaidStatus(self,event):
        print("Switch paid status")
        theClient=event.widget.master.nametowidget(".placeHolder.listboxFacs").get(ACTIVE)
        print ( "theClient="+theClient)
        print( "selectedFact "+self.activeFacture)
        for facture in self.clientList[theClient].factureList:
            if facture.dueDate == self.activeDate:
                facture.isPaid = not facture.isPaid
                self.refreshFactureDetails(None)
                print (" Facture updated")
    def drawScreen (self) :

        photo5 = PhotoImage(file="Ressources/tickAction.gif")
        nP5 = photo5.subsample(4, 4)
        w5 = Label(self.master, image=nP5, text="Payé", compound="top")
        w5.bind("<Button-1>", self.switchPaidStatus)
        w5.photo = photo5
        w5.grid(row=1, padx=20)
        #Avoid photo to be destroy by garbage collector
        self.listPhoto.append(nP5)

        placeHolder = Frame(self.master, name="placeHolder", bd=1, relief=SUNKEN,bg="white")
        placeHolder.grid(row=1,column=1,rowspan=5,columnspan=5, sticky=N)

        group = LabelFrame(placeHolder, padx=5, pady=5)
        group.grid(row=1,column=0)
        self.drawCalendar(group)

        placeHolder2 = Frame(placeHolder, name="placeHolder2",bg="white")
        placeHolder2.grid(row=1,column=1,rowspan=2,columnspan=2, sticky=N)

        aFakeLabel = Label(placeHolder, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)
        ix=1
        titleLateFact = Label(placeHolder2, name="titleLateFAct", text="Factures en retard",font=myFont).grid(row=1,column=1)
        ix=ix+1
        theDetailsLabel =Label(placeHolder2, name="theDetailsLabel", textvariable=self.detaislLabel, text=" "+str(ix)).grid(row=ix+1,column=1)
        ix=ix+1
        aLabelListFac = Label(placeHolder, text="Liste des clients").grid(row=ix+1,column=3)
        ix=ix+1
        aLabel =Label(placeHolder, text="Les factures auraient dû être payée le:",font=myFont).grid(row=ix+1,column=0)
        scrollbarDates = Scrollbar(placeHolder, orient=VERTICAL)
        listboxDates = Listbox(placeHolder, name="listDates", yscrollcommand=scrollbarDates.set)
        listboxDates.bind("<Double-Button-1>", self.refreshFactureList)
        listboxDates.grid(row=ix+1, column=1)
        scrollbarDates.config(command=listboxDates.yview)
        scrollbarDates.grid(row=ix+1, column=2, sticky=N + S,)
        for jx in self.listOfLateFact:
            listboxDates.insert(END, jx)
        self.activeDate=str(list(self.listOfLateFact.keys())[0])
        #activate the first element of the list
        ixItem=0
        for aDate in listboxDates.get(0, END):            
            if aDate == self.activeDate:
                listboxDates.activate(ixItem)
                listboxDates.select_set(ixItem)
                break            
            ixItem = ixItem + 1

        scrollbarFacs = Scrollbar(placeHolder, orient=VERTICAL)
        listboxFacs = Listbox(placeHolder, name="listboxFacs", yscrollcommand=scrollbarFacs.set)
        listboxFacs.bind("<Double-Button-1>", self.refreshFactureDetails)
        listboxFacs.grid(row=ix+1, column=3)
        scrollbarFacs.config(command=listboxFacs.yview)
        scrollbarFacs.grid(row=ix+1, column=4, sticky=N + S)

        for jx in self.listOfLateFact[self.activeDate].split(";"):
            listboxFacs.insert(END, jx)
        ix=ix+1
        aLabelDetailsFac = Label(placeHolder, text="Details de la facture:",font=myFont).grid(row=ix+1,column=0)
        listboxFactDetailsName = Listbox(placeHolder)            
        listboxFactDetailsName.insert(END, "N°")
        listboxFactDetailsName.insert(END, "Fait le")
        listboxFactDetailsName.insert(END, "Échéance")
        listboxFactDetailsName.insert(END, "Montant")
        listboxFactDetailsName.insert(END, "Payé")
        listboxFactDetailsName.grid(row=ix+1, column=1, sticky=N + S)
        listboxFactDetails = Listbox(placeHolder, name="maListeFacDetails")
        listboxFactDetails.grid(row=ix+1, column=3, sticky=N + S)



    def refreshFactureList(self,event) :
        activeElt=event.widget.get(ACTIVE)
        self.activeDate=activeElt
        theList= self.master.nametowidget(".placeHolder.listboxFacs")
        theList.delete(0, END)
        for jx in self.listOfLateFact[activeElt].split(";"):
            theList.insert(END, jx)

    def refreshFactureDetails(self,event):
        if event:
            self.activeFacture=event.widget.get(ACTIVE)
        theList= self.master.nametowidget(".placeHolder.maListeFacDetails")

        for aFact in self.clientList[self.activeFacture].factureList:
            if str(aFact.dueDate) == self.activeDate:
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

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
        self.detaislLabel = StringVar()
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
                    #pp.printWarning("A facture is late ! >>>>>>>>>"+aDueDate)
                    if aDueDate in self.listOfLateFact:                    
                        self.listOfLateFact[aDueDate]=    self.listOfLateFact[aDueDate]+";"+aClient
                    else :
                        self.listOfLateFact[aDueDate]=aClient
                if aDueDate in self.listOfDueDate:                    
                    self.listOfDueDate[aDueDate]=    self.listOfDueDate[aDueDate]+aClient
                else :
                    self.listOfDueDate[aDueDate]=aClient

    def highlightMe(self,event):
        event.widget["bg"]="light blue"

    def hideMe(self, event):
            event.widget["bg"] = "SystemWindow"

    def showDetails(self,event):
        pp.printGreen("Click on :"+str(event.widget))
        theClickedDate=event.widget.config("text")[4]
        if len(theClickedDate)<2:
            theClickedDate="0"+theClickedDate
        print("   Click on :"+theClickedDate)
        theKey=self.yearMonth+theClickedDate
        if theKey in self.listOfDueDate:
            self.detaislLabel.set(theKey+" "+self.listOfDueDate[theKey])
        else :
            self.detaislLabel.set(theKey)

    def drawCalendar(self,master):

        aFakeLabel = Label(master, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)
        


        day_list = ["Er", "Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
        today=datetime.now()
        todayDate = today.date()
        
        daysInCurrentMonth = calendar.monthrange(todayDate.year, todayDate.month)[1] + 1
        shiftValue=datetime(todayDate.year, todayDate.month, 1).date().weekday()

        self.yearMonth=str(todayDate.year)+"-"
        currentMonth=str(todayDate.month)
        if len(currentMonth) < 2:
           currentMonth="0" +currentMonth
        self.yearMonth=self.yearMonth+currentMonth+"-"
        currentWeek=int(datetime.strftime(today,'%W'))
        currentWeek-=1
        pp.printGreen("Today is :"+str(todayDate))
        master.config(text= today.strftime('%B'))


        #Comptue number of displayable week
        maxWeek= ((daysInCurrentMonth+shiftValue)/7)
        if maxWeek>5.0:
            maxWeek=6
        maxWeek+=1

        #Header print of calendar
        for aDay in range(1, 8):
            aLabel = Label(master, text=str(day_list[aDay]),font=myFont).grid(row=0,column=aDay)
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
            if aDay == todayDate.day:
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





    def drawScreen (self) :

        placeHolder = Frame(self.master, name="placeHolder", bd=1, relief=SUNKEN,bg="white")
        placeHolder.grid(row=1,column=1,rowspan=5,columnspan=5, sticky=N)
        group = LabelFrame(placeHolder, padx=5, pady=5)
        group.grid(row=1,column=0)

        self.drawCalendar(group)
        aFakeLabel = Label(placeHolder, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)

        titleLateFact = Label(placeHolder, name="titleLateFAct", text="Factures en retard", anchor=S, padx=50, pady=0,font=myFont).grid(row=1,column=1)
        ix=1
        for jx in self.listOfLateFact:
            aLabel =Label(placeHolder, text="Les factures auraient dû être payée le  "+str(jx)+" pour "+str(self.listOfLateFact[jx])).grid(row=ix+1,column=1)
            ix=ix+1
        
        titleLB = Label(placeHolder, name="titleLB", text="Prochaine échéance", anchor=S, padx=50, pady=0,font=myFont).grid(row=ix+1,column=1)
        #for kx in range (2,10):
        #    aLabel =Label(placeHolder, text="echéance "+str(ix)).grid(row=ix+1,column=1)

        ix=ix+1
        titleLB2 = Label(placeHolder, name="titleLB2", text="Détails", anchor=S, padx=50, pady=0,font=myFont).grid(row=ix,column=1)
        theDetailsLabel =Label(placeHolder, name="theDetailsLabel", textvariable=self.detaislLabel, text=" "+str(ix)).grid(row=ix+1,column=1)
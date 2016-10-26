import traceback
from Command.logger import bcolors as pp
from tkinter import *
from tkinter import font as tkFont
from datetime import datetime, date, time,timedelta
import calendar
from Bom.Client import Client
from  math import floor

class CalendarScreen:
    def __init__(self,master):
        self.master=master


        for widget in master.grid_slaves():
           # print(widget)
           # print (widget.widgetName)
            #Don't touch the menu bar !
            if widget.widgetName !="frame":
                widget.destroy()


    def drawCalendar(self,master):
        aFakeLabel = Label(master, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)

        day_list = ["Er", "Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
        todayDate = datetime.now().date()
        daysInCurrentMonth = calendar.monthrange(todayDate.year, todayDate.month)[1] + 1
        shiftValue=datetime(todayDate.year, todayDate.month, 1).date().weekday()

        pp.printGreen("Today is :"+str(todayDate))
        master.config(text= datetime.now().strftime('%B'))


        #Comptue number of displayable week
        maxWeek= ((daysInCurrentMonth+shiftValue)/7)
        if maxWeek>5.0:
            maxWeek=6
        maxWeek+=1

        pp.printGreen(str(maxWeek))

        #Header print of calendar
        for aDay in range(1, 8):
            aLabel = Label(master, text=str(day_list[aDay]),font=myFont).grid(row=0,column=aDay)
        for aWeek in range(1,maxWeek):
                aLabel=Label(master, text="w"+str(aWeek),font=myFont)
                aLabel.grid(row=aWeek+1,column=0)

        #Print calendar
        column = 1+shiftValue
        row = 2
        for aDay in range (1,daysInCurrentMonth):
            aLabel = Label(master, text=str(aDay))
            if aDay == todayDate.day:
                aLabel = Label(master, text=str(aDay),fg="red",font=myFont)
            if column >7 :
                row+=1
                column=1
            aLabel.grid(row=row, column=column )
            column+=1





    def drawScreen (self) :
        group = LabelFrame(self.master, padx=5, pady=5)
        group.grid(row=1,column=0)
        self.drawCalendar(group)
        aFakeLabel = Label(self.master, text="W" + str(1))
        myFont = tkFont.Font(font=aFakeLabel['font'])
        myFont.config(weight=tkFont.BOLD)
        titleLB = Label(self.master, name="titleLB", text="Prochaine échéance", anchor=S, padx=50, pady=0,font=myFont).grid(row=1,column=1)
        for ix in range (1,10):
            aLabel =Label(self.master, text="echéance "+str(ix)).grid(row=ix+1,column=1)

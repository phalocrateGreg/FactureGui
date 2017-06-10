import configparser
import os
import traceback
import Bom.Facture as Facture
#import Command.logger as pp
from Command.logger import bcolors as pp

class Client:
    def __init__(self,name, adress, period,mail="",city="",zipcode="",amount=0):
        self.name = name
        self.adress=adress
        self.period=period
        self.mail=mail
        self.city=city
        self.zipcode=str(zipcode)
        self.amount=amount
        self.factureList = []
        self.config = None
        self.lastFactureId=0

    def computeLastFactureId(self):
        for aFacture in self.factureList :
            if aFacture.numberId > self.lastFactureId:
                self.lastFactureId=aFacture.numberId

    def getNewFactureHandler(self):
        self.computeLastFactureId()
        return Facture.Facture(self.lastFactureId+1,self.name,None,None,self.amount)

    def loadConfig(self):
        try :
            pp.printGreen("Loading config file for client "+self.name+" ...")
            self.config = configparser.ConfigParser()
            self.config.read('./Config/'+self.name+".dat")
            section="1"
            for section in self.config.sections():
                print("[" + section + "]")
                if section != "info":
                    for key in self.config[section]:
                        print("   " + key + ":" + str(self.config[section][key]))
                    aNewFacture =  Facture.Facture (section,self.name,str(self.config[section]["editionDate"]),str(self.config[section]["dueDate"]),self.config[section]["amount"])
                   # aNewFacture = Facture.Facture(1,"Nom","2017-01-01","2017-01-01",10)
                    self.factureList.append(aNewFacture)
            self.lastFactureId=int(section)
            pp.printGreen("Done")
        except :
            pp.printError("Unable to open config file for  "+self.name)
            pp.printError(traceback.format_exc())

    def toString(self):
        return self.name+";"+self.adress+";"+self.city+";"+self.zipcode+";"+self.mail+";"+str(self.amount)+";"+self.period

    def toList(self):
        return self.toString().split(";")

    def toConfig(self,dump=False):
        config = configparser.ConfigParser()
        config["info"]={"name" : self.name,
                        "adress" :self.adress,
                        "period" :self.period,
                        "mail" : self.mail,
                        "city" : self.city,
                        "zipcode" :self.zipcode,
                        "amount" : self.amount,
                        "period" : self.period
                        }
        for facture in self.factureList:
            config[str(facture.numberId)]={
                "editionDate" : facture.editionDate,
                "dueDate" : facture.dueDate,
                "amount" : facture.amount
            }
        if dump:
            with open('./Config/'+self.name+".dat", 'w') as configfile:
                config.write(configfile)
        return config

    # def generateFacture(self):
    #     aWritter = factureWritter(self)
    #     gentime = aWritter.printFacture()
    #     self.lastFactureId+=1
    #     return gentime

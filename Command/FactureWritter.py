from pylatex import Document, Section, Itemize, Enumerate, Description,  Command, NoEscape,Figure,Package
import os
import sys
from datetime import datetime, date, time,timedelta
from Command.logger import bcolors as pp
from Bom.Facture import Facture

class FactureWritter :
    def __init__(self,aClient):
        self.client=aClient
        self.formatDate="%d/%m/%y"
        self.destination="Output\\"+aClient.name+"\\"
        if not os.path.isdir(self.destination):
            pp.printWarning("Path :"+self.destination+" does not exist")
            os.makedirs(self.destination)
        self.factureClient = Facture(self.client.lastFactureId+1,self.client.name)

    def printFacture (self):


            theSartDate=datetime.now()
            theTargetDate=theSartDate+timedelta(days=30)
            print("Début de la génération :"+str(theSartDate))
            print("TargetDate=" + str(theTargetDate))

            doc = Document()
            doc.packages.append(Package('eurosym', options=['official']))
            #doc.append(Command("title{TiLuNet}"))
            #doc.append(Command("maketitle"))

            #doc.append(Command("includegraphics","\"logo.png\""))
            image_filename =  '../../Ressources/logo.png'
            with doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image(image_filename, width='120px')

            #Company info
            doc.append(Command("quad"))
            doc.append(Command("newline"))
            doc.append("FIDEL Lucette")
            doc.append(Command("newline"))
            doc.append("139 avenue Corniche Fleurie")
            doc.append(Command("newline"))
            doc.append("06200 NICE")
            doc.append(Command("newline"))
            doc.append(Command("underline","SIRET"))
            doc.append("52148565600016")

            #
            with doc.create(Section("FACTURE N "+str(theSartDate.year)+"-"+str(self.client.lastFactureId+1),False)):
                doc.append("Émise le "+str(theSartDate.date().strftime(self.formatDate)) + ", à payer le " + theTargetDate.date().strftime(self.formatDate))
                doc.append(Command("newline"))

                doc.append(Command("begin","center"))
                doc.append(Command( "begin","bfseries"))
                doc.append(self.client.name)
                doc.append(Command("newline"))
                doc.append(self.client.adress)
                doc.append(Command("newline"))
                doc.append(Command("end", "bfseries"))
                doc.append(Command("end", "center"))

                #doc.append("Total HT" + Command("dotfill") + "291 €")
                doc.append("Total HT")
                doc.append( Command("dotfill"))
                doc.append( "291")
                doc.append(Command("euro",""))
                doc.append(Command("newline"))
                doc.append(Command("begin", "flushright"))
                doc.append("TVA 20% ")
                doc.append(Command("hspace","1cm"))
                doc.append("51")
                doc.append(Command("euro", ""))
                doc.append(Command("end", "flushright"))

                doc.append(Command("begin","bfseries"))
                doc.append("TOTAL DE LA FACTURE TTC")
                doc.append(Command("dotfill"))
                doc.append("242 ")
                doc.append(Command("euro",""))
                doc.append(Command("end", "bfseries"))
                doc.append(Command("newline"))

            doc.generate_pdf(self.destination+'Facture_'+self.client.name+"-"+str(self.client.lastFactureId+1), clean=True, clean_tex=False,
                             compiler="pdflatex", compiler_args=None, silent=True)

            theEndDate=datetime.now()
            print("Fin de la génération :"+str(theEndDate))
            self.client.lastFactureId+=1
            genTime=theEndDate-theSartDate
            print ("Temps de gen="+str(genTime))
            self.client.factureList.append(self.factureClient)
            return  genTime

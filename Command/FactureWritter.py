from pylatex import Document, Section, Itemize, Enumerate, Description,  Command, NoEscape,Figure,Package
import os
from datetime import datetime, date, time,timedelta
from Bom.Client import Client

class FactureWritter :
    def __init__(self,aClient):
        self.client=aClient
        self.formatDate="%d/%m/%y"

    def printFacture (self):


            theSartDate=datetime.now()
            theTargetDate=theSartDate+timedelta(days=30)
            print("Début de la génération :"+str(theSartDate))
            print("TargetDate=" + str(theTargetDate))

            doc = Document()
            doc.packages.append(Package('eurosym', options=['official']))

           
            #image_filename =  '../logo.png'
            #with doc.create(Figure(position='h!')) as kitten_pic:
            #    kitten_pic.add_image(image_filename, width='120px')

            #Company info


            #
            with doc.create(Section("FACTURE N "+str(theSartDate.year)+"-",False)):
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

            doc.generate_pdf('Output\\Facture_'+self.client.name, clean=True, clean_tex=False,
                             compiler="pdflatex", compiler_args=None, silent=True)

            theEndDate=datetime.now()
            print("Fin de la génération :"+str(theEndDate))
            genTime=theEndDate-theSartDate
            print ("Temps de gen="+str(genTime))
            return  genTime
from datetime import datetime, date, time,timedelta


class Facture:

     def __init__(self,numberId,clientName,editionDate=None,dueDate=None,amount=0,isPaid=False):
        self.numberId=numberId
        self.clientName = clientName
        if editionDate is None :
            self.editionDate = datetime.now().date()
        else :
            self.editionDate = editionDate

        if dueDate is None:
            self.dueDate = self.editionDate+timedelta(days=30)
        else :
            self.dueDate= dueDate

        self.amount=amount
        self.isPaid=False

     def toString(self):
         print ("Facture :"+str(self.numberId))
         print (self.clientName)
         print (self.editionDate)
         print (self.dueDate)
         print(self.amount)
         print(self.isPaid)





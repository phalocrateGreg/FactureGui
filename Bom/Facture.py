from datetime import datetime, date, time,timedelta

class Facture:

     def __init__(self,numberId,clientName,editionDate=None,dueDate=None,amount=0):
        self.numberId=numberId
        self.clientName = clientName
        if editionDate is None :
            self.editionDate = datetime.now().date()
        else :
            self.editionDate = editionDate

        if dueDate is None:
            self.dueDate = editionDate+timedelta(days=30)
        else :
            self.dueDate= dueDate
        self.amount=amount




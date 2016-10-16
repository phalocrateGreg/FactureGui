class Client :
    def __init__(self,name, adress, period,mail="",city="",zipcode="",amount=0):
        self.name = name
        self.adress=adress
        self.period=period
        self.mail=mail
        self.city=city
        self.zipcode=str(zipcode)
        self.amount=amount

        print ("==§§ "+self.toString())

    def toString(self):
        print ("#####")
        print (self.name+";"+self.adress+";"+self.city+";"+self.zipcode+";"+self.mail+";"+str(self.amount)+";"+self.period)
        print ("#####")
        return self.name+";"+self.adress+";"+self.city+";"+self.zipcode+";"+self.mail+";"+str(self.amount)+";"+self.period

    def toList(self):
        return self.toString().split(";")
import sys
#Use :
#from logger import bcolors
#bcolors.printGreen("Hello "+options.user)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    NICEBYELLOW = '\033[33;5m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def printGreen(mess):
        print (bcolors.OKGREEN+mess+bcolors.ENDC)

    @staticmethod
    def printError(mess):
         print (bcolors.FAIL+str(mess)+bcolors.ENDC)

    @staticmethod
    def printWarning(mess):
         print (bcolors.WARNING+mess+bcolors.ENDC)

    @staticmethod
    def staticPrint(mess):
        sys.stdout.write("\r"+str(mess))
        sys.stdout.flush()

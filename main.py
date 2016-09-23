from tkinter import *
from tkinter import simpledialog
# from PIL import Image, ImageTk
from Screen.ClientSCreen import ClientSCreen






def showOtherSCreen (event):
    print ("hello")



    master=event.widget.master.master
    for widget in master.grid_slaves() :
        widget.destroy()

    w = Spinbox(master, from_=0, to=10)
    w.pack()


##################
# Main code
#####################
root = Tk()
root.title("Mine")

#toplevel = root.winfo_toplevel()
#toplevel.wm_state('zoomed')

#print ("maxX="+str(root.winfo_screenwidth())+" "+str(root.winfo_screenheight()))



#aDiag=simpledialog.Dialog
# app = App(root)




#Menu bar
rowIndex=0
separator = Frame(bd=1, relief=SUNKEN,bg="red")
separator.grid(row=rowIndex,columnspan=2,sticky=W+E)

photo0 = PhotoImage(file="Client.gif")
nP0=photo0.subsample(6,6)
w0 = Label(separator, image=nP0, compound="top")
#w0.bind("<Button-1>", callbackAdd)
w0.photo = photo0
#w.pack(fill=BOTH,expand="true")
w0.grid(row=rowIndex,column=0)

photo00 = PhotoImage(file="30143-xsara54-Parametres.gif")
nP00=photo00.subsample(6,6)
w00 = Label(separator, image=nP00, compound="top")
w00.bind("<Button-1>", showOtherSCreen)
w00.photo = photo00
#w.pack(fill=BOTH,expand="true")
w00.grid(row=rowIndex,column=1)



#test = MyDialog(root)

#for i in myContainer1.pack_slaves():
#    print (str(i))



myScreen=ClientSCreen(root)
listPhoto=myScreen.drawScreen()
#myContainer1.pack()
root.mainloop()

#root.destroy()  # optional; see description below

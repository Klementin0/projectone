from tkinter import *

root = Tk() # Root word main Tk()

topFrame = Frame(root) # topFrame van Root aanmaken
topFrame.pack() #Plaats topFrame in de window
bottomFrame = Frame(root) #bottomFrame van root aanmaken
bottomFrame.pack(side=BOTTOM) #bottomFrame aan de onderkant van de window toevoegen

button1 = Button(topFrame, text="knoppie", fg="black") #button1 word een nieuwe button, word geplaats in het topFrame, bevat de text "knoppie" en is van de kleur "Black"


button1.pack() #Plaats de button in het window


root.mainloop() #Zorg er voor dat de window niet in een keer weggaat door er een loop van te maken.

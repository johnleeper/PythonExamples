import tkinter
import webbrowser
from functools import partial 
from tkinter import *
from tkscrolledframe import ScrolledFrame

def contAssign(contChoice):
    global continentValue
    continentValue = contChoice
#    print("continentValue = ", continentValue)

def minAgeAssign(minagechoice):
    global minAgeValue
    minAgeValue = minagechoice
#    print("minAgeValue = ", str(minAgeValue))

def maxAgeAssign(maxageChoice):
    global maxAgeValue
    maxAgeValue = maxageChoice
#    print("maxAgeValue = ", str(maxAgeValue))

def famAssign(famChoice):
    global familyValue
    familyValue = famChoice
#    print("familyValue = ", familyValue)

def ageConflict():
    print("minimum age greater than maximum age - no selection possible!")

def buttonSearch():
    for widget in resultsFrame.winfo_children():
        widget.destroy() ## Clears previous answers from the resultsFrame
    selectedList = []

    print("Values are: continent = " + continentValue + "; family = " + familyValue
          + "; min age = " + str(minAgeValue) + "; max age = "+ str(maxAgeValue))
    print("List is ", len(dinoList), "long")
    for dino in dinoList:
        selected = True
        if continentValue != ''and continentValue != dino[1]:
            selected = False
            print("rejected " + dino[0] + " due to continent")
        if minAgeValue > maxAgeValue:
            ageConflict()
        elif minAgeValue != 0 and minAgeValue > dino[2]:
            selected = False
            print("rejected " + dino[0] + " due to minAge")
        elif maxAgeValue != 0 and maxAgeValue < dino[2]:
            selected = False
            print("rejected " + dino[0] + " due to maxAge")
        if familyValue != '' and familyValue != dino[3]:
            selected = False
            print("rejected " + dino[0] + " due to family")
        if selected == True:
            selectedList.append(dino)
            print(dino)
    #print(selectedList)
    for line in selectedList:
        lineFrame = Frame(resultsFrame)
        linetxt = line[0] + " " + line[1] + " " + str(line[2]) + " " + line[3]
        lineLabel = Label(lineFrame, text=linetxt)
        # print("line text = ", linetxt)
        webButtonCommand = partial(webLinker, line[4])
        # partial is required to pass argument with button command - command: weblinker(line[4]) runs immediately when program starts
        webLink = Button(lineFrame, text='Wiki Link', fg ="blue", command= webButtonCommand)
        lineLabel.pack()
        webLink.pack()
        lineFrame.pack()
    print("resultsFrame packed")

def webLinker(linkText):
    linkText = linkText.rstrip()
    webbrowser.open_new(linkText)
    

# Getting data from text file
FH = open('dinodata2.txt', 'r')
dinoList = []
continentSet = set()
familySet = set()
ageSet = set()
for line in FH:
    splitLine = line.split(', ')
    splitLine[2] = int(splitLine[2])
    dinoList.append(splitLine)
    # Generating Lists
    continentSet.add(splitLine[1])
    familySet.add(splitLine[3])
    ageSet.add(splitLine[2])
FH.close()
continentList = list(continentSet)
continentList.sort()
continentList.append('')
ageList = list(ageSet)
ageList.sort()
#ageList.append('')
familyList = list(familySet)
familyList.sort()
familyList.append('')

continentValue = '' # setting default values for search because if 
minAgeValue = 0     # the widget is not used, the value is not set
maxAgeValue = 0
familyValue = ''
    
# Tkinter GUI
# Hierarchy: root -> sframe (scrolling frame) -> dispframe (display frame)
# dispFrame -> continentFrame
#           -> ageFrame
#           -> familyFrame
#           -> resultsFrame
root = tkinter.Tk()
root.title('Dinosaur lister')
#bar = Scrollbar(root)
#bar.pack(side = RIGHT, fill = Y, expand = True)  # fill = Y and expand = True needed for scrollbar to work
sframe = ScrolledFrame(root, width=400, height=500)
sframe.pack(side="top", expand=1, fill="both")
sframe.bind_arrow_keys(root)
sframe.bind_scroll_wheel(root)
dispFrame = sframe.display_widget(Frame)
continentchoice = tkinter.StringVar()
continentchoice.set('')
continentFrame = Frame(dispFrame)
continentLabel = Label(continentFrame, text='Which Continent?')
continentLabel.pack()
continentDropdown = tkinter.OptionMenu(continentFrame,
                                       continentchoice, '', *continentList, command=contAssign)
continentDropdown.pack()
continentFrame.pack()

ageFrame = Frame(dispFrame)
minAgeChoice = tkinter.IntVar()
minAgeChoice.set(0)
minAgeLabel = Label(ageFrame, text='Minimum Age (Millions of years)?')
minAgeLabel.pack()
minAgeDropdown = tkinter.OptionMenu(ageFrame, minAgeChoice, 0, *ageList, command=minAgeAssign)
minAgeDropdown.pack()

maxAgeChoice = tkinter.IntVar()
maxAgeChoice.set(0)
maxAgeLabel = Label(ageFrame, text='Maximum Age (Millions of years)?')
maxAgeLabel.pack()
maxAgeDropdown = tkinter.OptionMenu(ageFrame, maxAgeChoice, 0, *ageList, command=maxAgeAssign)
maxAgeDropdown.pack()
ageFrame.pack()

familyFrame = Frame(dispFrame)
familyChoice = tkinter.IntVar()
familyChoice.set('')
famLabel = Label(familyFrame, text='What Family?')
famLabel.pack()
famDropdown = tkinter.OptionMenu(familyFrame, familyChoice, '', *familyList, command=famAssign)
famDropdown.pack()
familyFrame.pack()

searchButton = tkinter.Button(root, text='Search', command=buttonSearch)
searchButton.pack()

resultsFrame = Frame(dispFrame)
resultsFrame.pack()

root.mainloop()

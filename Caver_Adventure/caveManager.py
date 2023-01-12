import sqlite3

def addtoTable():
    tableCount = 0
    for table in tableList:
        print(str(tableCount) + ") " + table)
        tableCount +=1
    tableChoice = input("Number of table for input? ")
    if tableChoice.isdigit() and int(tableChoice) <= tableCount:
        table = tableList[int(tableChoice)]
        print(table + " has been selected")
    else:
        print("Sorry, not a valid number choice")
        return
    

def getPrimaryKey(table):
    curs.execute("PRAGMA table_info("+table+");")
    pragmaDump = curs.fetchall()
    primKey = ""
    for column in pragmaDump:
        if column[5] == 1:
            primKey = column[1]
    return primKey
                             

def mainMenu():
    for table in tableList:
        primKey = getPrimaryKey(table)
        curs.execute("SELECT COUNT(" + primKey + ") FROM " + table + ";")
        recordCount = curs.fetchone()[0]
        print(table + " has " + str(recordCount) + " records")

    print("Main menu")
    print("W) Walkthrough")
    print("E) Edit entry in table")
    print("A) Add to table")
    print("Q) Quit this program")

    mainChoice = input("? ").upper()
    if mainChoice == "A":
        addtoTable()
    elif mainChoice == "E":
        editEntry()
    elif mainChoice == "Q":
        carryOn = False
        print("Quitting")
        return carryOn

print("Welcome to caver adventure game database manager")

databaseFolder = "..\\..\\SQLite\\databases\\caver03.db"
conn = sqlite3.connect(databaseFolder)
curs = conn.cursor()
tableList = ["creature", "location", "item"]
# Although I could do a SELECT schema, this program is for a specific database

carryOn = True
while carryOn == True:
    print("CarryOn = ", carryOn)
    carryOn = mainMenu()

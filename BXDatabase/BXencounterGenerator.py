import sqlite3
import random

def getHabList():
    cursor.execute("SELECT DISTINCT habitat FROM monsterhabitat")
    habDump = cursor.fetchall()
    habList = []
    for row in habDump:
        habList.append(row[0])
    habList.sort()
    return habList

conn = sqlite3.connect('../../SQLite/databases/BXData.db')
cursor = conn.cursor()

print("BX Encounter Generator! ")
habList = getHabList()
print(habList)
habChoice = input("Selected Habitat: ")
if habChoice in habList:
    print("Good Choice: "+ habChoice)
else:
    print("Sorry, "+habChoice+ " is not a good choice")
minCR = input("Minimum Challenge Rating: ")
maxCR = input("Maximum Challenge Rating: ")

if minCR == "":
    minCRint = 0
else:
    minCRint = int(minCR)
if maxCR == "":
    maxCRint = 100
else:
    maxCRint = int(maxCR)

query = 'SELECT basic.monname FROM monsterbasic AS basic JOIN monsterhabitat AS hab ON basic.monname = hab.monname WHERE basic.CR >= '+ str(minCRint)+ ' AND basic.CR <= '+ str(maxCRint) + ' AND hab.habitat = "'+habChoice+'"'
print(query)
cursor.execute(query)
resultDump = cursor.fetchall()
if len(resultDump) < 1:
    print("Sorry, no results found")
else:
    for row in resultDump:
        print(row[0])

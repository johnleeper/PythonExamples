import sqlite3
# functions should be kept in alphabetical order for ease of finding/editing

def abilsEdit(monsterName):
    abilChoice = ""
    while abilChoice != "Q":
        cursor.execute('SELECT * FROM monsterspecabil WHERE monName ="' + monsterName + '" ORDER BY specabilname')
        abilDump = cursor.fetchall()
        abilNameList = []
        if len(abilDump) > 0:
            print("Special abilities for "+ monsterName)
            abilCount = 0
            for abilTup in abilDump:
                print(str(abilCount) +') '+ abilTup[1] + ":: "+ abilTup[2])
                abilNameList.append(abilTup[1])
                abilCount += 1
        else:
            print(monsterName + " has no special abilities yet")
        abilChoice = input("Add (A) new ability, Delete (D) existing ability or Quit (Q): ").upper()
        if abilChoice == "A":
            abilidList = []
            cursor.execute("SELECT abilid FROM monsterspecabil")
            abilidDump = cursor.fetchall()
            for abilidTup in abilidDump:
                abilidList.append(abilidTup[0])
            abilidList.sort()
            if len(abilidList) > 0:
                newAbilid = abilidList[-1] +1
            else:
                newAbilid = 1
            newAbilName = input("New Ability Name: ")
            newAbilName = sanitizeString(newAbilName)
            if newAbilName in abilNameList:
                print("Sorry, that ability already exists for "+ monsterName)
                continue
            else:
                newAbilDesc = input("New Ability Description: ")
                newAbilDesc = sanitizeString(newAbilDesc)
                query = 'INSERT INTO monsterspecabil (monName, specabilname, specabildesc, abilid) values ("' + monsterName + '", "' + newAbilName + '", "' + newAbilDesc + '", '+str(newAbilid) +')'
                try:
                    cursor.execute(query)
                    cursor.execute('COMMIT')

                except:
                    print("Something went wrong: ")
                    print(query)
        elif abilChoice == "D" and len(abilDump) > 0:
            delChoice = input("Enter number of ability from list above to delete: ")
            try:
                delquery = 'DELETE FROM monsterspecabil WHERE abilid = ' + abilDump[int(delChoice)][3]
                cursor.execute(delquery)
                cursor.execute('COMMIT')
            except:
                print("Something went wrong")
        elif abilChoice == "Q":
            print("Quitting ability edit mode")
            continue
        else:
            print("Choice not valid")       
        
    return

def attackEdit(monsterName):
    attEditChoice = ""
    while attEditChoice != "Q":
        cursor.execute('SELECT * FROM monsterattack WHERE monName = "' + monsterName + '"')
        attDump = cursor.fetchall()
        print("Current attacks for "+ monsterName + " are: ")
        attCount = 0
        for att in attDump:
            print(str(attCount) + ") " + att[1] + " for " + att[2] + "  Avg: "+ str(att[3]) +" THAC0: "+ str(att[4]) + " (monster: "+ att[0] + ", attId: "+ str(att[5])+")")
            attCount += 1
        attEditChoice = input("Add new (A), Delete existing (D), Edit existing (E) or Quit (Q) ? ").upper()
        if attEditChoice == "A":
            newAttId = 1
            cursor.execute('SELECT attackid FROM monsterattack')
            attIdDump = cursor.fetchall()
            attIdList = []
            for attId in attIdDump:
                try: 
                    attIdList.append(attId[0])
                except:
                    print("Problem selecting existing attack ids")
            if len(attIdList) > 0:
                attIdList.sort()
                newAttId = attIdList[-1] +1
            attName = input("Attack name: ")
            thac0 = input("THAC0 (integer): ")
            damDice = input("Damage Dice: ")
            avgDam = input("Average damage (integer): ")
            query = 'INSERT INTO monsterattack (monName, attackname, damage, avgdamage, THAC0, attackId) VALUES("'+monsterName+'", "'+attName+'", "'+damDice+'", '+avgDam+', '+thac0+ ', '+str(newAttId)+')'
            try:
                cursor.execute(query)
                cursor.execute('COMMIT')
            except:
                print("Problem trying to run ")
                print(query)
        elif attEditChoice == "D":
            delChoice = input("Please enter number for attack from list above: ")
            #print(attDump[int(delChoice)])
            delAtt = attDump[int(delChoice)]
            print("Selected attack ID: "+ str(delAtt[5]))
            delQuery = 'DELETE FROM monsterattack WHERE attackid = '+ str(delAtt[5])
            try:
                cursor.execute(delQuery)
                cursor.execute('COMMIT')
            except:
                print("Sorry, something went wrong, Tried running: ")
                print(delQuery)

def editMonster(monsterName):
    fieldChoice = ""
    while fieldChoice != "q":
        print("Now editing " + monsterName)
        print("The following fields are available to edit: ")
        fieldDict = {"Monster Name": ("monName", "special"),
                     "Source": ("source", "text"),
                     "Monster Type": ("montype", "text"),
                     "Armour Class": ("ac", "int"),
                     "Hit Dice": ("HD", "int"),
                     "hp modifier": ("hpmod", "int"),
                     "Movement": ("movement", "text"),
                     "Attacks": ("", "special"),
                     "Special Abilities": ("", "special"),
                     "Morale": ("morale", "int"),
                     "Save As": ("saveAs", "text"),
                     "Treasure": ("treasure", "text"),
                     "Alignment": ("align", "text"),
                     "Intelligence": ("intelligence", "int" ), 
                     "XP Value": ("XPValue", "int"),
                     "Challenge Rating": ("cr", "int"),
                     "Habitats": ("", "special") 
            }
        fieldList = ["Monster Name", "Source", "Monster Type", "Armour Class",
                     "Hit Dice", "hp modifier", "Movement", "Attacks",
                     "Special Abilities", "Morale", "Save As", "Treasure",
                     "Alignment", "Intelligence", "XP Value", "Challenge Rating",
                     "Habitats"]
        fieldCount = 0
        subtableDict = {"Attacks":("monsterattack", "attackname") ,
                        "Special Abilities":("monsterspecabil", "specabilname"),
                        "Habitats":("monsterhabitat", "habitat")}
        for field in fieldList:
            fieldStr = ""
            if fieldDict[field][1] in ("text", "int"):
                cursor.execute('SELECT '+fieldDict[field][0] +' FROM monsterbasic WHERE monname = "'+ monsterName +'"')
                datum = cursor.fetchall()[0][0]
                if datum == None:
                    fieldStr = "None"
                else:
                    fieldStr = str(datum)
            elif field in ("Attacks", "Special Abilities", "Habitats"):
                summaryQuery = 'SELECT '+subtableDict[field][1]+' FROM '+subtableDict[field][0]+ ' WHERE monname = "'+monsterName +'"'
                try:
                    cursor.execute(summaryQuery)
                    summaryDump = cursor.fetchall()
                    fieldStr = ""
                    for row in summaryDump:
                        fieldStr += row[0] + ", "
                except:
                    print("Something went wrong with " + summaryQuery)
            print(str(fieldCount) + ") " + field + " :: " + fieldStr)
            fieldCount += 1
        print("Q to quit")
        
        fieldChoice = input("? ")
        if fieldChoice in ("q", "Q"):
            print("Quitting editing mode")
            continue
        else:
            try:
                fieldChoice = int(fieldChoice)
            except:
                print("Invalid choice: " + fieldChoice)
                continue
            fieldSelect = fieldDict[fieldList[fieldChoice]] 
        if fieldSelect[1] == "text":
            textFieldEdit(monsterName, fieldSelect[0])
        elif fieldSelect[1] == "int":
            intFieldEdit(monsterName, fieldSelect)
        elif fieldSelect[1] == "special":
            if fieldList[fieldChoice] == "Attacks":
                attackEdit(monsterName)
            elif fieldList[fieldChoice] == "Habitats":
                habitatsEdit(monsterName)
            elif fieldList[fieldChoice] == "Special Abilities":
                abilsEdit(monsterName)
            elif fieldList[fieldChoice] == "Monster Name":
                nameEdit(monsterName)
            else:
                print("Problem occured")
        else:
            print("Sorry, input not recognised")

def filterMonList():
    print("Filterable fields for monsters include Source (S), Challenge rating (C), Type (T) ")
    filterChoice = input("Enter choices on one line: ").upper()
    filterquery = 'SELECT monName FROM monsterbasic WHERE monsterid > 0 '
    if 'S' in filterChoice:
        print("Existing sources: " + str(sourceList()))
        sourceSearch = input("Source: ")
        filterquery += ' AND source = "' + sourceSearch + '"'
    if 'C' in filterChoice:
        chalChoice = input("Challenge Rating (integer): ")
        filterquery += 'AND cr = ' + chalChoice
    if 'T' in filterChoice:
        print("Existing types: "+ str(typeList()))
        typeChoice = input("Monster type: ")
        filterquery += ' AND montype = "' + typeChoice + '"'
    filterquery += ' ORDER BY monName;'
    try:
        cursor.execute(filterquery)
        filterResult = cursor.fetchall()
        if len(filterResult) == 0:
            print("Sorry, no results found")
        else:
            for monsterTup in  filterResult:
                print(monsterTup[0])
    except:
        print("Sorry, something went wrong")
        print(filterquery)

def habitatsEdit(monsterName):
    cursor.execute('SELECT DISTINCT habitat FROM monsterhabitat')
    fullHabDump = cursor.fetchall()
    cursor.execute('SELECT habitat, habId FROM monsterhabitat WHERE monName = "' + monsterName + '"')
    specHabDump = cursor.fetchall()
    cursor.execute('SELECT habId FROM monsterhabitat')
    idDump = cursor.fetchall()
    idList = []
    print("FullHabDump = ", fullHabDump) ## diagnostic
    fullHabList = []
    if len(fullHabDump) == 0:
        print("No habitats for any monster listed yet")
        maxId = 0
    else:
        #fullHabString = "All habitats: "
        for habTup in fullHabDump:
            #fullHabString += habTup[0] + ", "
            fullHabList.append(habTup[0])
        for idTup in idDump:
            idList.append(idTup[0])
            idList.sort()
            maxId = idList[-1]
        fullHabList.sort()
        fullHabString = "All Habitats:" +", ".join(fullHabList)
        print(fullHabString)
            
            
    print("specHabDump = ", specHabDump) ## diagnostic
    specHabList = []
    if len(specHabDump) == 0:
        print("No habitats for " + monsterName)
    else:
        specHabString = "habitats for "+ monsterName + ": "
        for habTup in specHabDump:
            specHabList.append(habTup[0])
            specHabString += habTup[0] + ", "
        print(specHabString)
    habEdChoice = ""
    while habEdChoice != "Q":
        habEdChoice = input("Add new (A), Delete (D) or Quit (Q): ").upper()
        if habEdChoice == "A":
            newHab = input("New habitat: ").lower()
            newHab = sanitizeString(newHab)
            newId =1
            if len(idList) > 0:
                idList.sort()
                newId = maxId +1
                maxId = newId
            if newHab in specHabList:
                print("Sorry, same habitat exists for "+ monsterName)
            elif newHab not in fullHabList:
                confirmNew = input("Add completely new habitat (Y/N)? ").upper()
                if confirmNew != "Y":
                    break
                else:
                    try:
                        cursor.execute('INSERT INTO monsterHabitat (monName, habitat, habId) values("'+monsterName+'", "'+newHab+'", '+str(newId)+')')
                        cursor.execute('COMMIT')
                    except:
                        print("Sorry, something went wrong")
            else:
                print('INSERT INTO monsterHabitat (monName, habitat, habId) values("'+monsterName+'", "'+newHab+'", '+str(newId)+')')
                try:
                    
                    cursor.execute('INSERT INTO monsterHabitat (monName, habitat, habId) values("'+monsterName+'", "'+newHab+'", '+str(newId)+')')
                    cursor.execute('COMMIT')
                except:
                    print("Sorry, something went wrong")
                    
        elif habEdChoice == "D":
            specHabDict = {}
            for specHabTup in specHabDump:
                specHabDict[specHabTup[1]] = specHabTup[0]
                print(specHabTup[1], ")", specHabTup[0])
            delChoice = input("Which ID to delete:  ")
            if int(delChoice) in specHabDict.keys():
                try:
                    cursor.execute('DELETE FROM monsterhabitat WHERE habId =' + delChoice)
                    cursor.execute('COMMIT')
                except:
                    print("Sorry, something went wrong")
            else:
                print("Sorry, selection not recognised")
    return
            
def habitatView():
    habitatList =[]
    cursor.execute('SELECT DISTINCT habitat from monsterhabitat')
    habDump = cursor.fetchall()
    for habTup in habDump:
        habitatList.append(habTup[0])
    habitatList.sort()
    print("Current habitats are: " + ", ".join(habitatList))
    habChoice = input("Which habitat do you want to view (or Q to quit)? ")
    if habChoice in habitatList:
        habQuery = 'SELECT monName FROM monsterhabitat WHERE habitat = "'+habChoice+'"'
        print(habQuery)
        cursor.execute(habQuery)
        inhabitantDump = cursor.fetchall()
        inhabList = []
        for inhabTup in inhabitantDump:
            inhabList.append(inhabTup[0])
        inhabList.sort()
        print(", ".join(inhabList))
    elif habChoice in ["Q", "q"]:
        print("Quitting habitat mode")
    else:
        print("Sorry, not recognised")
    return

def intFieldEdit(monName, field):
    dataEntry = input("New " + field[0] + " for "+ monName +" (integer)? ")
    updateString = ""
    try:
        dataEntry = str(int(dataEntry))
        updateString = 'UPDATE monsterbasic SET '+ field[0] +'='+ dataEntry + ' WHERE monname = "' + monName + '"'
        cursor.execute(updateString)
        cursor.execute('COMMIT')
    except:
        if updateString != "":
            print("Sorry, something went wrong with " + updateString)
        else:
            print("Sorry, cannot use that as integer")
    return                

def listmonsters():
    nameList = monsterNameList()
    print("There are " + str(len(nameList)) + " monsters. List all (A), filter (F) or quit (Q)? ")
    listChoice = input("? ").upper()
    if listChoice == "A":
        for name in nameList:
            print(name)
    elif listChoice == "F":
        #print("Working on that") ## to be done
        filterMonList()
    elif listChoice == "Q":
        return

def monsterNameList():
    cursor.execute('SELECT monName FROM monsterbasic')
    nameDump = cursor.fetchall()
    nameList = []
    for nameTup in nameDump:
        nameList.append(nameTup[0])
    nameList.sort()
    return nameList

def nameEdit(monsterName):
    print("Changing name of " + monsterName + ", this will affect multiple tables")
    revName = input("Please enter corrected name of monster: ")
    monNameList = monsterNameList()
    if revName in monNameList:
        print("Sorry, that name already exists. Name must be unique")
    else:
        try:
            basicUpdate = 'UPDATE monsterbasic SET monName = "'+revName +'" WHERE monName = "' + monsterName + '"'
            cursor.execute(basicUpdate)
            print("basic update done")
            attackUpdate = 'UPDATE monsterattack SET monName = "'+revName +'" WHERE monName = "' + monsterName + '"'
            cursor.execute(attackUpdate)
            print("attack update done")
            specAbilUpdate = 'UPDATE monsterspecabil SET monName = "'+revName +'" WHERE monName = "' + monsterName + '"'
            cursor.execute(specAbilUpdate)
            print("specabil update done")
            habUpdate = 'UPDATE monsterhabitat SET monName = "'+revName +'" WHERE monName = "' + monsterName + '"'
            cursor.execute(habUpdate)
            print("habitat update done")
            cursor.execute('COMMIT')
        except:
            print("Sorry, something went wrong")
    return
# newmonster() only establishes monName and monsterid
def newmonster():
    print("Creating new monster for database")
    monsterid = 1
    cursor.execute('SELECT monsterid, monname FROM monsterbasic')
    idDump = cursor.fetchall()
    idList = []
    monNameList = []
    if len(idDump) > 0:
        for idx in idDump:
            idList.append(idx[0])
            monNameList.append(idx[1])
        idList.sort()
        monsterid = idList[-1] +1 # should be 1 more than the biggest current id
    monName = input("New monster name: ").title()
    monName = sanitizeString(monName)
    if monName in monNameList:
        cursor.execute('SELECT id FROM monsterbasic WHERE monName = "'+ monName+'"')
        specificIdDump = cursor.fetchall()
        specId = specificIdDump[0][0]
        print(monName + " already exists, id =" + str(specId))
        return
    else:
        cursor.execute('INSERT into monsterbasic (monsterid, monName) values('+ str(monsterid) + ', "' + monName + '")')
        cursor.execute('COMMIT')
    editChoice = input("Continue in edit mode (Y/N)? ")
    if editChoice.upper() == "Y":
        editMonster(monName)
    return

def sanitizeString(suspectString):
    if "'" in suspectString:
        suspectString = suspectString.replace("'", "^")
    if '"' in suspectString:
        suspectString = suspectString.replace('"', '^^')
    if ";" in suspectString:
        suspectString = suspectString.replace(";", ":")
    return suspectString

def sourceList():
    cursor.execute("SELECT DISTINCT source FROM monsterbasic ORDER BY source;")
    sourceDump = cursor.fetchall()
    sourceList = []
    for row in sourceDump:
        sourceList.append(row[0])
    return sourceList

def textFieldEdit(monName, field):
    print("DB field: " + field)
    cursor.execute('SELECT DISTINCT '+field+' FROM monsterbasic ORDER BY '+ field)
    fieldDump = cursor.fetchall()
    ## print("SuggestionDump: " + str(fieldDump)) ## diagnostic
    suggestList = []
    for datum in fieldDump:
        if datum[0] != None:
            suggestList.append(datum[0])
    print(suggestList)  ## diagnostic
    if len(suggestList) > 0 and len(suggestList) < 10 and suggestList[0] != None: ## 
        suggestCount =0
        for suggest in suggestList:
            suggestCount +=1
            print(str(suggestCount) + ") " + suggest)
        dataEntry = input("New " + field + " for "+ monName +"? ")
        if dataEntry in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            dataEntry = suggestList[int(dataEntry) -1]
    else: 
        dataEntry = input("New " + field + " for "+ monName +" (text) ? ")
        dataEntry = sanitizeString(dataEntry)
    try:
        updateString = 'UPDATE monsterbasic SET '+ field +'="'+ dataEntry + '" WHERE monname = "' + monName + '"'
        cursor.execute(updateString)
        cursor.execute('COMMIT')
    except:
        print("Sorry, something went wrong with " + updateString)
    return
    
def typeList():
    cursor.execute("SELECT DISTINCT montype FROM monsterbasic  ORDER BY montype;")
    typeDump = cursor.fetchall()
    typeList = []
    for row in typeDump:
        typeList.append(row[0])
    return typeList

def viewMonster():
    monsterRequest = input("Name of monster? ").title()
    nameList = monsterNameList()
    if monsterRequest in nameList:

        cursor.execute('SELECT * FROM monsterbasic WHERE monName = "' + monsterRequest + '"')
        monDump = cursor.fetchall()
        monRow = monDump[0]
        ##print(monRow)
        fieldList = ["Monster name: ", "Armour Class: ", "Hit Dice: ", "Hitpoint Mod: ", "Alignment: ", "XP Value: ", "Morale: ", "Monster Type: ", "Movement: ", "Intelligence: ", "Save As: ", "Source: ", "Challenge: ", "ID: ", "Treasure: "]

        fieldCount = 0
        for monCol in monRow:
            if monCol is None:
                formatCol = "None"
            elif isinstance(monCol, int):
                formatCol = str(monCol)
            else:
                formatCol = monCol
            spacing = " " * (14- len(fieldList[fieldCount]))
            print(fieldList[fieldCount] + spacing + formatCol)
            fieldCount += 1
        cursor.execute('SELECT specabilname FROM monsterspecabil WHERE monname ="' + monsterRequest + '"')
        specAbilDump = cursor.fetchall()
        specAbilStr = ""
        for specAbil in specAbilDump:
            specAbilStr += specAbil[0] + ", "
        print("Special abilities: ", specAbilStr)

        cursor.execute('SELECT * FROM monsterattack WHERE monname ="' + monsterRequest + '"')
        attackDump = cursor.fetchall()
        print("Attacks: ")
        for att in attackDump:
            print(att[1] + " for " + att[2])

        cursor.execute('SELECT habitat FROM monsterHabitat WHERE monName ="'+monsterRequest+'";')
        habDump = cursor.fetchall()
        habStr = ""
        for hab in habDump:
            habStr += hab[0] + ", "
        print("Habitats: ", habStr)

        editChoice = input("Edit (Y/N)? ").upper()
        if editChoice == "Y":
            editMonster(monsterRequest)

    else:
        print("Sorry," + monsterRequest+" does not exist")
    

##### MAIN MENU #####
dbPath = 'BXdata.db'
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

print('Monster Database!')
menuchoice = ''
while menuchoice != 'Q':
    print ('N for New monster entry')
    print ('V to View and edit single monster')
    #print ('F to Filter monsters')
    #print ('R to Random Encounters')
    print ('H to view Habitats')
    print ('L to List monsters (optional filters)')
    print ('Q to Quit')
    menuchoice = input('? ')
    menuchoice = menuchoice.upper()
    #print (menuchoice)
    if menuchoice == 'N':
        newmonster()
    elif menuchoice == 'L':
        listmonsters()
    elif menuchoice == 'H':
        habitatView()
    elif menuchoice == 'V':
        viewMonster()
    elif menuchoice == 'Q':
        print("Quitting program - have a nice day!")
    else:
        print("Sorry, option not recognised.")

conn.close()

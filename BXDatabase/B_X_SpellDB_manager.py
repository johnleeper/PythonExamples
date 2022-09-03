import sqlite3

def descriptionChecker(text):
    newText = text.replace("'", "\'")
    return newText
    
def inputNewSpell():
    sqlinput = 'insert into BX_Spells (spellName, source, caster, spelllevel, duration, range, spelldescription) values("'
    try:
        spellName = input("Spell Name? ")
        sqlinput += spellName + '", '
        source = input("Source (B/E/C/Z/A)? ")
        if source.upper() == "B": source = "Basic Rules"
        elif source.upper() == "E": source = "Expert Rules"
        elif source.upper() == "C": source = "Companion Rules"
        elif source.upper() == "Z": source = "Mine on blog"
        elif source.upper() == "A": source = "AD&D"
        sqlinput += '"'+ source + '", '
        clas = input("Caster Class (M/C/D)? ")
        if clas.upper() == "M": clas = "Magic User"
        elif clas.upper() == "C": clas = "Cleric"
        elif clas.upper() == "D": clas = "Druid"
        sqlinput += '"' + clas + '", '
        level = int(input("Spell level? "))
        sqlinput += str(level) + ', '
        duration = input("Spell duration (text)? ")
        sqlinput += '"' + duration + '", '
        spellRange = input("Spell range (integer)? ")
        sqlinput += spellRange + ', '
        description = descriptionChecker(input("Description? "))
        sqlinput += '"' + description + '");'
        print(sqlinput)
        cursor.execute(sqlinput)
        cursor.execute('COMMIT;')
    except Error as e:
        print("Sorry, could not complete. Tried running: ")
        print(sqlinput)
        print(e)
    return

def viewLists():
    sqlinput = "SELECT * FROM BX_Spells "
    source = input("Enter source (B/E/C/Z/A): ")
    if source.upper() == "B": source = "Basic Rules"
    elif source.upper() == "E": source = "Expert Rules"
    elif source.upper() == "C": source = "Companion Rules"
    elif source.upper() == "Z": source = "Mine on blog"
    elif source.upper() == "A": source = "AD&D PHB"

    clas = input("Class (M/C/D)? ")
    if clas.upper() == "M": clas = "Magic User"
    elif clas.upper() == "C": clas = "Cleric"
    elif clas.upper() == "D": clas = "Druid"

    lev = input("What level? ")
    try:
        level = int(lev)
    except:
        print("Sorry, something went wrong. Did you input an integer?")
    if source != "" and clas != "" and lev != "" :
        sqlinput += 'WHERE source = "' + source + '" AND caster = "' + clas +'" AND spelllevel = '+ lev
    elif source != "" and clas != "":
        sqlinput += 'WHERE source = "' + source + '" AND caster = "' + clas +'" '
    elif source != "" and level !="":
        sqlinput += 'WHERE source = "' + source + '" AND spelllevel = '+ lev
    elif clas != "" and lev != "":
        sqlinput += 'WHERE caster = "' + clas +'" AND spelllevel = '+ lev
    elif source != "":
        sqlinput += 'WHERE source = "' + source + '" '
    elif clas != "":
        sqlinput += 'WHERE caster = "' + clas + '" '
    elif level != "":
        sqlinput += 'WHERE spelllevel = ' + lev
        
    sqlinput += ' ORDER BY caster, spelllevel, spellname'
    try:
        cursor.execute(sqlinput)
    except:
        print("Failed trying to run: ")
        print(sqlinput)
    spelldump = cursor.fetchall()
    spellcount = 0
    for line in spelldump:
        spaceA = " " * (30 - len(line[0]))
        #spaceB = " " * (20 - len(line[0]))
        #print(str(spellcount) +")", line[2], str(line[1]), spaceA, line[0], "(", line[3][:6], ")", spaceB, line[4][:25])
        if len(spelldump) > 99:
            countStr = "  "+str(spellcount)
        elif len(spelldump) > 9:
            countStr = " " + str(spellcount)
        else: countStr = str(spellcount)
        print(countStr, (line[0] + spaceA), line[1], line[2], str(line[3]))
        spellcount +=1
    specificSpell = input("Enter list number of spell to view in detail")
    if specificSpell != "":
        print(spelldump[int(specificSpell)])
    return

def deleteSpell():
    deletable = input("Enter exact name of spell to be deleted: ")
    deletelevel = input("Enter the level of spell to be deleted: ")
    deleteclass = input("Enter the class of spell to be deleted: ")
    try:
        cursor.execute('DELETE FROM BX_Spells WHERE spellname ="' + deletable +
                       '" AND spelllevel = '+ deletelevel + ' AND class = "' + deleteclass + '"')
        cursor.execute('COMMIT')
    except e:
        print(e)
    return

def editSpell():
    editName = input("Enter name of spell to be edited: ")
    cursor.execute('SELECT * FROM BX_Spells WHERE spellname ="' + editName + '"')
    editdump = cursor.fetchall()
    if len(editdump) == 0:
        print("Sorry, no spells match that name")
        return
    elif len(editdump) > 1:
        lineCount = 0
        for line in editdump:
            print(str(lineCount) + ") Name: " + line[0] + ", Level: " + str(line[1]) + ", Class: " + line[2] + ", Source: " + line[3])
            lineCount += 1
        lineChoice = int(input("Number? "))
        editSelection = editdump[lineChoice]
    elif len(editdump) == 1:
        editSelection = editdump[0]
    fieldChoice = input("Edit (N)name, (L)level, (C)class, (S)source or (D)description? ")
    if fieldChoice.upper() == "N":
        newField = "spellName"
        newData = input("New name: ")
    elif fieldChoice.upper() == "L":
        newField = "spelllevel"
        newData = input("New level: ")
    elif fieldChoice.upper() == "C":
        newField = "class"
        newData = input("New class: ")
    elif fieldChoice.upper() == "S":
        newField = "source"
        newData = input("New source: ")
    elif fieldChoice.upper() == "D":
        newField = "description"
        newDesc = input("New Description: ")
        newData = descriptionChecker(newDesc)
    else:
        print("Sorry, invalid choice")
        return

    if fieldChoice.upper() == "L":
        cursor.execute('UPDATE BX_Spells SET '+ newField +' = ' + newData +
                   ' WHERE spellname = "' + editSelection[0] + '" AND spelllevel = ' +
                   str(editSelection[1]) + ' AND class = "' + editSelection[2]
                   + '" AND source = "' +editSelection[3] + '"')
    else: 
        cursor.execute('UPDATE BX_Spells SET '+ newField +' = "' + newData +
                   '" WHERE spellname = "' + editSelection[0] + '" AND spelllevel = ' +
                   str(editSelection[1]) + ' AND class = "' + editSelection[2]
                   + '" AND source = "' +editSelection[3] + '"')
    cursor.execute('COMMIT')
    return


conn = sqlite3.connect("BXdata.db")
cursor = conn.cursor()

contProg = True
while contProg:
    print("Basic/Expert Spell Database Mananger")
    print("I: input new spell")
    print("D: delete incorrect spell")
    print("V: view spell lists")
    print("E: edit spell")
    print("Q: quit")
    mainchoice = input("? ").upper()
    
    if mainchoice == "Q":
        contProg = False
    elif mainchoice == "I":
        inputNewSpell()
    elif mainchoice == "V":
        viewLists()
    elif mainchoice == "D":
        deleteSpell()
    elif mainchoice == "E":
        editSpell()
    else:
        print("Sorry, that option is not recognised")
conn.close()

import sqlite3
import os

def copyRows(table, branchOnly):
    # first need to check primary keys
    branchCurs.execute(columnQuery)
    tableSchemaDump = branchCurs.fetchall()
    primKeyName = ""
    primKeyType = ""
    columnList = []
    for schemaRow in tableSchemaDump:
        columnList.append(schemaRow[1])
        if schemaRow[5] == 1:
            print("Found primary key name: " + schemaRow[1] + ",   type: " +  schemaRow[2])
            primKeyName = schemaRow[1]
            primKeyType = schemaRow[2]
        # Next bit is about BXData.db being peculiar
        if schemaRow[1] in ["habID", "attackid", "abilid"]:
            print("Found informal key name:" + schemaRow[1] + ",   type: " + schemaRow[2])
            primKeyName = schemaRow[1]
            primKeyType = schemaRow[2]
    if primKeyName == "":
        print("No primary or informal key found")
    else:
        primeKeyList = []
        keyQuery = "SELECT " + primKeyName + " FROM "+ table
        trunkCurs.execute(keyQuery)
        keyDump = trunkCurs.fetchall()
        for keyTuple in keyDump:
            primeKeyList.append(keyTuple[0])
            
    # second need to get column data types - strings need quotes, numbers don't
    # we can assume that columns stay in correct order both with schema and copied rows
    insertQueryBase = "INSERT into " + table + " (" + (", ".join(columnList)) + ") values ("


    if table == "monsterbasic":
        monnameList = []
        trunkCurs.execute('SELECT monname FROM monsterbasic;')
        monnameDump = trunkCurs.fetchall()
        for monnameRow in monnameDump:
            monnameList.append(monnameRow[0])
    for newRow in branchOnly:
        colPosition = 0
        dataList = []
        insertQuery = insertQueryBase
        validRow = True
        for datum in newRow:
            if datum == None:
                dataList.append('NULL')
            elif tableSchemaDump[colPosition][2] in ["text", "char", "varchar(255)", "varchar"]:
                datumStr = '"' + datum + '"'
                dataList.append(datumStr)
            else:
                dataList.append(str(datum))
            #Here we deal with primary key clashes
            if tableSchemaDump[colPosition][1] == primKeyName and (datum in primeKeyList):
                if primKeyType in ["integer", "Integer", "int", "Int"]:
                    # should just be arbitary ID numbers that can be changed, at least in BXdata.db
                    newKeyDatum = max(primeKeyList) +1
                    primeKeyList.append(newKeyDatum)
                    dataList[-1] = str(newKeyDatum)
                    # the datum has already been added to the datalist so needs to be changed not appended                    
                else:
                    print("Unresolvable Primary Key Clash: abandoning this row")
                    validRow = False                    
            colPosition += 1
            if table == "monsterbasic" and tableSchemaDump[colPosition][1] == "monname":
                if datum in monnameList:
                    validRow = False
                else:
                    monnameList.append(datum)
            
        if validRow == True:
            insertQuery += ", ".join(dataList) + ")"
            print(insertQuery)
            try:
                trunkCurs.execute(insertQuery)
                trunkCurs.execute("COMMIT;")
            except Exception as e:
                print("Problem trying to insert this row")
                print(e)
    return

directoryList = ["C:\\Users\\John\\Dropbox\\Misc Programming\\SQLite\\databases", "C:\\Users\\User\\Dropbox\\Misc Programming\\SQLite\\databases", "C:\\Users\\sorce\\Dropbox\\Misc Programming\\SQLite\\databases"]
directory = ""
for possibleDir in directoryList:
    if (os.path.exists(possibleDir)):
        directory = possibleDir
        print("Directory found: " + directory)

trunkDB = "BXdata.db"

fileList = os.listdir(directory)
#print(fileList)
fileCount = 0
for file in fileList:
    print(fileCount, file)
    fileCount+= 1

fileChoice = input("Which file is the conflicting database? ")
try:
    fileChoiceInt = int(fileChoice)
    branchFilename = fileList[fileChoiceInt]
except:
    print("Sorry, invalid input")
    exit

trunkConnection = sqlite3.connect(directory + "\\" + trunkDB)
trunkCurs = trunkConnection.cursor()
branchConnection = sqlite3.connect(directory + "\\" + branchFilename)
branchCurs = branchConnection.cursor()
schemaNameList = ["sqlite_schema", "sqlite_master", "sqlite_main"]
for schemaName in schemaNameList:
    try:
        trunkCurs.execute("SELECT * FROM "+ schemaName)
        goodSchemaName = schemaName
        break
    except:
        continue
trunkSchemaDump = trunkCurs.fetchall()
trunkTableNameSet = set()
for table in trunkSchemaDump:
    trunkTableNameSet.add(table[1])
branchCurs.execute("SELECT * FROM "+ goodSchemaName)
branchSchemaDump = branchCurs.fetchall()
branchTableNameSet = set()
for table in branchSchemaDump:
    branchTableNameSet.add(table[1])

## Comparing List of Tables
tableIntersect = trunkTableNameSet.intersection(branchTableNameSet)
tableDiffT = trunkTableNameSet.difference(branchTableNameSet)
tableDiffB = branchTableNameSet.difference(trunkTableNameSet)
print("Intersection has ", len(tableIntersect), "tables: " + str(tableIntersect))
print("Trunk has unique tables: " + str(tableDiffT))
print("Branch has unique tables: " + str(tableDiffB))

## Comparing schema of tables in common
for table in tableIntersect:
    columnQuery = "PRAGMA table_info("+table+");"
    branchCurs.execute(columnQuery)
    branchColDump = branchCurs.fetchall()
    trunkCurs.execute(columnQuery)
    trunkColDump = trunkCurs.fetchall()
    if str(trunkColDump) == str(branchColDump):
        #print("Table "+ table +" has same columns for both databases: " + str(mainColDump))
        print("Table "+ table +" has same columns for both databases ")
        print("Raw Schema: ")
        for rowTuple in trunkColDump:
            print("    "+ str(rowTuple))
    else:
        print("Differences found in table: "+ table)
        print("Trunk columns difference: "+ str(set(trunkColDump).difference(set(branchColDump))))
        print("Branch columns difference: " + str(set(branchColDump).difference(set(trunkColDump))))
        print("Raw Schema for trunk version: ")
        for rowTuple in trunkColDump:
            print("    "+ str(rowTuple))

# Comparing rows between table versions
    rowQuery = "SELECT * FROM " + table
    branchCurs.execute(rowQuery)
    branchRowDump = branchCurs.fetchall()
    trunkCurs.execute(rowQuery)
    trunkRowDump = trunkCurs.fetchall()
    print("Rows in Trunk version of " + table + " = " + str(len(trunkRowDump)))
    print("Rows in Branch version of " + table + " = " + str(len(branchRowDump)))
    branchRowSet = set(branchRowDump)
    trunkRowSet = set(trunkRowDump)
    intersect = trunkRowSet.intersection(branchRowSet)
    trunkOnly = trunkRowSet.difference(branchRowSet)
    branchOnly = branchRowSet.difference(trunkRowSet)
    print("Rows in common: " + str(len(intersect)))
    print("Rows only in Trunk: " + str(len(trunkOnly)))
    for row in trunkOnly:
        print("\t" + str(row))

    print("Rows only in Branch: " + str(len(branchOnly)))
    for row in branchOnly:
        print("\t" + str(row))
    if len(branchOnly) > 0:
        copyFromBranch = input("Copy rows unique to Branch over to Trunk in " + table + " (Y/N)? ").upper()
        if copyFromBranch == "Y":
            copyRows(table, branchOnly)
            print("Copying rows across")

    print("------------------------ \n \n")

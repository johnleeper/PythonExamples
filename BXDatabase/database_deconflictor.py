import sqlite3
import sys

def copyRows(sourceCurs, destinCurs, table):
    copyQuery = "SELECT * FROM " + table
    sourceCurs.execute(copyQuery)
    destinCurs.execute(copyQuery)
    sourceSet = set(sourceCurs.fetchall())
    destinSet = set(destinCurs.fetchall())
    rowsToAdd = sourceSet.difference(destinSet)
    for row in rowsToAdd:
        print(row)
    if sourceCurs == mainCurs:
        sourceName = mainDb
        destinName = branchDb
    else:
        sourceName = branchDb
        destinName = mainDb
    print("These rows for table "+ table + "found in " + sourceName + ", not found in " + destinName)
        
    confirm = input("Add these rows (Y/N) ?").upper()
    if confirm == "Y":
        columnQuery = "PRAGMA table_info("+table+");"
        sourceCurs.execute(columnQuery)
        columnDump = sourceCurs.fetchall()
        primeKName = ""
        primeKType = ""
        primeKPosit = -1
        colNameList = []
        colTypeList = []
        for tup in columnDump:
            colNameList.append(tup[1])  # needed for INSERT query
            colTypeList.append(tup[2])
            if tup[5] > 0: ## if pragma indicates this column is primary key
                print("Primary key name: " + tup[1] +", type:" + tup[2] + ", position: " + tup[0])
                primeKName = tup[1]
                primeKType = tup[2]
                primeKPosit = tup[0]
        if primeKName == "":  # if no formal primary key is found
            print("No formal primary key found.")
            for colTup in columnDump:
                print(colTup[0], colTup[1], colTup[2])
            uniqueColNum = input("Position Number of Column that should be unique: ")
            if uniqueColNum.isDigit():
                uniqueColNum = int(uniqueColNum)
            else:
                print("No key column given")
            if uniqueColNum >= 0 and uniqueColNum < len(collist):
                primeKName = columnDump[uniqueColNum][1]
                primeKType = columnDump[uniqueColNum][2]
                primeKPosit = uniqueColNum
                print("Selected as unique value column: " + columnDump[uniqueColNum])
            else:
                print("No unique-value columns for this table. ")   
        if primeKName == "": # no primary key (formal or informal) found
            for newRow in rowsToAdd:
                insertQuery = compileInsert(table, newRow, colNameList, colTypeList)
                print(insertQuery)
                try:
                    destinCurs.execute(insertQuery)
                    print("No errors for this row")
                except:
                    print("Error Encountered!")
                    
        elif primeKName != "" and primeKType in ["integer", "INT"]:  # should be primary key as integer
            destinCurs.execute('SELECT MAX(' + primeK +') FROM ' +table +';')  # This is why you need the name of the PK, not just colummn position. 
            maxKeyDump = destinCurs.fetchone()
            maxKey = int(maxKeyDump[0]) # should be maximum primary key in current destination table
            # This part may have incorrect assumptions, namely that the primary key is an abstract ID number and as long as it is unique, it is good.
            # What if it is something that needs to maintain its original value because the value represents something like Phone Number, Passport Number etc?  
            for row in rowsToAdd:
                rowList = list(row)
                maxKey += 1
                rowList[primeKPosit] = maxKey
                insertQuery = compileInsert(table, newRow, colNameList, colTypeList)
                print(insertQuery)
                try:
                    destinCurs.execute(insertQuery)
                    print("No errors for this row")
                except:
                    print("Error Encountered!")
        elif primeKName != "" and primeKType in ("text", "TEXT"):
            primeKeySourceSet = set()
            primeKeyDestinSet = set()
            keySetQuery = "SELECT DISTINCT(" + primeKName + " FROM "+ table + ";"
            sourceCurs.execute(keySetQuery)
            sourceKeySetDump = sourceCurs.fetchall()
            for keyTup in sourceKeySetDump:
                primeKeySourceSet.add(keyTup[0])
            destinCurs.execute(keySetQuery)
            destinKeySetDump = destinCurs.fetchall()
            for keyTup in destinKeySetDump:
                primeKeyDestinSet.add(keyTup[0])
            validKeySet = primeKeySourceSet.difference(primeKeyDestinSet)
            invalidKeySet = primeKeySourceSet.intersection(primeKeyDestinSet)
            if len(validKeySet) = 0:
                print("Sorry, no valid records to add")
                return
            else:
                print("valid keys to be added: " = len(validKeySet))
                print("invalid keys not added: " = len(invalidKeySet))
            for newRow in rowsToAdd:
                if newRow[primeKPosit] in invalidKeySet:
                    print("Row not added due to invalid key: " + str(newRow))
                else:
                    insertQuery = compileInsert(table, rowList, colNameList, colTypeList)
                    print(insertQuery)
                    try:
                        destinCurs.execute(insertQuery)
                        print("No errors for this row")
                    except:
                        print("Error Encountered!")
                    
        
# here we want to find if the primary key value for the new row clashes with existing rows' keys.
# if so we don't attempt to insert the row, maybe print a warning message
# if not (new row's primary key value is unique) we insert the new row as normal
                

def compileInsert(table, newRow, colNameList, colTypeList):
    # This method will assume that primary key has already been sorted out and primary key values have been adjusted within rowsToAdd
    insertQueryStart = 'INSERT INTO ' + table + '(' + (', '.join(colNameList)) + ') VALUES ('
    rowList = list(newRow)  # newRow may be tuple
    colCount = 0
    for value in rowList:
        dataType = colTypeList[colCount]
        if dataType in ("TEXT", "text"):
            value = '"' + value +'"'
            rowList[colCount] = value # should change value within row
        colCount +=1
    valueString = ', '.join(rowList)
    insertQuery = insertQueryStart + valueStr + ';'
    return insertQuery
            


print("For windows file paths remove quotes but don't worry about back slashes")
mainDb = input("What is the path of the main database? ")
##mainDb = pathProcess(mainDb)
try:
    mainConn = sqlite3.connect(mainDb)
    mainCurs = mainConn.cursor()
except:
    print("Sorry, not a valid database path. ")
    sys.exit()
branchDb = input("What is the path of the branch database? ")
try:
    branchConn = sqlite3.connect(branchDb)
    branchCurs = branchConn.cursor()
except:
    print("Sorry, not a valid database path. ")
    sys.exit()

# Compare table lists
tableQuery = "SELECT name FROM sqlite_schema WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY 1;"
mainCurs.execute(tableQuery)
mainTableDump = mainCurs.fetchall()
#print(mainTableDump)
mainTableSet = set()
for tup in mainTableDump:
    mainTableSet.add(tup[0])

branchCurs.execute(tableQuery)
branchTableDump =  branchCurs.fetchall()
#print(branchTableDump)
branchTableSet = set()
for tup in branchTableDump:
    branchTableSet.add(tup[0])

print("Tables unique to Main: " + str(mainTableSet.difference(branchTableSet)))
print("Tables unique to Branch: " + str(branchTableSet.difference(mainTableSet)))
print("Tables in common to both: " + str(mainTableSet.intersection(branchTableSet)))    
commonTableList = list(mainTableSet.intersection(branchTableSet))
for table in commonTableList:
    columnQuery = "PRAGMA table_info("+table+");"
    branchCurs.execute(columnQuery)
    branchColDump = branchCurs.fetchall()
    mainCurs.execute(columnQuery)
    mainColDump = mainCurs.fetchall()
    if str(mainColDump) == str(branchColDump):
        #print("Table "+ table +" has same columns for both databases: " + str(mainColDump))
        print("Table "+ table +" has same columns for both databases ")
    else:
        print("Differences found in table: "+ table)
        print("Main columns difference: "+ str(set(mainColDump).difference(set(branchColDump))))
        print("Branch columns difference: " + str(set(branchColDump).difference(set(mainColDump))))
    
## Next is finding out differences in rows. This could involve a similar method using sets.
# Or there might be a specific SQL query to run
    rowQuery = "SELECT * FROM " + table
    branchCurs.execute(rowQuery)
    branchRowDump = branchCurs.fetchall()
    mainCurs.execute(rowQuery)
    mainRowDump = mainCurs.fetchall()
    print("Rows in Main version of " + table + " = " + str(len(mainRowDump)))
    print("Rows in Branch version of " + table + " = " + str(len(branchRowDump)))
    branchRowSet = set(branchRowDump)
    mainRowSet = set(mainRowDump)
    intersect = mainRowSet.intersection(branchRowSet)
    mainOnly = mainRowSet.difference(branchRowSet)
    branchOnly = branchRowSet.difference(mainRowSet)
    print("Rows in common: " + str(len(intersect)))
    print("Rows only in Main: " + str(len(mainOnly)))
    print("Rows only in Branch: " + str(len(branchOnly)))
    if len(mainOnly) > 0:
        copyFromMain = input("Copy rows unique to Main over to Branch in " + table + " (Y/N)? ").upper()
        if copyFromMain == "Y":
            copyRows(mainCurs, branchCurs, table)
    if len(branchOnly) > 0:
        copyFromBranch = input("Copy rows unique to Branch over to Main in " + table + " (Y/N)? ").upper()
        if copyFromBranch == "Y":
            copyRows(branchCurs, mainCurs, table)

    print("------------------------ \n \n")




mainConn.close()
branchConn.close()


## C:\Users\sorce\Dropbox\Misc Programming\SQLite\databases\biology.db
## C:\Users\sorce\Dropbox\Misc Programming\SQLite\databases\biology_old.db

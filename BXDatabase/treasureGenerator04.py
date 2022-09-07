import sqlite3
import random

def testRun():
    gemTot = 0
    gemList = gemGenerate(2000)
    print("Gems: ")
    print(contentPresenter(gemList))
    for gem in gemList:
        gemTot += gem[0]
    print("Gem sum value: ", gemTot, "out of 2000")
    print("")

    jewelTot = 0
    jewelList = jewelGenerate(2000)
    print("Jewelry: ")
    print(contentPresenter(jewelList))
    for jewel in jewelList:
        jewelTot += jewel[0]
    print("Jewelry sum value: ", jewelTot, "out of 2000")
    print("")

    magicTot = 0
    magicList = magicGenerate(4000)
    print("Magic items: ")
    print(contentPresenter(magicList))
    for item in magicList:
        magicTot += item[0]
    print("Magic item sum value: ", magicTot, "out of 4000")
    print("")

    tradeTot = 0
    tradeList = tradeGenerate(2000)
    print("Trade items: ")
    print(contentPresenter(tradeList))
    for trade in tradeList:
        tradeTot += trade[0]
    print("Trade sum value: ", tradeTot, "out of 2000")
    print("")

def gemGenerate(parcelValue):
    cursor.execute('SELECT * FROM gemsize')
    gemsize_tuple = cursor.fetchall()
    cursor.execute('SELECT * FROM gemquality')
    gemquality_tuple = cursor.fetchall()
    cursor.execute('SELECT Item, BaseValue FROM combinedTreasure WHERE treasureType = "gem"')
    gemTypeList = cursor.fetchall()
    parcelList = []
    remainVal = parcelValue
    while remainVal > 10:
            size = random.choice(gemsize_tuple)
            quality = random.choice(gemquality_tuple)
            gemType = random.choice(gemTypeList)
            ## print("size: ", size, "quality: ", quality, "gemtype", gemType) ## diagnostic
            gemValue = int(int(gemType[1]) * size[1] * quality[1])
            if gemValue <= remainVal * 1.1 and gemValue > 5:
                    gemDesc = size[0] + " "+ quality[0] +" "+ gemType[0]
                    gemTuple = (gemValue, gemDesc)
                    parcelList.append(gemTuple)
                    remainVal -= gemValue
    #print("returning: ", parcelList)
    return parcelList

def jewelGenerate(parcelValue):
    cursor.execute('SELECT Item, BaseValue FROM combinedTreasure WHERE treasureType = "jewellery"')
    jewelItemList = cursor.fetchall()

    cursor.execute('SELECT * FROM jewelMaterial')
    jewelMaterial_tuple = cursor.fetchall()
    cursor.execute('SELECT * FROM jewelQuality')
    jewelQuality_tuple = cursor.fetchall()
    parcelList = []
    remainVal = parcelValue
    while remainVal > 10:
            material = random.choice(jewelMaterial_tuple)
            quality = random.choice(jewelQuality_tuple)
            jewelItem = random.choice(jewelItemList)
            jewelValue = int(int(jewelItem[1]) * int(material[1]) * int(quality[1]))
            if jewelValue <= remainVal * 1.1 and jewelValue > 5:
                    jewelDesc = quality[0] +" "+ material[0].lower() +" "+ jewelItem[0]
                    jewel = (jewelValue, jewelDesc)
                    parcelList.append(jewel) ## adds new jewelry to dictionary
                    remainVal -= jewelValue
    return parcelList
	
def magicGenerate(parcelValue):
    cursor.execute('SELECT basevalue, item FROM combinedTreasure WHERE treasureType LIKE "magic item%";')
    magicList = cursor.fetchall()
    parcelList = []
    remainVal = parcelValue
    while remainVal > 100:
        item = random.choice(magicList)
        if item[0] < remainVal * 1.1:
            remainVal -= item[0]
            parcelList.append(item)
    return parcelList

def tradeGenerate(parcelValue):
    cursor.execute('SELECT basevalue, item FROM combinedTreasure WHERE treasureType = "trade item"')
    tradeList = cursor.fetchall()
    parcelList = []
    remainVal = parcelValue
    while remainVal > 100:
        item = random.choice(tradeList)
        if item[0] < remainVal * 1.1:
            remainVal -= item[0]
            parcelList.append(item)
    return parcelList

def coinGenerate(parcelValue, type):
    copperCoins = parcelValue * 100
    return Coins

def contentPresenter(itemList):
    itemDict = {}
    presentedString = ""
    for item in itemList:
        if item[1] in itemDict:
            itemDict[item[1]] += 1 # increases dict count by 1
        else:
            itemDict[item[1]] = 1 # adds new item to dict
    for itemDesc in itemDict:
        itemVal = 0
        for item in itemList:
            if item[1] == itemDesc:
                itemVal = item[0]
                break
        if itemDict[itemDesc] == 1:
            itemStr = itemDesc + " worth " + str(itemVal) + "\n"
        else:
            itemStr = str(itemDict[itemDesc]) + " x " + itemDesc + " worth " + str(itemVal) + " each, total =" + str(itemVal * itemDict[itemDesc]) + "\n"
        presentedString += itemStr    
    return presentedString



def main(totalAmount, divisionSize):
    treasureTypeTable = {0.1: "Copper",
                     0.3: "Silver",
                     0.6: "Gold",
                     0.7: "Platinum",
                     0.8: "Gems",
                     0.9: "Jewelry",
                     0.95: "Magic Item",
                     1: "Trade Goods"}
    currentTotal = 0
    copperPieces = 0
    silverPieces = 0
    goldPieces = 0
    platinumPieces = 0
    gemList = []
    gemTot = 0
    jewelTot = 0
    jewelList = []
    magicTot = 0
    magicList = []
    tradeTot = 0
    tradeList = []
    while currentTotal < totalAmount:
        parcelValue = totalAmount * random.random() / divisionSize
        treasureTypeRoll = random.random()
        for ttype in treasureTypeTable:
            if treasureTypeRoll < ttype:
                ttypeDesc = treasureTypeTable[ttype]
                print("Parcel value = ", parcelValue, ", treasure type is: ", ttypeDesc)
                break
        if ttypeDesc == "Copper":
            copperPieces += int(parcelValue * 100)
        elif ttypeDesc == "Silver":
            silverPieces += int(parcelValue * 10)
        elif ttypeDesc == "Gold":
            goldPieces += int(parcelValue)
        elif ttypeDesc == "Platinum":
            platinumPieces += int(parcelValue /5)
        elif ttypeDesc == "Gems":
            gemList.extend(gemGenerate(parcelValue))
        elif ttypeDesc == "Jewelry":
            jewelList.extend(jewelGenerate(parcelValue))
        elif ttypeDesc == "Magic Item":
            magicList.extend(magicGenerate(parcelValue))
        elif ttypeDesc == "Trade Goods":
            tradeList.extend(tradeGenerate(parcelValue))
            
        currentTotal = currentTotal + parcelValue
    print("Total parcel value is ", currentTotal)
    print("CP: ", copperPieces)
    print("SP: ", silverPieces)
    print("GP: ", goldPieces)
    print("PP: ", platinumPieces)
    print("Gems: ")
    print(contentPresenter(gemList))
    for gem in gemList:
        gemTot += gem[0]
    print("Gem sum value: ", gemTot)
    print("")
    print("Jewelry: ")
    print(contentPresenter(jewelList))
    for jewel in jewelList:
        jewelTot += jewel[0]
    print("Jewelry sum value: ", jewelTot)
    print("")
    print("Magic items: ")
    print(contentPresenter(magicList))
    for item in magicList:
        magicTot += item[0]
    print("Magic item sum value: ", magicTot)
    print("")
    print("Trade items: ")
    print(contentPresenter(tradeList))
    for trade in tradeList:
        tradeTot += trade[0]
    print("Trade sum value: ", tradeTot)
    print()
    grandSum = (copperPieces /100) + (silverPieces / 10) + goldPieces + gemTot + jewelTot + magicTot + tradeTot
    print("Grand total is: ", grandSum)

conn = sqlite3.connect('BXdata.db')
cursor = conn.cursor()
print("Random D&D Treasure Generator")
totalAmount = input("What is minimum total amount? ")
divisionInput = input("minimum divisions? ")
if divisionInput == "":
    divisionSize = 1
else:
    divisionSize = int(divisionInput)

if totalAmount == "test":
    testRun()
else:
    totalAmount = int(totalAmount)
    main(totalAmount, divisionSize)
    


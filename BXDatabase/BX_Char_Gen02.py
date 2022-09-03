import random
import sqlite3

def spellSelector(charclass, level):
    conn = sqlite3.connect("BXdata.db")
    cursor = conn.cursor()
    clericSpellNumbers = [[0], #level 1
                          [1], #level 2
                          [2], #level 3
                          [2, 1], #level 4
                          [2, 2], # level 5
                          [2, 2, 1], #level 6
                          [3, 2, 2], #level 7
                          [3, 3, 2, 1], #level 8
                          [3, 3, 3, 2], #level 9
                          [4, 4, 3, 2, 1], #level 10
                          [4, 4, 3, 3, 2], #level 11
                          [4, 4, 4, 3, 2, 1], #level 12
                          [5, 5, 4, 3, 2, 2], #level 13
                          [5, 5, 5, 3, 3, 2] #level 14
                          ]

    mageSpellNumbers = [[1], #level 1
                        [2], #level 2
                        [2, 1], #level 3
                        [2, 2], #level 4
                        [2, 2, 1], #level 5
                        [2, 2, 2], #level 6
                        [3, 2, 2, 1], #level 7
                        [3, 3, 2, 2], #level 8
                        [3, 3, 3, 2, 1], #level 9
                        [3, 3, 3, 3, 2], #level 10
                        [4, 3, 3, 3, 2, 1], #level 11
                        [4, 4, 4, 3, 2, 1], #level 12
                        [4, 4, 4, 3, 2, 2], #level 13
                        [4, 4, 4, 4, 3, 2] #level 14
                    ]
    if charclass in ["Cleric", "Dwarf Cleric"]:
        caster = "Cleric"
        spellNumbers = clericSpellNumbers[level -1]
    else:
        caster = "Magic User"
        spellNumbers = mageSpellNumbers[level -1]
    spellsKnown = []
    spellListLevel = 0
    print("SpellNumbers variable is: ", spellNumbers)
    for spellLevelquant in spellNumbers:
        spellListLevel +=1
        query = 'SELECT spellname FROM BX_spells WHERE caster = "' + caster + '" AND spelllevel = ' + str(spellListLevel)
        cursor.execute(query)
        spellLevelDump = cursor.fetchall()
        spellListforLevel = []
        for row in spellLevelDump:
            spellListforLevel.append(row[0])
        print("spellListforLevel: " + str(spellListforLevel)) 
        for spellsPerLevel in range(spellLevelquant):
            spellsKnown.append(random.choice(spellListforLevel))
        
    conn.close()
    return spellsKnown
                        

statsDic = {"Str":0, "Int":0, "Wis":0, "Dex":0, "Con":0, "Cha":0}

for stat in statsDic:
    statTotal = 0
    rollList = []
    for roll in range(4):
        rollResult = random.randint(1, 6) # rolls d6
        rollList.append(rollResult)	# adds the d6 to a list
        statTotal = sum(rollList) - min(rollList) # 4d6, drop the lowest and add the others together
    #print(statTotal)
    statsDic[stat] = statTotal

maxStat = max(statsDic, key=statsDic.get)
print(statsDic)
print("max stat is ", maxStat)
charclass = ""
if maxStat == "Str":
    if statsDic["Str"] >= 9 and statsDic["Con"] >= 9:
        charclass = random.choice(["Dwarf Warrior", "Fighter"])
    else:
        charclass = "Fighter"
elif maxStat == "Int":
    if statsDic["Str"] >= 9 and statsDic["Int"] >= 9:
        charclass = random.choice(["Magic User", "Elf Spellsword"])
    else:
        charclass = "Magic User"
elif maxStat == "Wis":
    if statsDic["Wis"] >= 9 and statsDic["Con"] >= 9:
        charclass = random.choice(["Cleric", "Dwarf Cleric"])
    else:
        charclass = "Cleric"
elif maxStat == "Dex":
    if statsDic["Str"] >= 9 and statsDic["Dex"] >= 9:
        charclass = random.choice(["Thief", "Halfling Scout", "Elf Ranger"])
    else: charclass = "Thief"
elif maxStat == "Con":
    if statsDic["Str"] >= 9 and statsDic["Con"] >= 9:
        charclass = "Dwarf Warrior"
    elif statsDic["Wis"] >= 9 and statsDic["Con"] >= 9:
        charclass = "Dwarf Cleric"
    else:
        tempstatsDic = statsDic.copy()
        del tempstatsDic["Con"]
        secondStat = max(tempstatsDic, key=statsDic.get)
        if secondStat == "Str": charclass = "Fighter"
        elif secondStat == "Int": charclass = "Magic User"
        elif secondStat == "Wis": charclass = "Cleric"
        elif secondStat == "Dex": charclass = "Thief"
        elif secondStat == "Cha": charclass = "Fighter"
elif maxStat == "Cha":
        tempstatsDic = statsDic.copy()
        del tempstatsDic["Cha"]
        secondStat = max(tempstatsDic, key=statsDic.get)
        if secondStat == "Str": charclass = "Fighter"
        elif secondStat == "Int": charclass = "Magic User"
        elif secondStat == "Wis": charclass = "Cleric"
        elif secondStat == "Dex": charclass = "Thief"
        elif secondStat == "Con": charclass = "Fighter"
    
else:
    print("Something went wrong with class selection")
    
print("Class: ", charclass)

#Gender & Alignment
gender = random.choice(["Male", "Female"])
print("Gender: ", gender)
alignRoll = random.randint(1, 10)
if alignRoll < 5:
    alignment = "Lawful"
    trait = random.choice(["Pious", "Charitable", "Calm", "Noble", "Courageous", "Mystical"])
elif alignRoll >= 5 and alignRoll < 9:
    alignment = "Neutral"
    trait = random.choice(["Cautious", "Pragmatic", "Tacit", "Stoic", "Stubborn", "Fun-loving", "Scholarly"])
else:
    alignment = "Chaotic"
    trait = random.choice(["Malevolent", "Unpredictable", "Insane", "Deceitful", "Selfish", "Depraved", "Brutal"])
print("Alignment: ", alignment, ", trait: ", trait)


#Level
level = 0
topLevel = False
while topLevel == False:
    level += 1
    if random.random() > 0.6 or level > 13: # current max level 14 for expert rules
        topLevel = True
print("Level: ", level)

#Character Name
if gender == "Male":
    firstNameFile = open('textFiles/malenamelist.txt', 'r')
else:
    firstNameFile = open('textFiles/femalenamelist.txt', 'r')
surnameFile = open('textFiles/surnamelist.txt', 'r')
firstNameList = []
for line in firstNameFile:
    firstNameList.append(line.rstrip())
firstNameFile.close()
surnameList = []
for line in surnameFile:
    surnameList.append(line)
surnameFile.close()
suggestedName = random.choice(firstNameList) + " " + random.choice(surnameList)
print("Suggested name: ", suggestedName)



if charclass in ["Magic User", "Cleric", "Dwarf Cleric", "Elf Spellsword"]:
    spellsKnown = spellSelector(charclass, level)
    print(spellsKnown)
    
noArmourList = ["Peasant Clothes", "Scholar's Robes", "Merchant Clothes", "Noble Clothes"]
lightArmourList = ["Padded Armour", "Leather Armour", "Studded Leather Armour", "Hide Armour"]
heavyArmourList = ["Scale Mail", "Chain Mail", "Banded Armour", "Splint Armour", "Plate Mail", "Field Plate Armour", "Full Plate Armour"]


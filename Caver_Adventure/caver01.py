import sys

def nextparagraph(para, stam):
    print("*************")
    print(paradic[para])
    stam = deathcheck(para, stam)
    temptable = []
    for entry in optionstable:
        if entry[2] == para:
            temptable.append(entry)
    validchoice = False
    while validchoice == False:
        for entry in temptable:
            optnum = temptable.index(entry)
            print(optnum, entry[0])
        option = int(input("Option: "))
        if option >= 0 and option < (len(temptable)):
            validchoice = True
            newpara = temptable[option][1]
    nextparagraph(newpara, stam)

def deathcheck(para, stam):
    for item in staminaChangeDic:
        if item ==  para:
            stam += staminaChangeDic[item]
    if stam <= 0:
        print("Sorry, you have died. Your stamina is", stam)
        print("Better luck next time!")
        sys.exit()
    elif stam >=1000:
        print("Congratulations, you have survived the cave!")
        sys.exit()
    else:
        print("Current Stamina: ", stam)
        return stam
    
FH = open('caverdata01.txt', 'r')
paralist = [] # list of entire, unparsed paragraphs
parastring = '' #empty string to hold contents of each paragraph
for line in FH:
    #print (line)
    if line == '---\n':
        paralist.append(parastring)
        parastring = ''
    else:
        parastring += line
FH.close()

optionstable = []
paradic = {}
staminaChangeDic = {}
for para in paralist:
    templist = para.split('$')
    if len(templist) < 2:
        print("Problem with ", str(templist))
    pararef = templist[0].rstrip()
    paraprose = templist[1]
    if '//' in paraprose:
        staminaAdjust = int(paraprose.split('//')[1])
        paraprose = paraprose.split('//')[0]
        staminaChangeDic[pararef] = staminaAdjust
    for option in templist[2:]:
        tempopt = option.split('Goto ')
        if len(tempopt) < 2:
            print("Problem with ", str(tempopt))
        tempopt[1] = tempopt[1].rstrip()
        tempopt.append(pararef)
        optionstable.append(tempopt)
    paradic[pararef] = paraprose

print("Options Table")
for a in optionstable:
    print(a)
print("Paragraph keys")
for key in paradic.keys():
    print (key)
print("Stamina Adjustments")
for key in staminaChangeDic:
    print(staminaChangeDic[key])

stamina = 20
para = '0'
print("CAVE ADVENTURE!!!")
nextparagraph(para, stamina)

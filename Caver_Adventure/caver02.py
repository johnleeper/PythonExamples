
def main():
    global paradic
    paradic = {}
    FH = open('caverdata01.txt', 'r')
    paralist = [] # list of entire, unparsed paragraphs
    parastring = '' #empty string to hold contents of each paragraph
    for line in FH:
#        print (line)
        if line == '---\n':
            paralist.append(parastring)
            parastring = ''
        else:
            parastring += line
    FH.close()
    #paradic = dict()
    for parastring in paralist:
        templist = parastring.split('$')
        if len(templist) < 2:
            print("Problem with ", str(templist))
        pararef = templist[0].rstrip()
        paraprose = templist[1]
        print(pararef + " : " + paraprose)
        if '//' in paraprose:
            staminaAdjust = int(paraprose.split('//')[1])
            paraprose = paraprose.split('//')[0]
        else: staminaAdjust = 0

        optionsList = []
        for option in templist[2:]:
            tempopt = option.split('Goto ')
            if len(tempopt) < 2:
                print("Problem with ", str(tempopt))
            tempopt[1] = tempopt[1].rstrip()
            tempopt.append(pararef)
            optionsList.append(tempopt)
        paraObject = paragraph(pararef, paraprose, staminaAdjust, optionsList)
        #paraObject.toString()
        paradic[pararef] = paraObject
    print("Dictionary length is " + str(len(paradic)))
    stamina = 20
    paraRef = "1"
    status = "active"
    while status == "active":
        printpara(paraRef)
        stamina = deathCheck(stamina, paraRef)
        if status == "active":
            paraRef = chooseOptions(paraRef)

    if status == ("completed"):
        print("Congratulations!")
    else:
        print("Commiserations!");

#applies changes to stamina from current paragraph & changes status if appropriate
def deathCheck(stamina, paraRef):
    para = paradic[paraRef]
    if para.stamadj != "":
        stamina += para.stamadj
        if para.stamadj > 0:
            print("You have gained " + str(para.stamadj) + " stamina")
        elif para.stamadj < 0:
            print("You have lost " + str(para.stamadj) + " stamina")
    if stamina <= 0:
        status = "dead"
    elif stamina >= 1000:
        status = "completed"
    else:
        print("Current Stamina: " + str(stamina))
    return stamina

def printpara(para):
    paragraph = paradic[para]
    print(paragraph.text)

def chooseOptions(para):
    paraObject = paradic[para]
    optionCount = 0
    validOption = False
    for option in paraObject.optionList:
        optionCount += 1
        print(str(optionCount) + ") " + option[0])
    while validOption == False:
        choice = input("? ")
        try:
            intChoice = int(choice)
            paraChoice = paraObject.optionList[intChoice -1][1]
            validOption = True
        except:
            print("Must be an integer between 1 and " + str(optionCount))
    return paraChoice
    

class paragraph:
    def __init__(self, key, text, stamadj, optionList):
        self.key = key
        self.text = text
        self.stamadj = stamadj
        self.optionList = optionList

    def toString(self):
        print(self.key)
        print(self.text)
        print(self.stamadj)
        print(self.optionList)

main()

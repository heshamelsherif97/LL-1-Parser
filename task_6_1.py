import argparse

class terminal:
    def __init__(self, name):
        self.name = name
        self.productions = []
        self.first = []
        self.follow = []
        self.lla1 = {}

class Grammar:
    def __init__(self, parsed, input2):
        self.terminals = []
        self.input = input2
        self.ll1Ready = True
        self.inputCheck = True
        self.grammarVariables = []
        self.alphabet = []
        self.ll1Table = {}
        self.handleParse(parsed)
        self.handleAlpha()
        self.alphabet.append("$")
        self.initializeLL1()
        self.getLL1()
        self.checkLL1()
        self.printResult()

    def computeInput(self):
        stringInput1 = self.input[0]+" $"
        stringInput = stringInput1.split(" ")
        myStack = []
        myStack.append("$")
        myStack.append(self.terminals[0].name)
        i = 0
        while i < len(stringInput):
            print(myStack)
            s = stringInput[i]
            x = myStack.pop()
            if x == s:
                i+=1
            else:
                if x != "epsilon":
                    if x in self.grammarVariables:
                        if s in self.getTerminal(x).lla1:
                            if len(self.getTerminal(x).lla1[s]) == 0:
                                self.inputCheck = False
                                break
                            else:
                                prod = self.getTerminal(x).lla1[s][0]
                                stackIndex = len(myStack)
                                if prod == "epsilon":
                                    myStack.insert(stackIndex, "epsilon")
                                else:    
                                    for n in prod:
                                        myStack.insert(stackIndex, n)
                        else:
                            self.inputCheck = False
                            break
                    else:
                        self.inputCheck = False
                        break


    def checkLL1(self):
        check = True
        for i in self.terminals:
            for j in self.alphabet:
                if len(i.lla1[j]) > 1:
                    check = False
                    break
        self.ll1Ready = check


    def printResult(self):
        output_file = open("task_6_1_result.txt", "w+")
        if self.ll1Ready:
            for i in self.terminals:
                for j in self.alphabet:
                    write = ""
                    if len(i.lla1[j]) == 0:
                        write = i.name+" : "+j+" : "
                    else:
                        if i.lla1[j][0] != "epsilon":
                            write = i.name+" : "+j+" : "+" ".join(str(x) for x in i.lla1[j][0])
                        else: 
                            write = i.name+" : "+j+" : epsilon"
                    output_file.write(write + "\n")
            output_file2 = open("task_6_2_result.txt", "w+")
            self.computeInput()
            if self.inputCheck:
                output_file2.write("yes")
            else:
                output_file2.write("no")
        else:
            output_file.write("invalid LL(1) grammar")


    def initializeLL1(self):
        for i in self.terminals:
            for j in self.alphabet:
                i.lla1[j] = []

    def getLL1(self):
        for i in self.terminals:
            for f in i.first:
                if f != "epsilon":
                    for prod in i.productions:
                        letter = prod[0]
                        if f == letter:
                            i.lla1[f].append(prod)
                        else:
                            if letter in self.grammarVariables:
                                if f in self.getTerminal(letter).first:
                                    i.lla1[f].append(prod)
            if "epsilon" in i.first:
                for j in i.follow:
                    i.lla1[j].append("epsilon")
                

    def getTerminal(self, name):
        for i in self.terminals:
            if i.name==name:
                return i
        return ""

    def handleParse(self, parsed):
        for i in parsed:
            splitted = i.split(":")
            x = terminal(splitted[0].split(" ")[0])
            self.grammarVariables.append(x.name)
            x.first = self.removeEmpty(splitted[2].split(" "))
            x.follow = self.removeEmpty(splitted[3].split(" "))
            for u in splitted[1].split("|"):
                f = self.removeEmpty(u.split(" "))
                for q in f:
                    if q not in self.grammarVariables:
                        self.alphabet.append(q)
                x.productions+=[f] 
            self.terminals.append(x)

    def handleAlpha(self):
        self.alphabet = sorted(list(set(self.alphabet)))
        i = 0
        while i < len(self.alphabet):
            if self.alphabet[i] in self.grammarVariables:
                self.alphabet.remove(self.alphabet[i])
            else:
                i+=1
        for i in self.alphabet:
            if i == "epsilon":
                self.alphabet.remove(i)
        self.alphabet = sorted(list(set(self.alphabet)))

    def removeEmpty(self, x):
        newList =[]
        for i in x:
            if i!="":
                newList.append(i)
        return newList

def parseInput(x):
    newList = []
    for i in x:
        new = i.replace("\n", "")
        newList.append(new)
    return newList


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--grammar', action="store", help="path of file to take as input to read grammar", nargs="?", metavar="grammar")
    parser.add_argument('--input', action="store", help="path of file to take as input to test strings on LL table", nargs="?", metavar="input")
    
    args = parser.parse_args()
    lines = []
    with open(args.grammar, "r") as f:
        for line in f:
            lines.append(line)

    lines2 = []
    with open(args.input, "r") as f:
        for line in f:
            lines2.append(line)
       
    parsed = parseInput(lines)
    parsed2 = parseInput(lines2)
    Grammar(parsed, parsed2)   
    print(args.grammar)
    print(args.input)
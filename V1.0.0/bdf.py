from sys import *

class VariableManager:
    outputErrors = True

class BDF2:
    def __init__(*argv):
        try:
            VariableManager.outputErrors = argv[1]
        except IndexError:
            pass
        
    def getDF(self, *argvs):
        fileSrc = ""
        try:
            fileSrc = argvs[0]
        except IndexError:
            try:
                fileSrc = argvs[0]
            except IndexError:
                if VariableManager.outputErrors:
                    print("BDF Error: Could not find file specified")
                return False
        data = open(fileSrc, "r").read()    
        tokens = BDF2().CodeFunctions().tokenise(data)
        final = BDF2().CodeFunctions().parse(tokens)
        return final

    def findTable(self, data, tableName):
        try:
            return data[tableName][1:]
        except KeyError:
            if VariableManager.outputErrors:
                print("BDF Error: Not table called " + tableName + " found")
            return False

    def addNewRow(self, data, tableName, *contents):
        t = []
        tempTable = []
        dataToAdd = []
        currentRow = []
        currentRowLen = 0
        rows = 0
        cols = 0
        try:
           t = data[tableName]
           u = t[0]
           v = u[0]
           cols = t[0][0]
           rows = t[0][1]
        except KeyError:
            if VariableManager.outputErrors:
                print("BDF Error: No table called \"" + tableName + "\" found")
            return False
        for item in contents:
            if currentRowLen < cols:
                currentRow.append(item)
            else:
                dataToAdd.append(currentRow)
                currentRow = []
                currentRowLen = 0
                currentRow.append(tokens[i][5:-1])
            currentRowLen += 1
        if len(currentRow) > 0:
            while len(currentRow) < cols:
                currentRow.append("")
            dataToAdd.append(currentRow)
        for xtem in dataToAdd:
            data[tableName].append(xtem)
        return data

    def deleteRow(self, data, tableName, rowNumber):
        try:
            t = data[tableName]
        except KeyError:
            if VariableManager.outputErrors:
                print("BDF Error: No table called \"" + tableName + "\" found")
            return False
        del t[rowNumber]
        data[tableName] = t
        return data

    def write(self, filename, data, **kwargs):
        try:
            compressed = kwargs["compressed"]
        except KeyError:
            compressed = False
        cols = 0
        rowID = 0
        colID = 0
        currentData = []
        f = open(filename, "w+")
        for item in data:
            currentData = data[item]
            f.write("\""+item+"\" {")
            if not compressed:
                f.write("\n")
            for row in currentData:
                for obj in row:
                    if rowID == 0:
                        if not compressed:
                            f.write("\t")
                        if colID == 0:
                            cols = obj
                            toWrite = "cols="+str(cols)
                            if not compressed:
                                toWrite += "\n"
                            f.write(toWrite)
                            colID = 1
                        elif colID == 1:
                            toWrite = "rows="+str(obj)
                            if not compressed:
                                toWrite += "\n"
                            f.write(toWrite)
                            colID = 0
                            rowID = 1
                    else:
                        if colID == 0:
                            if not compressed:
                                f.write("\t")
                        if colID == cols:
                            if not compressed:
                                f.write("\n\t")
                            colID = 0
                            rowID += 1
                        toWrite = "\""+str(obj)+"\""
                        if not compressed:
                            toWrite += " "
                        f.write(toWrite)
                        colID += 1
            if not compressed:
                f.write("\n}\n")
            else:
                f.write("}")
            colID = 0
            rowID = 0
            cols = 0
            currentData = []
        f.close()
    
    class CodeFunctions:
        def tokenise(self, data):
            data += " "
            inString = False
            curTok = ""
            tokens = []
            for char in data:
                if inString:
                    if char == "\"":
                        tokens.append("STR:"+curTok+"\"")
                        char = ""
                        curTok = ""
                        inString = False
                else:
                    if char == "\t":
                        char = ""
                    elif char == "{":
                        char = "LB"
                    elif char == "}":
                        char = "RB"
                    elif char == "\"" or char == "\n" or char == " ":
                        if len(curTok) > 0:
                            tokens.append(curTok)
                            curTok =""
                        if char == "\"":
                            inString = True
                        else:
                            char = ""
                curTok += char
            return tokens

        def parse(self, tokens):
            inTable = False
            tableName = ""
            tableCols = 0
            tableRows = 0
            currentRowLen = 0
            currentData = {}
            currentTable = []
            currentRow = []
            i = 0
            while i < len(tokens):
                if not inTable:
                    if tokens[i][:4] == "STR:":
                        tableName = tokens[i][5:-1]
                        i += 1
                    else:
                        if tableName != "":
                            if tokens[i] == "LB":
                                inTable = True
                                i += 1
                        else:
                            i += 1
                else:
                    if tokens[i][:5].upper() == "COLS=":
                        tableCols = int(tokens[i][5:])
                        i += 1
                    elif tokens[i][:5].upper() == "ROWS=":
                        tableRows = int(tokens[i][5:])
                        i += 1
                    elif tokens[i][:4] == "STR:":
                        if len(currentTable) == 0 and len(currentRow) == 0:
                            currentTable.append([tableCols, tableRows])
                        if currentRowLen < tableCols:
                            currentRow.append(tokens[i][5:-1])
                        else:
                            currentTable.append(currentRow)
                            currentRow = []
                            currentRowLen = 0
                            currentRow.append(tokens[i][5:-1])
                        currentRowLen += 1
                        i+= 1
                    elif tokens[i] == "RB":
                        if len(currentRow) > 0:
                            currentTable.append(currentRow)
                        currentData[tableName] = currentTable
                        inTable = False
                        tableName = ""
                        tableCols = 0
                        tableRows = 0
                        currentRowLen = 0
                        currentTable = []
                        currentRow = []
                        i += 1
            return currentData

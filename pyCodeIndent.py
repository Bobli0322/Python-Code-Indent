import sys, os
#file = open("testProc1.py", 'r')
#fileStr = file.read()
#lineNum = 0
#tempStr = ''
#strList = []
#Begin0 = []
#End0 = []
#delim0 = "#0"
#Indent0 = "    "

##Issue:
##- (Fixed)Problem with beginning marker on the same line as end marker
##- Does not ignore block of code commented out ''' ..... '''
##
##Indentation hints
##-#{0 <...code...> #}0
##Good - if a == 0:#{0
##	    pass
##	 #}0
##	 continue
##Bad -  if a == 0:#{0
##	    pass
##	 continue
##	 #}0
##Cython static type hints
##key = 0, val = 0 ///int(key,val)
##
##Commented out lines to be ignored start with '##'

class indent:#{0
    def __init__(self, fileName):#{1
        self.file = open(fileName, 'r')
        self.fileStr = self.file.read()
        self.strList = []
        self.beginM = []
        self.endM = []
        self.indentStr = "    "
        self.level = 0
        tempStr = ''
        for i in range(len(self.fileStr)):#{2
            if self.fileStr[i] != '\n':#{3
                tempStr+=self.fileStr[i]
            #}3
            else:#{3
                #lstrip() remove space, tab and newline chars at beginning of string
                tempStr = tempStr.lstrip() 
                self.strList.append(tempStr + '\n')
                tempStr = ''
            #}3
        #}2
        #print(self.strList)
        #Each element in strList is one line with not indentation
        for i in range(len(self.strList)):#{2
            chkStr = self.strList[i]
            if chkStr[0] == '#' and chkStr[1] == '#':#{3
                continue
            #}3
            else:#{3
                delim = "#{"+str(self.level)
                while delim in self.strList[i]:#{4
                    self.level = self.level + 1
                    delim = "#{"+str(self.level)
                #}4
            #}3
        #}2
        for i in range(self.level):#{2
            begin0 = []
            end0 = []
            for c in range(len(self.strList)):#{3
                chkStr = self.strList[c]
                #print(chkStr)
                if chkStr[0] == '#' and chkStr[1] == '#':#{4
                    continue
                #}4
                else:#{4
                    tempBegin = "#{" + str(i)
                    tempEnd = "#}" + str(i)
                    if tempBegin in self.strList[c]:#{5
                        begin0.append(c)
                    #}5
                    if tempEnd in self.strList[c]:#{5
                        end0.append(c)
                    #}5
                #}4
            #}3
            self.beginM.append(begin0)
            self.endM.append(end0)
        #}2
    #}1
    def indent4Spaces(self):#{1
        for c in range(len(self.beginM)):#{2
            for i in range(len(self.beginM[c])):#{3
                beginLine = self.beginM[c][i]
                endLine = self.endM[c][i]
                #print(str(beginLine))
                #print(str(endLine))
                for d in range(beginLine+1, endLine):#{4
                    newStr = self.indentStr + self.strList[d]
                    self.strList[d] = newStr
                #}4
            #}3
        #}2
    #}1
    def checkSemantics(self):#{1
        for i in range(len(self.beginM)):#{2
            if len(self.beginM[i]) != len(self.endM[i]):#{3
                return False
            #}3
        #}2
        return True
    #}1
#}0
#inherent indent class and make use of level0 beginM and endM
class cythonise(indent):#{0
    def __init__(self, fileName):#{1
        super().__init__(fileName)
        self.intList = {}
        tempList = []
        for i in range(len(self.beginM[0])):#{2
            lineNum = self.beginM[0][i]+1
            while lineNum < self.endM[0][i]:#{3
                #print(self.strList[lineNum])
                if "///" in self.strList[lineNum]:#{4
                    tempStr = self.strList[lineNum].split("///")
                    tempStr = tempStr[1]
                    #print(tempStr)
                    ret = tempStr.find("int")
                    if ret != -1:#{5
                        intStr = tempStr[ret+4:tempStr.find(')')]
                        #print(intStr)
                        for k in intStr.split(','):#{6
                            tempList.append(k)
                        #}6
                    #}5
                #}4
                lineNum = lineNum + 1
            #}3
            listStr = ','.join(tempList)
            self.intList[self.beginM[0][i]] = listStr
            tempList.clear()
        #}2
    #}1
    #cdef int
    #This function increases total line number
    #It must be done after indent function
    def declareVar(self):#{1
        c = 0
        for k,v in self.intList.items():#{2
            if v != '':#{3
                insertStr = "    cdef int " + v + '\n'
                self.strList.insert(k+c+1, insertStr)
                c = c + 1
            #}3
        #}2
    #}1
#}0

if __name__ == '__main__':#{0
    print('Auto indent python code')
    cwd = os.getcwd()
    if cwd[0] == '/':#{1
        delim = '/'
    #}1
    else:#{1
        delim = '\\'
    #}1
    t = sys.argv
    for i in t:#{1
        print(i)
    #}1
    tarFile = str(t[1])
    if len(t) > 2:#{1
        print('Please one file at a time')
        quit()
    #}1
    if len(t) == 1:#{1
        print('Please input file name as argument')
        quit()
    #}1
    tt = tarFile.split('.')
    if tt[len(tt)-1] != 'py':#{1
        print('This program only works on Python code')
        quit()
    #}1
    #tt.insert(len(tt)-1, '_ind')
    tt[len(tt)-2] = tt[len(tt)-2] + '_ind'
    oFile = '.'.join(tt)
    fPath = cwd + delim + tarFile
    if not os.path.isfile(fPath):#{1
        print('Specified file does not exist in current directory')
        quit()
    #}1
    #obj = cythonise(str(t[1])) #for code to be compiled with Cython
    obj = indent(tarFile)
    '''
    print("Total levels of indentations: " + str(obj.level))
    print("Begin marks: " + str(obj.beginM))
    print(str(len(obj.beginM)))
    print("End marks: " + str(obj.endM))
    print(str(len(obj.endM)))
    print("Total lines: " + str(len(obj.strList)))
    print(obj.intList)
    '''
    if obj.checkSemantics() == False:#{1
        print("There must be equal amount of begin marks and end marks")
    #}1
    else:#{1
        obj.indent4Spaces()
        #obj.declareVar() #for code to be compiled with Cython
        output = ''.join(obj.strList)
        #print(output)
        #oFile = 'newProc1.py'
        newFile = open(oFile, 'w') #overwrite as well, for appending use 'a'
        newFile.write(output)
        newFile.close()
        print('Indentation of ' + t[0] + ' completed')
        print('Formatted code written to: ' + oFile)
        #fileStr = fileStr.replace('    ', '')
        #print(fileStr)
    #}1
#}0

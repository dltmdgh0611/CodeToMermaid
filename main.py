import os
from treelib import node, tree

filelist = []
linelist = []
ConnectInfolist = []
Classlist = []
Mermaidcode = []
tinymode = True

def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        filelist.append(full_filename)


def ReadallFile(filelist):
    for file in filelist:
        f = open(file, 'r', encoding="UTF-8")
        while True:
            line = f.readline()
            if not line : break
            if line.find("\n"):
                line = line.replace("\n","")
            linelist.append(line)
        f.close()

def cutName(line):
    cut = line.split(' ')
    for count, c in enumerate(cut):
        if c == "class" or c=="interface":
            return cut[count+1]

def recordinterfaceargs(line):
    line = line.replace(";","")
    pieceline = (list)(line.split(" "))
    for count, piece in enumerate(pieceline):
        if piece != "":
            pieceline.append("* "+pieceline[count])
            del pieceline[count]
            line = ' '.join(pieceline)
            break
    return line

def recordclassargs(line):
    line = line.replace(";","")
    try:
        line = line[:line.index('=')-1]
    except:
        pass

    line = line.replace('static ','')
    line = line.replace('override ','')
    line = line.replace('virtual ','')
    line = line.replace('delegate ','')
    line = line.replace('public','+')
    line = line.replace('private', '-')
    line = line.replace('protected', '#')
    line = line.replace('internal', '~')
    print(line)
    pieceline = (list)(line.split(" "))
    for count, piece in enumerate(pieceline):        
        if len(piece) > 1:
            if ")" in ''.join(pieceline):            
                pieceline.append("* "+pieceline[count])                
                del pieceline[count]
                break
    

    pieceline = list(filter(('').__ne__, pieceline ))
    
    if pieceline[0] != '+' and pieceline[0] !='-' and pieceline[0] !='~' and pieceline[0] !='#':
        pieceline.insert(0,'-')

    if len(pieceline) == 2 :
        return ""

    pieceline[1] = pieceline[0]+pieceline[1]
    pieceline[0] = "    "


    line = ' '.join(pieceline)
    return line

def AnalysisCode(linelist):
    depth = 0
    interfacestart = False
    readlineflag = False
    classStart = False
    for line in linelist:
        
        if "{" in line:
            if "," and ";" and "}" not in line:
                depth += 1
                if interfacestart:
                    readlineflag = True
                    continue
                if classStart:
                    readlineflag = True
                    continue

        elif "}" in line:
            if "," and ";" and "{" not in line:
                depth -= 1
                if interfacestart:
                    readlineflag = False
                    interfacestart = False
                    Mermaidcode.append("}\n")
                if classStart:
                    if depth == 1:
                        readlineflag = False
                        classStart = False
                        Mermaidcode.append("}\n")
        
        print(line, depth)

        if "interface" in line:
            Mermaidcode.append("class " + cutName(line) + "{")
            Classlist.append(cutName(line))
            Mermaidcode.append("<<interface>>")
            interfacestart = True

        if "class" in line:
            Mermaidcode.append("class " + cutName(line) + "{")
            Classlist.append(cutName(line))
            classStart = True
            try: 
                code = line[line.index(':')+2:]
                code = code.split(' ')
                for c in code :
                    if c != "":
                        ConnectInfolist.append(c + "<|--" +cutName(line) + ": Inheritance")
            except : pass

            if "abstract" in line:
                Mermaidcode.append("<<abstract>>")
            elif "public" in line: 
                Mermaidcode.append("<<public>>")
            else :
                Mermaidcode.append("<<private>>")
            
            
        if readlineflag:
            if "/" not in line:
                if interfacestart: 
                    Mermaidcode.append(recordinterfaceargs(line))
                elif classStart:
                    if depth == 2:
                        if "}" and "\n" not in line:
                            if "(" in line:
                                Mermaidcode.append(recordclassargs(line))

def AnalysisConnect():
    currentClass=""
    code = []
    for codeline in Mermaidcode:
        if "{" in codeline:
            for lineclass in Classlist:
                code = codeline.replace("{","").split(" ")
                if lineclass == code[1]:
                    currentClass = lineclass
                else: currentClass
        else :
            for lineclass in Classlist:
                code = codeline.split(" ")
                code = list(filter(('').__ne__, code))
                try:
                    code[0] = code[0].replace("+","").replace("-","").replace("~","").replace("#","")
                    if lineclass == code[0]:
                        if lineclass != currentClass:
                            ConnectInfolist.append(currentClass + "-->" + lineclass)
                except : pass
    
    for count, i in enumerate(ConnectInfolist):
        code = i
        ConnectInfolist[count] = ConnectInfolist[count].replace(",","")
        try:
            ConnectInfolist[count] = ConnectInfolist[count][:ConnectInfolist[count].index('<')] + ConnectInfolist[count][ConnectInfolist[count].index('>')+1:]
        except: pass


def makeshortmethod():
    for i, code in enumerate(Mermaidcode):
        if "(" and ")" in code:
            print("method")
            Mermaidcode[i] = code[:code.index('(')+1] + code[code.index(')'):] 
            
        

def WriteMermaid(path):
    f = open(path, 'w', encoding="UTF-8")
    f.writelines("## 제목을 입력하세요...\n")
    f.writelines("```mermaid\n")
    f.writelines("classDiagram\n")
    for code in Mermaidcode:
        f.writelines(code + "\n")
    
    for CI in ConnectInfolist:
        f.writelines(CI + "\n")

search("g:/autobot/CStoMermaid/codelist/")

ReadallFile(filelist)

AnalysisCode(linelist)

AnalysisConnect()

if tinymode:
    makeshortmethod()

for i in ConnectInfolist:
    print(i)

WriteMermaid("g:/autobot/CStoMermaid/result.md")
def relativos8():
    rel = []
    archivo = open("TABOP.txt")
    for linea in archivo:
        l = linea.split("|")
        if l[2] == "REL" and l[6].split("\n")[0] == "2":
            rel.append(l[0])
    archivo.close()
    return rel

def relativos16():
    rel = []
    archivo = open("TABOP.txt")
    for linea in archivo:
        l = linea.split("|")
        if l[2] == "REL" and l[6].split("\n")[0] == "4":
            rel.append(l[0])
    archivo.close()
    return rel
def tohex(val, nbits):
    var = hex((val + (1 << nbits)) % (1 << nbits))
    return var[2:]

def convertirOperandoHex(operando):
    if(operando[0].isdigit()):
        return int(operando)
    simbolo = operando[0]
    operando = operando[1:]
    if(simbolo == "$"):
        return int(operando, 16)
    elif(simbolo == "@"):
        return int(operando, 8)
    elif(simbolo == "%"):
        return int(operando, 2)

def convertirOperando(operando):
    if(operando[0] == "#"):
        operando = operando[1:]
    if(operando[0].isdigit()):
        return int(operando)
    simbolo = operando[0]
    operando = operando[1:]
    if(simbolo == "$"):
        return int(operando, 16)
    elif(simbolo == "@"):
        return int(operando, 8)
    elif(simbolo == "%"):
        try:
            return int(operando, 2)
        except:
            print("")

def validaCobop(conloc, op, cop):
    try:
        conloc = int(conloc, 16)
        op = convertirOperando(op)
        res = op-conloc
        print(res)
        if(len(cop.split()) == 2):
            if(res > -128 and res < 127):
                return str(tohex(res, 8).zfill(2))
            else:
                return str("rr rr")
        elif(len(cop.split()) == 3):
            if(res > -32768 and res < 65535):
                return str(tohex(res, 16).zfill(4))
            else: 
                return ("rr rr rr") 
        elif(len(cop.split()) == 4):
            if(res > -32768 and res < 32767):
                return str(tohex(res, 16).zfill(4))
            else: 
                return ("rr rr rr rr")                                    
    except:
        pass

def validaTabsim(op):
        tab = open("TABSIM.txt", "r")
        for linea in tab:
            l = linea.split()			
            if(l[0] == op):
                return l[1]
        tab.close()
        return ""

def cobop(patoDonald, dir):
    tabop = open("TABOP.txt", "r")
    for goofy in tabop:
        l = goofy.split("|")
        if(patoDonald == l[0] and dir == l[2]):
            return l[3]
    tabop.close()
if('BNE' in relativos8()):
    print("Simon")


from funciones import *
#-----------------------------------------------Mnemonicos-------------------------------------------------------------------------

mnemonico = ['ORG','equ','EQU','LDAA','SWI','DS.b','sWI','sWi','BRA','ADCA','ABA','LBRA','db', 'dc.b', 'fcb','DB', 'DC.B', 'FCB','dw', 'dc.w', 'fdb','DW', 'DC.W', 'FDB','DS','DS.B','RMB','DS.W','RMW','fcc','FCC', 'BSZ', 'bsz', 'ZMB', 'zmb','FCB','fcb',
'end', 'END','FILL','fill', 'ADDD','addd','adda','ADDA','addb','ADDB','ANDA','anda','ANDB','andb','andc','ANDC','ASL','asl','asla','ASLA','aslb','ASLB','asld','ASLD','asr','ASR','asra','ASRA','asrb','ASRB','BCC','bcc','bclr','BCLR','bcs','BCS','BEQ','beq','BGE','bge','BGND','bgnd',
'Jmp','JMP','jsr','JSR','ldaa','LDAA','LDAB','ldab','lddd','LDDD','LBCC','lbcc','lbcs','LBCS','LBEQ','lbeq','lbge','LBGE','lbgt','LBGT','LBHI','lbhi','LBHS','lbhs','lble','LBLS', 'START','start','ZMB','zmb','BNE','bne','bcs','BCS','LBNE','lbne',]
mnem=len(mnemonico)
conloc=0
cont=0
#hola mundo
#-------------------------------------------------------------------------------------------------------------------

archivo=open('entrada.asm','r')
inst=open('salida.lst','w')


err=open('P4ASM.txt','w')

bandera=0

caracteres=['|','!','#','$','%','&','/','(',')','=','¡','¿',';','.',':','-','{','[','+','*',']','}']
caracterescodop=['|','!','#','$','%','&','/','(',')','=','¡','¿',';',':','-','{','[','+','*',']','}']
caracter=['!','&','/','(',')','=','?','{','}','¡','.','¿']


def tamDis(cadena):
    return "{:<15}".format(cadena)
inst.write(tamDis('CONTLOC')+tamDis('ETQ')+tamDis('CODOP')+tamDis('OPER')+tamDis('MODOS')+tamDis('COP'))
inst.write('\n.................................................\n')

def directivasBW(direct, op):
    global conloc
    res = ""
    if(direct == "DC.B"):
        if(op == ""):
            return "00"
        op = op.split(",")
        for var in op:
            if(var.isdigit()):
                num = convertirOperando(var)
                res += tohex(num, 8).zfill(2) + " "
            else:
                car = var[1:]
                res += hex(ord(car))[2:] + " "
        return res
    elif(direct == "DC.W"):
        if(op == ""):
            return "00 00"
        op = op.split(",")
        for var in op:
            if(var.isdigit()):
                num = convertirOperando(var)
                res += tohex(num, 16).zfill(4) + " "
            else:
                car = var[1:]
                res += hex(ord(car))[2:].zfill(4) + " "
        return res
    elif(direct == "FCC"):
        if(op == ""):
            return ""
        if(op[0] == "/" and op[len(op) - 1] == "/"):
            op = op[1:len(op)-1]
            for var in op:
                res += hex(ord(var))[2:] + " "
            return res
    elif(direct == "FCB"):
        if(op == ""):
            return "00"
        op = op.split(",")
        for var in op:
            if(var.isdigit()):
                num = convertirOperando(var)
                res += tohex(num, 8).zfill(2) + " "
            else:
                car = var[1:]
                res += hex(ord(car))[2:] + " "
        return res
    elif(direct == "BSZ" or direct == "ZMB"):
        if(op == ""):
            return ""
        num = convertirOperando(op)
        for i in range(num):
            res += "00 "
            i
        return res
    elif(direct == "FILL"):
        if(op == ""):
            return ""
        elif(len(op.split(",")) != 2):
            return ""
        op = op.split(",")
        for i in range(int(op[1])):
            res += op[0].zfill(2) + " "
        return res
    return ""

def conloco(codop,operando,etiqueta, op):
    global conloc
    Dir = ["ORG", "END", "EQU", "START", "BSZ", "FILL", "ZMB", "org", "end", "equ", "start", "bsz", "fill", "zmb"]
    rel8 = relativos8()
    rel16 = relativos16()
    if (codop == "DC.B" or codop == "DC.W" or codop == "FCC" or codop == "FCB" or codop == "FILL" ):
        pass
    else:
        operando = str(convertirOperando(operando))
    if (codop=='ORG' or codop=='org') and operando!='NULL':
        conloc=int(operando)
    DirectivasdeconstantesDeunbyte=['db', 'dc.b', 'fcb','DB', 'DC.B', 'FCB']#incrementa 1 el conloc
    DirectivasdeconstantesDedosbytes=['dw', 'dc.w', 'fdb','DW', 'DC.W', 'FDB']#incrementa 2 elconloc
    #fcc incrementa el conloc con la longitud del operando
    DirectivasdereservadeespacioenmemoriaDeunbyte=['DS','DS.B','RMB']#Incrementa el CONTADOR DE LOCALIDADES con el valornumérico del OPERANDO
    DirectivasdereservadeespacioenmemoriaDedosbyte=['DS.W','RMW']#Incrementa el CONTADOR DE LOCALIDADES con eldoble del valor numérico del OPERANDO
    if codop in DirectivasdeconstantesDeunbyte:
        if(operando == 'NULL'):
            conloc+=1
        else:
            conloc += len(operando.split(",")) 
    elif codop in DirectivasdeconstantesDedosbytes:
        if(operando == 'NULL'):
            conloc+=2
        else:
            conloc += len(operando.split(",")) * 2		
    elif codop=='FCC' or codop=='fcc':
        if(operando == 'NULL'):
            conloc +=1
        else:
            long = len(op.split())
            conloc += long
    elif codop == "BSZ" or codop == "ZMB":
        if(operando == 'NULL'):
            conloc +=1
        else:
            conloc += int(operando)
    elif codop == 'FILL':
        if(operando == 'NULL'):
            conloc +=1
        else:
            conloc += int(operando.split(",")[1])
    elif codop == "JMP":
        conloc += 3
    elif codop in rel8:
        conloc += 2
    elif codop in rel16:
        conloc += 4
    elif codop == "START":
        conloc = 0
    elif codop in DirectivasdereservadeespacioenmemoriaDeunbyte and operando!='NULL':
        if '#' in operando:
            conloc+=int(operando[1:len(operando)-1])
        elif '$' in operando:
            conloc+=hex(operando[1:len(operando)-1])
        elif '%' in operando:
            conloc+=bin(operando[1:len(operando)-1])
        elif '@' in operando:
            conloc+=oct(operando[1:len(operando)-1])
        else:
            conloc+=int(operando)
            

    elif codop in DirectivasdereservadeespacioenmemoriaDedosbyte and operando!='NULL':
        if '#' in operando:
            conloc+=int(operando[1:len(operando)-1])*2
        elif '$' in operando:
            conloc+=int(hex(operando[1:len(operando)-1]))*2
        elif '%' in operando:
            conloc+=int(bin(operando[1:len(operando)-1]))*2
        elif '@' in operando:
            conloc+=int(oct(operando[1:len(operando)-1]))*2
        else:
            conloc+=int(operando)*2
    
    elif codop in Dir:
        pass
    else:
        try:
            if(len(op.split()) == 2):
                conloc += 2
            elif(len(op.split()) == 3):
                conloc += 3
        except:
            pass
    return hex(conloc).split('x')[1].zfill(16)

def direccionamiento(codop,operando):
    centin=0
    #print codop+operando
    if '%' in operando:
        f=operando.strip('%')
        for x in range(len(f)):
            if f[x]=='1' or f[x]=='0':
                centin+=1
        if centin==len(f):
            cad=str('0b')+f
            if int(cad,2)<=255:
                return 'DIR'
            else:
                return 'EXT'


    if codop in relativos8():
        return 'REL'
    if codop in relativos16():
        return 'REL'
    if codop == "JMP":
        return 'EXT'
    if codop=='ORG':
        return ''
    if codop == 'EQU':
        return ''
    if (codop == "DC.B" or codop == "DC.W" or codop == "FCC" or codop == "FCB" or codop == "FILL" or codop == "BSZ" or codop == "START"):
        return ''
    if operando.isdigit() and codop!='ORG' and int (operando)<=255:
        return 'DIR'
    if operando.isdigit() and codop!='ORG' and int (operando)>65545:
        return ''
        
    if operando.isdigit() and codop!='ORG' and int (operando)>255:
        return 'EXT'
        

    if operando=='NULL' and codop!='END':
        
        return 'INH'
        #print
    #if '#@' in operando or '#%' and operando[2:len(operando)].isdigit() and operando>65545:
    #	return 'IMM8' 
    if '#' in operando:
        return 'IMM'
        #print 
    if (('$' in operando) or ('@' in operando) or ('%' in operando)) and (operando[1:len(operando)].isdigit()) and ((int (operando[1:len(operando)]))<=255)  :
        
        return 'DIR'
    if (('$' in operando) or ('@' in operando) or ('%' in operando)) and ((int ('0x'+str(operando[1:len(operando)]),16))<=255):
        
        return 'DIR'

    if (('$' in operando) or ('@' in operando) or ('%' in operando)) and (operando[1:len(operando)].isdigit()) and((int (operando[1:len(operando)]))>255) and((int (operando[1:len(operando)]))<=65545) and codop!='ORG'  :
        return 'EXT'
    if (('$' in operando) or ('@' in operando) or ('%' in operando)) and (operando[1:len(operando)].isdigit()) and((int (operando[1:len(operando)]))>255) and((int (operando[1:len(operando)]))>65545) and codop!='ORG'  :
        #print operando
        return ''
    if (('$' in operando) or ('@' in operando) or ('%' in operando)) and operando[1:len(operando)].isalnum() and (operando[1:len(operando)].isdigit()==False) and codop!='ORG':
        return 'EXT'
    
    if ('[' in operando == 0) and (']' in operando==0):
        centin=1
    if ',' in operando and centin==0 :
         
        OPERA=operando.split(',')
        if OPERA[0].isdigit():
        
            if int(OPERA[0]) <= 15 and int (OPERA[0]) >= -16 :
            
                return 'IDX'

            if (int(OPERA[0]) >= -256 and int (OPERA[0]) <= -17) or (int(OPERA[0]) >= 16) and (int(OPERA[0]) <= 255) : 
                
                return 'IDX1'
            if (int(OPERA[0]) >= 256 and int (OPERA[0]) <= 65545):
                
                return 'IDX2'
    if '-SP' in operando or '-sp' in operando:
        
        
            return 'IDX'
    if 'SP-' in operando or 'sp-' in operando:
        
            
            return 'IDX'

    if '+SP' in operando or '+sp' in operando:
        
        
            return 'IDX'
    if 'SP+' in operando or 'sp+' in operando:
        
            return 'IDX'
            
    if ('[' in operando) and (']' in operando):
        
        #print operando #muestra la cadena [455,X] para verificar
        inicial=operando.index('[')
        final=operando.index(']')
        #print 'inicial',inicial
        #print 'final',final
        ####quitamos [ ]    de   [455,X]
        ini=int(inicial)+1
        fin=int(final)
        nuevoOpera=operando[ini:fin]####opteniendo    455,x
        if ',' in nuevoOpera:
            descuartiza=nuevoOpera.split(',')##partimos por  ,   y optenemos    455  x
            #print descuartiza#muesta la lista partida
            if descuartiza[0].isdigit() :
                if int(descuartiza[0])>=0 and int (descuartiza[0])<=65545:
                    
                    return '[IDX2]'


    if( (operando=='A,X') or (operando=='A,Y') or (operando=='A,SP') or (operando=='A,PC') or (operando=='B,X') or (operando=='B,Y') or 		   (operando=='B,SP') or (operando=='B,PC') or (operando=='D,X') or (operando=='D,Y') or (operando=='D,SP') or (operando=='D,PC') ):
        
        return 'IDX'
            



    if((operando=='[D,X]') or(operando=='[D,Y]') or (operando=='[D,SP]') or (operando=='[D,PC]') ):
        
        return '[D,IDX]'

    if (operando.isalpha() or operando.isdigit())  and codop[0]=='L':
        
        return 'REL16'
    if codop=='BRA':
        
        return 'REL8'

    return ''

def errordeoperando(k,h):
    a=open('TABOP.txt','r')
    while True:
        linea2=a.readline()
        if not linea2:break
        p=linea2.split('|')

        if k==p[0] and p[1]=='NO' and h!='NULL':	
            ('el mnemonico '+k+' no debe llevar operando\n')
            return 'NO'

        if k==p[0] and p[1]=='SI' and h=='NULL':	
            print('el mnemonico '+k+' espera  un operando\n')

def errordekratoss(oper):
    for x in range (len(caracter)):
        if caracter[x] in oper:
            err.write('Formato de operando no válido para ningún modo de direccionamiento '+oper)
            err.write('\n')
            return 1

def errordekratoss2(oper):
    for x in range (len(caracter)):
        if caracter[x] in oper:
            return 1

def instruc(cont,linea):
    l=linea.split()
    for x in range(mnem):
        if mnemonico[x] in l:
            palabras=linea.split()

            if len(palabras)==1:
                print (str(cont)+'		'+	hex(conloc).split('x')[1].zfill(4)+'   NULL		'+mnemonico[x]+'			NULL'+'			'+str(direccionamiento(mnemonico[x],'NULL')))
                inst.write(tamDis(str(hex(conloc).split('x')[1])))
                inst.write(tamDis('NULL'))
                inst.write(tamDis(mnemonico[x]))
                inst.write(tamDis('NULL\n'))
                errordeoperando(mnemonico[x],'NULL')
                conloco(mnemonico[x],'NULL','NULL', "")
                
            elif len(palabras)==2:

                if palabras.index(mnemonico[x])==0:
                    inst.write(tamDis(str(hex(conloc).split('x')[1])))
                    estaEnTabsim = validaTabsim(palabras[1])
                    if(estaEnTabsim != ""):
                        palabras[1] = estaEnTabsim
                    cob = palabras[0]
                    dir = direccionamiento(palabras[0], palabras[1])
                    conloco(mnemonico[x],palabras[1],'NULL', cob)
                    cobopValidado = ""
                    if(cob == "DC.B" or cob == "DC.W" or cob == "FCC" or cob == "FCB" or cob == "BSZ" or cob == "ZMB" or cob == "FILL"):
                        cob = directivasBW(palabras[0], palabras[1])
                    else:
                        cob = cobop(cob, dir)
                        cobopValidado = validaCobop(hex(conloc).split('x')[1].zfill(4), palabras[1], cob)

                    longa=hex(conloc).split('x')[1].zfill(4)+'	NULL	'+str(palabras[0])+'		'+str(palabras[1])+'			'+str(direccionamiento(palabras[0],palabras[1]) + '			'+str(cob) + '		\t' + str(cobopValidado))
                    if str(direccionamiento(palabras[0],palabras[1]))=='' and mnemonico[x]!='ORG' and errordekratoss2(palabras[1])!=1:
                        err.write('Operando fuera de rango para direccionamiento fulanito de tal '+palabras[1])
                        err.write('\n')
                    print (longa)
                    
                    #errordekratoss(palabras[1])
                    
                    inst.write(tamDis('NULL'))
                    inst.write(tamDis(mnemonico[x]))
                    
                    if errordeoperando(palabras[0],palabras[1])!='NO':
                        inst.write(tamDis(str(palabras[1])))
                    
                    inst.write(tamDis(str(direccionamiento(palabras[0],palabras[1]))))
                
                    inst.write(tamDis(str(cob) + ' ' +tamDis(str(cobopValidado))))
                    inst.write('\n')
                    errordeoperando(palabras[0],palabras[1])

                    
                elif palabras.index(mnemonico[x])==1:
                    inst.write(tamDis(str(hex(conloc).split('x')[1])))
                    cob = palabras[1]
                    dir = direccionamiento(palabras[0], palabras[1])
                    cob = cobop(cob, dir)
                    conloco(mnemonico[x],palabras[1],'NULL', cob)
                    cobopValidado = validaCobop(hex(conloc).split('x')[1].zfill(4), palabras[1], cob)
                    #guardarTabsim(palabras[0], palabras[1], 'NULL')

                    longa=hex(conloc).split('x')[1].zfill(4)+'			'+str(direccionamiento(palabras[1],'NULL') + '			'+str(cob) + '		 \t' + str(cobopValidado))
                    if str(direccionamiento(palabras[1],'NULL'))=='' and mnemonico[x]!='ORG' and errordekratoss2('NULL')!=1:
                        err.write('Operando fuera de rango para direccionamiento fulanito de tal  de NULL')
                        err.write('\n')
                    print (longa)
                    
                    
                    inst.write(tamDis(str(palabras[0])))
                    
                    inst.write(tamDis(str(palabras[1])))
                    
                    inst.write(tamDis(str(direccionamiento(palabras[1],'NULL'))))
                    
                    inst.write(tamDis(str(cob) + ' ' +tamDis(str(cobopValidado))))
                    inst.write('\n')
                    errordeoperando(palabras[1],'NULL')
                    

                
            elif len(palabras)==3:
                estaEnTabsim = validaTabsim(palabras[2])
                inst.write(tamDis(str(hex(conloc).split('x')[1])))
                if(estaEnTabsim != ""):
                    palabras[2] = estaEnTabsim
                #guardarTabsim(palabras[0], palabras[1], palabras[2])
                cob = palabras[1]
                dir = direccionamiento(palabras[1], palabras[2])
                cobopValidado = ""
                conloco(mnemonico[x],palabras[2],palabras[0], cob)
                if(cob == "DC.B" or cob == "DC.W" or cob == "FCC" or cob == "FCB" or cob == "BSZ" or cob == "ZMB" or cob == "FILL"):
                    cob = directivasBW(palabras[1], palabras[2])
                else:
                    cob = cobop(cob, dir)
                    cobopValidado = validaCobop(hex(conloc).split('x')[1].zfill(4), palabras[2], cob)						
                pali=linea.split(mnemonico[x])#codo operando
                var=str(direccionamiento(palabras[1],palabras[2]))
                god=hex(conloc).split('x')[1].zfill(4)+'	'+pali[0]+'	'+mnemonico[x]+pali[1].strip('\n')+'		'+str(var)
                print (god)
                
                
                inst.write(tamDis(palabras[0]))
                
                inst.write(tamDis(mnemonico[x]))
                
                inst.write(tamDis(palabras[2]))
                
                inst.write(tamDis(str(cob)) + ' ' +tamDis(str(cobopValidado)) + '\n')

            
                #enbuscadelaverdad(pali[0])
                errordeoperando(mnemonico[x],pali[1].strip('\n'))
                

                #if str(direccionamiento(palabras[1],palabras[2]))=='' and mnemonico[x]!='ORG' and errordekratoss(palabras[2])!=1:
                #	err.write('Operando fuera de rango para direccionamiento fulanito de tal '+palabras[2])
                #	err.write('\n')
                    
#CrearTabsim
def crearTabsim():
  archivo=open('entrada.asm','r')
  tabsim=open('TABSIM.txt','w')
  tabsim.write('ETIQUETA 				VALOR')
  tabsim.write('\n-------------------------------------------')                 
  
  for linea in archivo:
    l=linea.split()
    for x in range(mnem):
        if mnemonico[x] in l:
            palabras=linea.split()
            if(len(palabras) == 1):
                conloco(mnemonico[x],'NULL','NULL', "")
                pass
            elif(len(palabras) == 2):
                if palabras.index(mnemonico[x])==0:
                    cob = palabras[0]
                    dir = direccionamiento(palabras[0], palabras[1])
                    cob = cobop(cob, dir)
                    conloco(mnemonico[x],palabras[1],'NULL', cob)
                elif palabras.index(mnemonico[x]) == 1:
                    tabsim.write('\n')
                    tabsim.write(tamDis(palabras[0]) + tamDis("$" +str(hex(conloc))[2:]))
                
                  
            elif(len(palabras) == 3):

                if palabras[1] == "EQU" or palabras[1] == "ORG":
                    op = "$"
                    tabsim.write('\n')
                    tabsim.write(tamDis(str(palabras[0])))
                    op += str(hex(convertirOperando(palabras[2]))[2:])
                    tabsim.write(tamDis(op))
                    
                else:
                    op = "$"
                    tabsim.write('\n')
                    tabsim.write(tamDis(str(palabras[0])))
                    
                    op += str(hex(conloc).split('x')[1].zfill(4))
                    tabsim.write(tamDis(op))
              

                cob = palabras[1]
                dir = direccionamiento(palabras[1], palabras[2])
                conloco(mnemonico[x],palabras[2],palabras[0], cob)
                    
  archivo.close()
  tabsim.close()

crearTabsim()
conloc=0    

while True:
    linea=archivo.readline()
    if not linea: break
    cont+=1
    instruc(cont,linea)
archivo.close()
inst.close()

#input()
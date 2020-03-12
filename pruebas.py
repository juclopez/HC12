archivo = open("TABOP.txt")
algo = open("algo.txt", "w")
for linea in archivo:
    arr = linea.split("|")
    if(arr[2] == "REL"):
        algo.write(linea)
algo.close()
archivo.close()
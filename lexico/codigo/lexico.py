import pandas as pd
# pandas es una libreria para poder leer el excel
tabla_identificadores = []
archivo = open("archivo_fuente.txt", "r")
matriz = pd.read_excel("nuevaMatriz.xlsx")

texto = ""
# se lee todo el documento txt y se almacena como string
for linea in archivo.readlines():
    texto += linea

texto = texto.replace("\n", "")

estados_finales = {
    100: "reconoce digito",
    101: "reconoce identificador",
    102: "comentario una linea",
    103: "comentario varias lineas",
    104: "reconoce string",
    105: "reconoce {",
    106: "reconoce { {",
    107: "reconoce }",
    108: "reconoce } }",
    109: "recnoce (",
    110: "reconoce ((",
    111: "reconoce :=:",
    112: "reconoce ::",
    113: "reconoce <:<",
    114: "reconoce <:=",
    115: "reconoc >:>",
    116: "reconoce >:=",
    117: "reconoce coma",
    118: "reconoce [",
    119: "reconoce ]",
    120: "reconoce ;",
    121: "reconoce =",
    122: "reconoce =:=",
    123: "reconoce +",
    124: "reconoce -",
    125: "reconoce *",
    126: "reconoce !",
    127: "reconoce ! =:=",
    128: "reconoce ||",
    129: "reconoce &&",
    130: "reconoce )",
    131: "reconoce ((",
    200: "error"
}

reservadas = ["define", "starting", "returning", "finishing", "int", "real", "string", "main", "whether", "elif", "else", "when", "since", "do", "print", "input",
              "fact", "power", "abs", "minimal", "maximal", "range", "or", "and", "not"]

# indica la posicion del caracter en el texto
caracter = 0
fila = 0
estado = 0
# lista auxiliar para comparar palabras reservadas,identificadores o numeros
contenido = []

indice = 0
while caracter < len(texto):
    # se recorre la matriz por las filas y comparando los caracteres
    # y checando por aparte el caso especial de la e
    estado = matriz.loc[fila, "digito" if texto[caracter].isdigit(
    ) else "letra" if texto[caracter].isalpha() and texto[caracter] != "e" else texto[caracter]]

    if estado in estados_finales:

        # estados finales números e identificadores
        if estado in [100, 101]:
            # verifica si el estado final es un identificador
            if estado == 101:
                if "".join(contenido) in reservadas:
                    print("Reconoce la palabra reservada",
                          f"'{''.join(contenido)}'")
                    caracter -= 1
                else:
                    print(estados_finales[estado], f"{''.join(contenido)}")
                    indice += 1
                    tabla_identificadores.append(
                        {"Indice": indice, "Identificador": f"{''.join(contenido)}", "Tipo-Dato": None, "Valor": None})
                    caracter -= 1

            # reconoce los numeros si es entero, decimal etc
            elif estado == 100:
                if "." not in f"{''.join(contenido)}" and "e" not in f"{''.join(contenido)}":
                    print("Número Entero", f"{''.join(contenido)}")
                if "." in f"{''.join(contenido)}" and "e" not in f"{''.join(contenido)}":
                    print("Numero Decimal", f"{''.join(contenido)}")
                if "e" in f"{''.join(contenido)}" and "." not in f"{''.join(contenido)}":
                    print("Número con notación", f"{''.join(contenido)}")
                if "." in f"{''.join(contenido)}" and "e" in f"{''.join(contenido)}":
                    print("Decimal con notacion", f"{''.join(contenido)}")
            else:
                print(estados_finales[estado])
                caracter -= 1
        else:
            print(estados_finales[estado])
        estado = fila = 0
        contenido = []
    else:
        fila = estado
        if texto[caracter] != " ":
            contenido.append(texto[caracter])
    caracter += 1

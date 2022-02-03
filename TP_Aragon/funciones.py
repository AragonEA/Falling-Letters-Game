from principal import *
from configuracion import *
from extras import*

import random
import math


def cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer):
    #elige una palabra de la lista, la carga en las 3 listas
    # y les inventa una posicion para que aparezca en la columna correspondiente

    palabra=random.choice(lista) #Elige aleatoriamente una palabra del lemario
    cantLetras=random.randint(0,len(palabra))
    cantLetras2=random.randint(cantLetras,len(palabra))

    for pos in range(len(palabra)):
        if flag.flagListaIzq: # Si la primera columna no esta anulada:
            if pos<cantLetras:  #las posiciones menores al numero random van a la primer columna
                listaIzq.append(palabra[pos])
                posicionesIzq.append([random.randint(1,252),0])

        if flag.flagListaMedio: # Si la segunda columna no esta anulada:
            if pos>=cantLetras and pos<=cantLetras2:  #las posiciones < al primer num random y > las seg van a la segunda columna
                listaMedio.append(palabra[pos])
                posicionesMedio.append([random.randint(273,520),0])

        if pos>cantLetras2: #las posiciones mayores al seg numero random van a la tercera columna
            listaDer.append(palabra[pos])
            posicionesDer.append([random.randint(538,780),0])


def bajar(lista, posiciones):
    # hace bajar las letras y elimina las que tocan el piso
    lugares = []
    for i in range(len(posiciones)):
        posicion = posiciones[i]
        posicion[1] += 10 # Velocidad a la que caeran las letras.
        if len(lista) > 0 and posicion[1] >= 500:
            lugares.append(i)
    lugares.reverse()
    for i in lugares:
        lista.pop(i)
        posiciones.pop(i)


def actualizar(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer):
##     llama a otras funciones para bajar las letras, eliminar las que tocan el piso y
##     cargar nuevas letras a la pantalla (esto puede no hacerse todo el tiempo para que no se
##     llene de letras la pantalla)

    i=random.randrange(0,10)
    if not i%2!=0 and i%3==0:
        cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer)

    segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

    if segundos > 40:
        bajar(listaIzq,posicionesIzq)
        bajar(listaMedio,posicionesMedio)
        bajar(listaDer,posicionesDer)
    else:     # Si los segundos son menor que 40, llama a velocidad para incrementar la velocidad de caida de las letras
       velocidad(listaIzq,posicionesIzq)
       velocidad(listaMedio,posicionesMedio)
       velocidad(listaDer,posicionesDer)

def Puntos(candidata):
    #devuelve el puntaje que le corresponde a candidata
    puntaje=0
    vocales="aeiou"
    consDificiles="jkqwxyz"
    for letra in candidata:
        if letra in vocales:
            puntaje+=1
        else:
            if letra in consDificiles:
                puntaje+=5
            else:
                puntaje+=2
    return puntaje


def procesar(lista, candidata, listaIzq, listaMedio, listaDerecha):
    #chequea que candidata sea correcta en cuyo caso devuelve el puntaje y 0 si no es correcta
    if esValida(lista, candidata, listaIzq, listaMedio, listaDerecha):
        return Puntos(candidata)
    else:
        return 0

def contieneTodasLasLetras(str,str2):
    for char in str2:
        if char not in str: return False
    return True

def esValida(lista, candidata, listaIzq, listaMedio, listaDerecha):
     #devuelve True si candidata cumple con los requisitos

    if candidata not in lista:
        return False

    if flag.flagListaIzq: # Si la lista izq se puede usar:
        if contieneTodasLasLetras(listaIzq,candidata):
            return True
        else:
            flag.flagListaIzq=False # Anula la columna izquierda porque no encontro la palabra completa en esta columna

    if not flag.flagListaIzq and flag.flagListaMedio: #Si la columna izq esta anulada y la columna medio no lo esta:
        if contieneTodasLasLetras(listaMedio+listaIzq,candidata):
            return True
        else:
            flag.flagListaMedio=False # Anula la columna del medio porque no encontro la palabra completa
            if contieneTodasLasLetras(listaDerecha+listaMedio,candidata): # Busca en la columna derecha como ultima opcion
                return True
            else:
                return False

    if not flag.flagListaIzq and not flag.flagListaMedio: # Si ya estan anuladas las columnas izq y medio
        if contieneTodasLasLetras(listaDerecha,candidata):
            return True
        else:
            return False


class flag():
    flagListaIzq=True
    flagListaMedio=True

####EXTRAS####

def velocidad(lista,posiciones):
    lugares = []
    segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

    if  segundos <40 and segundos > 15: #Si quedan 40seg restantes, la velocidad incrementa de 10 a 15 unidades
        for i in range(len(posiciones)):
            posicion = posiciones[i]
            posicion[1] += 15    # Velocidad a la que caerán las letras.
            if len(lista) > 0 and posicion[1] >= 500:
                lugares.append(i)

        lugares.reverse()

        for i in lugares:
            lista.pop(i)
            posiciones.pop(i)

    else:   #Si quedan menos de 15 segundos, la velocidad incrementa de 15 a 22 unidades
        for i in range(len(posiciones)):
            posicion = posiciones[i]
            posicion[1] += 22    # Velocidad a la que caeran las letras.
            if len(lista) > 0 and posicion[1] >= 500:
                lugares.append(i)

        lugares.reverse()

        for i in lugares:
            lista.pop(i)
            posiciones.pop(i)



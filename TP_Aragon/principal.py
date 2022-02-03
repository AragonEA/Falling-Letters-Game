#! /usr/bin/env python
import os, random, sys, math

import pygame
from pygame.locals import *

from configuracion import *
from funciones import *
from extras import *

#Funcion principal
def main():
        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        pygame.mixer.init()  #inicializa el modulo mixer
        musicaFondo=pygame.mixer.music.load("Sounds\Pokemon Song.mp3")#carga la musica de fondo
        pygame.mixer.music.set_volume(0.2) # selecciona el volumen
        pygame.mixer.music.play(3) #toma como parametro las veces que se va a reproducir y la reproduce

        #Preparar la ventana
        pygame.display.set_caption("Armar palabras...")
        screen = pygame.display.set_mode((ANCHO, ALTO))

        #tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        segundos = TIEMPO_MAX
        fps = FPS_inicial

        puntos = 0
        candidata = ""
        listaIzq = []
        listaMedio = []
        listaDer = []
        posicionesIzq = []
        posicionesMedio = []
        posicionesDer = []
        lista = []
        sonidoPuntos=pygame.mixer.Sound("Sounds\Good.wav") #guarda el sonido para los aciertos
        sonidoPuntos.set_volume(0.3) #le establece el volumen
        sonidoError=pygame.mixer.Sound("Sounds\Error.wav") #guarda el sonido para los errores
        sonidoError.set_volume(0.2) #le establece el volumen

        archivo= open("Lemario\lemario.txt","r")
        for linea in archivo.readlines():
            lista.append(linea[0:-1])

        cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer)
        dibujar(screen, candidata, listaIzq, listaMedio, listaDer, posicionesIzq ,
                posicionesMedio, posicionesDer, puntos,segundos)


        while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if True:
            	fps = 3

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():

                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()

                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letra = dameLetraApretada(e.key)
                    candidata += letra
                    if e.key == K_BACKSPACE:
                        candidata = candidata[0:len(candidata)-1]
                    if e.key == K_RETURN:
                        puntosCandidata=procesar(lista, candidata, listaIzq, listaMedio, listaDer)
                        puntos += puntosCandidata
                        candidata = ""
                        # Reproduce los efectos de sonido
                        if puntosCandidata!=0: #si candidata devuelve puntos
                            pygame.mixer.Sound.play(sonidoPuntos)
                        if puntosCandidata==0: #si candidata no devuelve puntos
                            pygame.mixer.Sound.play(sonidoError)

            segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, candidata, listaIzq, listaMedio, listaDer, posicionesIzq ,
                posicionesMedio, posicionesDer, puntos,segundos)

            pygame.display.flip()

            actualizar(lista, listaIzq, listaMedio, listaDer, posicionesIzq,
                posicionesMedio, posicionesDer)

        pygame.mixer.music.stop() # cuando el tiempo llega a 0 frena la musica

        while 1:
            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return


##Programa Principal ejecuta Main
if __name__ == "__main__":
    main()

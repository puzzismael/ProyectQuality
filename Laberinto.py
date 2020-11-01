from Cell import Celda
import random
import os

celdas = []  #posible solucion a celdas inddefinidas
Notvisited = []


def getRandomCell(lab):    
    return lab[random.randint( 0, lab.__len__()-1)][random.randint( 0, lab[0].__len__()-1)]

def menu():
	os.system('cls') 
	print ("Selecciona una opción")
	print ("\t1 - Generar Laberinto")
	print ("\t2 - Leer JSON")
	print ("\t3 - Salir")
 
def seleccionarOp(): 
	while True:
		menu()
		opcionMenu = input("Elige una opción: ")
 
		if opcionMenu == "1":
			print ("")
			lab = crearLaberinto()
			print(lab)
			 
		elif opcionMenu == "2":
			#leerJson()
			print ("")
			
		elif opcionMenu == "3":
			print("FIN")
			break
		
		else:
			print ("")
			input("No has pulsado ninguna opción correcta...\nPulsa una tecla para continuar")

def crearLaberinto():
	print("Dame el Nº de columnas: ")
	columnas = int(input())
	i=0

	print ("Dame el Nº de filas: ")
	filas = int(input())
		
	Laberinto = [[0] * filas for i in range(columnas)]
	for i in range(columnas):
		for j in range(filas):
			Laberinto[i][j] = Celda(i,j)
			Laberinto[i][j].getPosicion()
	Notvisited.append(Laberinto[0][0]) #posible warning
	return Laberinto

def obtenerVecinos(Celda, lab):
    posicion = Celda.pintarPosicion()

    vecinos = []
    vecinos.append(lab[posicion[0]-1,posicion[0]])
    vecinos.append(lab[posicion[0],posicion[0]+1])
    vecinos.append(lab[posicion[0]+1,posicion[0]])
    vecinos.append(lab[posicion[0],posicion[0]-1])

    return vecinos

def camino(Notvisited):
    
    posiblecamino = []
    celdaAux = getRandomCell(Notvisited)
    posiblecamino.append(celdaAux)

def getCamino(pila, columnas, filas): #BORRADOR
	while pila.length > 0:
		actual = pila[pila.length - 1]
		valid = False
		checks = 0

		while not valid and checks < 10:
			checks+1
			direccion = random.randint(0, 3)  

			#NORTE
			if direccion == 0:
				if actual.positionY > 0:
					next = celdas[actual.positionY - 1][actual.positionX]
				  
					if next.visited == False: 
						actual.norte = False
						next.sur = False

						next.visited = True
						pila.append(next)
						valid = True
		
			#ESTE
			if direccion == 1: 
				if actual.positionX < (columnas - 1): 
					next = celdas[actual.positionY][actual.positionX + 1]

					if next.visited == False: 
						actual.este = False
						next.oeste = False

						next.visited = True
						pila.append(next)
						valid = True
		
			#SUR
			if direccion == 2:
				if actual.positionY < (filas - 1): 
					next = celdas[actual.positionY + 1][actual.positionX]

					if next.visited == False: 
						actual.sur = False
						next.norte = False

						next.visited = True
						pila.append(next)
						valid = True

			#OESTE
			if direccion == 3:
				if actual.positionX > 0: 
					next = celdas[actual.positionY][actual.positionX - 1]

					if next.visited == False: 
						actual.oeste = False
						next.este = False

						next.visited = True
						pila.append(next)
						valid = True

		if valid == False: 
			pila.pop()    


#def visitar():

#Lista de celdas visitadas

print(seleccionarOp())

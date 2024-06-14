import random

class Mapa:
    def __init__(self, filas, columnas):
        self.mapa = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.filas = filas
        self.columnas = columnas
        self.fuegos = {}
        self.personas =  [] 
        self.generar_elementos()

    def generar_elementos(self):
        num_obstaculos = random.randint(5, 15)
        num_fuegos = random.randint(3, 7)
        num_personas = random.randint(1, 5)

        for _ in range(num_obstaculos):
            x, y = self.generar_coordenadas()
            self.mapa[x][y] = 'O'

        for _ in range(num_fuegos):
            x, y = self.generar_coordenadas()
            self.mapa[x][y] = 'F'
            self.fuegos[(x, y)] = random.randint(1, 5)

        for _ in range(num_personas):
            x, y = self.generar_coordenadas()
            self.mapa[x][y] = 'P'
            self.personas.append((x, y))

    def generar_coordenadas(self):
        while True:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)

            if self.mapa[x][y] == ' ':
                return x, y
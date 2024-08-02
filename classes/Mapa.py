import random

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.fuegos = {}
        self.personas = []
        self.obstaculos = []
        self.base = (0,0)
        self.mapa[0][0] = 'B'
        self.generar_obstaculos()
        self.generar_fuegos()
        self.generar_personas()

    def generar_obstaculos(self):
        cantidad_obstaculos = random.randint(5, 10)
        for _ in range(cantidad_obstaculos):
            while True:
                x, y = random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1)
                if self.mapa[x][y] == ' ' and (x, y) != (0, 0):
                    self.mapa[x][y] = 'O'
                    self.obstaculos.append((x, y))
                    break

    def generar_fuegos(self):
        cantidad_fuegos = random.randint(3, 7)
        for _ in range(cantidad_fuegos):
            while True:
                x, y = random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1)
                if self.mapa[x][y] == ' ':
                    self.mapa[x][y] = 'F'
                    self.fuegos[(x, y)] = random.randint(1, 2)
                    print(f"Fuego añadido en ({x}, {y}) con intensidad {self.fuegos[(x, y)]}")
                    break

    def generar_personas(self):
        cantidad_personas = random.randint(1, 5)
        for _ in range(cantidad_personas):
            while True:
                x, y = random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1)
                if self.mapa[x][y] == ' ':
                    self.mapa[x][y] = 'P'
                    self.personas.append((x, y))
                    break

    def es_posicion_valida(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.mapa[x][y] == ' '
    
    def actualizar_mapa(self, x, y, nuevo_valor):
        self.mapa[x][y] = nuevo_valor
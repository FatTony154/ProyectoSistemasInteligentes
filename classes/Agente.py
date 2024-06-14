import random

class Agente:
    def __init__(self, id, x, y, mapa):
        self.id = id
        self.x = x
        self.y = y
        self.mapa = mapa
        self.mapa_explorado = [['?' for _ in range(mapa.columnas)] for _ in range(mapa.filas)]
        self.mapa_explorado[x][y] = 'A'
        self.taCargao = True
        self.origen = (x, y)

    def mover(self):
        direcciones = ['norte', 'sur', 'este', 'oeste']
        random.shuffle(direcciones)
        encontrado = False

        for direccion in direcciones:
            nuevo_x, nuevo_y = self.x, self.y
            if direccion == 'norte' and self.x > 0:
                if self.mapa.mapa[self.x - 1][self.y] != 'O':
                    nuevo_x -= 1
            elif direccion == 'sur' and self.x < self.mapa.filas - 1:
                if self.mapa.mapa[self.x + 1][self.y] != 'O':
                    nuevo_x += 1
            elif direccion == 'este' and self.y < self.mapa.columnas - 1:
                if self.mapa.mapa[self.x][self.y + 1] != 'O':
                    nuevo_y += 1
            elif direccion == 'oeste' and self.y > 0:
                if self.mapa.mapa[self.x][self.y - 1] != 'O':
                    nuevo_y -= 1

            if self.es_movimiento_valido(nuevo_x, nuevo_y):
                self.x, self.y = nuevo_x, nuevo_y
                encontrado = True
                break

        if not encontrado:
            for i in range(self.mapa.filas):
                for j in range(self.mapa.columnas):
                    if self.mapa_explorado[i][j] == '?':
                        self.x, self.y = i, j
                        encontrado = True
                        break
                if encontrado:
                    break
                
        self.explorar()
        
    def es_movimiento_valido(self, x, y):
        if x < 0 or x >= self.mapa.filas or y < 0 or y >= self.mapa.columnas:
            return False
        if self.mapa.mapa[x][y] == 'O':
            return False
        return True

    def explorar(self):
        celda_actual = self.mapa.mapa[self.x][self.y]
        self.mapa_explorado[self.x][self.y] = celda_actual

        if celda_actual == 'F':
            self.apagar()
        elif celda_actual == 'P':
            self.report_persona()
        else:
            self.mapa_explorado[self.x][self.y] = ' '

    def apagar(self):
        if self.taCargao:
            if self.mapa.fuegos[(self.x, self.y)] > 1:
                self.mapa.fuegos[(self.x, self.y)] -= 1
            else:
                del self.mapa.fuegos[(self.x, self.y)]
                self.mapa.mapa[self.x][ self.y] = ' '
                self.mapa_explorado[self.x][self.y] = ' '
            self.taCargao = False
            self.x, self.y = self.origen
            self.taCargao = True
        else:
            self.x, self.y = self.origen
            self.taCargao = True

    def report_persona(self):
        self.mapa.personas.remove((self.x, self.y))
        self.mapa.mapa[self.x][self.y] = ' '
        self.mapa_explorado[self.x][self.y] = ' '
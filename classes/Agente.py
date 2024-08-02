import heapq
import random

mapa_explorado_global = []

fuegos_criticos = []

class Agente:
    
    colors = ['purple', 'blue', 'brown', 'orange']
    
    def __init__(self, id, x, y, mapa):
        self.id = id
        self.x = x
        self.y = y
        self.mapa = mapa
        self.mapa_explorado = [['?' for _ in range(mapa.columnas)] for _ in range(mapa.filas)]
        self.mapa_explorado[x][y] = 'A'
        self.taCargao = True
        self.origen = (0, 0)
        self.camino_recorrido = []
        self.fuego_actual = None
        self.persona_actual = None
        self.regresando = False
        self.camino_de_vuelta = []
        self.color = Agente.colors[id % len(Agente.colors)]
        self.ayudando = False
        self.llevando_persona = False
        self.personas_encontradas = []
        
        #Mapa compartido
        global mapa_explorado_global
        
        if not mapa_explorado_global:
            mapa_explorado_global = [['?' for _ in range(mapa.columnas)] for _ in range(mapa.filas)]
            mapa_explorado_global[x][y] = 'A'

    def mover(self):
        print(f"Agente {self.id} en posición ({self.x}, {self.y})")
        if self.regresando and self.camino_de_vuelta:
            print(f"Agente {self.id} regresando a la base")
            self.x, self.y = self.camino_de_vuelta.pop(0)
            if not self.camino_de_vuelta:
                self.regresando = False
                if not self.taCargao:
                    self.taCargao = True
                    if self.fuego_actual:
                        self.regresar_al_fuego()
                elif self.fuego_actual:
                    self.camino_de_vuelta = list(reversed(self.camino_recorrido))
        elif self.ayudando:
            print(f"Agente {self.id} ayudando a una persona")
            self.x, self.y = self.camino_de_vuelta.pop(0)
            if not self.camino_de_vuelta:
                self.ayudando = False
                return
        else:
            self.buscar_fuego_o_persona_cercana()
            if self.fuego_actual:
                print(f"Agente {self.id} moviéndose hacia fuego en {self.fuego_actual}")
                self.mover_hacia_objetivo(self.fuego_actual)
                if self.mapa.fuegos.get((self.x, self.y)) == 0:
                    self.fuego_actual = None
                    self.camino_de_vuelta = self.a_star((self.x, self.y), self.origen)
                    self.regresando = True
            elif self.persona_actual:
                print(f"Agente {self.id} moviéndose hacia persona en {self.persona_actual}")
                self.mover_hacia_objetivo(self.persona_actual)
            else:
                print(f"Agente {self.id} explorando")
                self.explorar()
        if self.fuego_actual and self.mapa.fuegos.get((self.x, self.y)) == 0:
            self.fuego_actual = None
            self.buscar_fuego_o_persona_cercana()

                
    def mover_hacia_objetivo(self, objetivo):
        print(f"Agente {self.id} moviéndose hacia {objetivo}")
        direcciones = ['norte', 'ur', 'este', 'oeste']
        random.shuffle(direcciones)
        encontrado = False

        for direccion in direcciones:
            nuevo_x, nuevo_y = self.x, self.y
            if direccion == 'norte' and self.x > 0:
                if self.mapa.mapa[self.x - 1][self.y] != 'O':
                    nuevo_x -= 1
            elif direccion == 'ur' and self.x < self.mapa.filas - 1:
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
                self.camino_recorrido.append((self.x, self.y))
                self.explorar()
                break

        if not encontrado:
            for i in range(self.mapa.filas):
                for j in range(self.mapa.columnas):
                    if self.mapa_explorado[i][j] == '?':
                        self.x, self.y = i, j
                        self.camino_recorrido.append((self.x, self.y))
                        break
                if encontrado:
                    break

        self.explorar()

    
    def calcular_distancia(self, pos):
        x, y = pos
        return abs(self.x - x) + abs(self.y - y)   
            
    def buscar_fuego_o_persona_cercana(self):
        print(f"Agente {self.id} buscando fuego o persona cercana")
        fuegos_cercanos = [(x, y) for x, y in self.mapa.fuegos.keys() if self.calcular_distancia((x, y)) < 5]
        personas_cercanas = [(x, y) for x, y in self.mapa.personas if self.calcular_distancia((x, y)) < 5]

        if fuegos_cercanos:
            fuego_mas_cercano = min(fuegos_cercanos, key=lambda x: self.calcular_distancia(x))
            print(f"Fuego más cercano encontrado en {fuego_mas_cercano}")
            self.camino_de_vuelta = self.a_star((self.x, self.y), fuego_mas_cercano)
            self.fuego_actual = fuego_mas_cercano
        elif personas_cercanas:
            persona_mas_cercana = min(personas_cercanas, key=lambda x: self.calcular_distancia(x))
            print(f"Persona más cercana encontrada en {persona_mas_cercana}")
            self.camino_de_vuelta = self.a_star((self.x, self.y), persona_mas_cercana)
            self.persona_actual = persona_mas_cercana

        
    def es_movimiento_valido(self, x, y):
        if x < 0 or x >= self.mapa.filas or y < 0 or y >= self.mapa.columnas:
            return False
        if self.mapa.mapa[x][y] == 'O':
            return False
        return True

    def explorar(self):
        global mapa_explorado_global
        celda_actual = self.mapa.mapa[self.x][self.y]
        self.mapa_explorado[self.x][self.y] = celda_actual
        mapa_explorado_global[self.x][self.y] = celda_actual

        if celda_actual == 'F':
            print(f"Agente {self.id} encontró un fuego en ({self.x}, {self.y})")
            self.apagar()
        elif celda_actual == 'P':
            self.report_persona()
        else:
            self.mapa_explorado[self.x][self.y] = ' '
            mapa_explorado_global[self.x][self.y] = ' '
            
    def apagar(self):
        if self.fuego_actual == (self.x, self.y) and (self.x, self.y) in self.mapa.fuegos:
            if self.taCargao:
                if self.mapa.fuegos[(self.x, self.y)] > 2:
                    self.solicitar_ayuda()
                elif self.mapa.fuegos[(self.x, self.y)] > 1:
                    print(f"Reduciendo intensidad del fuego en ({self.x}, {self.y}) de {self.mapa.fuegos[(self.x, self.y)]} a {self.mapa.fuegos[(self.x, self.y)] - 1}")
                    self.mapa.fuegos[(self.x, self.y)] -= 1
                else:
                    print(f"Extinguiendo el fuego en ({self.x}, {self.y})")
                    del self.mapa.fuegos[(self.x, self.y)]
                    self.extinguir_fuego(self.x, self.y)
                    self.fuego_actual = None
                self.taCargao = False
                self.regresar_al_origen_y_volver()
            else:
                print(f"El agente {self.id} necesita regresar a recargar antes de apagar el fuego")
                self.regresar_al_origen_y_volver()
        
    def extinguir_fuego(self, x, y):
        print(f"Fuego extinguido en ({x}, {y}) por agente {self.id}")
        if (x, y) in self.mapa.fuegos:
            del self.mapa.fuegos[(x, y)]
        self.mapa.mapa[x][y] = ' '
        self.mapa_explorado[x][y] = ' '
        mapa_explorado_global[x][y] = ' '
        self.mapa.actualizar_mapa(x, y, ' ')
        print(f"Mapa actualizado: {self.mapa.mapa}")
    
    def a_star(self, inicio, objetivo):
        def heuristica(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        fila_inicial, columna_inicial = inicio
        fila_objetivo, columna_objetivo = objetivo
        
        open_set = []
        heapq.heappush(open_set, (0, fila_inicial, columna_inicial))
        came_from = {}
        g_score = { (fila_inicial, columna_inicial): 0 }
        f_score = { (fila_inicial, columna_inicial): heuristica(inicio, objetivo) }
        
        while open_set:
            _, fila_actual, columna_actual = heapq.heappop(open_set)
            
            if (fila_actual, columna_actual) == objetivo:
                camino = []
                while (fila_actual, columna_actual) in came_from:
                    camino.append((fila_actual, columna_actual))
                    fila_actual, columna_actual = came_from[(fila_actual, columna_actual)]
                camino.reverse()
                return camino
            
            vecinos = [
                (fila_actual - 1, columna_actual), (fila_actual + 1, columna_actual),
                (fila_actual, columna_actual - 1), (fila_actual, columna_actual + 1)
            ]
            
            for vecino in vecinos:
                fila_vecino, columna_vecino = vecino
                if not self.es_movimiento_valido(fila_vecino, columna_vecino):
                    continue
                
                tentative_g_score = g_score[(fila_actual, columna_actual)] + 1
                
                if vecino not in g_score or tentative_g_score < g_score[vecino]:
                    came_from[vecino] = (fila_actual, columna_actual)
                    g_score[vecino] = tentative_g_score
                    f_score[vecino] = tentative_g_score + heuristica(vecino, objetivo)
                    if vecino not in [pos[1:] for pos in open_set]:
                        heapq.heappush(open_set, (f_score[vecino], fila_vecino, columna_vecino))
        
        return []
    
    def regresar_al_origen_y_volver(self):
        self.camino_de_vuelta = self.a_star((self.x, self.y), self.origen)
        self.regresando = True
        
    def regresar_al_fuego(self):
        if self.fuego_actual and self.fuego_actual in self.mapa.fuegos:
            if self.x == self.origen[0] and self.y == self.origen[1]:
                self.camino_de_vuelta = self.a_star(self.origen, self.fuego_actual)
                self.regresando = True

            
    def report_persona(self):
        self.mapa.personas.remove((self.x, self.y))
        self.mapa.mapa[self.x][self.y] = ' '
        self.mapa_explorado[self.x][self.y] = ' '
        self.personas_encontradas.append((self.x, self.y))
        mapa_explorado_global[self.x][self.y] = ' '
        
    def llevar_persona(self):
        self.llevando_persona = True
        self.camino_de_vuelta = self.a_star((self.x, self.y), self.origen)
        self.regresando = True
        
    def liberar_persona(self):
        self.llevando_persona = False
        self.mapa.personas.remove((self.x, self.y))
        self.mapa.mapa[self.x][self.y] = ' '
        self.mapa_explorado[self.x][self.y] = ' '
        mapa_explorado_global[self.x][self.y] = ' '

    def solicitar_ayuda(self):
        global fuegos_criticos
        if (self.x, self.y) not in fuegos_criticos:
            fuegos_criticos.append((self.x, self.y))
            
    def compartir_conocimiento(self):
        global mapa_explorado_global
        for i in range(self.mapa.filas):
            for j in range(self.mapa.columnas):
                if self.mapa_explorado[i][j] != '?':
                    mapa_explorado_global[i][j] = self.mapa_explorado[i][j]
        
        self.mapa_explorado = [row[:] for row in mapa_explorado_global]
        
    def actualizar_mapa(self):
        for x in range(self.filas):
            for y in range(self.columnas):
                self.mapa[x][y]
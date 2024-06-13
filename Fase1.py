from flask import Flask, render_template, jsonify
import random

app = Flask(__name__, template_folder='Templates')

# Mapa
class Mapa:
    def __init__(self, filas, columnas):
        self.mapa = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.filas = filas
        self.columnas = columnas
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

        for _ in range(num_personas):
            x, y = self.generar_coordenadas()
            self.mapa[x][y] = 'P'

    def generar_coordenadas(self):
        while True:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)

            if self.mapa[x][y] == ' ':
                return x, y

# Agente
class Agente:
    def __init__(self, x, y, mapa):
        self.x = x
        self.y = y
        self.mapa = mapa
        self.mapa_explorado = [['?' for _ in range(mapa.columnas)] for _ in range(mapa.filas)]
        self.mapa_explorado[x][y] = 'A'

    def mover(self):
        direcciones = ['norte', 'sur', 'este', 'oeste']
        random.shuffle(direcciones)

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

            if self.mapa.mapa[nuevo_x][nuevo_y] != 'O':
                self.x, self.y = nuevo_x, nuevo_y
                break

        self.explorar()

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
        self.mapa.mapa[self.x][self.y] = ' '
        self.mapa_explorado[self.x][self.y] = ' '

    def report_persona(self):
        self.mapa.mapa[self.x][self.y] = ' '
        self.mapa_explorado[self.x][self.y] = ' '

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_map_data')
def get_map_data():
    global agente
    agente.mover()
    return jsonify({
        'mapa': agente.mapa.mapa,
        'mapa_explorado': agente.mapa_explorado,
        'agente_pos': (agente.x, agente.y)
    })

if __name__ == '__main__':
    filas, columnas = 10, 10
    mapa = Mapa(filas, columnas)
    agente = Agente(0, 0, mapa)
    app.run(debug=True)

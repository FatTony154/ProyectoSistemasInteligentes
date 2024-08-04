from flask import Flask, render_template, jsonify
from classes.Mapa import Mapa
from classes.Agente import Agente

app = Flask(__name__, template_folder='Templates')

def crear_nuevo_juego():
    filas, columnas = 10, 10
    mapa = Mapa(filas, columnas)
    agentes = [Agente(i, 0, 0, mapa) for i in range(4)]
    juego_terminado = False
    return mapa, agentes, juego_terminado

mapa, agentes, juego_terminado = crear_nuevo_juego()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_map_data')
def get_map_data():
    global agentes, juego_terminado, mapa

    if not juego_terminado:
        for agente in agentes:
            agente.mover()

        for agente in agentes:
            agente.compartir_conocimiento()

        juego_terminado = not mapa.fuegos and not mapa.personas and all(agente.x == 0 and agente.y == 0 for agente in agentes)

        if juego_terminado:
            print("El juego ha terminado")
            for agente in agentes:
                agente.regresar_al_origen_y_volver()
    else:
        return jsonify({
            'message': 'El juego ha terminado'
        })
        
    return jsonify({
        'mapa': mapa.mapa,
        'agentes': [
            {
                'id': agente.id,
                'mapa_explorado': agente.mapa_explorado,
                'agente_pos': (agente.x, agente.y),
                'color': agente.color,
                'personas_encontradas': agente.personas_encontradas
            }
            for agente in agentes
        ],
        'juego_terminado': juego_terminado
    })

if __name__ == '__main__':
    app.run(debug=True)

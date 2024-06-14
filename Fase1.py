from flask import Flask, render_template, jsonify
from classes.Mapa import Mapa
from classes.Agente import Agente
import random

app = Flask(__name__, template_folder='Templates')

filas, columnas = 10, 10
mapa = Mapa(filas, columnas)
juego_terminado = False

if 'agentes' not in globals():
    agentes = [Agente(i, 0, 0, mapa) for i in range(4)]

def verificar_estado_juego(mapa):
    return not mapa.fuegos and not mapa.personas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_map_data')
def get_map_data():
    
    global agentes, juego_terminado
    
    if not juego_terminado:
        for agente in agentes:
            agente.mover()
        
        juego_terminado = verificar_estado_juego(mapa)
    
        if juego_terminado:
            for agente in agentes:
                agente.x, agente.y = agente.origen
            print("El juego ha terminado")
    
    return jsonify({
        'mapa': mapa.mapa,
        'agentes': [{'id': agente.id, 'mapa_explorado': agente.mapa_explorado, 
                    'agente_pos': (agente.x, agente.y)} 
                    for agente in agentes],
        'juego_terminado': juego_terminado
    })

if __name__ == '__main__':
    app.run(debug=True)

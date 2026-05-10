import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import portalocker
from shared.errors import APIError, registrar_manejadores_errores

app = Flask(__name__)
CORS(app)
registrar_manejadores_errores(app)

#contexto definido en dockercompose!!!!!
PATH = os.getenv('DATA_PATH_AUTOR', '/app/data/autores.json')
PORT = int(os.getenv('PORT_AUTOR', 8082))
IP = '0.0.0.0'

@app.route('/autor/<int:id_item>', methods=['GET'])
def obtenerAutorPorId(id_item):
    with open(PATH, 'r') as f:
        portalocker.lock(f, portalocker.LOCK_SH)
        datos = json.load(f)
        resultado = next((item for item in datos if item.get('id') == id_item), None)
        portalocker.unlock(f)

        if not resultado:
            raise APIError(f"Autor ID {id_item} no encontrado", 404)
        
        return jsonify(resultado), 200

@app.route('/autores?autor=<int:id_item>', methods=['GET'])
def listarAutoresPorEditorial(id_item):
    with open(PATH, 'r') as f:
        portalocker.lock(f, portalocker.LOCK_SH)
        datos = json.load(f)
        portalocker.unlock(f)
        return jsonify([item for item in datos if item.get('editorial_id') == id_item]), 200

@app.route('/autor', methods=['POST'])
def crearAutor():
    payload = request.get_json()
    
    if not payload or 'nombre' not in payload:
        raise APIError("Falta el nombre del autor", 400)

    with open(PATH, 'r+') as f:
        
        portalocker.lock(f, portalocker.LOCK_EX | portalocker.LOCK_NB)
        
        contenido = f.read()
        datos = json.loads(contenido) if contenido else []
        
        id_nuevo = max((item.get('id', 0) for item in datos), default=0) + 1
        nuevo_autor = {"id": id_nuevo, **payload}
        datos.append(nuevo_autor)

        f.seek(0)
        f.truncate()
        json.dump(datos, f, indent=4, ensure_ascii=False)
        
        portalocker.unlock(f)

    return jsonify(nuevo_autor), 201

if __name__ == '__main__':
    app.run(host=IP, port=PORT)
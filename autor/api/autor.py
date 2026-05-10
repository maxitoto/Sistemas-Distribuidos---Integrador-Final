import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import portalocker

app = Flask(__name__)
CORS(app)

#contexto definido en dockercompose!!!!!
PATH = os.getenv('DATA_PATH_AUTOR', '/app/data/autores.json')
PORT = int(os.getenv('PORT_AUTOR', 8082))
IP = '0.0.0.0'

@app.route('/autor/<int:id_item>', methods=['GET'])
def obtenerAutorPorId(id_item):
    try:
    
        with open(PATH, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)
            datos = json.load(f)
            resultado = next((item for item in datos if item.get('id') == id_item), None)
            portalocker.unlock(f)

            if not resultado:
                return jsonify({"status": "error", "message": f"Autor ID {id_item} no encontrado"}), 404
            return jsonify({"status": "success", "item": resultado}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/autores', methods=['GET'])
def listarAutores():
    try:
        with open(PATH, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)
            datos = json.load(f)
            portalocker.unlock(f)
            return jsonify({"status": "success", "items": datos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/autor', methods=['POST'])
def crearAutor():
    payload = request.get_json()
    
    # Validación mínima de datos
    if not payload or 'nombre' not in payload:
        return jsonify({"status": "error", "message": "Falta el nombre del autor"}), 400

    try:
        
        with open(PATH, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            
            contenido = f.read()
            datos = json.loads(contenido) if contenido else []
            
            id_nuevo = max((item.get('id', 0) for item in datos), default=0) + 1
            nuevo_autor = {"id": id_nuevo, **payload}
            datos.append(nuevo_autor)

            f.seek(0)
            f.truncate()
            json.dump(datos, f, indent=4, ensure_ascii=False)
            
            portalocker.unlock(f)

        return jsonify({"status": "success", "item": nuevo_autor}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al guardar: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host=IP, port=PORT)
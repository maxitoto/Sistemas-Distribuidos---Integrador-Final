import json
import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import portalocker


app = Flask(__name__)
CORS(app)

#contexto armado en dockercompose!!
PATH = os.getenv('DATA_PATH_LIBRO', '/app/data/libros.json')
PORT = int(os.getenv('PORT_LIBRO', 8083))
IP = '0.0.0.0'

#hayuna endpoint que necesita consultar un autor que esta en otro servicio
URL_AUTOR = os.getenv('AUTOR_API_URL') 

@app.route('/libro/<int:id_item>', methods=['GET'])
def obternerLibroPorId(id_item):
    try:
        
        with open(PATH, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)
            datos = json.load(f)
            resultado = next((item for item in datos if item.get('id') == id_item), None)
            portalocker.unlock(f)
            if not resultado:
                return jsonify({"status": "error", "message": f"No se encontró el ID {id_item}"}), 404
            return jsonify({"status": "success", "item": resultado}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/libro', methods=['POST'])
def crearLibroDeUnAutor():
    payload = request.get_json()
    supuestoAutorId = payload.get('autor_id')

    try:
        # Docker lo resuelve "autor-api"
        autor_res = requests.get(f'{URL_AUTOR}/autor/{supuestoAutorId}')
    except Exception as e:
        return jsonify({"status": "error", "message": f"Servicio Autor no disponible: {str(e)}"}), 503
    
    if autor_res.status_code != 200: 
        return jsonify({"status": "error", "message": "Autor inexistente", "details": autor_res.json()}), 400

    try:
        with open(PATH, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            contenido = f.read()
            datos = json.loads(contenido) if contenido else []
            id_nuevo = max((item.get('id', 0) for item in datos), default=0) + 1
            new_item = {"id": id_nuevo, **payload}
            datos.append(new_item)

            f.seek(0)
            f.truncate()
            json.dump(datos, f, indent=4, ensure_ascii=False)
            portalocker.unlock(f)

        return jsonify({"status": "success", "item": new_item}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fallo en persistencia: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host=IP, port=PORT)
import json
import os #acceso a directorios y archivos
import requests
from flask import Flask, jsonify, request #levantar servidor y enviar respuestas
from flask_cors import CORS #permite comunicar el index sin error de CORS
from dotenv import load_dotenv #acceso a variables de entorno
import portalocker #permite manejar archivos entre nodos de manera segura

load_dotenv() #cargar variables de entorno

app = Flask(__name__) #crea el app o servidor (es una variale global)
CORS(app) #permite CORS en la red

#nos traemos la variables de entorno
PATH = os.getenv('PATH_AUTOR')
PORT = os.getenv('PORT_AUTOR')
IP = os.getenv('IP')

@app.route('/autor/<int:id_item>', methods=['GET'])
def obternerAutorPorId(id_item):
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

@app.route('/autores', methods=['GET'])
def obtenerAutoresDeEditorial():
    id_editorial = request.args.get('editorial', type=int)
    try:
        with open(PATH, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)

            datos = json.load(f)
            resultado = [item for item in datos if item.get('editorial_id') == id_editorial]

            portalocker.unlock(f)

            if not resultado:
                return jsonify({"status": "error", "message": f"No se encontró el ID {id_editorial}"}), 404
            return jsonify({"status": "success", "item": resultado}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/autor', methods=['POST'])
def crearAutor():
    payload = request.get_json()
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

            return jsonify({"status": "success", "item": new_item}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host=IP, port=PORT) #arranca el server asi de facil



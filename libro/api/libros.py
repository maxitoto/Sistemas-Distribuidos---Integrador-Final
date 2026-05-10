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
PATH = os.getenv('PATH_LIBRO')
PORT = os.getenv('PORT_LIBRO')
IP = os.getenv('IP')

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
        

@app.route('/libros', methods=['GET'])
def obtenerLibrosDeUnAutor():
    id_autor = request.args.get('autor', type=int)
    try:
        with open(PATH, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)

            datos = json.load(f)
            resultado = [item for item in datos if item.get('autor_id') == id_autor]

            portalocker.unlock(f)

            if not resultado:
                return jsonify({"status": "error", "message": f"No se encontró el ID {id_autor}"}), 404
            return jsonify({"status": "success", "item": resultado}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/libro', methods=['POST'])
def crearLibroDeUnAutor():
    payload = request.get_json()
    supuestoAutorId = payload['autor_id']

    PORT_AUTOR = os.getenv('PORT_AUTOR')
    HOST_AUTOR = os.getenv('HOST_AUTOR')

    ##llamar a microservicio de autor
    try:
        autor = requests.get(f'http://{HOST_AUTOR}:{PORT_AUTOR}/autor/{supuestoAutorId}')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "service": "autor"}), 503
    
    if autor.status_code != 200: 
        return autor

    try:
        with open(PATH, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)

            contenido = f.read()
            datos = json.loads(contenido) if contenido else []
            id_nuevo = max((item.get('id', 0) for item in datos), default=0) + 1
            new_item = {"id": id_nuevo, **payload}
            datos.append(new_item)

            f.seek(0)          # Volvemos al inicio del archivo
            f.truncate()       # Borramos todo el contenido viejo, tremendo perdida de tiempo jaj 

            json.dump(datos, f, indent=4, ensure_ascii=False)

            portalocker.unlock(f)

        return jsonify({"status": "success", "item": new_item}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": f"Fallo atómico: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host=IP, port=PORT) #arranca el server asi de facil



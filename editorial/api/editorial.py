import json
import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from shared.errors import APIError, registrar_manejadores_errores

app = Flask(__name__)
CORS(app)
registrar_manejadores_errores(app)

PATH = os.getenv('DATA_PATH_EDITORIAL', "/app/database/editorial.json")
PORT = int(os.getenv('PORT_EDITORIAL', 8081))
IP = "0.0.0.0"

URL_AUTOR = os.getenv('AUTOR_API_URL')
URL_LIBRO = os.getenv('LIBRO_API_URL')

@app.route('/editorial/<int:id_item>', methods=['GET'])
def obternerEditorialPorId(id_item):
    resultado = buscar_editorial_en_archivo(id_item)
            
    if not resultado:
        raise APIError(f"No se encontró el ID {id_item}", 404)

    return jsonify(resultado), 200

@app.route('/editorial', methods=['POST'])
def crearEditorial():
    payload = request.get_json()

    with open(PATH, 'r+') as f:
        contenido = f.read()
        datos = json.loads(contenido) if contenido else []
        
        id_nuevo = max((item.get('id', 0) for item in datos), default=0) + 1
        new_item = {"id": id_nuevo, **payload}
        datos.append(new_item)

        f.seek(0)
        f.truncate()
        json.dump(datos, f, indent=4, ensure_ascii=False)
        
    return jsonify(new_item), 201
    
@app.route('/editorial/<int:id_item>/dashboard', methods=['GET'])
def datosCompletoPorEditorial(id_item):
    # 1. Buscamos la editorial local. Si esto falla, es 404 porque el dato no existe.
    editorial = buscar_editorial_en_archivo(id_item)
    if editorial is None:
        raise APIError(f"La editorial {id_item} no existe", 404)

    # 2. Armamos el esqueleto de la respuesta. ¡Acá garantizamos que la Editorial SIEMPRE se devuelve!
    respuesta_final = {
        "editorial": editorial,
        "autores_y_libros": [],
        "estado_sistema": {
            "api_autores": "online",
            "api_libros": "online"
        }
    }

    # 3. Intentamos traer los Autores
    try:
        respuesta_autores = requests.get(f'{URL_AUTOR}/autores?editorial={id_item}', timeout=3)
        respuesta_autores.raise_for_status()
        lista_autores = respuesta_autores.json()
    except requests.exceptions.RequestException:
        lista_autores = [] 
        # Degradación elegante: avisamos que falló, pero no matamos el proceso
        respuesta_final["estado_sistema"]["api_autores"] = "offline"

    # 4. Intentamos traer los Libros (Solo si logramos conseguir los autores)
    for autor in lista_autores:
        try:
            respuesta_libros = requests.get(f'{URL_LIBRO}/libros?autor={autor["id"]}', timeout=3)
            respuesta_libros.raise_for_status()
            lista_libros = respuesta_libros.json()
        except requests.exceptions.RequestException:
            lista_libros = []
            respuesta_final["estado_sistema"]["api_libros"] = "offline"
            
        respuesta_final["autores_y_libros"].append({
            "autor": autor, 
            "libros": lista_libros
        })    

    return jsonify(respuesta_final), 200

def buscar_editorial_en_archivo(id_buscado):
    with open(PATH, 'r') as f:
        datos = json.load(f)
        return next((item for item in datos if item.get('id') == id_buscado), None)

if __name__ == '__main__':
    app.run(host=IP, port=PORT)
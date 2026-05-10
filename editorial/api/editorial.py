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
PATH = os.getenv('DATA_PATH_EDITORIAL', "/app/data/editorial.json")
PORT = int(os.getenv('PORT_EDITORIAL', 8081))
IP = "0.0.0.0"

#definimos la url de los otros servicios que este servicio va a consultar
URL_AUTOR = os.getenv('AUTOR_API_URL')
URL_LIBRO = os.getenv('LIBRO_API_URL')


#esta etiqueta indica la ruta del serivico y su metodo
#en este cado ese codigo es dinamico, depende de cada servicio
@app.route(f'/editorial/<int:id_item>', methods=['GET'])
def obternerEditorialPorId(id_item): #Flask va a inyectar el valor de id_item en la variable id_item
   
    resultado = buscar_editorial_en_archivo(id_item)
            
    if not resultado:
        return jsonify({"status": "error", "message": f"No se encontró el ID {id_item}"}), 404

    return jsonify({"status": "success", "item": resultado}), 200


    
@app.route(f'/editorial', methods=['POST'])
def crearEditorial():
    payload = request.get_json()

    try:
        # Abrimos en modo r+ (lectura y escritura sin borrar nada al abrir)
        with open(PATH, 'r+') as f:
    
            portalocker.lock(f, portalocker.LOCK_EX)
        
            contenido = f.read()
         
            datos = json.loads(contenido) if contenido else [] #puede estar vacio
            
            id_nuevo = max((item.get('id', 0) for item in datos), default=0) + 1
            new_item = {"id": id_nuevo, **payload}
            datos.append(new_item)

            f.seek(0)          # Volvemos al inicio del archivo
            f.truncate()       # Borramos todo el contenido viejo (ahora que ya lo tenemos en memoria) 
            
            json.dump(datos, f, indent=4, ensure_ascii=False)
            
            portalocker.unlock(f)
            
        return jsonify({"status": "success", "item": new_item}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": f"Fallo atómico: {str(e)}"}), 500

    
@app.route(f'/editorial/<int:id_item>/dashboard', methods=['GET'])
def datosCompletoPorEditorial(id_item):

    editorial = buscar_editorial_en_archivo(id_item)

    if editorial is None:
        return jsonify({"status": "error", "message": f"La editorial {id_item} no existe"}), 404

    payload = []

    try:
        respuesta_autores = requests.get(f'http://{URL_AUTOR}/autores?editorial={id_item}').json()
        lista_autores = respuesta_autores.get('item', [])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "service": "autor"}), 503

    try:
        for autor in lista_autores:
            respuesta_libros = requests.get(f'http://{URL_LIBRO}/libros?autor={autor["id"]}').json()
            lista_libros = respuesta_libros.get('item', [])
            payload.append({"autor": autor, "libros": lista_libros})    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "service": "libro"}), 503


    return jsonify({"status": "success", "item": payload}), 200


#funcion comun para n apis
def buscar_editorial_en_archivo(id_buscado):
    try:
        with open(PATH, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)
            datos = json.load(f)
            # Retorna el diccionario o None si no existe
            return next((item for item in datos if item.get('id') == id_buscado), None)
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return None
        

if __name__ == '__main__':
    app.run(host=IP, port=PORT) #arranca el server asi de facil



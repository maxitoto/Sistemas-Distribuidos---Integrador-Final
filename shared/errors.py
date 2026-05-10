import json
from flask import jsonify
from werkzeug.exceptions import HTTPException
import requests
import portalocker

# Nuestra excepción personalizada para lanzar errores a mano (ej: ID no existe)
class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

def registrar_manejadores_errores(app):

    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(portalocker.exceptions.LockException)
    def handle_lock_error(error):
        return jsonify({
            "error": "El recurso está siendo modificado por otro proceso simultáneo. Reintente."
        }), 409


    @app.errorhandler(FileNotFoundError)
    @app.errorhandler(PermissionError)
    def handle_file_access_error(error):
        return jsonify({
            "error": "El recurso es inaccesible en este momento."
        }), 503

    @app.errorhandler(requests.exceptions.RequestException)
    def handle_request_error(error):
        return jsonify({
            "error": "Fallo en la comunicación con un servicio interno."
        }), 503

    @app.errorhandler(json.JSONDecodeError)
    def handle_json_error(error):
        return jsonify({
            "error": "Error interno de codificación."
        }), 500

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        print(f"CRÍTICO - Error no manejado: {str(error)}")
        return jsonify({
            "error": "Ocurrió un error interno crítico en el servidor."
        }), 500
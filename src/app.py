from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from diagnostico import procesar_audio_y_generar_json
import json

# Create the Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Ruta para diagnóstico
@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    url = request.json['url']
    genero = request.json['genero']
    
    try:
        resultado_json = procesar_audio_y_generar_json(url, genero)
        return jsonify(json.loads(resultado_json)), 200
    except Exception as e:
        return jsonify({'message': f'Error al procesar el diagnóstico: {str(e)}'}), 500

# Error handler
@app.errorhandler(404)
def not_found(error=None):
    message = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })

    message.status_code = 404

    return message

# Error handler: missing parameters
@app.errorhandler(400)
def bad_request(error=None):
    message = jsonify({
        'message': 'Missing parameters',
        'status': 400
    })

    message.status_code = 400

    return message

# Debug mode
if __name__ == '__main__':
    app.run(debug=True)
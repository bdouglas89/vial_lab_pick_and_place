import os
from flask import Flask, jsonify, request, render_template, send_file
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Obtiene la ruta del directorio actual del script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Carga el contenido de vial.json en una variable global al iniciar
def load_data():
    with open(os.path.join(base_dir, 'vial.json'), 'r') as file:
        return json.load(file)

global data
data = load_data()

@app.route('/', methods=['GET'])
def root():
    return "Sitio en Ejecucion  - API Pick and Place Vial"

@app.route('/app', methods=['GET'])
def index():
    return render_template('index.html')

# Rutas GET existentes
@app.route('/all', methods=['GET'])
def get_all():
    return jsonify(data)

@app.route('/all', methods=['POST'])
def add_all():
    new_data = request.json
    data.clear()
    data.update(new_data)
    save_data()
    return jsonify(new_data), 201


from pick_and_place.routine import gcode_maker

# @app.route('/gcode', methods=['POST'])
# def create_gcode():
#     new_data = request.json
#     data.clear()
#     data.update(new_data)
#     save_data()
#     gcode_maker(data)
#     return jsonify({'message': 'GCode File Created'}), 201

@app.route('/gcode', methods=['POST'])
def create_gcode():
    new_data = request.json
    data.clear()
    data.update(new_data)
    save_data()
    gcode_path = gcode_maker(data)
    # gcode_path = os.path.join(base_dir, 'pick_and_place', 'gcode_files', 'temp_routine.gcode')
    
    # Agregar impresión de depuración
    if not os.path.exists(gcode_path):
        print(f"Error: El archivo {gcode_path} no existe.")
        return jsonify({"error": "G-code file not found"}), 500
    
    print(f"PATH: {gcode_path}")
    return send_file(gcode_path, as_attachment=True, download_name='routine.gcode')


@app.route('/rack', methods=['GET'])
def get_racks():
    return jsonify(data['racks'])

@app.route('/rack/<string:rack_id>', methods=['GET'])
def get_rack_by_id(rack_id):
    for rack in data['racks']:
        if str(rack['rack_id']) == rack_id:
            return jsonify(rack)
    return jsonify({'error': 'Rack not found'}), 404

@app.route('/deck', methods=['GET'])
def get_decks():
    return jsonify(data['deck'])

@app.route('/deck/<string:stand_number>', methods=['GET'])
def get_deck_by_number(stand_number):
    for stand in data['deck']:
        if str(stand['stand_number']) == stand_number:
            return jsonify(stand)
    return jsonify({'error': 'Stand not found'}), 404

# Nueva ruta GET para "preferences"
@app.route('/preferences', methods=['GET'])
def get_preferences():
    return jsonify(data['preferences'])

# Rutas POST existentes
@app.route('/rack', methods=['POST'])
def add_rack():
    new_rack = request.json
    data['racks'].append(new_rack)
    save_data()
    return jsonify(new_rack), 201

@app.route('/deck', methods=['POST'])
def add_deck():
    new_deck = request.json
    data['deck'].append(new_deck)
    save_data()
    return jsonify(new_deck), 201

# Nueva ruta POST para "preferences"
@app.route('/preferences', methods=['POST'])
def update_preferences():
    updated_prefs = request.json
    data['preferences'] = updated_prefs
    save_data()
    return jsonify(updated_prefs), 200

# Rutas PUT existentes
@app.route('/rack/<string:rack_id>', methods=['PUT'])
def update_rack(rack_id):
    new_rack = request.json
    for i, rack in enumerate(data['racks']):
        if str(rack['rack_id']) == rack_id:
            data['racks'][i] = new_rack
            save_data()
            return jsonify(new_rack)
    return jsonify({'error': 'Rack not found'}), 404

@app.route('/deck/<string:stand_number>', methods=['PUT'])
def update_deck(stand_number):
    new_deck = request.json
    for i, stand in enumerate(data['deck']):
        if str(stand['stand_number']) == stand_number:
            data['deck'][i] = new_deck
            save_data()
            return jsonify(new_deck)
    return jsonify({'error': 'Stand not found'}), 404

# Función para guardar los datos modificados en vial.json
def save_data():
    with open('vial.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Carga el contenido de vial.json en una variable global al iniciar
def load_data():
    with open('vial.json', 'r') as file:
        return json.load(file)

global data
data = load_data()

@app.route('/', methods=['GET'])
def root():
    return "Sitio en Ejecucion  - API Pick and Place Vial"


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
    app.run(debug=True)

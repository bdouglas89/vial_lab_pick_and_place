import json


def load_data_from_json(json_file):
    """
    Carga los datos desde un archivo JSON a la variable data.
    
    :param json_file: La ruta hacia el archivo JSON.
    :return: Los datos cargados del archivo JSON o None si ocurre un error.
    """
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: El archivo {json_file} no se encontró.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {json_file} no se pudo decodificar.")
        return None
    except Exception as e:
        print(f"Se produjo un error: {e}")
        return None

# Ejemplo de cómo llamar a la función y almacenar los datos cargados en la variable 'data':
# data = load_data_from_json('vial.json')
# print(data)

def get_rack_by_id(rack_id, data):
    """
    Devuelve el objeto rack que coincide con el rack_id proporcionado.
    
    :param rack_id: El ID del rack a buscar.
    :param data: Los datos cargados del archivo JSON.
    :return: El objeto rack con el ID especificado o None si no se encuentra.
    """
    for rack in data['racks']:
        if rack['rack_id'] == rack_id:
            if rack:
                print("--> Datos del rack encontrado: ")
                #print(rack)
                for key, value in rack.items():
                    print(f"{key} : {value}")
                return rack
            
    print("Rack no encontrado.")        
    return None

# Carga los datos del archivo JSON
#data = load_data_from_json()

# Obtén los datos de un rack específico por su ID
#rack_data = get_rack_by_id(1, data)  # Cambia '1' por el ID del rack que desees buscar
#if rack_data:
#    print("Datos del rack encontrado:", rack_data)
#else:
#    print("Rack no encontrado.")




# Esta función imprimirá el contenido de la variable 'data' que contiene los datos cargados desde un archivo JSON.
def print_data_content(data):
    """
    Imprime el contenido de la variable data que contiene datos JSON.
    
    :param data: Los datos JSON cargados que serán impresos.
    """
    print(json.dumps(data, indent=4))

# Uso de la función:
# Suponiendo que 'data' ya contiene los datos cargados del archivo JSON:
# print_data_content(data)


def print_rack_data(rack_data):
    """
    Imprime el contenido de la variable rack_data de forma legible.
    
    :param rack_data: El objeto rack a imprimir.
    """
    if rack_data:
        print(json.dumps(rack_data, indent=4))
    else:
        print("No hay datos de rack para imprimir.")

# Suponiendo que ya tienes la variable rack_data con los datos de un rack:
# print_rack_data(rack_data)





# Esta función busca el valor de 'stand_location_X o Y para un número de stand específico en la variable 'data'.

def get_stand_location_y(stand_number, info_deck):
 
    for stand in info_deck:
        if stand['stand_number'] == stand_number:
            return stand['stand_location_Y']
    return "Stand number not found"

def get_stand_location_x(stand_number, info_deck):

    for stand in info_deck:
        if stand['stand_number'] == stand_number:
            return stand['stand_location_X']
    return "Stand number not found"

# Uso de la función:
# Suponiendo que 'data' ya contiene los datos cargados del archivo JSON:
#stand_location_x = get_stand_location_x(1, data)
#print(stand_location_x)



def get_info_deck(data):
    """
    Devuelve la lista completa de todos los objetos deck.
    :param data: Los datos cargados del archivo JSON.
    :return: Una lista con todos los objetos deck.
    """
    deck_data = data['deck']
    if deck_data:
        print("--> Coordenadas de Rack encontradas: ")
        for a_deck in deck_data:
            print(f"Rack #{a_deck['stand_number']}, Location(x,y): {a_deck['stand_location_X']}, {a_deck['stand_location_Y']}") 
    else:
        print ("Rack no ubicados con la key: deck")
    return deck_data

# Ejemplo de uso:
"""
# Carga los datos del archivo JSON
data = load_data_from_json()

# Obtén la lista completa de decks
all_decks = get_all_decks(data)
print("Lista completa de decks:", all_decks)
"""


#En eje X Calcula la suma del diámetro del vial y el separador de base del rack y multiplica por espacios requeridos al resultado le suma la localizacion del stand.
def mm_x(st_number, position_x, rack_data, info_deck):
    st_value = get_stand_location_x(st_number, info_deck)

    if position_x == 1:
        return st_value
    
    result = st_value + (rack_data['vial_diameter']) * (int(position_x) - 1)
    print("st_value: {} + (rackdata: {} * px-1: {} = result: {})".format(st_value, rack_data['vial_diameter'], int(position_x)-1, result))
    #return int(st_value) + ((int(rack_data['vial_diameter']) + int(rack_data['rack_base_separator'])) * int(position_x)-1)
    return st_value + (8.9) * (int(position_x) - 1)

#Recibe stand_number, position_y, rack_data para devolver position si es = a 1 o suma del diámetro del vial y el separador de base del rack y multiplica por espacios requeridos al resultado le suma la localizacion del stand
def mm_y(st_number, position_y, rack_data, data):
    st_value = get_stand_location_y(st_number, data)
    #print(f"------------------------------------>  " + {st_value})
    if position_y == 1:
        return st_value
    #return int(st_value) + ((int(rack_data['vial_diameter']) + int(rack_data['rack_base_separator'])) * int(position_y)-1)
    return st_value + (rack_data['vial_diameter'] * (int(position_y) - 1))


    
# Ejemplo de uso
""""
# Suponiendo que 'rack_data' es un diccionario que ya contiene los datos de un rack específico
rack_data_example = {
    'vial_diameter': 8.7,
    'rack_base_separator': 0.9,
    # Otros campos...
}
result = mm_x(rack_data_example, B,)
print(f"La suma de vial_diameter y rack_base_separator es: {result}")
"""


#Bajar a distancia segura piker
def mm_z_piker_empty(rack_data):
    return rack_data['empty_secure_height']

def mm_z_piker_holding(rack_data):
    return rack_data['holding_secure_height']

def mm_z_piking(rack_data):
    return rack_data['picking_height']

def mm_z_placing(rack_data):
    return rack_data['placing_height']

def xy_holding_speed(rack_data):
    return rack_data['xy_holding_speed']

def xy_empyt_speed(rack_data):
    return rack_data['xy_empyt_speed']

def z_holding_speed(rack_data):
    return rack_data['z_holding_speed']

def z_empyt_speed(rack_data):
    return rack_data['z_empyt_speed']

def z_picking_speed(rack_data):
    return rack_data['z_picking_speed']



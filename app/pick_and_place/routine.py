import json
from pick_and_place.mm_solver import * 
from pick_and_place.gcode_creator import *
from pick_and_place.input_a2b import *

"""
    La aplicacion recibe instrucciones desde el config_json  donde se encuentra llave con el nombre de "vial_selected" y "pick_and_place_list"
    en pick_and_place son 2 columnas en el formato 1A1, donde se lee de la siguiente manera:  numero de Rack , Columna de Viales, Fila de Viales.
    La primer columna "Pick" indica de donde se recoge la muestra y "Place" donde se deposita la mustra.

    Cuando se ejecuta la funcion  "create_a2b" se procesa la informacion y se genera un archivo .gcode con el nombre routina_fechayhora.gcode

    El archivo generado ".gcode" es el que se le envia a la maquina, pero se puede hacer uso de simulador en linea para visualizar el recorrido de la maquina.
    Link de simulador: https://ncviewer.com/
"""

def gcode_maker(config_json):
    #  Recibir configuracion json y lista de pick and place para ejecutrar create_a2b

    vial_selected = config_json.get('vial_selected', 1)

    pick_and_place_list = config_json.get('pick_and_place_list', [])

    #Seleccion de Rack
    rack_data = get_rack_by_id(vial_selected, config_json)   

    # Cargar los valores de Bandejas
    deck_data = get_info_deck(config_json)

    print ("csv_list: ")
    print (pick_and_place_list)
    print (type(pick_and_place_list))
    print ("\n")

    new_file_name = create_a2b(rack_data, deck_data, pick_and_place_list)

    return new_file_name

"""
# Prueba de la funcion gcode_maker
# Ruta al archivo JSON
config_json = 'vial.json'
# Cargar los datos desde el archivo JSON
data = load_data_from_json(config_json)
gcode_maker(data)

"""
from mm_solver import * 
from gcode_creator import *
from input_a2b import *

"""
    La aplicacion recibe instrucciones desde el archivo .csv 
    son 2 columnas en el formato 1A1, donde se lee de la siguiente manera:  numero de Rack , Columna de Viales, Fila de Viales.
    La primer columna "Pick" indica de donde se recoge la muestra y "Place" donde se deposita la mustra.

    Cuando se ejecuta la funcion  "create_a2b" se procesa la informacion del .csv y se genera un archivo .gcode con el nombre routina_fechayhora.gcode

    El archivo generado ".gcode" es el que se le envia a la maquina, pero se puede hacer uso de simulador en linea para visualizar el recorrido de la maquina.
    Link de simulador: https://ncviewer.com/
    
"""

# Ruta al archivo JSON
config_json = 'vial.json'

# Cargar los datos desde el archivo JSON
data = load_data_from_json(config_json)

#Seleccion de Rack
rack_data = get_rack_by_id(1, data)   #Cambia "#" por el ID del rack que desees 

# Cargar los valores de Bandejas
deck_data = get_info_deck(data)

print("\n\n")

create_a2b(rack_data, deck_data)


"""
    Leer CSV con lista de origen - destiono
    crear adchivo .gcode


    hacer home
    Establecer distacias apsolutas
    
    loop por cada movimiento
        ir a ubicacion origen
        bajar a distancia segura
        (Piker / Bajar a  Altura de agarre)
        (Piker / Colectar )
        (Piker / Levantar a Altura Segura)
        Ir a destino
        Bajar la muestra
        (Piker Soltar )
        Ir a Altura Segura
    fin_loop

    Finalizar el archivo.

"""

from pick_and_place.gcode_creator import *
from pick_and_place.mm_solver import *

def create_a2b(rack_data, deck_data, pick_drop_list):

    #Cargar CSV 
    pick_and_drop_list = pick_drop_list

    #Crar el archivo temporal
    create_gcode_file()

    #Establecer unidades en Milimetros
    gcode_set_mm()

    #Establecer distanciaos Apsolutas
    gcode_set_apsolute()

    #Hacer Home
    gcode_do_home_XYZ()

    #Home de Piker
    gcode_home_piker()

    #Generar GCODE de los movimientos
    gcode_pick_and_drop_create(pick_and_drop_list, rack_data, deck_data)

    #Home Final
    gcode_end(rack_data)

    #Finalizar Archivox
    new_file_name = gcode_file_rename()
    
    return new_file_name



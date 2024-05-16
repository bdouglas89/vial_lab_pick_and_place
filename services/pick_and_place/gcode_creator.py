from mm_solver  import *
from datetime import datetime
import csv
import os

#Funcion LOOP para movimiento de Viales
def gcode_pick_and_drop_create(pick_and_drop_list, rack_data, info_deck):

    for pick, drop in pick_and_drop_list:
        #print (" ---> Linea:\n"+pick+" - "+ drop)
        do_a2b(pick, drop, rack_data, info_deck)

#Realiza GCode del movimento de 1 vial.
def do_a2b(pick, drop, rack_data, info_deck):


    #gcode_comment(f";Origen_{insert_spaces_around_letters(pick)}  --> Destino_{insert_spaces_around_letters(drop)} ")

    #Valocidad Rapida
    gcode_set_high_speed(rack_data)

    #ir a ubicacion origen
    gcode_goto_xy(pick, rack_data, info_deck)

    #bajar a distancia segura
    gcode_goto_z_empty(rack_data)

     #Hacer pausa antes del Picking
    gcode_pause(800)

    #(Piker / Bajar a  Altura de agarre)
    #gcode_comment("G1 Z320 ;??? Bajar en Z a altura de agarre.")
    gcode_goto_z_peaking(rack_data)
    
    #(Piker / Colectar )  ----------#############
    #gcode_comment(";G1 E## ;??? Cerrar el Piker eje \"E\"  (Sugetar Vial)")
    #gcode_macro_agarre() SE ELIMINA POR EL CAMBIO DE MECANISMO DEL PICKER

    #(Piker / Levantar a Altura Segura con Vial)
    gcode_goto_z_holding(rack_data)

    #Velocidad Lenta
    gcode_set_low_speed(rack_data)
    
    #Ir a destino
    gcode_goto_xy(drop, rack_data, info_deck)
    
    #Hacer pausa antes del placing
    gcode_pause(1400)

    #(Piker / Bajar a  Altura para Depositar el Vial)
    #gcode_comment("G1 Z310 ;??? Bajar en Z a altura para Depositar el Vial.")
    gcode_goto_z_placing(rack_data)

    #(Obturador empuja el vial )
    gcode_macro_pickeron()

#(Obturador vuelve a la posicion de reposo )
    gcode_macro_pickeroff()

    #Ir a Altura Segura
    gcode_goto_z_empty(rack_data)

#Lee el CSV
def csv_load_list(csv_file_name="input_file.csv"):
    """
    Lee cada línea de un archivo CSV y obtiene los valores de cada línea.

    Args:
    - nombre_archivo (str): La ruta al archivo CSV que se va a leer.
    """
    
    with open(csv_file_name, newline='', encoding='utf-8') as file_csv:
        reader = csv.reader(file_csv)
        next(reader) # Omitir la primera línea (encabezado)
        reader_list = list(reader)
        pick_and_drop_list = []
        for i, line in enumerate(reader_list, start=1):
            pick_and_drop_list.append((line[0],line[1]))
            print(f"Cargando Movimiento #{i}: {line[0]} --> {line[1]}")
            #print(f"Línea {i}: {reader}")
        return pick_and_drop_list
# Ejemplo de uso de la función
#pick_and_drop_list = csv_load_values('input_file.csv')


def leer_valores_csv_omitir_encabezado(nombre_archivo="input_file.csv"):
    """
    Lee cada línea de un archivo CSV omitiendo la primera línea (encabezado) y muestra el índice de cada línea.

    Args:
    - nombre_archivo (str): La ruta al archivo CSV que se va a leer.
    """
    with open(nombre_archivo, newline='') as archivo_csv:
        lector = csv.reader(archivo_csv)
        next(lector)  # Omitir la primera línea (encabezado)
        for indice, linea in enumerate(lector, start=1):
            # Imprime el índice y los valores de cada línea
            print(f"Línea {indice} : {linea}")



def create_gcode_file():
    """
        Crea o reemplaza el archivo routine.gcode con el contenido proporcionado.

        Args:
        - content (str): El contenido que se escribirá en el archivo.

        
    """
    now = datetime.now()
    now = now.strftime("%d-%m-%Y_%H:%M:%S")
    file_name = "gcode_files/temp_routine.gcode"
    with open( file_name, 'w') as file:
        file.write(f";FILE CREATED  {now}\n")
    print("New temp 'temp_routine.gcode' file Created.  " + now)

def append_gcode_file(line, file_name="gcode_files/temp_routine.gcode"):
    """
    Agrega una línea al final del archivo routine.gcode.

    Args:
    - line (str): La línea que se agregará al archivo.
    """
    with open(file_name, 'a') as file:
        file.write(line + '\n')
    print("GCODE Append: "+ line + "\n") 
# Ejemplo de uso
#line = "G1 X100 Y100 ; Mover a la posición X100 Y100"
#add_gcode_line(line)

#Remombrar archivo GCODE temporal
def gcode_file_rename(file_name="gcode_files/temp_routine.gcode"):
    now = datetime.now()
    now = now.strftime("%d%m%Y_%H%M%S")
    new_file_name = f"gcode_files/routine_{now}.gcode"
    try:
        os.rename(file_name, new_file_name)
        print (f"Gcode File Rename from \"{file_name}\" to \"{new_file_name}\"")
        
        #os.remove(file_name)
        print ("Gcode File Done Succesfull")
    except OSError as e:
        print(f"Error al renombrar Archivo {e}")


#************************************************************************************************************************

import re

def letter_to_value(letter):
    """
    Transforma una letra en su correspondiente valor numérico (A=0, B=1, C=2, ...).
    
    :param letra: La letra a transformar.
    :return: El valor numérico correspondiente a la letra.
    """
    return ord(letter.upper()) - ord('A') + 1

def extract_components(s):
    # La expresión regular para dividir el string
    match = re.match(r"(\d+)([A-Z])(\d+)", s)
    if match:
        return match.groups()
    else:
        raise ValueError("El formato del string no es válido")

def get_rack_value(s): #Recibe texto en el formato --> 1A3 y devuelve 1 (Obtiene  # de Rack)
    return int(extract_components(s)[0])

def get_x_value(s): #Recibe texto en el formato --> 1B3 y devuelve 2 (Obtiene  # de pocsición de Vial en X)
    return int(extract_components(s)[2])

def get_y_value(s): #Recibe texto en el formato --> 1B3 y devuelve 3 (Obtiene  # de pocsición de Vial en Y)
    return letter_to_value(extract_components(s)[1])

# Pruebas de las funciones
print(get_rack_value("1A5"))  # Debe imprimir: 1
print(get_rack_value("15D12")) # Debe imprimir: 15

print(get_x_value("1A5"))     # Debe imprimir: A
print(get_x_value("15D6"))    # Debe imprimir: D

print(get_y_value("1A5"))     # Debe imprimir: 5
print(get_y_value("15D12"))    # Debe imprimir: 6



#************************************************************************************************************************
"""""
def get_rack_value(texto):
     
    
    origen = int(texto[0])  # El primer caracter es el origen "Rack"
    return origen

def get_x_value(texto):
    
    
    posicion_x = letter_to_value(texto[1])   # El segundo caracter es la posición en x
    return posicion_x

def get_y_value(texto):
    
    
    posicion_y = int(texto[2:])  # El resto del texto corresponde a la posición en y
    return posicion_y
"""
#************************************************************************************************************************
def gcode_goto_xy(route, rack_data, info_deck ):
    
    x= mm_x(get_rack_value(route), get_x_value(route), rack_data, info_deck)
    y= mm_y(get_rack_value(route), get_y_value(route), rack_data, info_deck)

    print("X: "+str(x))
    print("Y: "+str(y))
    #APPEND GCODE
    append_gcode_file(f"G1 X{x} Y{y}")

#Mueve el Piker a una altura segura Sin el Vial
def gcode_goto_z_empty(rack_data):
    z = mm_z_piker_empty(rack_data)
    append_gcode_file(f"G1 Z{z} F2000")

#Mueve el Piker a una altura indicada
def gcode_goto_z_value(value):
    
    append_gcode_file(f"G1 Z{value}")

#Mueve el Piker a una altura segura Con el Vial
def gcode_goto_z_holding(rack_data):
    z = mm_z_piker_holding(rack_data)

    append_gcode_file(f"G1 Z{z} F1500; Mueve el Piker con Vial a una altura segura")

#Mover en Z al indice valor indicado
def gcode_goto_z(z, speed):
    append_gcode_file(f"G1 Z{z} F{speed} ; Movimiento en Z")


#Establece Establece la velocidad de avance  Lenta
def gcode_set_low_speed(rack_data):
    speed = xy_holding_speed(rack_data)
    append_gcode_file(f"G1 F{speed} ; Velicidad Lenta")

#Establece Establece la velocidad de avance a 150 mm/min
def gcode_set_high_speed(rack_data):
    speed = xy_empyt_speed(rack_data)
    append_gcode_file(f"G1 F{speed} ; Velocidad Alta")

# Establece unidades en milimetros
def gcode_set_mm():
    append_gcode_file(f"G21 ; Establece unidades en milimetros")

#Uso de coordenadas absolutas
def gcode_set_apsolute():
    append_gcode_file(f"G90 ; Uso de coordenadas absolutas")

#Hacer HOME 
def gcode_do_home_XYZ():
    append_gcode_file(f"G28 ; Hacer home en ejes XYZ")

#Home Final - Todos los ejes se desplazan a 0
def gcode_end(rack_data):
    speed_z = z_empyt_speed(rack_data)
    speed_xy = xy_empyt_speed(rack_data)

    gcode_goto_z(0, speed_z)
    append_gcode_file(f"G1 X0 Y0 F{speed_xy}; Hacer home en ejes XY")

#Hacer Pause 
def gcode_pause(time):
    append_gcode_file(f"G4 P{time} ; Hacer pausa antes del placing")

#Funcion para agregar comentario al GCode
def gcode_comment(text):
    append_gcode_file(f";{text}")

#Funcion para agregar espacios a Origen o Destino ej: 2A11  pasa a  2 A 11
def insert_spaces_around_letters(s):
    """
    Inserts spaces before and after each letter in a string.
    
    Args:
    - s (str): The original string.
    
    Returns:
    A new string with spaces inserted before and after each letter.
    """
    result = []  # List to store characters and spaces

    for i, char in enumerate(s):
        # If the character is a letter, insert spaces before and after
        if char.isalpha():
            # Ensure not to duplicate spaces if there's already one before the letter
            if i > 0 and s[i-1] != ' ':
                result.append(" ")
            result.append(char)
            # Ensure not to duplicate spaces if the next character is also a space
            if i < len(s)-1 and s[i+1] != ' ':
                result.append(" ")
        else:
            result.append(char)

    return ''.join(result)


def gcode_home_piker():
    append_gcode_file('SENSORLESS_HOME_PICKER_STEPPER')

def gcode_macro_pickeroff():
    append_gcode_file('PICKER_OFF')

def gcode_macro_pickeron():
    append_gcode_file('PICKER_ON')

def gcode_goto_z_peaking(rack_data):
    z = mm_z_piking(rack_data)
    s = z_picking_speed(rack_data)
    append_gcode_file(f"G1 Z{z} F{s} ; Movimiento en Z lento para ATRAPAR el vial")

def gcode_goto_z_placing(rack_data):
    z = mm_z_placing(rack_data)
    s = z_holding_speed(rack_data)
    append_gcode_file(f"G1 Z{z} F{s} ; Movimiento en Z lento para COLOCAR el vial")

# Example of use
#original_text = "1C12"
#modified_text = insert_spaces_around_letters(original_text)
#print(modified_text)  # Expected output: "1 C 12"

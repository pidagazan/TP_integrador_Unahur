import os
import csv
import os

#la ruta del archivo es ./TP_INTEGRADOR_TALLER_/gamesec_logs.csv  
def verificar_existencia_archivo(ruta_archivo:str)-> None:  #Verifica que exista el archivo a traves de un path, si existe retorna TRUE, caso contrario levanta una excepcion. #
    existe = False
    if os.path.exists(ruta_archivo):
        existe = True

    if existe == False:
        raise FileNotFoundError("El archivo no existe o está mal especificada la ruta")




def verificar_contenido_lista(lista: list)-> None:      #Verifica que una lista no este vacia, en caso de estarlo levanta una excepcion #
    if len(lista) == 0:
        raise ValueError("El archivo está vacío o no se cargaron de forma correcta los valores")



def cargar_telemetria(ruta_archivo: str) -> list[dict]:  #Funcion que carga el .csv al programa, verificando que exista ese archivo, y anexando cada fila a la lista de diccionarios.
    sesiones = list()                                    # El acceso a los diccionario sera a traves de los indices de la lista, ya que es una LISTA de DICCIONARIOS.

    verificar_existencia_archivo(ruta_archivo)

    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lectura_archivo = csv.DictReader(archivo)
    
    
        for fila in lectura_archivo:
            sesion = {
                'id_sesion': int(fila['id_sesion']),
                'servidor': (fila['servidor']),
                'jugador_id': (fila['jugador_id']),
                'tipo_partida': (fila['tipo_partida']),
                'ping_promedio': int(fila['ping_promedio']),
                'fps_promedio': int(fila['fps_promedio']),
                'duracion_minutos': float(fila['duracion_minutos']),
                'intentos_fallidos': int(fila['intentos_fallidos']),
                'reportes_trampa': int(fila['reportes_trampa'])
            }
            sesiones.append(sesion)

    verificar_contenido_lista(sesiones)
    return sesiones



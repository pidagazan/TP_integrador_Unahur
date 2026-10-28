import sys
from carga import *
from procesamiento import *
#FUNCIONES AUXILIARES.
#La mayoria se explican asi misma, excepto las que estan relacionadas a los funciones1-6 del menu, donde cada indice corresponde a su numero de menu

def imprimir_linea()-> None:
    print("="*75)

def imprimir_linea_cuerpo()-> None:
    print("-"*75)

def imprimir_cabecera() -> None:
    imprimir_linea()
    print(""*10+"GAMESEC MONITOR - PANEL DE CONTROL")
    imprimir_linea()

def pause()-> None:
    input("Presiona una tecla...")

def reporte_primer_apartado(sesiones)-> None: #Funcion que imprime el primer apartado del reporte del resumen global
                                                #NOTA IMPORTANTE -> Las funciones de reporte estan pensadas para redigirir la salida standard a un archivo por eso se usa print como método principal
    dic_globales = calcular_estadisticas_globales(sesiones) #DICCIONARIO#
    
    print("[1] RESUMEN GLOBAL OPERATIVO")
    imprimir_linea_cuerpo()
    print(f"Total de sesiones procesadas: {dic_globales['total_sesiones']}")
    print(f"Ping promedio global: {dic_globales['ping_promedio']}")
    print(f"Duracion media de partida : {dic_globales['duracion_promedio']}")
    print(f"Partidas de alta competencia (Ranked/Torneo): {dic_globales['porcentaje_competitivas']}")

def reporte_segundo_apartado(sesiones) -> None: #Funcion que imprime el segundo apartado del reporte por servidor
    print("[2] RENDIMIENTO REGIONAL POR SERVIDOR")
    imprimir_linea_cuerpo()
    print("Servidor" + " "*20 + "| Sesiones |" + "| Ping Promedio |" + "| FPS Promedio")
    rendimiento_por_servidor = analizar_por_servidor(sesiones)
    
    for key in rendimiento_por_servidor.keys():
        elemento = rendimiento_por_servidor[key]
        print(f"{key}" + " "*20 + f"| {elemento['cantidad']} |" + f"| {elemento['ping_promedio']}ms |" + f"| {elemento['fps_promedio']}fps")

def reporte_tercer_apartado(sesiones)-> None: #Funcion que imprime el tercer apartado del reporte de auditoria de seguridad e incidentes
    tupla_dict_lista_criticas = clasificar_incidentes(sesiones)
    
    sesiones_criticas = tupla_dict_lista_criticas[1]
    dict_contador = tupla_dict_lista_criticas[0]

    print("[3] AUDITORIA DE SEGURIDAD E INCIDENTES")
    imprimir_linea_cuerpo()
    print("Distribucion de estados de seguridad:")
    print(f"\t Normales: {dict_contador['Normal']}")
    print(f"\t Sospechosos: {dict_contador['Sospechoso']}")
    print(f"\t Criticos: {dict_contador['Critico']}")
    print("\n")

    print("Detalles de Sesiones Criticas Detectadas: ")
    for registro in sesiones_criticas:
        print(f"[!] Sesion: {registro['id_sesion']}/ Jugador: {registro['jugador_id']}/ Servidor: {registro['servidor']}")
        print(registro['motivo'])
        print("")
    
def reporte_cuarto_apartado()-> None: #Funcion qe imprime el cuatro apartado del reporte
    print("[4] CONCLUSIONES TECNICAS DEL EQUIPO")
    print("1..")
    print("2..")
    print("3..")
    imprimir_linea()
    print("FIN DEL REPORTE GAMESEC")
    imprimir_linea()








def exportar_reporte(sesiones, ruta_salida='./reporte_gamesec.txt'): # Llama a todas las funciones que imprimer los apartados del reportes y lo redirige al archivo, segun la ruta que introduzca el usuario
#VERIFICAR RUTA DE USUARIO EN CASO DE PERSONALIZADA
    stdout_original = sys.stdout

    with open(ruta_salida,'w+') as sys.stdout:
    
        imprimir_linea()
        print("REPORTE DE AUDITORIA Y TELETRIA GAMESEC")
        imprimir_linea()
        print("\n")
        reporte_primer_apartado(sesiones)
        reporte_segundo_apartado(sesiones)
        reporte_tercer_apartado(sesiones)
        reporte_cuarto_apartado()

    
    sys.stdout = stdout_original
    print(f"Reporte creado con exito en {ruta_salida}")
    pause()

    
def verificar_csv_cargado(csv_cargado):
    resultado = True
    if not csv_cargado:
        print("Debe cargar un csv con la opción 1")
        pause()
        resultado = False
    return resultado

# Las funciones "funcion1-5" Corresponden al llamado de las funciones de menu
# 1 -> Verifica y carga el archivo de telemetria
# 2 -> Imprime por pantalla las estadisticas globales
# 3 -> Imprime por pantalla las estadisticas por servidor
# 4 -> Imprime por pantalla los registros criticos
# 5 -> Exporta el reporte a archivo ./reporte_gamesex.txt
# 6 -> Break que sale del loop de menu y finaliza el programa
def funcion1()-> list[dict]:
    ruta_archivo = input("Por favor cargue la ruta de su archivo: ")
    csv_procesado = cargar_telemetria(ruta_archivo) # La misma funcion se encarga de verificar la existencia del archivo
    print("Archivo cargado de forma existosa")
    csv_cargado = True
    pause()
  
    return csv_procesado, csv_cargado # Retorna la tupla para que la funcion menu() pueda trabajar con el csv ya cargado, y el true, para "HABILITAR" a las otras funciones

def funcion2(csv_procesado,csv_cargado)-> None:
    if not verificar_csv_cargado(csv_cargado):
        return None

    estadisticas_globales = calcular_estadisticas_globales(csv_procesado)
    print("Estadisticas globales:")
    print(estadisticas_globales)
    pause()

def funcion3(csv_procesado,csv_cargado)-> None:
    if not verificar_csv_cargado(csv_cargado):
        return None
    
    estadisticas_por_servidor = analizar_por_servidor(csv_procesado)
    print("Estadisticas por servidor:")
    print(estadisticas_por_servidor)
    pause()

def funcion4(csv_procesado,csv_cargado)-> None:
    if not verificar_csv_cargado(csv_cargado):
        return None
    
    tupla = clasificar_incidentes(csv_procesado)
    dic_sospechosos = tupla[1]
    for registro in dic_sospechosos:
        print(registro)
    pause()

def funcion5(csv_procesado,csv_cargado)-> None:
    if not verificar_csv_cargado(csv_cargado):
        return None
    exportar_reporte(csv_procesado)



def menu()-> None:
    ingreso = None
    list_dic_principal = []
    csv_cargado = False
    while True:
        imprimir_cabecera()
        print("1. Cargar y validar dataset")
        print("2. Ver estadisticas globales de servidores")
        print("3. Ver rendimiento por region de servidor")
        print("4. Auditar incidentes de seguridad (Criticos y sospechosos)")
        print("5. Exportar reporte consolidades (reporte_gamesec.txt)")
        print("6. Salir")
        imprimir_linea()
        ingreso = int(input("Seleccione una opcion: "))
        if  not (0 < int(ingreso) <= 6):
            print("Por favor ingrese una opcion válida")
            pause()
            continue

        match ingreso:

            case 1:
               list_dic_principal,csv_cargado = funcion1()
                    
            case 2:
                funcion2(list_dic_principal,csv_cargado)
            case 3:
                funcion3(list_dic_principal,csv_cargado)
            case 4:
                funcion4(list_dic_principal,csv_cargado)
            case 5:
                funcion5(list_dic_principal,csv_cargado)
            case 6:
                break
    
#la ruta del archivo es ./TP_INTEGRADOR_TALLER_/gamesec_logs.csv
#OPCIONES QUE TAN BIEN
#1,2,3,4
menu()
print("Programa terminado...")
input(" ")
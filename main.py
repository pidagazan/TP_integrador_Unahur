from carga import *
from procesamiento import *

def imprimir_linea()-> None:
    print("="*75)

def imprimir_cabecera() -> None:
    imprimir_linea()
    print(""*10+"GAMESEC MONITOR - PANEL DE CONTROL")
    imprimir_linea()

def pause()-> None:
    input("Presiona una tecla...")


def exportar_reporte():
    pass

def funcion1()-> list[dict]:
    ruta_archivo = input("Por favor cargue la ruta de su archivo: ")
    csv_procesado = cargar_telemetria(ruta_archivo)
    print("Archivo cargado de forma existosa")
    pause()
    return csv_procesado

def funcion2(csv_procesado)-> None:
    estadisticas_globales = calcular_estadisticas_globales(csv_procesado)
    print("Estadisticas globales:")
    print(estadisticas_globales)
    pause()

def funcion3(csv_procesado)-> None:
    estadisticas_por_servidor = analizar_por_servidor(csv_procesado)
    print("Estadisticas por servidor:")
    print(estadisticas_por_servidor)
    pause()

def funcion4(csv_procesado)-> None:
    tupla = clasificar_incidentes(csv_procesado)
    dic_sospechosos = tupla[1]
    for registro in dic_sospechosos:
        print(registro)
    pause()

def funcion5()-> None:
    exportar_reporte()
    pause()



def menu()-> None:
    ingreso = None
    archivo_cargado = False
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

        match ingreso:

            case 1:
               list_dic_principal = funcion1()
                    
            case 2:
                funcion2(list_dic_principal)
            case 3:
                funcion3(list_dic_principal)
            case 4:
                funcion4(list_dic_principal)
            case 5:
                funcion5(list_dic_principal)
            case 6:
                break
    
#la ruta del archivo es ./TP_INTEGRADOR_TALLER_/gamesec_logs.csv
#OPCIONES QUE TAN BIEN
#1,2,3,4
#FALTA HACER LA 5, REPORTE A ARCHIVO.
menu()
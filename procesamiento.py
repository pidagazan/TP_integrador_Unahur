from carga import *

def calcular_promedio(valor:int, cantidad:int)-> float:
    return valor/cantidad

def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    dict_salida = {
        'total_sesiones': 0,
        'ping_promedio': 0.00, #redondeada a 2 dec
        'duracion_promedio': 0.00, #redondeada a 2 dec
        'porcentaje_competitivas': 0.00 #competitiva o torneo sobre global
    }

    total_sesiones = 0
    ping_promedio = 0
    duracion_promedio = 0
    porcentaje_competitivas = 0
            
    for registro in sesiones:
        total_sesiones += 1
        ping_promedio += registro['ping_promedio']
        duracion_promedio += registro['duracion_minutos']
        if registro['tipo_partida']== "Torneo" or registro['tipo_partida']== "Competitiva":
            porcentaje_competitivas += 1

    dict_salida['total_sesiones'] = total_sesiones
    dict_salida['ping_promedio'] = {f"{ping_promedio / total_sesiones:.2f}"}
    dict_salida['duracion_promedio'] = {f"{duracion_promedio / total_sesiones:.2f} Minutos"}
    dict_salida['porcentaje_competitivas'] = {f"{(porcentaje_competitivas / total_sesiones)*100:.2f}% ({porcentaje_competitivas}Competitivas/{total_sesiones}Casual)"}

    return dict_salida

def analizar_por_servidor(sesiones: list[dict]) -> dict:
    dict_salida = dict()

    for sesion in sesiones:
        if sesion['servidor'] not in dict_salida.keys():
            dict_salida[sesion['servidor']] = {'cantidad':1, 'ping_promedio':0, 'fps_promedio':0}
        else:
            dict_salida[sesion['servidor']]['cantidad'] += 1
            dict_salida[sesion['servidor']]['ping_promedio'] += sesion['ping_promedio']
            dict_salida[sesion['servidor']]['fps_promedio'] += sesion['fps_promedio']
    


    for key in dict_salida.keys():
        servidor = dict_salida[key]

        cantidad_sesiones = servidor.get("cantidad")
        
        dict_salida[key]['ping_promedio'] = f"{dict_salida[key]['ping_promedio'] / cantidad_sesiones:.2f}"
        dict_salida[key]['fps_promedio'] = f"{dict_salida[key]['fps_promedio'] / cantidad_sesiones:.2f}"

    
    return dict_salida

def reglas_seguridad(registro:dict):
    clasificacion = None
    if registro['reportes_trampa'] >= 3 or registro['intentos_fallidos'] >= 4:
        clasificacion = "Critica"
    elif (registro['ping_promedio'] > 200 and registro['intentos_fallidos'] >= 2) or (registro['reportes_trampa'] ==2 ):
        clasificacion = "Sospechoso"
    else:
        clasificacion = "Normal"
    
    return clasificacion

def clasificar_incidentes(sesiones: list[dict])-> tuple[dict, list[dict]]:
    dict_contador = dict()
    lista_criticos = list()


    total_normales = 0
    total_criticos = 0
    total_sospechosos = 0
    
    for sesion in sesiones:
        seguridad_sesion = reglas_seguridad(sesion)
        match seguridad_sesion:
            case "Normal":
                total_normales += 1
            case "Critica":
                total_criticos += 1
            case "Sospechoso":
                total_sospechosos += 1
        if seguridad_sesion == "Critica":
            dic_resumido = {
                'id_sesion':sesion['id_sesion'],
                'jugador_id':sesion['jugador_id'],
                'servidor':sesion['servidor'],
                'motivo':f"Exceso de reportes trampa ({sesion['reportes_trampa']}) e intentos fallidos ({sesion['intentos_fallidos']})"
            }
            lista_criticos.append(dic_resumido)

    dict_contador['Normal']=total_normales
    dict_contador['Sospechoso']=total_sospechosos
    dict_contador['Critico']=total_criticos

    return dict_contador, lista_criticos

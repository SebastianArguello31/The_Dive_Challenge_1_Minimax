# Importamos librerias
import os
import time
import random

# Definimos el tamaño del laberinto
FILAS = 10
COLUMNAS = 20

# Definimos la cantidad maximo de turnos que tendra el juego
TURNOS_MAX = 50

# Funcion para generar una ubicacion valida en el laberinto
def generar_posicion(lugar_ocupado):
    while True:
        x = random.randint(0 , FILAS - 1)
        y = random.randint(0, COLUMNAS - 1)

        if [x, y] not in lugar_ocupado: 
            return [x, y]

# Funcion para mostrar el laberinto
def mostrar_laberinto(meta, pos_gato, pos_raton, turnos):
    os.system('cls')

    print('-------------------------- LABERINTO --------------------------')
    print(f'----- TURNO {turnos} / {TURNOS_MAX} ------\n')
    print('#' * (COLUMNAS * 3 + 2))

    for x in range(FILAS):
        linea = '#' # lado izquierdo

        for y in range(COLUMNAS):
            posicion_actual = [x, y]
            if posicion_actual == pos_raton and posicion_actual == pos_gato: 
                linea += '💀 '
            elif posicion_actual == pos_gato: 
                linea += '😺 '
            elif posicion_actual == pos_raton: 
                linea += '🐭 '
            elif posicion_actual == meta: 
                linea += '🏁 '
            else: 
                linea += ' . '

        print(linea + '#') # lado derecho
    print('#' * (COLUMNAS * 3 + 2))

# Funcion para calcular la heuristica con distancia Manhattan -> d = |y1 - y2| + |x1 - x2|
def heuristica(meta, pos_gato, pos_raton):
    dist_gato_raton = abs(pos_gato[1] - pos_raton[1]) + abs(pos_gato[0] - pos_raton[0])
    dist_raton_meta = abs(pos_raton[1] - meta[1]) + abs(pos_raton[0] - meta[0])
    
    # El ratón quiere maximizar distancia al gato y minimizar a la meta
    return dist_gato_raton - (dist_raton_meta * 2) # 2 --> Peso

# Funcion para obtener todos los movimientos posibles
def obtener_movimientos(posicion):
    x, y = posicion
    movimientos = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < FILAS and 0 <= ny < COLUMNAS:
            movimientos.append([nx, ny])
    return movimientos

# Algoritmo MINIMAX
def minimax(pos_gato, pos_raton, meta, profundidad, es_max):
    # Casos Base
    if pos_gato == pos_raton: return -10000 + (50 - profundidad)
    if pos_raton == meta: return 10000 + profundidad
    if profundidad == 0: return heuristica(meta, pos_gato, pos_raton)

    if es_max:
        mejor_valor = -float('inf')
        for mov in obtener_movimientos(pos_raton):
            # Llamada recursiva (cambia a turno del Gato)
            valor = minimax(pos_gato, mov, meta, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for mov in obtener_movimientos(pos_gato):
            # Llamada recursiva (cambia a turno del Ratón)
            valor = minimax(mov, pos_raton, meta, profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def obtener_mejor_movimiento(esRaton, pos_gato, pos_raton, meta):
    profundidad = 5
    movimientos = obtener_movimientos(pos_raton if esRaton else pos_gato)
    mejores_movs = []

    if esRaton:
        mejor_val = -float('inf')
        for mov in movimientos:
            val = minimax(pos_gato, mov, meta, profundidad, False)
            if val > mejor_val:
                mejor_val, mejores_movs = val, [mov]
            elif val == mejor_val:
                mejores_movs.append(mov)
    else:
        mejor_val = float('inf')
        for mov in movimientos:
            val = minimax(mov, pos_raton, meta, profundidad, True)
            if val < mejor_val:
                mejor_val, mejores_movs = val, [mov]
            elif val == mejor_val:
                mejores_movs.append(mov)
                
    return random.choice(mejores_movs)

# Funcion que gestiona y valida las entradas del usuario para generar el movimiento
def movimiento_jugador(pos_actual):
    direcciones = {'w' : [-1, 0], 's' : [1, 0], 'a' : [0, -1], 'd' : [0, 1]}

    while True:
        tecla = input('\nTu movimiento (WASD): ').lower()

        if tecla in direcciones:
            dx, dy = direcciones[tecla]
            nx, ny = pos_actual[0] + dx, pos_actual[1] + dy
            if 0 <= nx < FILAS and 0 <= ny < COLUMNAS: return [nx, ny]
            else: print('Hay un obstaculo bloqueando el paso. Intenta otra vez')
        else: print('Tecla invalida. Usa W, A, S o D')

def empezar_juego():
    bandera = True
    
    # Menu de Inicio
    while bandera: 
        os.system('cls')
        print('-' * 50)
        print('JUEGO DEL LABERINTO - GATO VS. RATON')
        print('-' * 50)
        print('1. Jugar como Raton (🐭) --> Escapa del Gato IA')
        print('2. Jugar como Gato (😺) --> Atrapa al Raton IA')
        print('-' * 50)
        opcion = input('Elige (1 o 2): ')

        if opcion == '1' or opcion == '2':
            bandera = False
        else:
            print('\nLa opcion debe ser 1 o 2 para iniciar el juego')
            time.sleep(1)

    # Generar la meta, el gato y el raton en lugares vacios
    meta = generar_posicion([])
    posicion_gato = generar_posicion([meta])
    posicion_raton = generar_posicion([meta, posicion_gato])
    
    turnos = 1

    while turnos <= TURNOS_MAX:
        mostrar_laberinto(meta, posicion_gato, posicion_raton, turnos)

        # Turno del raton
        if opcion == '1': # --> El jugador es el raton
            posicion_raton = movimiento_jugador(posicion_raton)
        else: # --> La IA es el raton
            print('\nEl raton esta pensando...')
            posicion_raton = obtener_mejor_movimiento(True, posicion_gato, posicion_raton, meta)

        if posicion_raton == meta:
            mostrar_laberinto(meta, posicion_gato, posicion_raton, turnos)
            print('\nEl raton ha escapado. VICTORIA el raton')
            break

        # Turno del gato
        if opcion == '2': # --> El jugador es el gato
            posicion_gato = movimiento_jugador(posicion_gato)
        else: # --> La IA es el gato
            print('\nEl gato esta pensado...')
            posicion_gato = obtener_mejor_movimiento(False, posicion_gato, posicion_raton, meta)

        if posicion_gato == posicion_raton:
            mostrar_laberinto(meta, posicion_gato, posicion_raton, turnos)
            print('\nEl raton ha sido atrapado. VICTORIA el gato')
            break

        turnos += 1
        time.sleep(0.5)
    
    if turnos > TURNOS_MAX:
        mostrar_laberinto(meta, posicion_gato, posicion_raton, TURNOS_MAX)
        print(f'\nTIEMPO AGOTADO. Se alcanzaron los {TURNOS_MAX} turnos')
        print('El raton no llego a la meta, pero el gato no lo atrapo. EMPATE')

if __name__ == '__main__':
    empezar_juego()
                                 
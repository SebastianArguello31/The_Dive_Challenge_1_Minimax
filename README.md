# LABERINTO GATO Y RATON: MINIMAX EN PYTHON

Este proyecto consiste en el desarrollo de un simulador táctico en Python donde se modela una persecución inteligente dentro de un entorno controlado. La aplicación utiliza el algoritmo **Minimax** para gestionar la toma de decisiones de los agentes, permitiendo una confrontación de estrategias entre un perseguidor (gato) y un evasivo (ratón).

---

## Descripción del Entorno

El sistema genera un tablero bidimensional de $10 \times 20$ unidades. En este espacio, se posicionan de forma aleatoria tres entidades:

- **El Gato (😺):** Agente cuyo objetivo es interceptar al ratón.
- **El Ratón (🐭):** Agente cuyo objetivo es alcanzar la salida evitando la captura.
- **La Meta (🏁):** El punto de escape para el ratón.

El programa gestiona una lógica de turnos estricta con un límite de **50 movimientos**, tras los cuales, si no hay un ganador claro, se declara un empate por agotamiento de recursos.

---

## Fundamentos de la Inteligencia Artificial: Minimax

El núcleo estratégico del proyecto es el algoritmo **Minimax**, una técnica de búsqueda en árboles de decisión para juegos de suma cero.

### **Función de Evaluación y Heurística**

Dado que el estado del juego debe ser cuantificable, se implementó la **Distancia Manhattan** ($d = |x_1 - x_2| + |y_1 - y_2|$) para calcular la ventaja de cada posición:

$$
Valor = Distancia(Gato, Ratón) - (Distancia(Ratón, Meta) \times 2)
$$

- **Perspectiva del Ratón (MAX):** Busca maximizar este valor. Un valor alto indica que está lejos del peligro y cerca de su objetivo.
- **Perspectiva del Gato (MIN):** Busca minimizar este valor. Un valor bajo indica que ha logrado reducir la distancia de captura.

### Optimización y Profundidad

Se ha configurado una profundidad de búsqueda de **5 niveles**. Esta decisión técnica garantiza un comportamiento inteligente y anticipatorio sin comprometer el rendimiento de la CPU, permitiendo respuestas en tiempo real.

---

## Modos de Juego

El simulador ofrece una experiencia interactiva donde puedes elegir tu bando:

1. **Jugar como Ratón (🐭):** Controla al ratón con las teclas `WASD` e intenta burlar a un Gato IA que predice tus movimientos.
2. **Jugar como Gato (😺):** Intenta acorralar a un Ratón IA extremadamente escurridizo antes de que alcance la meta o se acaben los **50 turnos**.

---

## Estructura del Código y Funciones Clave

El archivo principal incluye:

- `minimax()`: Función recursiva que evalúa los estados futuros.
- `obtener_mejor_movimiento()`: Actúa como puente entre la lógica de la IA y el motor del juego.
- `heuristica()`: Calcula el peso estratégico de cada casilla basándose en las distancias relativas.
- `mostrar_laberinto()`: Gestiona el renderizado visual en la terminal mediante la limpieza de búfer (`cls`).

---

## Cómo Ejecutar

Para iniciar la simulación, asegúrese de tener Python 3 instalado y ejecute:

```git clone git@github.com:SeBa031/Minimax.git``` 
```cd Minimax```
```python minimax_lab.py```

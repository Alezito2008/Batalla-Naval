from enum import Enum

class Estados(Enum):
    AGUA = '🌊'
    BARCO = '🚢'
    DISPARADO = '🔫'
    HUNDIDO = '❌'

class Tablero:
    def __init__(self, ancho: int, alto: int, disparos: int):
        self.ancho = ancho
        self.alto = alto
        self.disparos = disparos
        self.tablero: list[list[Estados]] = []
        # iterar por cada fila
        for _ in range(alto):
            fila: list[Estados] = []
            # iterar por cada columna de cada fila
            for _ in range(ancho):
                fila.append(Estados.AGUA)
            self.tablero.append(fila)

    # formato para imprimir
    def __str__(self):
        tablero_texto: str = ''
        # iterar por cada fila
        for fila in range(self.alto):
            # iterar por cada elemento de cada fila
            for columna in range(self.ancho):
                tablero_texto += self.tablero[fila][columna].value
            tablero_texto += '\n'
        return tablero_texto

    def cambiarEstado(self, x, y, estado):
        if not isinstance(estado, Estados):
            raise ValueError(f"{Estados} no es un estado")
        if x > self.ancho or y > self.alto:
            raise IndexError(f"Las coordenadas (x={x}, y={y}) están fuera del tablero ({self.ancho}, {self.alto})")
        self.tablero[x][y] = estado


tablero = Tablero(
    ancho=10,
    alto=10,
    disparos=20
)

tablero.cambiarEstado(0, 0, Estados.BARCO)

print(tablero)

# Documentación Clases: https://www.w3schools.com/python/python_classes.asp
# Vars: https://www.w3schools.com/python/ref_func_vars.asp

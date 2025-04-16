from tablero import Tablero

class Jugador:
    """
    Clase Jugador que contiene al nombre y su tablero
    Args:
        nombre (str): Nombre del jugador
        tablero (Tablero): Tablero del jugador
    """
    def __init__(self, nombre: str, tablero: Tablero):
        self.nombre = nombre
        self.tablero = tablero

    def __str__(self) -> str:
        return self.nombre
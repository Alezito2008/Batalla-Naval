from enum import Enum

class Estados(Enum):
    AGUA = '🌊'
    BARCO = '🚢'
    DISPARADO = '🔫'
    HUNDIDO = '❌'

class Direcciones(Enum):
    """Direcciones con sus respectivos desplazamientos"""
    ARRIBA = (-1, 0)
    ABAJO = (1, 0)
    IZQUIERDA = (0, -1)
    DERECHA = (0, 1)
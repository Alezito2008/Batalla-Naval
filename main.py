from enum import Enum

type Punto = tuple[int, int]

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

class Barco:
    """
    Crea un barco
    Args:
        posiciones (list[Punto]): Posiciones que ocupa el barco
    """
    def __init__(self, posiciones: list[Punto]) -> None:
        self.posiciones: list[Punto] = posiciones
        self.disparado: set[Punto] = set()


class Casilla:
    def __init__(self) -> None:
        self.estado: Estados = Estados.AGUA

    def __str__(self) -> str:
        return self.estado.value

class Juego:
    """
    Inicializa un juego con un tablero vacío.

    Crea una tabla del tamaño `ancho` x `alto` con elementos de tipo `Casilla`.
    Args:
        ancho (int): Cantidad de columnas del tablero.
        alto (int): Cantidad de filas del tablero.
        disparos (int): Cantidad de disparos disponibles para el jugador.
    """
    def __init__(self, ancho: int, alto: int, disparos: int) -> None:
        self.barcos: list[Barco] = []
        self.disparos: int = disparos

        self.ancho: int = ancho
        self.alto: int = alto
        self.tablero: list[list[Casilla]] = []
        # iterar por cada fila
        for _ in range(alto):
            fila: list[Casilla] = []
            # iterar por cada columna de cada fila
            for _ in range(ancho):
                casilla = Casilla()
                fila.append(casilla)
            self.tablero.append(fila)

    # formato para imprimir
    def __str__(self) -> str:
        tablero_texto: str = ''
        # iterar por cada fila
        for fila in range(self.alto):
            # iterar por cada elemento de cada fila
            for columna in range(self.ancho):
                tablero_texto += str(self.obtener_casilla((fila, columna)))
            tablero_texto += '\n'
        return tablero_texto
    
    def obtener_casilla(self, coords: Punto) -> Casilla:
        """
        Obtiene una casilla según sus coordenadas.
        Args:
            coords (Punto): Las coordenadas de la casilla a obtener.
        Returns:
            Casilla: Objeto `Casilla` correspondiente a la posición del tablero.
        """
        x, y = coords
        return self.tablero[x][y]

    def esta_adentro(self, coords: Punto) -> bool:
        """
        Comprueba si un punto está dentro del tablero.
        Args:
            coords (Punto): Las coordenadas de la casilla a obtener.
        Returns:
            bool: True si está dentro, de lo contrario False.
        """
        x, y = coords
        return x < self.ancho and y < self.alto and x >= 0 and y >= 0
    
    def validar_coordenadas(self, coords: Punto) -> None:
        """
        Valida si las coordenadas dadas están dentro del tablero.
        Args:
            coords (Punto): Las coordenadas de la casilla a obtener.
        Raises:
            IndexError: Si el punto está fuera de la tabla.
        """
        x, y = coords
        if not self.esta_adentro((x, y)):
            raise IndexError(f"Las coordenadas (x={x}, y={y}) están fuera del tablero ({self.ancho}, {self.alto})")

    def cambiar_estado(self, coords: Punto, estado: Estados) -> None:
        """
        Cambia el estado de una casilla.
        Args:
            coords (Punto): Las coordenadas de la casilla a obtener.
            estado (Estados): Estado a establecer la casilla.
        Raises:
            ValueError: Si el argumento `estado` no es del tipo `Estados`.
        Ejemplo::

            self.cambiar_estado((0, 0), Estados.BARCO)
        """
        x, y = coords
        self.validar_coordenadas(coords)
        if not isinstance(estado, Estados):
            raise ValueError(f"{Estados} no es un estado")
        self.obtener_casilla(coords).estado = estado

    def agregar_barco(self, punto_inicio: Punto, largo: int, direccion: Direcciones):
        """
        Agrega un barco al tablero.

        Crea un barco con el largo y dirección dada, cambia los estados de las casillas y agrega un objeto `Barco` a la lista de barcos del juego
        Args:
            punto_inicio (Punto): Punto desde el que se va a generar.
            largo (int): Largo del barco.
            direccion (Direcciones): Direccion del barco.
        Raises:
            IndexError: Si ya hay otro barco o queda fuera del tablero
        Ejemplo::

            juego.agregar_barco(punto_inicio=(3, 2), largo=5, direccion=Direcciones.DERECHA)
        """
        self.validar_coordenadas(punto_inicio)
        x, y = punto_inicio
        dx, dy = direccion.value

        posiciones: list[Punto] = []

        # compara la coordenada inicial con cada elemento que sigue
        for i in range(largo):
            posX = x + dx * i
            posY = y + dy * i

            if not self.esta_adentro((posX, posY)):
                raise IndexError("La posición no está dentro del tablero")
            if self.obtener_casilla((posX, posY)).estado != Estados.AGUA:
                raise IndexError(f"Ya hay otro barco en la posición (x={posX}, y={posY})")
            
            posiciones.append((posX, posY))
            
        self.barcos.append(Barco(posiciones))
        for posicion in posiciones:
            self.cambiar_estado(posicion, Estados.BARCO)

    # TODO poder disparar
    def disparar(self, coords: Punto) -> None:
        x, y = coords


        

juego = Juego(
    ancho=10,
    alto=10,
    disparos=20
)

juego.agregar_barco(punto_inicio=(3, 2), largo=5, direccion=Direcciones.DERECHA)

print(juego)

# Documentación clases: https://www.w3schools.com/python/python_classes.asp
# Documentación sets: https://www.w3schools.com/python/python_sets.asp
# Documentacion enum: https://docs.python.org/3/library/enum.html
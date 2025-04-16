from utils import Punto, LETRAS
from enums import Estados, Direcciones

from itertools import product
import random

class Barco:
    """
    Crea un barco
    Args:
        posiciones (list[Punto]): Posiciones que ocupa el barco
    """
    def __init__(self, posiciones: list[Punto]) -> None:
        self.posiciones: list[Punto] = posiciones
        self.disparado: set[Punto] = set()

    def disparar(self, coordenada: Punto) -> Estados:
        """
        Llamado al ser disparado
        Args:
            coordenada (Punto): Coordenada en la que fue disparado
            Returns:
                Estados: Devuelve `Estados.BARCO_DISPARADO` hasta que no quede ninguna parte sin disparar y ahí devuelve `Estados.HUNDIDO`
        """
        self.disparado.add(coordenada)
        if len(self.posiciones) != len(self.disparado):
            return Estados.BARCO_DISPARADO
        return Estados.HUNDIDO

class Casilla:
    def __init__(self) -> None:
        self.estado: Estados = Estados.MAR
        self.barco: Barco | None = None

    def __str__(self) -> str:
        return self.estado.value

class Tablero:
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
        self.disparos_restantes: int = disparos
        self.barcos_hundidos: int = 0

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
        tablero_texto: str = '   '
        # agregar letras
        tablero_texto += ''.join([f' {i} ' for i in LETRAS[:self.ancho]]) + '\n'
        # iterar por cada fila
        for fila in range(self.alto):
            # agregar numeros
            tablero_texto += f' {fila} '
            # iterar por cada elemento de cada fila
            for columna in range(self.ancho):
                tablero_texto += str(self.obtener_casilla((fila, columna))) + ' '
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
            coords (Punto): Las coordenadas de la casilla a comprobar.
        Returns:
            bool: True si está dentro, de lo contrario False.
        """
        x, y = coords
        return x < self.ancho and y < self.alto and x >= 0 and y >= 0
    
    def validar_coordenadas(self, coords: Punto) -> None:
        """
        Valida si las coordenadas dadas están dentro del tablero.
        Args:
            coords (Punto): Las coordenadas de la casilla a validar.
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
            coords (Punto): Las coordenadas de la casilla que cambiará de estado.
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
            # consigue la nueva posicion
            posX: int = x + dx * i
            posY: int = y + dy * i

            casilla: Casilla = self.obtener_casilla((posX, posY))

            if not self.esta_adentro((posX, posY)):
                raise IndexError("La posición no está dentro del tablero")
            if casilla.estado != Estados.MAR:
                raise IndexError(f"Ya hay otro barco en la posición (x={posX}, y={posY})")
            
            # si salió todo bien lo agrega a `posiciones`
            posiciones.append((posX, posY))
            
        nuevo_barco: Barco = Barco(posiciones)
        self.barcos.append(nuevo_barco)

        for posicion in posiciones:
            self.cambiar_estado(posicion, Estados.BARCO)
            self.obtener_casilla(posicion).barco = nuevo_barco

    def disparar(self, coords: Punto) -> bool:
        """
        Dispara a un barco
        Args:
            coords (Punto): Las coordenadas de la casilla a disparar.
        Returns:
            bool: True si se disparó en una nueva posición, de lo contrario False
        Raises:
            IndexError: Si el punto está fuera de la tabla.
        """
        self.validar_coordenadas(coords)

        casilla = self.obtener_casilla(coords)

        if casilla.estado == Estados.BARCO and casilla.barco is not None:
            # disparar y obtener el estado luego de ser disparado
            estado_barco: Estados = casilla.barco.disparar(coords)

            if estado_barco == Estados.BARCO_DISPARADO:
                casilla.estado = Estados.BARCO_DISPARADO
            else:
                # si el barco se hundió
                self.barcos_hundidos += 1
                for posicion in casilla.barco.posiciones:
                    self.obtener_casilla(posicion).estado = Estados.HUNDIDO
            self.disparos_restantes -= 1
            return True
        elif casilla.estado == Estados.MAR:
            casilla.estado = Estados.MAR_DISPARADO
            self.disparos_restantes -= 1
            return True
        return False
    
    def colocar_barcos_random(self, cantidad: int, largo: int) -> None:
        """
        Coloca barcos aleatoriamente en el tablero.
        
        Barcos son colocados aleatoriamente en el tablero. Se busca cada posición y dirección en el tablero, se randomiza y cicla por cada uno hasta que se hayan puesto los barcos
        Args:
            cantidad (int): Cantidad de barcos a colocar.
            largo_maximo (int): Largo máximo de los barcos.
        """
        posibles_posiciones: list[tuple[Punto, Direcciones]] = []
        barcos_agregados: int = 0
        # Obtener combinaciones: https://stackoverflow.com/questions/10975045/python-return-combinations-of-a-list-of-ranges
        for x, y in product(range(self.ancho), range(self.alto)):
            # por cada punto del tablero
            for direccion in Direcciones:
                posibles_posiciones.append(((x, y), direccion))

        random.shuffle(posibles_posiciones)

        for punto, direccion in posibles_posiciones:
            try:
                self.agregar_barco(punto_inicio=punto, direccion=direccion, largo=largo)
                barcos_agregados += 1
                if barcos_agregados == cantidad:
                    break
            except IndexError:
                continue

        if barcos_agregados != cantidad:
            print(f"Solo se pudieron colocar {barcos_agregados} / {cantidad} barcos")

if __name__ == "__main__":
    print("⚠️ Este archivo es un módulo, ejecutar `main.py`")

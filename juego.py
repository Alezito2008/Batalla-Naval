from tablero import Tablero
from jugador import Jugador
from enums import Direcciones
from utils import limpiar_pantalla, pedir_entero, pedir_coordenadas, pedir_nombre, pedir_direccion, preguntar_si_o_no, Punto

class Juego:
    def __init__(self) -> None:
        self._configurado: bool = False
        self._juego_terminado: bool = False

    def configurar(self) -> None:
        """Pide la configuración al usuario para el juego, debe ser llamado antes de ser iniciado"""
        self.ancho: int = pedir_entero("⬅️  ➡️  Ancho del tablero (10): ", 10)
        self.alto: int = pedir_entero("⬆️  ⬇️  Alto del tablero (10): ", 10)
        self.disparos: int = pedir_entero("🔫 Disparos (20): ", 20)
        self.cantidad_barcos:int = pedir_entero("🚢 Cantidad de barcos (5): ", 5)
        self.largo_barcos: int = pedir_entero("🚢 Tamaño de los barcos (3): ", 3)
        self.jugadores: list[Jugador] = []
        self._es_multijugador: bool

        self._es_multijugador = preguntar_si_o_no("👥 Multijugador (s/n): ", "n")

        if self._es_multijugador:
            for i in range(2):
                jugador = self._crear_jugador(i + 1)
                self.jugadores.append(jugador)
        else:
            self.jugadores.append(self._crear_jugador(1))

        self._configurado = True

        limpiar_pantalla()

    def _crear_jugador(self, jugador_num: int) -> Jugador:
        """Crea un jugador con nombre y tablero"""
        nombre: str = pedir_nombre(f"Nombre del jugador {jugador_num}: ", f"Jugador {jugador_num}")
        tablero = Tablero(ancho=self.ancho, alto=self.alto, disparos=self.disparos)
        return Jugador(nombre=nombre, tablero=tablero)

    def _mostrar_tablero(self, jugador: Jugador) -> None:
        """Muestra el tablero actualizado junto con la información del juego"""
        limpiar_pantalla()
        print(jugador.tablero)
        print('---' * self.ancho + '--')
        print(f"🔫 {jugador.tablero.disparos_restantes} - 🚢 {jugador.tablero.barcos_hundidos} / {self.cantidad_barcos}")
        print('---' * self.ancho + '--')

    def _poner_barcos(self, jugador: Jugador) -> None:
        """Coloca los barcos en el tablero del jugador"""
        if preguntar_si_o_no("🚢 ¿Colocar barcos aleatoriamente? (s/n): ", "s"):
            jugador.tablero.colocar_barcos_random(cantidad=self.cantidad_barcos, largo=self.largo_barcos)
            return
        limpiar_pantalla()
        for i in range(self.cantidad_barcos):
            while True:
                limpiar_pantalla()
                print('---' * self.ancho + '--')
                print(f"{jugador.nombre} - 🚢 {i} / {self.cantidad_barcos}")
                print('---' * self.ancho + '--')

                print(jugador.tablero)
                coords: Punto = pedir_coordenadas()
                direccion: Direcciones = pedir_direccion()
                try:
                    jugador.tablero.agregar_barco(punto_inicio=coords, largo=self.largo_barcos, direccion=direccion)
                    self._mostrar_tablero(jugador)
                    break
                except IndexError as e:
                    print(e)
                    print("Presionar Enter para continuar")
                    input()

    def iniciar(self) -> None:
        """
        Loop principal del juego
        Raises:
            RuntimeError: Cuando el juego no está configurado
        """
        if not self._configurado:
            raise RuntimeError("El juego no está configurado. Llamar a `configurar` antes")

        if self._es_multijugador:
            for jugador in self.jugadores:
                self._poner_barcos(jugador)
        else:
            self.jugadores[0].tablero.colocar_barcos_random(cantidad=self.cantidad_barcos, largo=self.largo_barcos)

        while not self._juego_terminado:
            for turno, jugador_actual in enumerate(self.jugadores):
                if self._es_multijugador:
                    oponente = self.jugadores[(turno + 1) % 2]
                else:
                    oponente = self.jugadores[0]

                self._mostrar_tablero(oponente)
                print(f"Turno de {jugador_actual.nombre}")
                coords = pedir_coordenadas()

                try:
                    oponente.tablero.disparar(coords)
                except IndexError:
                    print(IndexError)
                
                if self._es_multijugador:
                    self._mostrar_tablero(oponente)
                    print("Presionar Enter para continuar")
                    input()

                if oponente.tablero.barcos_hundidos == self.cantidad_barcos:
                    print(f"¡{jugador_actual.nombre} ganó! 🎉")
                    self._juego_terminado = True
                    break

                if oponente.tablero.disparos_restantes <= 0:
                    print("Te quedaste sin disparos 😣")
                    self._juego_terminado = True
                    break

if __name__ == "__main__":
    print("⚠️ Este archivo es un módulo, ejecutar `main.py`")

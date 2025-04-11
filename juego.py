from tablero import Tablero
from utils import letras_a_coordenadas, limpiar_pantalla, pedir_entero, Punto

class Juego:
    def __init__(self) -> None:
        self.ancho: int
        self.alto: int
        self.disparos: int
        self.cantidad_barcos: int
        self.largo_barcos: int

        self.tablero: Tablero

        self.configurado: bool = False
        self.juego_terminado: bool = False

    def pedir_configuracion(self) -> None:
        """Pide la configuración al usuario para el juego, debe ser llamado antes de ser iniciado"""
        self.ancho: int = pedir_entero("⬅️  ➡️  Ancho del tablero (10): ", 10)
        self.alto: int = pedir_entero("⬆️  ⬇️  Alto del tablero (10): ", 10)
        self.disparos: int = pedir_entero("🔫 Disparos (20): ", 20)
        self.cantidad_barcos:int = pedir_entero("🚢 Cantidad de barcos (5): ", 5)
        self.largo_barcos: int = pedir_entero("🚢 Tamaño de los barcos (3): ", 3)

        self.tablero = Tablero(
            ancho=self.ancho,
            alto=self.alto,
            disparos=self.disparos
        )

        self.tablero.colocar_barcos(
            cantidad=self.cantidad_barcos,
            largo=self.largo_barcos
        )

        self.configurado = True

        limpiar_pantalla()

    def refrescar_pantalla(self) -> None:
        """Muestra el tablero actualizado junto con la información del juego"""
        limpiar_pantalla()
        print(self.tablero)
        print('-' * self.ancho * 3 + '--')
        print(f"🔫 {self.tablero.disparos_restantes} - 🚢 {self.tablero.barcos_hundidos} / {self.cantidad_barcos}")
        print('-' * self.ancho * 3 + '--')

    def pedir_coordenadas(self) -> Punto:
        """
        Pide las coordenadas al usuario
        Returns:
            Punto: Coordenadas ingresadas
        """
        entrada_coordenadas: str = input("Coordenadas a disparar: ")
        try:
            coords: Punto = letras_a_coordenadas(entrada_coordenadas)
        except ValueError as e:
            print(e)
            return self.pedir_coordenadas()
        
        return coords

    def mainloop(self) -> None:
        """
        Loop principal del juego
        Raises:
            RuntimeError: Cuando el juego no está configurado
        """
        if not self.configurado:
            raise RuntimeError("El juego no está configurado. Llamar a `pedir_configuracion` antes")

        self.refrescar_pantalla()

        while not self.juego_terminado:

            coords = self.pedir_coordenadas()

            try:
                self.tablero.disparar(coords)
            except IndexError:
                print(IndexError)

            self.refrescar_pantalla()

            if self.tablero.disparos_restantes <= 0:
                print("Te quedaste sin disparos 😣")
                self.juego_terminado = True

if __name__ == "__main__":
    print("⚠️ Este archivo es un módulo, ejecutar `main.py`")

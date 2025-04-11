import string
import re

LETRAS = string.ascii_uppercase

type Punto = tuple[int, int]

def letras_a_coordenadas(letras: str) -> Punto:
    """
    Convierte entrada de letras y números a una coordenada
    Args:
        letras (str): Letras y números que serán usados como coordenada
    Raises:
        ValueError: Si no contiene letras y números
    Ejemplo::

        letras_a_coordenadas('C2') // (6, 3)
        letras_a_coordenadas('2C') // (6, 3)
    """
    match_numeros: re.Match[str] | None = re.search(r'\d+', letras)
    match_letras: re.Match[str] | None = re.search(r'[a-zA-Z]', letras)
    if match_numeros is None:
        raise ValueError(f'No se encontraron números')
    if match_letras is None:
        raise ValueError(f'No se encontraron letras')
    
    x: int = int(match_numeros.group(0))
    y: int = LETRAS.index(match_letras.group(0).upper())
    return (x, y)

def limpiar_pantalla() -> None:
    """
    Limpia la pantalla de la consola.
    """
    print("\033[H\033[J", end="")

def pedir_entero(mensaje: str, default: int) -> int:
    """
    Pide un número entero al usuario mayor a 0.
    Args:
        mensaje (str): Mensaje de la entrada.
        default (int): Valor predeterminado para el número.
    Returns:
        int: Numero ingresado
    Ejemplo::

        largo: int = pedir_entero(mensaje="Introduce el largo (3): ", default=3)
    """
    while True:
        entrada = input(mensaje) or str(default)
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        print("⚠️ Ingresá número entero mayor a 0")

if __name__ == "__main__":
    print("⚠️ Este archivo es un módulo, ejecutar `main.py`")

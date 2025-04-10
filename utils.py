import string
import re

LETRAS = string.ascii_uppercase

type Punto = tuple[int, int]

def letras_a_coordenadas(letras: str) -> Punto:
    """
    Convierte entrada de letras y números a una coordenada
    Args:
        letras (str): Letras y números que serán usados como coordenada
    Ejemplo::

        letras_a_coordenadas('C2') // (6, 3)
        letras_a_coordenadas('2C') // (6, 3)
    """
    match_numeros: re.Match[str] | None = re.search(r'\d+', letras)
    match_letras: re.Match[str] | None = re.search(r'[a-zA-Z]', letras)
    if match_numeros is None:
        raise ValueError(f'No se encontraron números en {letras}')
    if match_letras is None:
        raise ValueError(f'No se encontraron letras en {letras}')
    
    x: int = int(match_numeros.group(0))
    y: int = LETRAS.index(match_letras.group(0).upper())
    return (x, y)

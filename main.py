import sys
sys.path.append(".")

from enums import Direcciones
from tablero import Juego
from utils import letras_a_coordenadas

def jugar():
    # TODO: Poder ingresar los datos y jugar
    juego = Juego(
        ancho=20,
        alto=10,
        disparos=20
    )

    juego.agregar_barco(punto_inicio=(0, 1), largo=5, direccion=Direcciones.DERECHA)
    juego.disparar(letras_a_coordenadas('B0'))
    juego.disparar(letras_a_coordenadas('C0'))
    juego.disparar(letras_a_coordenadas('D0'))
    juego.disparar(letras_a_coordenadas('E0'))
    juego.disparar(letras_a_coordenadas('F0'))

    juego.disparar(letras_a_coordenadas('H3'))

    print(juego)

if __name__ == '__main__':
    jugar()

# Documentación clases: https://www.w3schools.com/python/python_classes.asp
# Documentación sets: https://www.w3schools.com/python/python_sets.asp
# Documentacion enum: https://docs.python.org/3/library/enum.html
# Documentacion RegEx: https://docs.python.org/es/3.13/library/re.html
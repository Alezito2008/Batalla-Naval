import sys
sys.path.append(".")

from juego import Juego

if __name__ == '__main__':
    juego = Juego()
    juego.configurar()
    juego.iniciar()

# Documentación clases: https://www.w3schools.com/python/python_classes.asp
# Documentación sets: https://www.w3schools.com/python/python_sets.asp
# Documentacion enum: https://docs.python.org/3/library/enum.html
# Documentacion RegEx: https://docs.python.org/es/3.13/library/re.html
# Documentaicón enumerate: https://www.w3schools.com/python/ref_func_enumerate.asp
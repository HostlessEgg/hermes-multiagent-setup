#!/usr/bin/env python3
"""
primos_rapido.py - Test de primalidad determinista rapido para enteros hasta ~10^20.

Estrategia
==========
1. Manejo de casos limite triviales (n < 2 -> no primo; n en {2,3} -> primo).
2. Criba de divisores primos pequenos (2,3,5,...,47). Descarta rapidamente
   la gran mayoria de los compuestos y los numeros pares con coste minimo.
3. Miller-Rabin DETERMINISTA con las 13 primeras bases primas:
       {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}

Por que estas bases son deterministas en el rango objetivo
----------------------------------------------------------
Miller-Rabin es en general un test PROBABILISTICO: con bases aleatorias la
probabilidad de error es < 4^-k para k rondas. Sin embargo, se sabe que para
ciertos conjuntos FIJOS de bases pequenas el test es DEMOSTRATIVAMENTE
DETERMINISTA por debajo de una cota conocida.

El resultado clasico (Jaeschke 1993; verificado y refinado por Sorenson &
Webster 2015) establece que el conjunto de las 12 primeras bases primas
    {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}
es determinista para todo n < 3.317.044.064.679.887.385.961.981
(~3.317 x 10^24, aproximadamente 3.3 sextillones).

Ese limite es el "strong pseudoprime" mas pequeno que enganaria a todas esas
bases, y cubre con amplisimo margen cualquier numero de hasta 20 digitos
(maximo ~10^20). Anadimos ademas la base 41 (13 bases) por robustez extra y
porque es un conjunto de uso comun; el limite de determinismo con {2,...,41}
es aun mayor. En consecuencia, para n <= 10^20 el resultado del test es
EXACTO, no probabilistico.

Referencias:
  - Jaeschke, G. (1993). "On strong pseudoprimes to several bases",
    Mathematics of Computation 61(204), 915-926.
  - Sorenson, J. & Webster, J. (2015). "Strong pseudoprimes to twelve prime
    bases", Mathematics of Computation 84(293), 2245-2261.

Rendimiento
===========
Toda la aritmetica modular se delega en pow(a, d, n), la exponenciacion
modular nativa de Python, implementada en C con algoritmos eficientes.
Por eso el coste total es de unos pocos miles de multiplicaciones modulares
en C, lo que resuelve un numero de 20 digitos en milisegundos.

Uso
===
    python3 /tmp/primos_rapido.py <numero>
    /tmp/primos_rapido.py <numero>

Salida: "<n> es primo" o "<n> no es primo".
Codigos de salida: 0 si es primo, 1 si no lo es o si la entrada es invalida.
"""

import sys

# Bases primas para Miller-Rabin determinista (ver docstring del modulo).
BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)

# Limite de determinismo del conjunto de 12 bases primas
# {2,3,5,7,11,13,17,19,23,29,31,37}: todo n por debajo de este valor
# clasificado como primo por el test es realmente primo.
DETERMINISTIC_LIMIT = 3317044064679887385961981  # ~3.317 x 10^24

# Primos pequenos usados en la criba previa.
_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def is_prime(n: int) -> bool:
    """Devuelve True si n es primo, False en caso contrario.

    Determinista para todo n < 3317044064679887385961981 (~3.317e24), lo que
    incluye con margen todo el rango de 20 digitos. Acepta cualquier entero
    de Python; los valores negativos, 0 y 1 no son primos.

    Algoritmo: criba de divisores pequenos + Miller-Rabin con 13 bases primas.
    """
    # Casos limite triviales.
    if not isinstance(n, int):
        raise TypeError("is_prime requiere un entero")
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Criba de divisores primos pequenos: descarta compuestos de forma barata.
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p

    # Miller-Rabin determinista.
    # n es impar y n > 47 en este punto. Escribimos n - 1 = d * 2^r con d impar.
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for a in BASES:
        if a % n == 0:
            # La base es multiplo de n (solo posible para n primo pequeno,
            # ya cubierto arriba); no aporta informacion, se omite.
            continue
        x = pow(a, d, n)  # exponenciacion modular nativa, rapida (C)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            # Ningun testigo de Fermat fuerte se cumple: n es compuesto.
            return False
    return True


def _usage(prog: str) -> str:
    return (
        "Uso: {} <numero>\n"
        "Determina si <numero> (entero, hasta ~10^20) es primo.\n"
        "Ejemplo: {} 99999999999999999989".format(prog, prog)
    )


def main(argv) -> int:
    """Punto de entrada CLI. Devuelve el codigo de salida."""
    if len(argv) < 2:
        sys.stderr.write(_usage(argv[0] if argv else "primos_rapido.py") + "\n")
        return 1

    raw = argv[1]
    try:
        n = int(raw, 10)
    except (ValueError, TypeError):
        sys.stderr.write(
            "Error: '{}' no es una entrada numerica valida. "
            "Se esperaba un numero entero.\n".format(raw)
        )
        return 1

    print("{} {}".format(n, "es primo" if is_prime(n) else "no es primo"))
    return 0 if is_prime(n) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

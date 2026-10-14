"""
Módulo del núcleo formal matemático del Autómata Finito Determinista (AFD).
Define el alfabeto formal Sigma, los estados Q, la función delta(q, a) y los simuladores.
"""

from .validador import (
    LETRAS_VALIDAS,
    DIGITOS_VALIDOS,
    ESTADO_INICIAL,
    ESTADO_ACEPTACION,
    ESTADO_TRAMPA,
    clasificar_simbolo,
    delta,
    validar_placa
)

from .simulador import (
    AFDPlacas
)

__all__ = [
    "LETRAS_VALIDAS",
    "DIGITOS_VALIDOS",
    "ESTADO_INICIAL",
    "ESTADO_ACEPTACION",
    "ESTADO_TRAMPA",
    "clasificar_simbolo",
    "delta",
    "validar_placa",
    "AFDPlacas"
]

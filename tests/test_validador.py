"""
================================================================================
BATERÍA FORMAL DE PRUEBAS UNITARIAS (TEST SUITE)
Validador de Autómata Finito Determinista (AFD) - Placas Colombia (Temática 23)
================================================================================
Uso de la librería estándar 'unittest' para garantizar determinismo y cobertura.
"""

import os
import sys
import unittest

# Asegurar disponibilidad del paquete src en el path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.core.validador import (
    LETRAS_VALIDAS,
    DIGITOS_VALIDOS,
    ESTADO_INICIAL,
    ESTADO_ACEPTACION,
    ESTADO_TRAMPA,
    clasificar_simbolo,
    delta,
    validar_placa
)
from src.core.simulador import AFDPlacas


class TestAFDPlacas(unittest.TestCase):
    """Pruebas unitarias formales para la lógica matemática del AFD."""

    def setUp(self):
        self.afd = AFDPlacas()

    # --------------------------------------------------------------------------
    # 1. PRUEBAS DE PLACAS VÁLIDAS (PERTENECEN A L)
    # --------------------------------------------------------------------------
    def test_placas_validas_estandar(self):
        """Cadenas válidas con estructura canónica LLLDDD."""
        casos_validos = [
            "ABC123",  # Estándar
            "KLR890",  # Letras intermedias
            "ZZZ000",  # Casos límite: letras Z y ceros
            "AAA111",  # Casos límite: letras A y unos
            "XYZ999",  # Letras finales y dígitos máximos
            "MNO541",  # Combinación mixta aleatoria
            "QWE789",  # Letras teclado superior
            "PAS042",  # Ceros intermedios
        ]
        for placa in casos_validos:
            with self.subTest(placa=placa):
                # Validación funcional pura
                self.assertTrue(
                    validar_placa(placa, mostrar_traza=False),
                    f"La placa '{placa}' debió ser ACEPTADA por la función delta."
                )
                # Validación con objeto AFDPlacas
                res = self.afd.procesar_cadena(placa)
                self.assertTrue(
                    res["es_aceptada"],
                    f"La placa '{placa}' debió ser aceptada por AFDPlacas."
                )
                self.assertEqual(res["estado_final"], ESTADO_ACEPTACION)

    # --------------------------------------------------------------------------
    # 2. PRUEBAS DE LONGITUD INVÁLIDA (|w| != 6)
    # --------------------------------------------------------------------------
    def test_longitud_invalida(self):
        """Cadenas que no cumplen estrictamente |w| = 6."""
        casos_longitud = [
            "",          # Cadena vacía lambda (|w| = 0)
            "A",         # Longitud 1
            "AB",        # Longitud 2
            "ABC",       # Longitud 3 (solo letras)
            "ABC1",      # Longitud 4
            "ABC12",     # Longitud 5 (falta 1 dígito)
            "ABC1234",   # Longitud 7 (un dígito de más)
            "ABC12345",  # Longitud 8
            "ABCD123",   # Longitud 7 (una letra de más)
        ]
        for placa in casos_longitud:
            with self.subTest(placa=placa):
                self.assertFalse(
                    validar_placa(placa, mostrar_traza=False),
                    f"La cadena '{placa}' de longitud {len(placa)} debió ser RECHAZADA."
                )

    # --------------------------------------------------------------------------
    # 3. PRUEBAS DE CARACTERES FUERA DEL ALFABETO (c not in Sigma)
    # --------------------------------------------------------------------------
    def test_simbolos_fuera_del_alfabeto(self):
        """Cadenas con minúsculas, caracteres especiales, espacios o diacríticos."""
        casos_simbolos = [
            "abc123",    # Minúsculas
            "Abc123",    # Mayúscula y minúsculas mixtas
            "AB-123",    # Guión separador
            "ABC 123",   # Espacio en blanco
            "ABC.123",   # Punto
            "ABÑ123",    # Letra Ñ (excluida de Lambda reglamentario)
            "ÁBC123",    # Letra con tilde
            "ABC12#",    # Carácter especial hash
            "ABC12$",    # Signo de pesos
        ]
        for placa in casos_simbolos:
            with self.subTest(placa=placa):
                self.assertFalse(
                    validar_placa(placa, mostrar_traza=False),
                    f"La cadena '{placa}' con símbolos fuera de Sigma debió ser RECHAZADA."
                )

    # --------------------------------------------------------------------------
    # 4. PRUEBAS DE ESTRUCTURA SINTÁCTICA ALTERADA
    # --------------------------------------------------------------------------
    def test_sintaxis_desordenada(self):
        """Cadenas con símbolos válidos pero orden erróneo (no LLLDDD)."""
        casos_orden = [
            "123ABC",    # Dígitos antes de letras (DDDLLL)
            "AB1234",    # 2 letras y 4 dígitos (LLDDDD)
            "ABCD12",    # 4 letras y 2 dígitos (LLLLDD)
            "A1B2C3",    # Alternancia letra-dígito
            "1ABC23",    # Dígito inicial
            "ABC12D",    # Termina en letra en vez de dígito
            "123456",    # Solo dígitos (DDDDDD)
            "ABCDEF",    # Solo letras (LLLLLL)
        ]
        for placa in casos_orden:
            with self.subTest(placa=placa):
                self.assertFalse(
                    validar_placa(placa, mostrar_traza=False),
                    f"La cadena '{placa}' con orden incorrecto debió ser RECHAZADA."
                )

    # --------------------------------------------------------------------------
    # 5. VERIFICACIÓN DE PROPIEDADES MATEMÁTICAS FORMALES DEL AFD
    # --------------------------------------------------------------------------
    def test_propiedad_estado_trampa_absorbente(self):
        """delta(qE, a) = qE para cualquier símbolo del alfabeto o externo."""
        for simbolo in list(LETRAS_VALIDAS[:5]) + list(DIGITOS_VALIDOS[:5]) + ["-", "*", "z"]:
            siguiente = delta(ESTADO_TRAMPA, simbolo)
            self.assertEqual(
                siguiente, ESTADO_TRAMPA,
                f"El estado trampa qE debe ser absorbente frente al símbolo '{simbolo}'."
            )

    def test_clasificacion_exhaustiva_de_simbolos(self):
        """Verifica la correcta partición del universo de caracteres."""
        for c in LETRAS_VALIDAS:
            self.assertEqual(clasificar_simbolo(c), "letra")
        for d in DIGITOS_VALIDOS:
            self.assertEqual(clasificar_simbolo(d), "digito")
        for especial in ["a", "z", "ñ", "Ñ", " ", "-", "_", "!", "9" + "1"]:
            if len(especial) == 1:
                self.assertEqual(clasificar_simbolo(especial), "otro")


if __name__ == "__main__":
    unittest.main(verbosity=2)

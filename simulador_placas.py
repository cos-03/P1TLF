"""
================================================================================
UNIVERSIDAD - FACULTAD DE INGENIERÍA
PROGRAMA DE INGENIERÍA DE SISTEMAS Y COMPUTACIÓN
TEORÍA DE LENGUAJES FORMALES - PARCIAL 1

SIMULADOR FORMAL DE AUTÓMATA FINITO DETERMINISTA (AFD)
Temática 23: Reconocedor de Matrículas / Placas Vehiculares (Normativa Colombia)

Integrantes:
- Nikoll Morales Londoño
- Felipe Valencia Londoño

RESTRICCIÓN FORMAL:
Queda estrictamente prohibido el uso de la librería 're' (expresiones regulares)
o parsers genéricos en la lógica del autómata. La validación se realiza 
exclusivamente mediante la simulación pura de la función de transición delta(q, a).
================================================================================
"""

import sys

# Configuración de codificación para compatibilidad universal con consolas Windows (evitar errores cp1252)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, Exception):
        pass

# ==============================================================================
# DEFINICIONES FORMALES DEL MODELO MATEMÁTICO
# M = (Q, Sigma, delta, q0, F)
# ==============================================================================

# Conjuntos base del alfabeto
LETRAS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Conjunto Lambda (|Lambda| = 26)
DIGITOS = set("0123456789")                  # Conjunto Delta (|Delta| = 10)
ALFABETO = LETRAS.union(DIGITOS)             # Alfabeto Sigma = Lambda U Delta (|Sigma| = 36)

# Conjunto de estados Q = {q0, q1, q2, q3, q4, q5, q6, qE}
ESTADO_INICIAL = "q0"
ESTADOS_ACEPTACION = {"q6"}
ESTADO_TRAMPA = "qE"

# Descripciones semánticas de cada estado para trazabilidad didáctica
DESCRIPCION_ESTADOS = {
    "q0": "Inicio: Esperando primera letra (L1)",
    "q1": "Leyó 1 letra válida: Esperando segunda letra (L2)",
    "q2": "Leyó 2 letras válidas: Esperando tercera letra (L3)",
    "q3": "Leyó 3 letras válidas: Esperando primer dígito (D1)",
    "q4": "Leyó 3 letras y 1 dígito: Esperando segundo dígito (D2)",
    "q5": "Leyó 3 letras y 2 dígitos: Esperando tercer dígito (D3)",
    "q6": "Estado de Aceptación: Placa completa (3 letras + 3 dígitos)",
    "qE": "Estado Trampa / Error: Desvío irreversible de la sintaxis"
}


class AFDPlacas:
    """
    Implementación formal del Autómata Finito Determinista para validación
    de placas colombianas de formato LLLDDD (3 letras y 3 dígitos).
    """

    def __init__(self):
        self.q0 = ESTADO_INICIAL
        self.F = ESTADOS_ACEPTACION
        self.qE = ESTADO_TRAMPA
        self.sigma = ALFABETO

    def clasificar_simbolo(self, simbolo: str) -> str:
        """
        Determina la pertenencia del símbolo al alfabeto y su clase formal:
        'L' si pertenece a Lambda (letras A-Z), 
        'D' si pertenece a Delta (dígitos 0-9), 
        'OTHER' si no pertenece a Sigma.
        """
        if simbolo in LETRAS:
            return "L"
        elif simbolo in DIGITOS:
            return "D"
        else:
            return "OTHER"

    def delta(self, estado_actual: str, simbolo: str) -> str:
        """
        Función de transición formal delta: Q x Sigma -> Q
        
        Implementa rigurosamente la tabla de transiciones:
        - Si el símbolo no pertenece a Sigma, transita directamente a qE.
        - Desde qE, cualquier entrada permanece en qE (estado trampa absorbente).
        - En cualquier estado, símbolos fuera del orden esperado llevan a qE.
        """
        tipo = self.clasificar_simbolo(simbolo)
        
        # Cualquier carácter fuera del alfabeto formal Sigma lleva inmediatamente a la trampa
        if tipo == "OTHER":
            return self.qE

        # Transiciones deterministas según el estado actual y el tipo de símbolo
        if estado_actual == "q0":
            return "q1" if tipo == "L" else self.qE

        elif estado_actual == "q1":
            return "q2" if tipo == "L" else self.qE

        elif estado_actual == "q2":
            return "q3" if tipo == "L" else self.qE

        elif estado_actual == "q3":
            return "q4" if tipo == "D" else self.qE

        elif estado_actual == "q4":
            return "q5" if tipo == "D" else self.qE

        elif estado_actual == "q5":
            return "q6" if tipo == "D" else self.qE

        elif estado_actual == "q6":
            # Si ya se alcanzó la aceptación y llegan caracteres adicionales (|w| > 6), pasa a qE
            return self.qE

        elif estado_actual == self.qE:
            # Estado trampa absorbente: delta(qE, a) = qE para todo símbolo
            return self.qE

        return self.qE

    def procesar_cadena(self, cadena: str) -> dict:
        """
        Procesa una cadena símbolo por símbolo simulando el recorrido del AFD.
        
        Retorna un diccionario estructurado con:
        - cadena: Cadena procesada
        - estados_recorridos: Lista ordenada de estados recorridos
        - traza: Registro paso a paso (paso, símbolo, origen, destino, motivo)
        - estado_final: Estado en el que finalizó el autómata
        - es_aceptada: Booleano que indica si estado_final in F
        - diagnostico: Explicación lingüística del resultado
        """
        estado_actual = self.q0
        traza = []
        estados_recorridos = [estado_actual]

        for i, simbolo in enumerate(cadena, start=1):
            clase = self.clasificar_simbolo(simbolo)
            estado_siguiente = self.delta(estado_actual, simbolo)
            
            # Construir diagnóstico didáctico del paso
            if clase == "OTHER":
                motivo = f"Símbolo '{simbolo}' NO pertenece al alfabeto Sigma"
            elif estado_siguiente == self.qE and estado_actual != self.qE:
                if estado_actual in {"q0", "q1", "q2"}:
                    motivo = f"Se esperaba Letra (L), pero llegó Dígito '{simbolo}'"
                elif estado_actual in {"q3", "q4", "q5"}:
                    motivo = f"Se esperaba Dígito (D), pero llegó Letra '{simbolo}'"
                elif estado_actual == "q6":
                    motivo = f"Longitud excede 6 símbolos. Carácter extra '{simbolo}'"
                else:
                    motivo = "Transición inválida hacia estado trampa"
            elif estado_actual == self.qE:
                motivo = f"Permanece en trampa qE con '{simbolo}'"
            else:
                motivo = f"Transición válida: {DESCRIPCION_ESTADOS.get(estado_siguiente, '')}"

            traza.append({
                "paso": i,
                "simbolo": simbolo,
                "clase": clase,
                "origen": estado_actual,
                "destino": estado_siguiente,
                "motivo": motivo
            })

            estado_actual = estado_siguiente
            estados_recorridos.append(estado_actual)

        es_aceptada = (estado_actual in self.F)

        # Generar diagnóstico global
        if es_aceptada:
            diagnostico = "La cadena cumple la estructura LLLDDD (|w| = 6) y culminó en estado de aceptación q6."
        else:
            if len(cadena) == 0:
                diagnostico = "Cadena vacía (lambda): Longitud 0. El autómata permanece en q0 (q0 no es de aceptación)."
            elif estado_actual == self.qE:
                diagnostico = f"Cadena RECHAZADA: Cayó en el estado trampa ({self.qE}) por error de sintaxis o carácter ajeno a Sigma."
            elif estado_actual in {"q0", "q1", "q2", "q3", "q4", "q5"}:
                diagnostico = f"Cadena RECHAZADA: Incompleta (|w| = {len(cadena)} < 6). Se detuvo en {estado_actual} sin llegar a q6."
            else:
                diagnostico = f"Cadena RECHAZADA: Culminó en {estado_actual} fuera de F."

        return {
            "cadena": cadena,
            "estados_recorridos": estados_recorridos,
            "traza": traza,
            "estado_final": estado_actual,
            "es_aceptada": es_aceptada,
            "diagnostico": diagnostico
        }


# ==============================================================================
# BATERÍA DE PRUEBAS AUTOMATIZADA
# ==============================================================================

CASOS_DE_PRUEBA = [
    # --- Casos Exitosos (Esperado: ACEPTADA) ---
    {
        "cadena": "ABC123",
        "esperado": True,
        "descripcion": "Estructura estándar correcta (3 letras y 3 dígitos)"
    },
    {
        "cadena": "KLR890",
        "esperado": True,
        "descripcion": "Combinación válida arbitraria en rango intermedio"
    },
    {
        "cadena": "ZZZ000",
        "esperado": True,
        "descripcion": "Límite superior alfabético (ZZZ) y dígitos en cero (000)"
    },
    {
        "cadena": "XYZ999",
        "esperado": True,
        "descripcion": "Límite superior de dígitos numéricos (999)"
    },
    {
        "cadena": "MNO541",
        "esperado": True,
        "descripcion": "Transición adecuada en la frontera letra-dígito (q3 -> q4)"
    },
    {
        "cadena": "AAA111",
        "esperado": True,
        "descripcion": "Secuencia uniforme repetitiva válida"
    },

    # --- Casos con Fallas Esperadas (Esperado: RECHAZADA) ---
    {
        "cadena": "abc123",
        "esperado": False,
        "descripcion": "Letras minúsculas (no pertenecen al alfabeto Sigma)"
    },
    {
        "cadena": "AB1234",
        "esperado": False,
        "descripcion": "Falta una letra y sobra un dígito (2 letras + 4 dígitos)"
    },
    {
        "cadena": "ABC1234",
        "esperado": False,
        "descripcion": "Longitud 7: Excede los 6 caracteres requeridos"
    },
    {
        "cadena": "ABC12",
        "esperado": False,
        "descripcion": "Longitud 5: Cadena incompleta, falta el sexto símbolo"
    },
    {
        "cadena": "123ABC",
        "esperado": False,
        "descripcion": "Orden invertido: Dígitos antes que letras"
    },
    {
        "cadena": "AB-123",
        "esperado": False,
        "descripcion": "Contiene un carácter separador '-' ajeno al alfabeto"
    },
    {
        "cadena": "ABC12D",
        "esperado": False,
        "descripcion": "La posición 6 es una letra en lugar de un dígito"
    },
    {
        "cadena": "",
        "esperado": False,
        "descripcion": "Cadena vacía (lambda): longitud 0"
    },
    {
        "cadena": "AÑC123",
        "esperado": False,
        "descripcion": "Contiene la letra 'Ñ' (fuera de Sigma según normativa)"
    }
]


# ==============================================================================
# INTERFAZ DE USUARIO (CLI)
# ==============================================================================

def imprimir_separador(char="=", ancho=80):
    print(char * ancho)


def imprimir_traza(resultado: dict):
    """Muestra de forma formateada la traza paso a paso del autómata."""
    cadena = resultado["cadena"]
    print(f"\nCadena analizada: \"{cadena}\"  (Longitud: {len(cadena)})")
    imprimir_separador("-", 80)
    
    if len(cadena) == 0:
        print("  [Cadena vacía lambda] No hay símbolos que procesar.")
    else:
        print(f"{'Paso':<6}{'Símb.':<8}{'Clase':<8}{'Origen':<10}{'Destino':<10}{'Detalle':<38}")
        print("-" * 80)
        for paso in resultado["traza"]:
            detalle_truncado = paso['motivo'][:37]
            print(f"{paso['paso']:<6}{paso['simbolo']:<8}{paso['clase']:<8}"
                  f"{paso['origen']:<10}{paso['destino']:<10}{detalle_truncado:<38}")

    imprimir_separador("-", 80)
    print(f"Ruta de estados: {' -> '.join(resultado['estados_recorridos'])}")
    print(f"Estado final alcanzado: {resultado['estado_final']}")
    
    if resultado["es_aceptada"]:
        print("\n>>> RESULTADO FINAL: [ ACEPTADA ] <<<")
    else:
        print("\n>>> RESULTADO FINAL: [ RECHAZADA ] <<<")
    print(f"Diagnóstico: {resultado['diagnostico']}\n")


def ejecutar_bateria_pruebas():
    """Ejecuta la suite automatizada de pruebas y reporta los resultados."""
    afd = AFDPlacas()
    imprimir_separador("=")
    print("         EJECUCIÓN DE LA BATERÍA DE PRUEBAS FORMALES (AFD PLACAS)        ")
    imprimir_separador("=")
    
    exitos = 0
    total = len(CASOS_DE_PRUEBA)

    for i, test in enumerate(CASOS_DE_PRUEBA, start=1):
        cadena = test["cadena"]
        esperado = test["esperado"]
        desc = test["descripcion"]
        
        resultado = afd.procesar_cadena(cadena)
        obtenido = resultado["es_aceptada"]
        coincide = (obtenido == esperado)

        if coincide:
            exitos += 1
            veredicto = "OK (Superada)"
        else:
            veredicto = "FALLA"

        tipo_esperado = "ACEPTADA" if esperado else "RECHAZADA"
        tipo_obtenido = "ACEPTADA" if obtenido else "RECHAZADA"

        print(f"Prueba #{i:02d}: \"{cadena}\"")
        print(f"  Propósito:  {desc}")
        print(f"  Esperado:   [{tipo_esperado}] | Obtenido: [{tipo_obtenido}] -> {veredicto}")
        print(f"  Ruta:       {' -> '.join(resultado['estados_recorridos'])}")
        print("-" * 80)

    imprimir_separador("=")
    print(f"Resumen de Pruebas: {exitos}/{total} pruebas superadas exitosamente ({(exitos/total)*100:.1f}%).")
    imprimir_separador("=")


def modo_interactivo():
    """Permite al usuario ingresar cadenas arbitrarias en tiempo real."""
    afd = AFDPlacas()
    imprimir_separador("=")
    print("    MODO INTERACTIVO - RECONOCEDOR DE PLACAS VEHICULARES COLOMBIANAS   ")
    print("             Autómata Finito Determinista (8 estados)                  ")
    imprimir_separador("=")
    print("Ingrese cualquier placa o texto para verificar su validez sintáctica.")
    print("Escriba 'salir' o 'exit' para volver al menú principal.\n")

    while True:
        try:
            entrada = input("Ingrese placa a validar > ").strip()
            if entrada.lower() in {"salir", "exit"}:
                break
            
            resultado = afd.procesar_cadena(entrada)
            imprimir_traza(resultado)
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            break


def mostrar_especificacion_formal():
    imprimir_separador("=")
    print("                  ESPECIFICACIÓN FORMAL DEL AFD M = (Q, Sigma, delta, q0, F)   ")
    imprimir_separador("=")
    print("• Alfabeto (Sigma): Sigma = Lambda U Delta (|Sigma| = 36)")
    print("  - Lambda = {A, B, C, ..., Z} (|Lambda| = 26 letras mayúsculas)")
    print("  - Delta  = {0, 1, 2, ..., 9} (|Delta|  = 10 dígitos)")
    print("• Conjunto de Estados (Q): {q0, q1, q2, q3, q4, q5, q6, qE} (|Q| = 8)")
    print("• Estado Inicial (q0): q0")
    print("• Estados de Aceptación (F): {q6}")
    print("• Estado Trampa (qE): qE (absorbente, cualquier símbolo adicional o no esperado permanece en qE)")
    print("\n• Tabla de Transición Resumida delta:")
    print("  +--------+-----------+-----------+----------------+")
    print("  | Estado | delta(q,L)| delta(q,D)|delta(q,c !in S)|")
    print("  +--------+-----------+-----------+----------------+")
    print("  | -> q0  |     q1    |     qE    |       qE       |")
    print("  |    q1  |     q2    |     qE    |       qE       |")
    print("  |    q2  |     q3    |     qE    |       qE       |")
    print("  |    q3  |     qE    |     q4    |       qE       |")
    print("  |    q4  |     qE    |     q5    |       qE       |")
    print("  |    q5  |     qE    |     q6    |       qE       |")
    print("  |  * q6  |     qE    |     qE    |       qE       |")
    print("  |    qE  |     qE    |     qE    |       qE       |")
    print("  +--------+-----------+-----------+----------------+")
    print("\n• Expresión Regular Equivalente: ER = L L L D D D (ó L^3 D^3)")
    print("• Número exacto de palabras en L: 26^3 * 10^3 = 17,576,000 palabras de longitud 6.\n")


def main():
    while True:
        imprimir_separador("=")
        print(" SISTEMA SIMULADOR DE TEORÍA DE LENGUAJES - PARCIAL 1")
        print(" Temática 23: Validador de Placas Vehiculares (Colombia)")
        print(" Integrantes: Nikoll Morales Londoño y Felipe Valencia Londoño")
        imprimir_separador("=")
        print(" 1. Ingresar una placa y ver la traza paso a paso (Modo Interactivo)")
        print(" 2. Ejecutar la Batería de Pruebas Automatizada (15 casos)")
        print(" 3. Ver especificación formal del Autómata (Tupla M, Estados, Alfabeto)")
        print(" 4. Salir")
        imprimir_separador("-")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            modo_interactivo()
        elif opcion == "2":
            ejecutar_bateria_pruebas()
        elif opcion == "3":
            mostrar_especificacion_formal()
        elif opcion == "4":
            print("\nFinalizando el simulador. ¡Éxitos en la sustentación!\n")
            break
        else:
            print("\nOpción no válida. Por favor ingrese un número del 1 al 4.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"--test", "-t"}:
        ejecutar_bateria_pruebas()
    else:
        main()

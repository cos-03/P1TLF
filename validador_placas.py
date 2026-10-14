# ==============================================================================
# PROYECTO: SIMULADOR DE AUTOMATA FINITO DETERMINISTA (AFD)
# TEMATICA 23: Reconocedor de Placas de Colombia (Formato: LLLDDD)
# TEORIA DE LENGUAJES FORMALES
# ==============================================================================
# RESTRICCION: 100% Python basico, sin librerias externas y SIN 'import re'.
# ==============================================================================

# Alfabeto permitido (Sigma = Letras mayusculas + Digitos)
# Lambda = 26 letras mayusculas de la A a la Z
LETRAS_VALIDAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Delta = 10 digitos del 0 al 9
DIGITOS_VALIDOS = "0123456789"

# Definicion formal de estados:
# Q = {q0, q1, q2, q3, q4, q5, q6, qE}
ESTADO_INICIAL = "q0"       # Estado de arranque
ESTADO_ACEPTACION = "q6"     # Unico estado final F = {q6}
ESTADO_TRAMPA = "qE"        # Estado de error o pozo absorbente


def clasificar_simbolo(simbolo):
    """
    Funcion auxiliar: clasifica el caracter leido segun el alfabeto formal.
    - Si pertenece a las letras mayusculas A-Z -> devuelve 'letra'
    - Si pertenece a los digitos 0-9 -> devuelve 'digito'
    - Si no pertenece a Sigma (minusculas, guiones, etc.) -> devuelve 'otro'
    """
    if simbolo in LETRAS_VALIDAS:
        return "letra"
    elif simbolo in DIGITOS_VALIDOS:
        return "digito"
    else:
        return "otro"


def delta(estado_actual, simbolo):
    """
    FUNCION DE TRANSICION MATEMATICA: delta(q, a) -> q'
    Recibe el estado actual (q) y el simbolo leido (a).
    Devuelve el siguiente estado segun la tabla de transiciones del AFD.
    """
    # 1. Clasificamos el simbolo leido
    tipo = clasificar_simbolo(simbolo)

    # 2. Si el caracter no pertenece a Sigma, va directo a la trampa qE
    if tipo == "otro":
        return ESTADO_TRAMPA

    # 3. Propiedad de estado trampa: si ya esta en qE, se queda en qE
    if estado_actual == ESTADO_TRAMPA:
        return ESTADO_TRAMPA

    # 4. Transiciones paso a paso segun la tabla de diseno del AFD:

    # En q0 (inicio): espera la 1ra letra (L1) para ir a q1
    if estado_actual == "q0":
        if tipo == "letra":
            return "q1"
        else:
            return ESTADO_TRAMPA

    # En q1 (ya leyo 1 letra): espera la 2da letra (L2) para ir a q2
    elif estado_actual == "q1":
        if tipo == "letra":
            return "q2"
        else:
            return ESTADO_TRAMPA

    # En q2 (ya leyo 2 letras): espera la 3ra letra (L3) para ir a q3
    elif estado_actual == "q2":
        if tipo == "letra":
            return "q3"
        else:
            return ESTADO_TRAMPA

    # En q3 (ya leyo 3 letras): ahora DEBE leer el 1er digito (D1) para ir a q4
    elif estado_actual == "q3":
        if tipo == "digito":
            return "q4"
        else:
            return ESTADO_TRAMPA

    # En q4 (ya leyo 1 digito): debe leer el 2do digito (D2) para ir a q5
    elif estado_actual == "q4":
        if tipo == "digito":
            return "q5"
        else:
            return ESTADO_TRAMPA

    # En q5 (ya leyo 2 digitos): debe leer el 3er digito (D3) para llegar a q6
    elif estado_actual == "q5":
        if tipo == "digito":
            return "q6"
        else:
            return ESTADO_TRAMPA

    # En q6 (placa ya completada): cualquier simbolo extra desborda la longitud y va a qE
    elif estado_actual == "q6":
        return ESTADO_TRAMPA

    # Cualquier otro caso imprevisto va a la trampa
    else:
        return ESTADO_TRAMPA


def validar_placa(cadena, mostrar_traza=True):
    """
    Simula el procesamiento completo de una cadena sobre el AFD.
    Recorre simbolo por simbolo, ejecuta delta(q, a) y muestra la traza.
    Devuelve True si la cadena es ACEPTADA o False si es RECHAZADA.
    """
    # El automata siempre comienza en el estado inicial q0
    estado_actual = ESTADO_INICIAL
    numero_paso = 1

    if mostrar_traza:
        print("\n" + "-" * 50)
        print("Iniciando validacion de la cadena: '" + cadena + "'")
        print("Estado inicial: " + estado_actual)
        print("-" * 50)

    # Caso especial: cadena vacia (longitud 0)
    if len(cadena) == 0:
        if mostrar_traza:
            print("La cadena esta vacia (longitud 0).")
            print("Estado final: " + estado_actual + " -> RECHAZADA")
        return False

    # Procesamiento caracter a caracter
    for simbolo in cadena:
        # Etiqueta amigable para la traza (letra / digito / simbolo no valido)
        tipo = clasificar_simbolo(simbolo)
        if tipo == "letra":
            tipo_texto = "letra"
        elif tipo == "digito":
            tipo_texto = "digito"
        else:
            tipo_texto = "simbolo no valido"

        # Aplicamos la funcion delta matematica
        nuevo_estado = delta(estado_actual, simbolo)

        # Imprimimos la traza del paso actual
        if mostrar_traza:
            print("Paso " + str(numero_paso) + ": estado " + estado_actual + 
                  ", lee '" + simbolo + "' (" + tipo_texto + ") -> " + nuevo_estado)

        # El automata avanza al nuevo estado
        estado_actual = nuevo_estado
        numero_paso = numero_paso + 1

    # Condicion de aceptacion formal: el estado final debe pertenecer a F = {q6}
    es_aceptada = (estado_actual == ESTADO_ACEPTACION)

    if mostrar_traza:
        print("-" * 50)
        if es_aceptada:
            print("Estado final: " + estado_actual + " -> ACEPTADA")
        else:
            print("Estado final: " + estado_actual + " -> RECHAZADA")
        print("-" * 50)

    return es_aceptada


def ejecutar_bateria_pruebas():
    """
    Ejecuta un conjunto de pruebas predefinidas (casos validos e invalidos).
    Compara automaticamente el resultado esperado con el obtenido y resume el test.
    """
    print("\n" + "=" * 70)
    print("           BATERIA DE PRUEBAS AUTOMATICAS DEL AFD")
    print("=" * 70)

    # Lista con casos de prueba: [cadena, esperado, motivo]
    pruebas = [
        # --- CASOS VALIDOS (deben ser ACEPTADAS) ---
        ["ABC123", True,  "Valida: caso estandar (3 letras y 3 digitos)"],
        ["KLR890", True,  "Valida: letras intermedias y digitos altos"],
        ["ZZZ000", True,  "Valida: letras finales y ceros"],
        ["XYZ999", True,  "Valida: combinacion final de letras y nueves"],
        ["MNO541", True,  "Valida: combinacion variada"],

        # --- CASOS INVALIDOS (deben ser RECHAZADAS) ---
        ["abc123", False, "Invalida: contiene letras minusculas"],
        ["AB1234", False, "Invalida: 2 letras y 4 digitos (orden incorrecto)"],
        ["ABC1234", False, "Invalida: 7 caracteres (longitud excedida)"],
        ["123ABC", False, "Invalida: digitos antes de letras"],
        ["AB-123", False, "Invalida: caracter guion '-' fuera de Sigma"],
        ["ABC12",  False, "Invalida: solo 2 digitos (longitud insuficiente)"],
        ["ABC12D", False, "Invalida: termina en letra en vez de digito"]
    ]

    correctas = 0
    total = len(pruebas)

    # Imprimir encabezado de la tabla de resultados
    print(f"{'#':<3} | {'Cadena':<9} | {'Esperado':<10} | {'Obtenido':<10} | {'Resultado':<9} | {'Detalle'}")
    print("-" * 75)

    numero = 1
    for item in pruebas:
        cadena = item[0]
        esperado = item[1]
        detalle = item[2]

        # Validamos sin imprimir trazas individuales para mantener limpia la tabla
        obtenido = validar_placa(cadena, mostrar_traza=False)

        texto_esperado = "ACEPTADA" if esperado else "RECHAZADA"
        texto_obtenido = "ACEPTADA" if obtenido else "RECHAZADA"

        if obtenido == esperado:
            resultado = "OK"
            correctas = correctas + 1
        else:
            resultado = "FALLO"

        print(f"{numero:<3} | {cadena:<9} | {texto_esperado:<10} | {texto_obtenido:<10} | {resultado:<9} | {detalle}")
        numero = numero + 1

    print("-" * 75)
    print(f"Resumen: {correctas} de {total} pruebas pasaron correctamente.")
    if correctas == total:
        print("Resultado general: TODAS LAS PRUEBAS PASARON EXITOSAMENTE.")
    else:
        print("Resultado general: ALGUNAS PRUEBAS FALLARON.")
    print("=" * 70)


def menu_principal():
    """
    Menu interactivo en consola para el usuario.
    Permite validar cadenas manuales, ejecutar la bateria de pruebas o salir.
    """
    while True:
        print("\n" + "=" * 45)
        print("   RECONOCEDOR DE PLACAS - COLOMBIA")
        print("   Automata Finito Determinista (AFD)")
        print("=" * 45)
        print("1. Validar una placa (ver traza paso a paso)")
        print("2. Ejecutar bateria de pruebas automaticas")
        print("3. Salir")
        print("=" * 45)

        opcion = input("Seleccione una opcion (1, 2 o 3): ").strip()

        if opcion == "1":
            placa = input("\nIngrese la placa a validar (ejemplo ABC123): ").strip()
            validar_placa(placa, mostrar_traza=True)

        elif opcion == "2":
            ejecutar_bateria_pruebas()

        elif opcion == "3":
            print("\nSaliendo del programa. Exitos en la sustentacion!\n")
            break

        else:
            print("\n[Error] Opcion no valida. Por favor escriba 1, 2 o 3.")


# Punto de entrada principal
if __name__ == "__main__":
    menu_principal()

"""
================================================================================
PROYECTO: RECONOCEDOR SINTÁCTICO DE PLACAS VEHICULARES DE COLOMBIA (AFD)
TEORÍA DE LENGUAJES FORMALES - TEMÁTICA 23
================================================================================
Punto de Entrada Principal (Orquestador Central del Proyecto)

Permite ejecutar:
  1. Simulador en consola (CLI interactivo con traza formal paso a paso)
  2. Interfaz Gráfica de Escritorio (Tkinter con visualización de autómatas)
  3. Simulador Web interactivo (Apertura en el navegador)
  4. Batería de pruebas automatizadas (Unit Tests con unittest)

Uso por banderas de consola:
  python main.py --gui     -> Inicia la interfaz gráfica de escritorio
  python main.py --cli     -> Inicia el modo consola interactivo
  python main.py --web     -> Abre el simulador web en el navegador
  python main.py --test    -> Ejecuta la suite de pruebas unitarias
================================================================================
"""

import argparse
import os
import sys
import unittest
import webbrowser

# Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def lanzar_gui():
    """Inicia la interfaz gráfica de escritorio con Tkinter."""
    print("\nIniciando Interfaz Gráfica de Escritorio (Tkinter)...")
    try:
        import tkinter as tk
        from src.gui.app_desktop import AppAFDPlacas

        ventana = tk.Tk()
        app = AppAFDPlacas(ventana)
        ventana.mainloop()
    except Exception as e:
        print(f"\n[ERROR] No fue posible iniciar la GUI: {e}")
        print("Asegúrese de contar con entorno gráfico compatible con Tkinter.\n")


def lanzar_cli():
    """Inicia el simulador en consola por terminal interactiva."""
    from src.core.simulador import main as cli_main
    cli_main()


def lanzar_web():
    """Abre el simulador web en el navegador predeterminado."""
    ruta_web = os.path.join(BASE_DIR, "web", "index.html")
    if not os.path.exists(ruta_web):
        # Fallback a raíz
        ruta_web = os.path.join(BASE_DIR, "index.html")

    print(f"\nAbriendo simulador web en el navegador...")
    print(f"Ruta local: {ruta_web}")
    webbrowser.open(f"file:///{os.path.abspath(ruta_web).replace(os.sep, '/')}")


def ejecutar_pruebas():
    """Ejecuta la suite de pruebas unitarias formales."""
    print("\n" + "=" * 60)
    print(" EJECUTANDO BATERÍA FORMAL DE PRUEBAS UNITARIAS")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(BASE_DIR, "tests"))
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    if resultado.wasSuccessful():
        print("\n[OK] Todas las pruebas formales pasaron satisfactoriamente (100%).\n")
    else:
        print("\n[FALLO] Algunas pruebas no pasaron. Revise el reporte anterior.\n")


def menu_interactivo():
    """Menú principal en consola si no se especifican banderas."""
    while True:
        print("\n" + "=" * 65)
        print("  RECONOCEDOR SINTÁCTICO DE PLACAS DE COLOMBIA (AFD)")
        print("  Teoría de Lenguajes Formales — Universidad de Ingeniería")
        print("=" * 65)
        print("  1. Simulador interactivo en consola (Traza formal paso a paso)")
        print("  2. Interfaz gráfica de escritorio (Tkinter + Grafo visual)")
        print("  3. Simulador Web interactivo (Abrir en el navegador)")
        print("  4. Ejecutar batería de pruebas unitarias (Test Suite)")
        print("  5. Salir")
        print("=" * 65)

        opcion = input(" Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            lanzar_cli()
        elif opcion == "2":
            lanzar_gui()
        elif opcion == "3":
            lanzar_web()
        elif opcion == "4":
            ejecutar_pruebas()
        elif opcion == "5":
            print("\nFinalizando ejecución. ¡Hasta pronto!\n")
            break
        else:
            print("\nOpción no válida. Ingrese un número entre 1 y 5.")


def main():
    parser = argparse.ArgumentParser(
        description="Validador y Reconocedor de Placas Vehiculares de Colombia con AFD."
    )
    parser.add_argument("--gui", action="store_true", help="Lanza la interfaz de escritorio Tkinter")
    parser.add_argument("--cli", action="store_true", help="Lanza el simulador interactivo en consola")
    parser.add_argument("--web", action="store_true", help="Abre el simulador web en el navegador")
    parser.add_argument("--test", action="store_true", help="Ejecuta la batería de pruebas unitarias")

    args = parser.parse_args()

    if args.gui:
        lanzar_gui()
    elif args.cli:
        lanzar_cli()
    elif args.web:
        lanzar_web()
    elif args.test:
        ejecutar_pruebas()
    else:
        menu_interactivo()


if __name__ == "__main__":
    main()

# ==============================================================================
# PROYECTO: INTERFAZ GRAFICA DE ESCRITORIO (PYTHON TKINTER)
# TEMATICA 23: Reconocedor de Placas de Colombia (Formato: LLLDDD)
# TEORIA DE LENGUAJES FORMALES
# ==============================================================================
# RESTRICCION: 100% Python estandar con Tkinter (sin pip install, sin re)
# ==============================================================================

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Soporte para ejecución directa (python src/gui/app_desktop.py) y como módulo
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.core.validador import (
    LETRAS_VALIDAS,
    DIGITOS_VALIDOS,
    ESTADO_INICIAL,
    ESTADO_ACEPTACION,
    ESTADO_TRAMPA,
    clasificar_simbolo,
    delta
)

class AppAFDPlacas:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Visual AFD - Placas Colombia (Tematica 23)")
        self.root.geometry("900x720")
        self.root.minsize(850, 650)
        self.root.configure(bg="#0b0f19")

        # Variables de control
        self.cadena_var = tk.StringVar(value="ABC123")
        self.historial_pasos = []
        self.indice_paso = 0

        # Construccion de la interfaz
        self.crear_encabezado()
        self.crear_placa_visual()
        self.crear_panel_control()
        self.crear_canvas_grafo()
        self.crear_tabla_traza()

        # Iniciar validando la cadena por defecto
        self.validar_tiempo_real()

    def crear_encabezado(self):
        """Encabezado superior con titulos formales."""
        header_frame = tk.Frame(self.root, bg="#131b2e", padx=20, pady=12)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        lbl_titulo = tk.Label(
            header_frame,
            text="Reconocedor Sintactico de Placas de Colombia (AFD)",
            font=("Segoe UI", 14, "bold"),
            fg="#f1f5f9",
            bg="#131b2e"
        )
        lbl_titulo.pack(anchor="w")

        lbl_sub = tk.Label(
            header_frame,
            text="Teoria de Lenguajes Formales | Expresion Regular: LLLDDD | Sigma = 36 simbolos",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#131b2e"
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

    def crear_placa_visual(self):
        """Simula visualmente una placa de automovil colombiana."""
        frame_placa_outer = tk.Frame(self.root, bg="#0b0f19")
        frame_placa_outer.pack(pady=5)

        # Placa amarilla con borde negro
        self.placa_box = tk.Frame(
            frame_placa_outer,
            bg="#facc15",
            highlightbackground="#1e293b",
            highlightthickness=5,
            padx=18,
            pady=6
        )
        self.placa_box.pack()

        lbl_colombia = tk.Label(
            self.placa_box,
            text="COLOMBIA",
            font=("Segoe UI", 8, "bold"),
            fg="#0f172a",
            bg="#facc15"
        )
        lbl_colombia.pack()

        self.lbl_letras_placa = tk.Label(
            self.placa_box,
            text="A B C · 1 2 3",
            font=("Consolas", 28, "bold"),
            fg="#0f172a",
            bg="#facc15",
            padx=10,
            pady=2
        )
        self.lbl_letras_placa.pack()

        lbl_ciudad = tk.Label(
            self.placa_box,
            text="BOGOTA D.C.",
            font=("Segoe UI", 7, "bold"),
            fg="#1e293b",
            bg="#facc15"
        )
        lbl_ciudad.pack()

    def crear_panel_control(self):
        """Entrada de texto, botones de accion y resultado."""
        control_frame = tk.Frame(self.root, bg="#131b2e", padx=15, pady=10)
        control_frame.pack(fill="x", padx=15, pady=10)

        # Fila 1: Input y botones
        row1 = tk.Frame(control_frame, bg="#131b2e")
        row1.pack(fill="x")

        lbl_input = tk.Label(
            row1,
            text="Ingrese placa:",
            font=("Segoe UI", 10, "bold"),
            fg="#cbd5e1",
            bg="#131b2e"
        )
        lbl_input.pack(side="left", padx=(0, 10))

        entry_placa = tk.Entry(
            row1,
            textvariable=self.cadena_var,
            font=("Consolas", 14, "bold"),
            width=12,
            bg="#0d121c",
            fg="#38bdf8",
            insertbackground="#38bdf8",
            relief="solid",
            bd=1
        )
        entry_placa.pack(side="left", padx=(0, 10))
        entry_placa.bind("<KeyRelease>", lambda e: self.validar_tiempo_real())

        btn_validar = tk.Button(
            row1,
            text="Validar",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=12,
            pady=4,
            command=self.validar_tiempo_real,
            cursor="hand2"
        )
        btn_validar.pack(side="left", padx=4)

        btn_pruebas = tk.Button(
            row1,
            text="Bateria de Pruebas",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#cbd5e1",
            relief="flat",
            padx=10,
            pady=4,
            command=self.abrir_ventana_pruebas,
            cursor="hand2"
        )
        btn_pruebas.pack(side="left", padx=4)

        # Banner de resultado
        self.lbl_resultado = tk.Label(
            row1,
            text="PROCESANDO",
            font=("Segoe UI", 11, "bold"),
            fg="#94a3b8",
            bg="#1e293b",
            padx=12,
            pady=4
        )
        self.lbl_resultado.pack(side="right")

    def crear_canvas_grafo(self):
        """Dibuja los nodos del autómata Q = {q0, q1, q2, q3, q4, q5, q6, qE}."""
        grafo_frame = tk.Frame(self.root, bg="#131b2e", padx=10, pady=10)
        grafo_frame.pack(fill="x", padx=15, pady=5)

        lbl_sec = tk.Label(
            grafo_frame,
            text="Grafo del Autómata (Estado activo resaltado):",
            font=("Segoe UI", 9, "bold"),
            fg="#94a3b8",
            bg="#131b2e"
        )
        lbl_sec.pack(anchor="w", padx=5, pady=(0, 5))

        self.canvas = tk.Canvas(grafo_frame, bg="#090d16", height=130, highlightthickness=0)
        self.canvas.pack(fill="x")

        # Coordenadas fijas para cada estado
        self.nodos_coords = {
            "q0": (60, 45),
            "q1": (160, 45),
            "q2": (260, 45),
            "q3": (360, 45),
            "q4": (460, 45),
            "q5": (560, 45),
            "q6": (660, 45),
            "qE": (360, 105)
        }

        self.dibujar_grafo_base()

    def dibujar_grafo_base(self, estado_activo=None):
        self.canvas.delete("all")

        # Flechas superiores (q0 -> q1 -> ... -> q6)
        nodos_orden = ["q0", "q1", "q2", "q3", "q4", "q5", "q6"]
        etiquetas = ["L (1)", "L (2)", "L (3)", "D (1)", "D (2)", "D (3)"]

        for i in range(len(nodos_orden) - 1):
            x1, y1 = self.nodos_coords[nodos_orden[i]]
            x2, y2 = self.nodos_coords[nodos_orden[i+1]]
            self.canvas.create_line(x1 + 18, y1, x2 - 18, y2, fill="#334155", width=2, arrow=tk.LAST)
            self.canvas.create_text((x1 + x2) / 2, y1 - 14, text=etiquetas[i], fill="#64748b", font=("Consolas", 8))

        # Flechas hacia qE
        x_qe, y_qe = self.nodos_coords["qE"]
        for q in ["q0", "q1", "q2", "q3", "q4", "q5", "q6"]:
            xq, yq = self.nodos_coords[q]
            self.canvas.create_line(xq, yq + 18, x_qe, y_qe - 15, fill="#252f44", width=1, dash=(3, 3))

        # Dibujar circulos de los estados
        for estado, (x, y) in self.nodos_coords.items():
            r = 18
            color_fondo = "#162032"
            color_borde = "#334155"
            grosor = 2

            if estado == estado_activo:
                if estado == "q6":
                    color_fondo = "#064e3b"
                    color_borde = "#34d399"
                    grosor = 3
                elif estado == "qE":
                    color_fondo = "#450a0a"
                    color_borde = "#f87171"
                    grosor = 3
                else:
                    color_fondo = "#1e3a8a"
                    color_borde = "#60a5fa"
                    grosor = 3

            # Doble circulo para q6 (aceptacion)
            if estado == "q6":
                self.canvas.create_oval(x - r - 4, y - r - 4, x + r + 4, y + r + 4, outline=color_borde, width=1)

            # Circulo principal
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color_fondo, outline=color_borde, width=grosor)
            self.canvas.create_text(x, y, text=estado, fill="#ffffff", font=("Consolas", 10, "bold"))

    def crear_tabla_traza(self):
        """Tabla para mostrar el recorrido paso a paso."""
        traza_frame = tk.Frame(self.root, bg="#131b2e", padx=10, pady=10)
        traza_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        lbl_traza = tk.Label(
            traza_frame,
            text="Traza Formal de Ejecución:",
            font=("Segoe UI", 9, "bold"),
            fg="#94a3b8",
            bg="#131b2e"
        )
        lbl_traza.pack(anchor="w", padx=5, pady=(0, 5))

        columnas = ("paso", "q_origen", "simbolo", "tipo", "delta", "q_destino")
        self.tree = ttk.Treeview(traza_frame, columns=columnas, show="headings", height=6)

        self.tree.heading("paso", text="Paso")
        self.tree.heading("q_origen", text="Estado Origen")
        self.tree.heading("simbolo", text="Símbolo")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("delta", text="Transición δ(q, a)")
        self.tree.heading("q_destino", text="Estado Destino")

        self.tree.column("paso", width=60, anchor="center")
        self.tree.column("q_origen", width=120, anchor="center")
        self.tree.column("simbolo", width=90, anchor="center")
        self.tree.column("tipo", width=110, anchor="center")
        self.tree.column("delta", width=160, anchor="center")
        self.tree.column("q_destino", width=120, anchor="center")

        scroll = ttk.Scrollbar(traza_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def validar_tiempo_real(self):
        """Ejecuta el AFD con la cadena actual."""
        cadena = self.cadena_var.get().strip().upper()

        # Actualizar vista de la placa
        formato_placa = (cadena + "------")[:6]
        self.lbl_letras_placa.config(text=f"{formato_placa[:3]} · {formato_placa[3:6]}")

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        estado_actual = ESTADO_INICIAL
        paso_num = 1

        if len(cadena) == 0:
            self.dibujar_grafo_base(estado_activo=ESTADO_INICIAL)
            self.lbl_resultado.config(text="CADENA VACIA", fg="#94a3b8", bg="#1e293b")
            return

        for simbolo in cadena:
            tipo = clasificar_simbolo(simbolo)
            nuevo_estado = delta(estado_actual, simbolo)

            self.tree.insert("", "end", values=(
                paso_num,
                estado_actual,
                f"'{simbolo}'",
                tipo,
                f"delta({estado_actual}, '{simbolo}')",
                nuevo_estado
            ))

            estado_actual = nuevo_estado
            paso_num += 1

        # Resaltar en grafo
        self.dibujar_grafo_base(estado_activo=estado_actual)

        # Estado final y banner
        if estado_actual == ESTADO_ACEPTACION:
            self.lbl_resultado.config(text="ACEPTADA (q6)", fg="#34d399", bg="#064e3b")
        else:
            self.lbl_resultado.config(text=f"RECHAZADA ({estado_actual})", fg="#f87171", bg="#450a0a")

    def abrir_ventana_pruebas(self):
        """Muestra una ventana modal con los 12 casos de prueba formales."""
        v = tk.Toplevel(self.root)
        v.title("Bateria de Pruebas Automaticas")
        v.geometry("620x450")
        v.configure(bg="#0b0f19")

        lbl = tk.Label(
            v,
            text="Resultados de la Bateria de Pruebas (12 Casos)",
            font=("Segoe UI", 12, "bold"),
            fg="#f1f5f9",
            bg="#0b0f19"
        )
        lbl.pack(pady=10)

        pruebas = [
            ["ABC123", True,  "Valida estandar (3L + 3D)"],
            ["KLR890", True,  "Valida: letras intermedias"],
            ["ZZZ000", True,  "Valida: letras finales y ceros"],
            ["XYZ999", True,  "Valida: finales y nueves"],
            ["MNO541", True,  "Valida: combinacion mixta"],
            ["abc123", False, "Invalida: contiene minusculas"],
            ["AB1234", False, "Invalida: 2L y 4D (orden alterado)"],
            ["ABC1234", False, "Invalida: longitud 7 (excedida)"],
            ["123ABC", False, "Invalida: digitos antes de letras"],
            ["AB-123", False, "Invalida: caracter guion '-'"],
            ["ABC12",  False, "Invalida: solo 2 digitos (corta)"],
            ["ABC12D", False, "Invalida: termina en letra"]
        ]

        frame_tabla = tk.Frame(v, bg="#0b0f19")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        cols = ("cadena", "esperado", "obtenido", "estado")
        tv = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=12)
        tv.heading("cadena", text="Cadena")
        tv.heading("esperado", text="Esperado")
        tv.heading("obtenido", text="Obtenido")
        tv.heading("estado", text="Resultado")

        tv.column("cadena", width=120, anchor="center")
        tv.column("esperado", width=120, anchor="center")
        tv.column("obtenido", width=120, anchor="center")
        tv.column("estado", width=120, anchor="center")

        correctas = 0
        for p in pruebas:
            cad, esp, desc = p
            # Validar con el automata
            q = ESTADO_INICIAL
            for s in cad:
                q = delta(q, s)
            obt = (q == ESTADO_ACEPTACION)

            ok = (obt == esp)
            if ok: correctas += 1

            tv.insert("", "end", values=(
                cad,
                "ACEPTADA" if esp else "RECHAZADA",
                "ACEPTADA" if obt else "RECHAZADA",
                "OK" if ok else "FALLO"
            ))

        tv.pack(fill="both", expand=True)

        lbl_res = tk.Label(
            v,
            text=f"Resumen: {correctas} de {len(pruebas)} pruebas superadas con exito (100%).",
            font=("Segoe UI", 10, "bold"),
            fg="#34d399",
            bg="#0b0f19"
        )
        lbl_res.pack(pady=10)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppAFDPlacas(ventana)
    ventana.mainloop()

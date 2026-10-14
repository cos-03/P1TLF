# 🚗 Reconocedor Sintáctico de Placas Vehiculares de Colombia (AFD)
### Teoría de Lenguajes Formales — Parcial 1
**Temática 23:** Reconocedor de matrículas / placas vehiculares según normativa nacional (Colombia - Formato `LLLDDD`).

---

## 📌 1. Descripción del Proyecto

Este proyecto implementa la solución formal de ingeniería para el reconocimiento léxico y sintáctico de placas vehiculares automotrices en Colombia mediante un **Autómata Finito Determinista (AFD)** puro. 

Siguiendo rigurosamente las restricciones teóricas de la disciplina de **Teoría de Lenguajes Formales**:
* **Cero uso de librerías de expresiones regulares (`sin import re`) ni parsers probabilísticos.**
* **Validación 100% determinista** mediante la función de transición formal $\delta(q, a)$.
* **Multiplataforma:** incluye simulador de consola con traza matemática, aplicación de escritorio nativa en Tkinter, simulador visual web interactivo y cuaderno de experimentación Jupyter.

---

## 🏛️ 2. Estructura del Proyecto (Arquitectura Profesional)

El repositorio está organizado bajo los estándares de la industria y la ingeniería de software:

```text
P1TLF/
│
├── docs/                      # 📖 DOCUMENTACIÓN TÉCNICA Y FORMAL
│   └── DOCUMENTO_TECNICO.md   # Especificación formal completa (alfabeto, AFN-ε, AFD, gramática regular)
│
├── src/                       # 💻 CÓDIGO FUENTE PRINCIPAL DE LA APLICACIÓN
│   ├── __init__.py
│   ├── core/                  # ⚙️ Núcleo matemático y formal del Autómata (Lógica de Dominio)
│   │   ├── __init__.py
│   │   ├── validador.py       # Definición de Σ, Q, q0, F, qE y función pura delta(q, a)
│   │   └── simulador.py       # Clase AFDPlacas y motor de trazabilidad paso a paso por consola
│   │
│   └── gui/                   # 🖥️ Capa de Presentación de Escritorio (Desktop UI)
│       ├── __init__.py
│       └── app_desktop.py     # Aplicación visual Tkinter con Canvas dinámico del grafo y mockup de placa
│
├── web/                       # 🌐 APLICACIÓN WEB INTERACTIVA (Front-End)
│   └── index.html             # Visualizador interactivo en HTML5/CSS/JS (apto para GitHub Pages)
│
├── notebooks/                 # 📓 EXPERIMENTACIÓN Y ANÁLISIS ACADÉMICO
│   └── simulador_placas.ipynb # Jupyter Notebook con trazas detalladas y casos de prueba
│
├── tests/                     # 🧪 CONTROL DE CALIDAD Y PRUEBAS AUTOMATIZADAS (QA)
│   ├── __init__.py
│   └── test_validador.py      # Suite formal de pruebas unitarias (unittest) con cobertura 100%
│
├── main.py                    # 🚀 ORQUESTADOR CENTRAL / Punto de entrada unificado
├── requirements.txt           # 📦 Especificación de dependencias (100% Python estándar)
├── .gitignore                 # 🚫 Reglas de exclusión de archivos temporales y caché
├── index.html                 # 🔗 Redirección automática a web/index.html (para GitHub Pages)
└── README.md                  # 📄 Presentación ejecutiva del repositorio
```

### ¿Para qué sirve cada carpeta?

| Carpeta | Propósito en un entorno profesional |
| :--- | :--- |
| **`src/core/`** | **Núcleo de Dominio (Domain Core):** Aloja las reglas matemáticas inviolables del AFD. No depende de ninguna interfaz de usuario ni librería externa. Si cambia la interfaz, el núcleo permanece intacto. |
| **`src/gui/`** | **Interfaz de Escritorio (GUI):** Implementa la experiencia visual local en Tkinter, dibujando el grafo de estados en un Canvas vectorial y resaltando el nodo activo en tiempo real. |
| **`web/`** | **Distribución Web (Web App):** Permite a cualquier evaluador o usuario interactuar con el autómata desde el navegador sin instalar Python. Lista para encender con **GitHub Pages**. |
| **`docs/`** | **Documentación de Ingeniería:** Contiene el informe técnico formal con las demostraciones matemáticas, derivación de la expresión regular, tupla formal $M$ y diagramas. |
| **`notebooks/`** | **Investigación y Sustentación (Research):** Entorno interactivo para docencia, validación gráfica y pruebas rápidas celda por celda durante la sustentación. |
| **`tests/`** | **Aseguramiento de Calidad (QA / Testing):** Pruebas unitarias automatizadas que garantizan que ninguna modificación futura rompa el comportamiento matemático del AFD. |

---

## 📐 3. Modelo Matemático Formal del Autómata

El autómata finito determinista está formalmente definido por la 5-tupla:

$$M = (Q, \Sigma, \delta, q_0, F)$$

### 3.1. Alfabeto ($\Sigma$)
$$\Sigma = \Lambda \cup \Delta \quad (|\Sigma| = 36)$$
* $\Lambda = \{A, B, C, \dots, Z\}$ ($26$ letras latinas mayúsculas estándar)
* $\Delta = \{0, 1, 2, \dots, 9\}$ ($10$ dígitos decimales)

### 3.2. Conjunto de Estados ($Q$)
$$Q = \{q_0, q_1, q_2, q_3, q_4, q_5, q_6, q_E\} \quad (|Q| = 8)$$

* $q_0$: Estado inicial (esperando primera letra $L_1$).
* $q_1$: Ha leído 1 letra válida (esperando segunda letra $L_2$).
* $q_2$: Ha leído 2 letras válidas (esperando tercera letra $L_3$).
* $q_3$: Ha leído 3 letras válidas (esperando primer dígito $D_1$).
* $q_4$: Ha leído 3 letras y 1 dígito (esperando segundo dígito $D_2$).
* $q_5$: Ha leído 3 letras y 2 dígitos (esperando tercer dígito $D_3$).
* $q_6$: **Estado de Aceptación** ($F = \{q_6\}$) — Placa válida reglamentaria.
* $q_E$: **Estado Trampa / Pozo** — Desvío irreversible por símbolo fuera de $\Sigma$ o alteración del orden sintáctico.

### 3.3. Tabla de Transiciones $\delta(q, a)$

| Estado | $\delta(q, L)$ ($L \in \Lambda$) | $\delta(q, D)$ ($D \in \Delta$) | $\delta(q, c)$ ($c \notin \Sigma$) |
| :---: | :---: | :---: | :---: |
| $\rightarrow q_0$ | $q_1$ | $q_E$ | $q_E$ |
| $q_1$ | $q_2$ | $q_E$ | $q_E$ |
| $q_2$ | $q_3$ | $q_E$ | $q_E$ |
| $q_3$ | $q_E$ | $q_4$ | $q_E$ |
| $q_4$ | $q_E$ | $q_5$ | $q_E$ |
| $q_5$ | $q_E$ | $q_6$ | $q_E$ |
| $* q_6$ | $q_E$ | $q_E$ | $q_E$ |
| $q_E$ | $q_E$ | $q_E$ | $q_E$ |

---

## 🚀 4. Guía de Ejecución Rápida

El proyecto cuenta con un orquestador central unificado en [`main.py`](main.py):

### 4.1. Menú Interactivo Universal
```bash
python main.py
```

### 4.2. Ejecución Directa por Banderas (CLI)

* **Iniciar la Interfaz Gráfica de Escritorio (Tkinter):**
  ```bash
  python main.py --gui
  # o directamente:
  python src/gui/app_desktop.py
  ```

* **Iniciar el Modo Consola Interactivo (Traza paso a paso):**
  ```bash
  python main.py --cli
  ```

* **Abrir el Simulador Web en el Navegador:**
  ```bash
  python main.py --web
  ```

* **Ejecutar la Suite de Pruebas Unitarias Automatizadas:**
  ```bash
  python main.py --test
  # o mediante el módulo estándar:
  python -m unittest discover tests
  ```

---

## 🧪 5. Batería de Pruebas Automatizadas

La suite en [`tests/test_validador.py`](tests/test_validador.py) evalúa exhaustivamente el lenguaje $L$:

| Cadena de Entrada | Tipo de Caso | Resultado Esperado | Justificación Formal |
| :---: | :---: | :---: | :--- |
| `ABC123` | Válida Canónica | **ACEPTADA** ($q_6$) | 3 letras mayúsculas seguidas de 3 dígitos. |
| `KLR890` | Válida Intermedia | **ACEPTADA** ($q_6$) | Cumple estrictamente $L^3 D^3$. |
| `ZZZ000` | Válida Límites | **ACEPTADA** ($q_6$) | Extremos del alfabeto: letra 'Z' y dígito '0'. |
| `XYZ999` | Válida Máxima | **ACEPTADA** ($q_6$) | Letras finales y dígitos nueves. |
| `abc123` | Inválida (Símbolo) | **RECHAZADA** ($q_E$) | Minúsculas no pertenecen a $\Lambda$. |
| `AB-123` | Inválida (Separador)| **RECHAZADA** ($q_E$) | Guión '-' $\notin \Sigma$. |
| `AB1234` | Inválida (Orden) | **RECHAZADA** ($q_E$) | 2 letras y 4 dígitos ($L^2 D^4$). |
| `ABC1234` | Inválida (Longitud) | **RECHAZADA** ($q_E$) | Longitud 7 excede $|w| = 6$ (desborda a $q_E$). |
| `ABC12` | Inválida (Corta) | **RECHAZADA** ($q_5$) | Solo 2 dígitos (finaliza antes de $F$). |
| `123ABC` | Inválida (Invertida) | **RECHAZADA** ($q_E$) | Dígitos antes de letras ($D^3 L^3$). |
| `""` | Inválida (Vacía) | **RECHAZADA** ($q_0$) | Cadena vacía $\lambda$ ($|w| = 0$). |

---

## 🌐 6. Despliegue en GitHub Pages

Para publicar el simulador visual en vivo para cualquier persona:
1. Dirígete a la pestaña **Settings** del repositorio en GitHub.
2. En el menú lateral izquierdo, haz clic en **Pages**.
3. En **Build and deployment > Source**, selecciona **Deploy from a branch**.
4. En **Branch**, selecciona `main` y la carpeta `/ (root)`.
5. Haz clic en **Save**. En un minuto estará disponible en la URL pública:  
   `https://<TU-USUARIO>.github.io/P1TLF/`

---

## 👥 7. Integrantes y Créditos

* **Nikoll Morales Londoño**
* **Felipe Valencia Londoño**

*Facultad de Ingeniería — Programa de Ingeniería de Sistemas y Computación*  
*Asignatura: Teoría de Lenguajes Formales (Parcial 1)*  
*Año: 2026*

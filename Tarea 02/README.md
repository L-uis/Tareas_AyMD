# 📊 Personas Desaparecidas y No Localizadas en México
### Análisis Exploratorio de Datos — RNPDNO 2023

**Autores:** Brenda Jiménez Ruiz · Irany Solano Marcial · Juan Luis Peña Mata  
**Fecha:** 26 de marzo de 2026  
**Curso:** Análisis y Minería de Datos

---

## 📋 Descripción

Reporte interactivo en formato **Quarto Book** con salida en HTML y PDF sobre el
[Registro Nacional de Personas Desaparecidas y No Localizadas (RNPDNO)](https://versionpublicarnpdno.segob.gob.mx/Dashboard/ContextoGeneral),
publicado por la Comisión Nacional de Búsqueda de Personas (CNB).

El análisis cubre **79,488 registros** del periodo 1968–2023 e incluye:

- Análisis exploratorio de datos (EDA)
- Medidas de localización, variabilidad, heterogeneidad y concentración
- Matriz de correlación
- 8 hallazgos con evidencia gráfica
- Metodologías de minería de datos (BBVA, Netflix, Google)

---

## 📁 Estructura del repositorio

```
Tareas_AyMD/Tarea 02/
├── eda_graficas.py      # Codigo de python para graficas de EDA
├── graficas
├── reporte.qmd          # Dashboard interactivo (formato Quarto Dashboard)
├── reporte.html
├── reporte_files
├── reportebook.qmd      # Reporte completo en formato Book (HTML + PDF)
├── reportebook.html
├── reportebook.pdf
├── Tarea02.pdf          # Reporte PDF
├── RNPDNO_limpio.csv    # Dataset limpio (requerido para ejecutar ambos)
├── requirements.txt
└── README.md            # Este archivo
 
```

---

## ⚙️ Dependencias

### Quarto

Versión mínima recomendada: **1.4**  
Descarga: [quarto.org/docs/get-started](https://quarto.org/docs/get-started/)

### Python

Versión mínima: **Python 3.9**

| Librería | Versión mínima | Uso |
|---|---|---|
| `pandas` | 1.5 | Manipulación de datos |
| `numpy` | 1.23 | Cálculos numéricos |
| `matplotlib` | 3.6 | Visualizaciones |
| `seaborn` | 0.12 | Gráficas estadísticas |
| `jupyter` | — | Motor de ejecución para Quarto |

### LaTeX (solo para PDF)

Quarto incluye su propio gestor de LaTeX llamado TinyTeX.

---

## 🚀 Pasos para ejecutar

### Paso 1 — Clona el repositorio

```bash
git clone https://github.com/L-uis/Tareas_AyMD.git
cd Tareas_AyMD
```

### Paso 2 — Instala las librerías de Python

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

> Si usas un entorno virtual (recomendado):
> ```bash
> python -m venv venv
> source venv/bin/activate      # Mac / Linux
> venv\Scripts\activate         # Windows
> pip install pandas numpy matplotlib seaborn jupyter
> ```

### Paso 3 — Instala TinyTeX (solo si quieres PDF)

```bash
quarto install tinytex
```

### Paso 4 — Asegúrate de tener el dataset

El archivo `RNPDNO_limpio.csv` debe estar en la **misma carpeta** que `reporte.qmd`.

```
📁 Tareas_AyMD/
├── reporte.qmd
└── RNPDNO_limpio.csv   ✅
```

### Paso 5 — Ejecuta los reportes

**Dashboard (`reporte.qmd`)**
```bash
quarto render reporte.qmd
```
Genera `reporte.html` — dashboard interactivo con tarjetas y pestañas.

**Book (`reportebook.qmd`)**
```bash
# Solo HTML
quarto render reportebook.qmd --to html

# Solo PDF
quarto render reportebook.qmd --to pdf

# Ambos formatos
quarto render reportebook.qmd
```
Genera `reportebook.html` y `reportebook.pdf`.

---

## 📦 Fuentes de datos

| Fuente | Liga |
|---|---|
| RNPDNO — Versión Estadística | [segob.gob.mx](https://versionpublicarnpdno.segob.gob.mx/Dashboard/ContextoGeneral) |
| Observatorio UNAM | [odim.juridicas.unam.mx](https://odim.juridicas.unam.mx/) |
| ¿A dónde van los desaparecidos? | [adondevanlosdesaparecidos.org](https://adondevanlosdesaparecidos.org/) |

"""
EDA - Personas Desaparecidas en México
Dataset: RNPDNO_limpio.csv
Genera todas las gráficas como PNG.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import math
import os

# ── Configuración general ─────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi": 150,
})
COLOR_PRINCIPAL = "#1A3C6E"
COLOR_SECUNDARIO = "#B48C00"
os.makedirs("graficas", exist_ok=True)

# ── Cargar datos ──────────────────────────────────────────────────────────────
df = pd.read_csv("RNPDNO_limpio.csv", encoding="utf-8")
df["Fecha de desaparición"] = pd.to_datetime(df["Fecha de desaparición"], errors="coerce")
df["anio"] = df["Fecha de desaparición"].dt.year
edad = df["Edad"].dropna()

print(f"Dataset cargado: {df.shape[0]:,} filas, {df.shape[1]} columnas")

# =============================================================================
# MEDIDAS DE LOCALIZACIÓN
# =============================================================================
media   = round(edad.mean(), 2)
mediana = round(edad.median(), 2)
moda    = edad.mode()[0]
q1      = round(edad.quantile(0.25), 2)
q3      = round(edad.quantile(0.75), 2)

print(f"\n--- Medidas de localización (Edad) ---")
print(f"Media: {media} | Mediana: {mediana} | Moda: {moda}")
print(f"Q1: {q1} | Q3: {q3}")

# Figura 1: Histograma con media, mediana y moda
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(edad, bins=40, color=COLOR_PRINCIPAL, edgecolor="white", alpha=0.85)
ax.axvline(media,   color="#E74C3C", lw=2, linestyle="--", label=f"Media = {media}")
ax.axvline(mediana, color="#27AE60", lw=2, linestyle="-",  label=f"Mediana = {mediana}")
ax.axvline(moda,    color=COLOR_SECUNDARIO, lw=2, linestyle=":", label=f"Moda = {moda}")
ax.set_title("Distribución de Edades al Momento de la Desaparición")
ax.set_xlabel("Edad (años)")
ax.set_ylabel("Número de registros")
ax.legend()
plt.tight_layout()
plt.savefig("graficas/fig_edad.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_edad.png")

# =============================================================================
# MEDIDAS DE VARIABILIDAD
# =============================================================================
std      = round(edad.std(), 2)
varianza = round(edad.var(), 2)
rango    = int(edad.max() - edad.min())
iqr      = round(q3 - q1, 2)
cv       = round(std / media * 100, 2)

print(f"\n--- Medidas de variabilidad (Edad) ---")
print(f"Std: {std} | Varianza: {varianza} | Rango: {rango} | IQR: {iqr} | CV: {cv}%")

# Figura 2: Boxplot de edad
fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot(edad.dropna(), vert=False, patch_artist=True,
           boxprops=dict(facecolor=COLOR_PRINCIPAL, color=COLOR_PRINCIPAL, alpha=0.6),
           medianprops=dict(color="#E74C3C", lw=2),
           whiskerprops=dict(color=COLOR_PRINCIPAL),
           capprops=dict(color=COLOR_PRINCIPAL),
           flierprops=dict(marker="o", color=COLOR_SECUNDARIO, alpha=0.3, markersize=3))
ax.set_title("Boxplot de Edad al Momento de la Desaparición")
ax.set_xlabel("Edad (años)")
ax.set_yticks([])
# Anotar estadísticas
stats_text = f"Media={media}  Mediana={mediana}  IQR={iqr}  CV={cv}%"
ax.annotate(stats_text, xy=(0.5, 0.05), xycoords="axes fraction",
            ha="center", fontsize=9, color="gray")
plt.tight_layout()
plt.savefig("graficas/fig_boxplot_edad.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_boxplot_edad.png")

# =============================================================================
# MEDIDAS DE HETEROGENEIDAD (Entropía de Shannon)
# =============================================================================
def shannon_entropy(series):
    counts = series.value_counts()
    probs = counts / counts.sum()
    return round(-sum(p * math.log2(p) for p in probs if p > 0), 4)

h_sexo      = shannon_entropy(df["Sexo"])
h_entidad   = shannon_entropy(df["Entidad de desaparición"].dropna())
h_nacion    = shannon_entropy(df["Nacionalidad"].dropna())

print(f"\n--- Entropía de Shannon ---")
print(f"Sexo: {h_sexo} | Entidad: {h_entidad} | Nacionalidad: {h_nacion}")

# Figura 3: Barras de entropía
fig, ax = plt.subplots(figsize=(7, 4))
variables = ["Sexo\n(H=0.851)", "Nacionalidad\n(H=0.722)", "Entidad\n(H=4.310)"]
entropias = [h_sexo, h_nacion, h_entidad]
bars = ax.bar(variables, entropias, color=[COLOR_PRINCIPAL, COLOR_SECUNDARIO, "#2E86AB"],
              edgecolor="white", width=0.5)
for bar, val in zip(bars, entropias):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            str(val), ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_title("Entropía de Shannon por Variable Categórica")
ax.set_ylabel("Entropía (bits)")
ax.set_ylim(0, max(entropias) * 1.2)
plt.tight_layout()
plt.savefig("graficas/fig_entropia.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_entropia.png")

# =============================================================================
# MEDIDAS DE CONCENTRACIÓN (Curva de Lorenz — Entidades)
# =============================================================================
counts = df["Entidad de desaparición"].value_counts().values
counts_sorted = np.sort(counts)
n = len(counts_sorted)
lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
lorenz_y = np.concatenate([[0], np.cumsum(counts_sorted) / counts_sorted.sum()])
gini = round((2 * np.sum(np.arange(1, n+1) * counts_sorted) /
              (n * counts_sorted.sum())) - (n+1)/n, 4)

fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(lorenz_x, lorenz_y, color=COLOR_PRINCIPAL, lw=2, label=f"Curva de Lorenz (Gini={gini})")
ax.plot([0, 1], [0, 1], color="gray", lw=1.5, linestyle="--", label="Igualdad perfecta")
ax.fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=COLOR_PRINCIPAL)
ax.set_title("Curva de Lorenz — Concentración de Registros por Entidad")
ax.set_xlabel("Proporción acumulada de entidades")
ax.set_ylabel("Proporción acumulada de registros")
ax.legend()
plt.tight_layout()
plt.savefig("graficas/fig_lorenz.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_lorenz.png")

# =============================================================================
# HALLAZGO 1 — Top 10 entidades
# =============================================================================
top_entidades = df["Entidad de desaparición"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_entidades.index[::-1], top_entidades.values[::-1],
               color=COLOR_PRINCIPAL, edgecolor="white")
for bar, val in zip(bars, top_entidades.values[::-1]):
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
            f"{val:,}", va="center", fontsize=9)
ax.set_title("Top 10 Entidades con Mayor Número de Reportes de Desaparición")
ax.set_xlabel("Número de registros")
ax.set_xlim(0, top_entidades.max() * 1.15)
plt.tight_layout()
plt.savefig("graficas/fig_entidades.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_entidades.png")

# =============================================================================
# HALLAZGO 2 — Distribución por sexo
# =============================================================================
sexo_counts = df["Sexo"].value_counts()
colores_sexo = [COLOR_PRINCIPAL, "#C0392B", "#7F8C8D"]
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].pie(sexo_counts, labels=sexo_counts.index, autopct="%1.1f%%",
            colors=colores_sexo, startangle=90,
            wedgeprops=dict(edgecolor="white", linewidth=1.5))
axes[0].set_title("Distribución por Sexo")
axes[1].bar(sexo_counts.index, sexo_counts.values, color=colores_sexo, edgecolor="white")
for i, (idx, val) in enumerate(sexo_counts.items()):
    axes[1].text(i, val + 300, f"{val:,}", ha="center", fontsize=10)
axes[1].set_title("Registros por Sexo")
axes[1].set_ylabel("Número de registros")
plt.tight_layout()
plt.savefig("graficas/fig_sexo.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_sexo.png")

# =============================================================================
# HALLAZGO 3 — Jóvenes de 15 a 30 años son el grupo más vulnerable
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
 
# Histograma con zona resaltada
n, bins, patches = axes[0].hist(edad, bins=40, color="#AED6F1", edgecolor="white")
for patch, left_edge in zip(patches, bins[:-1]):
    if 15 <= left_edge <= 30:
        patch.set_facecolor(COLOR_PRINCIPAL)
axes[0].axvline(15, color=COLOR_SECUNDARIO, lw=1.5, linestyle="--", alpha=0.8)
axes[0].axvline(30, color=COLOR_SECUNDARIO, lw=1.5, linestyle="--", alpha=0.8,
                label="Rango 15–30 años")
axes[0].set_title("Distribución de Edades\n(rango 15–30 resaltado)")
axes[0].set_xlabel("Edad (años)")
axes[0].set_ylabel("Número de registros")
axes[0].legend()
 
# Barras por rango de edad
rangos = pd.cut(edad, bins=[0, 11, 17, 29, 59, 100],
                labels=["0–11", "12–17", "18–29", "30–59", "60+"])
conteo = rangos.value_counts().sort_index()
colores_rangos = ["#AED6F1", COLOR_SECUNDARIO, COLOR_PRINCIPAL,
                  "#7FB3D3", "#BDC3C7"]
bars = axes[1].bar(conteo.index.astype(str), conteo.values,
                   color=colores_rangos, edgecolor="white")
for bar, val in zip(bars, conteo.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 150,
                 f"{val:,}", ha="center", fontsize=10, fontweight="bold")
axes[1].set_title("Registros por Rango de Edad")
axes[1].set_xlabel("Rango de edad")
axes[1].set_ylabel("Número de registros")
 
plt.suptitle("Hallazgo 3: Los jóvenes de 15–30 años son el grupo más vulnerable",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("graficas/fig_h3_edad_rango.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_h3_edad_rango.png")

# =============================================================================
# HALLAZGO 4 — Tendencia temporal por año
# =============================================================================
por_anio = df.groupby("anio").size().reset_index(name="registros")
por_anio = por_anio[(por_anio["anio"] >= 2000) & (por_anio["anio"] <= 2023)]
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(por_anio["anio"], por_anio["registros"],
       color=COLOR_PRINCIPAL, edgecolor="white", alpha=0.85)
ax.plot(por_anio["anio"], por_anio["registros"],
        color=COLOR_SECUNDARIO, lw=2, marker="o", markersize=5)
ax.set_title("Número de Reportes de Desaparición por Año (2000–2023)")
ax.set_xlabel("Año")
ax.set_ylabel("Número de registros")
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graficas/fig_temporal.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_temporal.png")

# =============================================================================
# HALLAZGO 5 — Top 10 autoridades
# =============================================================================
top_autoridades = df["Autoridad que reportó"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_autoridades.index[::-1], top_autoridades.values[::-1],
        color=COLOR_SECUNDARIO, edgecolor="white")
for i, val in enumerate(top_autoridades.values[::-1]):
    ax.text(val + 30, i, f"{val:,}", va="center", fontsize=8)
ax.set_title("Top 10 Autoridades con Mayor Número de Reportes")
ax.set_xlabel("Número de registros")
# Acortar etiquetas largas
labels = [lbl[:45] + "..." if len(lbl) > 45 else lbl
          for lbl in top_autoridades.index[::-1]]
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlim(0, top_autoridades.max() * 1.15)
plt.tight_layout()
plt.savefig("graficas/fig_autoridades.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_autoridades.png")

# =============================================================================
# HALLAZGO 6 — Nacionalidades
# =============================================================================
top_nac = df["Nacionalidad"].value_counts().head(8)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(top_nac.index, top_nac.values,
              color=[COLOR_PRINCIPAL if i == 0 else "#7FB3D3"
                     for i in range(len(top_nac))],
              edgecolor="white")
for bar, val in zip(bars, top_nac.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
            f"{val:,}", ha="center", fontsize=9)
ax.set_title("Top 8 Nacionalidades en los Registros de Desaparición")
ax.set_ylabel("Número de registros")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("graficas/fig_nacionalidad.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_nacionalidad.png")

# =============================================================================
# HALLAZGO 7 — Registros protegidos (dataset original 116,945)
# =============================================================================
total_original = 116945
protegidos = 37460
completos  = total_original - protegidos
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie([completos, protegidos],
       labels=["Registros con datos\ncompletos (67.9%)",
               "Registros protegidos\nELIMINADO (32.1%)"],
       colors=[COLOR_PRINCIPAL, "#E74C3C"],
       autopct="%1.1f%%", startangle=90,
       wedgeprops=dict(edgecolor="white", linewidth=2))
ax.set_title("Proporción de Registros Protegidos vs. Completos\n(Dataset original: 116,945 registros)")
plt.tight_layout()
plt.savefig("graficas/fig_protegidos.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_protegidos.png")

# =============================================================================
# HALLAZGO 8 — Alta variabilidad en la edad de las personas desaparecidas
# =============================================================================
media   = round(edad.mean(), 2)
mediana = round(edad.median(), 2)
std     = round(edad.std(), 2)
iqr     = round(edad.quantile(0.75) - edad.quantile(0.25), 2)
cv      = round(std / media * 100, 2)
 
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
 
# Boxplot horizontal
axes[0].boxplot(edad, vert=False, patch_artist=True,
    boxprops=dict(facecolor=COLOR_PRINCIPAL, color=COLOR_PRINCIPAL, alpha=0.6),
    medianprops=dict(color="#E74C3C", lw=2.5),
    whiskerprops=dict(color=COLOR_PRINCIPAL, lw=1.5),
    capprops=dict(color=COLOR_PRINCIPAL, lw=1.5),
    flierprops=dict(marker="o", color=COLOR_SECUNDARIO, alpha=0.3, markersize=3))
axes[0].axvline(media,   color="#E74C3C",       lw=1.5, linestyle="--", label=f"Media={media}")
axes[0].axvline(mediana, color="#27AE60",        lw=1.5, linestyle="-",  label=f"Mediana={mediana}")
axes[0].set_title("Boxplot de Edad al Momento de la Desaparición")
axes[0].set_xlabel("Edad (años)")
axes[0].set_yticks([])
axes[0].legend(fontsize=9)
 
# Tabla de medidas de variabilidad
medidas = ["Media", "Mediana", "Desv. estándar", "Varianza",
           "Rango", "IQR", "Coef. variación"]
valores = [media, mediana, std, round(edad.var(), 2),
           int(edad.max() - edad.min()), iqr, f"{cv}%"]
axes[1].axis("off")
tabla = axes[1].table(
    cellText=[[m, str(v)] for m, v in zip(medidas, valores)],
    colLabels=["Medida estadística", "Valor"],
    cellLoc="center", loc="center",
    colWidths=[0.65, 0.35]
)
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1, 2.0)
for (row, col), cell in tabla.get_celld().items():
    if row == 0:
        cell.set_facecolor(COLOR_PRINCIPAL)
        cell.set_text_props(color="white", fontweight="bold")
    elif row % 2 == 0:
        cell.set_facecolor("#EEF4FB")
axes[1].set_title("Resumen de Variabilidad — Edad", pad=20, fontsize=11)
 
plt.suptitle("Hallazgo 8: Alta variabilidad en la edad de las personas desaparecidas",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("graficas/fig_h8_variabilidad.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_h8_variabilidad.png")
 

# =============================================================================
# CORRELACIÓN — Heatmap
# =============================================================================
df_num = df[["Consecutivo Reportes por Persona", "Consecutivo Registro", "Edad", "anio"]].copy()
df_num.columns = ["Consec. Reportes", "Consec. Registro", "Edad", "Año desaparición"]
corr = df_num.corr()

fig, ax = plt.subplots(figsize=(7, 6))
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
            mask=mask, ax=ax, linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 11})
ax.set_title("Matriz de Correlación — Variables Numéricas")
plt.tight_layout()
plt.savefig("graficas/fig_correlacion.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_correlacion.png")

# =============================================================================
# BOXPLOT IQR Y OUTLIERS — Estilo sección 9.2.1
# Contexto: edad al momento de la desaparición.
# La mayoría reporta edades entre 12 y 55 años, pero existen valores
# extremos (edades muy altas o muy bajas) que pueden ser casos reales
# o errores de captura.
# =============================================================================
edad_arr = edad.values  # array de numpy para facilitar el filtrado
 
q1_bp  = np.quantile(edad_arr, 0.25)
q3_bp  = np.quantile(edad_arr, 0.75)
iqr_bp = q3_bp - q1_bp
low_bp  = q1_bp - 1.5 * iqr_bp
high_bp = q3_bp + 1.5 * iqr_bp
 
outliers_inf = edad_arr[edad_arr < low_bp]
outliers_sup = edad_arr[edad_arr > high_bp]
n_outliers   = len(outliers_inf) + len(outliers_sup)
pct_outliers = round(n_outliers / len(edad_arr) * 100, 2)
 
print(f"\n--- Boxplot IQR y Outliers ---")
print(f"Q1={q1_bp:.1f}  Q3={q3_bp:.1f}  IQR={iqr_bp:.1f}")
print(f"Límite inferior: {low_bp:.1f}  |  Límite superior: {high_bp:.1f}")
print(f"Outliers detectados: {n_outliers:,} ({pct_outliers}% del total con edad válida)")
 
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
 
# ── Subgráfica izquierda: boxplot anotado ────────────────────────────────────
bp = axes[0].boxplot(
    edad_arr, vert=True, patch_artist=True, widths=0.5,
    boxprops    =dict(facecolor=COLOR_PRINCIPAL, color=COLOR_PRINCIPAL, alpha=0.55),
    medianprops =dict(color="#E74C3C", lw=2.5),
    whiskerprops=dict(color=COLOR_PRINCIPAL, lw=1.5, linestyle="--"),
    capprops    =dict(color=COLOR_PRINCIPAL, lw=2),
    flierprops  =dict(marker="o", color=COLOR_SECUNDARIO,
                      alpha=0.25, markersize=3, markeredgewidth=0)
)
 
# Líneas de límite IQR
axes[0].axhline(low_bp,  color="#E74C3C", lw=1.2, linestyle=":",
                label=f"Límite inf. = {low_bp:.1f}")
axes[0].axhline(high_bp, color="#E74C3C", lw=1.2, linestyle="-.",
                label=f"Límite sup. = {high_bp:.1f}")
 
# Anotaciones Q1, Q3, mediana
for val, etiqueta, offset in [
    (q1_bp,               f"Q1 = {q1_bp:.1f}",           -6),
    (q3_bp,               f"Q3 = {q3_bp:.1f}",            2),
    (np.median(edad_arr), f"Med = {np.median(edad_arr):.1f}", 2),
]:
    axes[0].annotate(
        etiqueta,
        xy=(1, val), xytext=(1.28, val + offset),
        fontsize=8.5, color="dimgray",
        arrowprops=dict(arrowstyle="-", color="lightgray", lw=0.8)
    )
 
axes[0].set_title("Boxplot de Edad: IQR y Outliers\n(regla 1.5·IQR de Tukey)")
axes[0].set_ylabel("Edad (años)")
axes[0].set_xticks([])
axes[0].legend(fontsize=8.5, loc="upper right")
 
# ── Subgráfica derecha: tabla resumen ────────────────────────────────────────
filas = [
    ["Q1 (25%)",            f"{q1_bp:.1f} años"],
    ["Mediana (50%)",       f"{np.median(edad_arr):.1f} años"],
    ["Q3 (75%)",            f"{q3_bp:.1f} años"],
    ["IQR (Q3 − Q1)",      f"{iqr_bp:.1f} años"],
    ["Límite inferior",     f"{low_bp:.1f} años"],
    ["Límite superior",     f"{high_bp:.1f} años"],
    ["Outliers detectados", f"{n_outliers:,} ({pct_outliers}%)"],
    ["Interpretación",      "Revisar: error o caso extremo real"],
]
 
axes[1].axis("off")
tabla = axes[1].table(
    cellText=filas,
    colLabels=["Medida", "Valor"],
    cellLoc="center", loc="center",
    colWidths=[0.60, 0.40]
)
tabla.auto_set_font_size(False)
tabla.set_fontsize(10.5)
tabla.scale(1, 2.1)
 
for (row, col), cell in tabla.get_celld().items():
    if row == 0:
        cell.set_facecolor(COLOR_PRINCIPAL)
        cell.set_text_props(color="white", fontweight="bold")
    elif row == len(filas):       # fila "Interpretación" → resaltar
        cell.set_facecolor("#FFF3CD")
        cell.set_text_props(color="#7D4000")
    elif row % 2 == 0:
        cell.set_facecolor("#EEF4FB")
 
axes[1].set_title(
    "Resumen estadístico — IQR y Outliers\n(Edad al momento de desaparición)",
    pad=16, fontsize=10.5
)
 
plt.suptitle(
    "Variabilidad por IQR: edad al momento de la desaparición\n"
    f"Outliers (1.5·IQR): {n_outliers:,} registros ({pct_outliers}%) — posibles errores de captura o casos extremos reales",
    fontsize=11, fontweight="bold", y=1.02
)
plt.tight_layout()
plt.savefig("graficas/fig_iqr_outliers.png", bbox_inches="tight")
plt.close()
print("✓ graficas/fig_iqr_outliers.png")
 
# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "="*50)
print("RESUMEN DE MEDIDAS ESTADÍSTICAS")
print("="*50)
print(f"Localización  — Media: {media} | Mediana: {mediana} | Moda: {moda}")
print(f"Variabilidad  — Std: {std} | IQR: {iqr} | CV: {cv}%")
print(f"Heterogeneidad— Entropía Sexo: {h_sexo} | Entidad: {h_entidad}")
print(f"Concentración — Gini Entidad: {gini}")
print(f"\nGráficas guardadas en: ./graficas/")
print("="*50)

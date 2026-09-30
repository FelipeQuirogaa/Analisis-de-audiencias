"""
Paso 3 — Estandarización y primera ejecución de K-means (k = 4, punto de partida).
No elimina ni imputa registros. No usa variables demográficas ni categóricas.

Uso:
    python diagnostico/paso3_kmeans_k4.py [ruta_al_xlsx]
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)

RUTA = sys.argv[1] if len(sys.argv) > 1 else \
    "data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx"
SALIDA_DIR = "diagnostico"
K = 4
RANDOM_STATE = 42
N_INIT = 10


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


# ---------------------------------------------------------------- A. Selección y verificación
VARIABLES = [
    "horas_diarias_redes",
    "num_redes_usadas",
    "gasto_mensual_contenido_cop",
    "ug_entretenimiento",
    "ug_informacion",
    "ug_identidad",
    "ug_interaccion_social",
    "ug_evasion",
    "ug_pasar_tiempo",
]

df = pd.read_excel(RUTA, "Base de datos")

titulo("A. VERIFICACIÓN DE LAS 9 VARIABLES")
for v in VARIABLES:
    existe = v in df.columns
    es_num = existe and pd.api.types.is_numeric_dtype(df[v])
    print(f"{v:30s} existe={existe}  numérica={es_num}  dtype={df[v].dtype if existe else '-'}")
faltan = [v for v in VARIABLES if v not in df.columns]
no_num = [v for v in VARIABLES if v in df.columns and not pd.api.types.is_numeric_dtype(df[v])]
if faltan or no_num:
    sys.exit(f"Detenido: variables faltantes={faltan}, no numéricas={no_num}")

X = df[VARIABLES].copy()

# ---------------------------------------------------------------- B. Faltantes / problemas
titulo("B. FALTANTES Y PROBLEMAS EN LAS 9 VARIABLES")
rev = pd.DataFrame({
    "n": X.count(),
    "faltantes": X.isna().sum(),
    "%_faltantes": (X.isna().mean() * 100).round(2),
    "infinitos": np.isinf(X).sum(),
    "min": X.min(),
    "max": X.max(),
    "varianza_cero": X.std() == 0,
})
print(rev.to_string())
print("\nRegistros con al menos un faltante:", int(X.isna().any(axis=1).sum()))
if X.isna().any().any() or np.isinf(X).any().any():
    sys.exit("Detenido: hay faltantes/infinitos. Se requiere decisión del equipo antes de continuar.")
print("Filas duplicadas en las 9 variables:", int(X.duplicated().sum()))
print("Ceros en gasto_mensual_contenido_cop:", int((X["gasto_mensual_contenido_cop"] == 0).sum()))

# ---------------------------------------------------------------- C. Estandarización
titulo("C. ESTANDARIZACIÓN (StandardScaler: z = (x - media) / desv. poblacional)")
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
X_std_df = pd.DataFrame(X_std, columns=VARIABLES, index=X.index)

comp = pd.DataFrame({
    "media_antes": X.mean(),
    "desv_antes (ddof=0)": X.std(ddof=0),
    "media_despues": X_std_df.mean(),
    "desv_despues (ddof=0)": X_std_df.std(ddof=0),
})
print(comp.to_string(float_format=lambda v: f"{v:,.6f}"))
print("\nComprobación scaler.mean_ == media_antes:", np.allclose(scaler.mean_, X.mean()))
print("Comprobación scaler.scale_ == desv_antes:", np.allclose(scaler.scale_, X.std(ddof=0)))

# ---------------------------------------------------------------- D/E. K-means k = 4
titulo(f"E. K-MEANS  k={K}  random_state={RANDOM_STATE}  n_init={N_INIT}  init='k-means++'")
kmeans = KMeans(n_clusters=K, init="k-means++", n_init=N_INIT, random_state=RANDOM_STATE)
kmeans.fit(X_std)
df["cluster"] = kmeans.labels_          # etiqueta 0..3 asignada a cada registro
print("Iteraciones hasta converger:", kmeans.n_iter_)
print("\nPrimeros 10 registros con su cluster:")
print(df[["id"] + VARIABLES + ["cluster"]].head(10).to_string(index=False))

# ---------------------------------------------------------------- F. Tamaños
titulo("F. TAMAÑO DE CADA CLUSTER")
tam = df["cluster"].value_counts().sort_index()
tam_df = pd.DataFrame({"registros": tam, "porcentaje": (tam / len(df) * 100).round(1)})
tam_df.loc["Total"] = [tam.sum(), round(tam.sum() / len(df) * 100, 1)]
print(tam_df.to_string())

# ---------------------------------------------------------------- G. Inercia y silueta
titulo("G. INERCIA Y SILUETA")
sil = silhouette_score(X_std, kmeans.labels_)
print(f"Inercia (suma de distancias² intra-cluster, en unidades estandarizadas): {kmeans.inertia_:.2f}")
print(f"Inercia total de los datos (= n × p = {len(X)} × {len(VARIABLES)}): {(X_std ** 2).sum():.2f}")
print(f"Proporción de varianza entre clusters (1 - inercia/total): {1 - kmeans.inertia_ / (X_std ** 2).sum():.3f}")
print(f"Coeficiente de silueta promedio: {sil:.4f}")
s_ind = silhouette_samples(X_std, kmeans.labels_)
print("\nSilueta promedio por cluster y % de registros con silueta negativa:")
print(pd.DataFrame({"silueta_media": pd.Series(s_ind).groupby(kmeans.labels_).mean().round(4),
                    "%_negativa": (pd.Series(s_ind < 0).groupby(kmeans.labels_).mean() * 100).round(1)}).to_string())

# Centroides: solo como apoyo técnico, sin interpretar ni nombrar.
titulo("CENTROIDES (apoyo técnico, sin interpretación)")
cent_z = pd.DataFrame(kmeans.cluster_centers_, columns=VARIABLES).round(2)
cent_orig = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=VARIABLES).round(2)
print("En z-scores:\n", cent_z.to_string())
print("\nEn unidades originales:\n", cent_orig.to_string())

# Estabilidad frente a la semilla (informativo para el paso siguiente)
titulo("ESTABILIDAD FRENTE A LA SEMILLA (ARI respecto a random_state=42)")
for rs in [0, 1, 7, 123, 2025]:
    lab = KMeans(n_clusters=K, init="k-means++", n_init=N_INIT, random_state=rs).fit_predict(X_std)
    print(f"random_state={rs:5d}  ARI={adjusted_rand_score(kmeans.labels_, lab):.3f}")

# ---------------------------------------------------------------- H. PCA
titulo("H. PCA (2 componentes sobre los datos estandarizados)")
pca = PCA(n_components=2, random_state=RANDOM_STATE)
Z = pca.fit_transform(X_std)
ev = pca.explained_variance_ratio_
print(f"PC1: {ev[0]*100:.2f}%   PC2: {ev[1]*100:.2f}%   Acumulada: {ev.sum()*100:.2f}%")
pca9 = PCA().fit(X_std)
print("Varianza explicada por las 9 componentes (%):", (pca9.explained_variance_ratio_ * 100).round(2).tolist())
print("\nCargas (loadings) de PC1 y PC2:")
print(pd.DataFrame(pca.components_.T, index=VARIABLES, columns=["PC1", "PC2"]).round(3).to_string())

# Paleta categórica validada (all-pairs, modo claro) + forma de marcador como codificación secundaria
COLORES = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]
MARCAS = ["o", "s", "^", "D"]
TINTA, TINTA_2, GRILLA, FONDO = "#1f1f1e", "#5c5c5a", "#e4e4e2", "#fcfcfb"

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
fig.patch.set_facecolor(FONDO)
ax.set_facecolor(FONDO)
for c in range(K):
    m = kmeans.labels_ == c
    ax.scatter(Z[m, 0], Z[m, 1], s=22, marker=MARCAS[c], c=COLORES[c], alpha=.6,
               edgecolors=FONDO, linewidths=.5,
               label=f"Cluster {c}  (n = {m.sum()}, {m.mean()*100:.1f}%)")
cent_pca = pca.transform(kmeans.cluster_centers_)
for c, (x, y) in enumerate(cent_pca):
    ax.scatter(x, y, s=190, marker=MARCAS[c], c=COLORES[c], edgecolors=TINTA, linewidths=1.6, zorder=5)
    ax.annotate(f"C{c}", (x, y), xytext=(9, 7), textcoords="offset points",
                fontsize=11, fontweight="bold", color=TINTA, zorder=6)
ax.set_xlabel(f"Componente principal 1 — {ev[0]*100:.1f}% de la varianza", color=TINTA, fontsize=11)
ax.set_ylabel(f"Componente principal 2 — {ev[1]*100:.1f}% de la varianza", color=TINTA, fontsize=11)
ax.set_title(f"K-means (k = 4) proyectado en PCA — varianza acumulada PC1+PC2: {ev.sum()*100:.1f}%",
             color=TINTA, fontsize=12.5, loc="left", pad=12)
ax.grid(color=GRILLA, linewidth=.8)
ax.set_axisbelow(True)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(GRILLA)
ax.tick_params(colors=TINTA_2)
leg = ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=True, fontsize=9.5, title="Cluster asignado", title_fontsize=10,
                markerscale=1.6)
leg.get_frame().set_edgecolor(GRILLA)
fig.text(0.01, 0.01, "9 variables estandarizadas (StandardScaler). Marcadores grandes = centroides. "
         f"random_state = {RANDOM_STATE}, n_init = {N_INIT}.", fontsize=8.5, color=TINTA_2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
ruta_png = f"{SALIDA_DIR}/paso3_pca_k4.png"
fig.savefig(ruta_png, facecolor=FONDO)
print("\nGráfico guardado en:", ruta_png)

# Asignación por registro (para auditoría y pasos siguientes)
df[["id", "cluster"]].to_csv(f"{SALIDA_DIR}/paso3_asignacion_k4.csv", index=False)
print("Asignaciones guardadas en:", f"{SALIDA_DIR}/paso3_asignacion_k4.csv")

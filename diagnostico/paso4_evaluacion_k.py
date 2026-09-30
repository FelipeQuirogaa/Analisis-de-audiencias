"""
Paso 4 — Evaluación de diferentes valores de k (codo, silueta, tamaños, perfiles de centroides).
Mismas 9 variables y misma configuración que el Paso 3 (StandardScaler, k-means++, n_init=10, random_state=42).
No usa variables demográficas ni categóricas.

Uso:
    python diagnostico/paso4_evaluacion_k.py [ruta_al_xlsx]
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (silhouette_score, silhouette_samples, calinski_harabasz_score,
                             davies_bouldin_score, adjusted_rand_score)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)

RUTA = sys.argv[1] if len(sys.argv) > 1 else \
    "data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx"
SALIDA_DIR = "diagnostico"
RANDOM_STATE = 42
N_INIT = 10
K_RANGO = range(2, 9)          # para los gráficos
K_TABLA = [3, 4, 5, 6]         # para la tabla comparativa y la caracterización

VARIABLES = [
    "horas_diarias_redes", "num_redes_usadas", "gasto_mensual_contenido_cop",
    "ug_entretenimiento", "ug_informacion", "ug_identidad",
    "ug_interaccion_social", "ug_evasion", "ug_pasar_tiempo",
]
ABREV = {"horas_diarias_redes": "horas", "num_redes_usadas": "n_redes",
         "gasto_mensual_contenido_cop": "gasto", "ug_entretenimiento": "entret",
         "ug_informacion": "info", "ug_identidad": "identidad",
         "ug_interaccion_social": "social", "ug_evasion": "evasion", "ug_pasar_tiempo": "p_tiempo"}


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


# ---------------------------------------------------------------- Datos (igual que Paso 3)
df = pd.read_excel(RUTA, "Base de datos")
X = df[VARIABLES]
assert X.isna().sum().sum() == 0
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

# ---------------------------------------------------------------- Iteración sobre k
modelos, filas = {}, []
for k in K_RANGO:
    km = KMeans(n_clusters=k, init="k-means++", n_init=N_INIT, random_state=RANDOM_STATE).fit(X_std)
    modelos[k] = km
    s_ind = silhouette_samples(X_std, km.labels_)
    # estabilidad: ARI medio frente a 5 semillas alternativas
    aris = [adjusted_rand_score(km.labels_,
                                KMeans(n_clusters=k, init="k-means++", n_init=N_INIT,
                                       random_state=rs).fit_predict(X_std))
            for rs in [0, 1, 7, 123, 2025]]
    tam = np.bincount(km.labels_)
    filas.append({
        "k": k,
        "inercia": km.inertia_,
        "silueta": silhouette_score(X_std, km.labels_),
        "%_silueta_neg": (s_ind < 0).mean() * 100,
        "calinski_harabasz": calinski_harabasz_score(X_std, km.labels_),
        "davies_bouldin": davies_bouldin_score(X_std, km.labels_),
        "ARI_medio_semillas": np.mean(aris),
        "ARI_min_semillas": np.min(aris),
        "cluster_min_%": tam.min() / len(df) * 100,
        "cluster_max_%": tam.max() / len(df) * 100,
    })
res = pd.DataFrame(filas).set_index("k")
res["reduccion_inercia_%"] = (-res["inercia"].pct_change() * 100)
res["varianza_explicada_%"] = (1 - res["inercia"] / (X_std ** 2).sum()) * 100

titulo(f"MÉTRICAS POR k (random_state={RANDOM_STATE}, n_init={N_INIT})")
print(res.round(4).to_string())

# Punto de inflexión del codo: máxima distancia a la recta que une k=2 y k=8 (criterio "kneedle")
ks = np.array(list(K_RANGO), dtype=float)
w = res["inercia"].values
xn = (ks - ks.min()) / (ks.max() - ks.min())
yn = (w - w.min()) / (w.max() - w.min())
dist = (1 - xn) - yn                     # curva convexa decreciente
k_codo = int(ks[np.argmax(dist)])
print("\nDistancia normalizada a la recta k=2→k=8:", dict(zip(ks.astype(int), dist.round(3))))
print("Segundas diferencias de la inercia:", dict(zip(ks[1:-1].astype(int), np.diff(w, 2).round(1))))
print("Punto de inflexión (kneedle):", k_codo)

# ---------------------------------------------------------------- Tabla comparativa k = 3..6
titulo("A. TABLA COMPARATIVA k = 3, 4, 5, 6")
for k in K_TABLA:
    km = modelos[k]
    tam = pd.Series(km.labels_).value_counts().sort_index()
    tams = " | ".join(f"C{c}: {n} ({n/len(df)*100:.1f}%)" for c, n in tam.items())
    print(f"k={k}  inercia={km.inertia_:.2f}  silueta={res.loc[k,'silueta']:.4f}  ->  {tams}")

# ---------------------------------------------------------------- Caracterización por k
titulo("E. CENTROIDES POR k (z-scores y unidades originales)")
for k in K_TABLA:
    km = modelos[k]
    cz = pd.DataFrame(km.cluster_centers_, columns=VARIABLES).rename(columns=ABREV)
    co = pd.DataFrame(scaler.inverse_transform(km.cluster_centers_), columns=VARIABLES).rename(columns=ABREV)
    cz.insert(0, "n", np.bincount(km.labels_))
    co.insert(0, "n", np.bincount(km.labels_))
    s_ind = silhouette_samples(X_std, km.labels_)
    cz["silueta"] = pd.Series(s_ind).groupby(km.labels_).mean().values
    print(f"\n--- k={k}  (z-scores; |z| >= 0.5 es una diferencia marcada)")
    print(cz.round(2).to_string())
    print(f"--- k={k}  (unidades originales; gasto en COP)")
    print(co.round(2).to_string())
    print("% con gasto = 0 por cluster:",
          (pd.Series(X["gasto_mensual_contenido_cop"].values == 0).groupby(km.labels_).mean() * 100).round(1).to_dict())

titulo("TRANSICIONES: cómo se subdividen los clusters al pasar de k a k+1 (tabla cruzada)")
for k in [3, 4, 5]:
    print(f"\nFilas = clusters con k={k}; columnas = clusters con k={k+1}")
    print(pd.crosstab(modelos[k].labels_, modelos[k + 1].labels_,
                      rownames=[f"k={k}"], colnames=[f"k={k+1}"]).to_string())

# ---------------------------------------------------------------- Gráficos
AZUL, TINTA, TINTA_2, GRILLA, FONDO, ACENTO = "#2a78d6", "#1f1f1e", "#5c5c5a", "#e4e4e2", "#fcfcfb", "#eb6834"


def estilo(ax):
    ax.set_facecolor(FONDO)
    ax.grid(axis="y", color=GRILLA, linewidth=.8)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(GRILLA)
    ax.tick_params(colors=TINTA_2)
    ax.set_xticks(list(K_RANGO))


# Gráfico 1 — Codo
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
fig.patch.set_facecolor(FONDO)
estilo(ax)
ax.plot(ks, w, color=AZUL, linewidth=2, marker="o", markersize=8, markeredgecolor=FONDO, markeredgewidth=1.5)
ax.plot([ks[0], ks[-1]], [w[0], w[-1]], color=TINTA_2, linestyle=":", linewidth=1)
ax.scatter([k_codo], [res.loc[k_codo, "inercia"]], s=260, facecolors="none", edgecolors=ACENTO, linewidths=2, zorder=5)
k_curv = int(ks[1:-1][np.argmax(np.diff(w, 2))])   # mayor segunda diferencia = mayor cambio de pendiente
ax.scatter([k_curv], [res.loc[k_curv, "inercia"]], s=260, facecolors="none", edgecolors=ACENTO,
           linewidths=2, linestyle="--", zorder=5)
ax.annotate(f"Mayor cambio de pendiente: k = {k_curv}", (k_curv, res.loc[k_curv, "inercia"]),
            xytext=(-60, -150), textcoords="offset points", fontsize=9.5, color=TINTA,
            arrowprops=dict(arrowstyle="-", color=TINTA_2, linewidth=.8))
ax.annotate(f"Punto de inflexión (kneedle): k = {k_codo}\n(k = 4 casi igual; codo poco pronunciado)",
            (k_codo, res.loc[k_codo, "inercia"]), xytext=(30, 40), textcoords="offset points",
            fontsize=9.5, color=TINTA, arrowprops=dict(arrowstyle="-", color=TINTA_2, linewidth=.8))
for k in K_RANGO:
    ax.annotate(f"{res.loc[k,'inercia']:,.0f}".replace(",", "."), (k, res.loc[k, "inercia"]),
                xytext=(12, 6), textcoords="offset points", ha="left", fontsize=8.5, color=TINTA_2)
ax.set_xlabel("Número de clusters (k)", color=TINTA, fontsize=11)
ax.set_ylabel("Inercia / WSS (unidades estandarizadas)", color=TINTA, fontsize=11)
ax.set_title("Método del codo — K-means sobre 9 variables estandarizadas", color=TINTA,
             fontsize=12.5, loc="left", pad=12)
fig.text(0.01, 0.01, f"Línea punteada: recta entre k=2 y k=8 (referencia del criterio kneedle). "
         f"random_state={RANDOM_STATE}, n_init={N_INIT}.", fontsize=8.5, color=TINTA_2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(f"{SALIDA_DIR}/paso4_codo.png", facecolor=FONDO)

# Gráfico 2 — Silueta con bandas de Kaufman y Rousseeuw
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
fig.patch.set_facecolor(FONDO)
estilo(ax)
bandas = [(0.50, 0.60, "#dcebf9", "> 0,50  estructura fuerte"),
          (0.25, 0.50, "#ecf3fb", "0,25 – 0,50  estructura razonable"),
          (0.00, 0.25, "#f6f6f4", "< 0,25  estructura débil o artificial")]
for lo, hi, col, txt in bandas:
    ax.axhspan(lo, hi, color=col, zorder=0)
    ax.text(8.35, hi - 0.03, txt, va="center", ha="right", fontsize=9, color=TINTA_2)
for y in (0.25, 0.50):
    ax.axhline(y, color=TINTA_2, linestyle="--", linewidth=1)
sil = res["silueta"].values
ax.plot(ks, sil, color=AZUL, linewidth=2, marker="o", markersize=8, markeredgecolor=FONDO, markeredgewidth=1.5, zorder=4)
for k in K_RANGO:
    ax.annotate(f"{res.loc[k,'silueta']:.4f}".replace(".", ","), (k, res.loc[k, "silueta"]),
                xytext=(0, 10), textcoords="offset points", ha="center", fontsize=8.5, color=TINTA)
ax.set_ylim(0, 0.60)
ax.set_xlim(1.6, 8.4)
ax.set_xlabel("Número de clusters (k)", color=TINTA, fontsize=11)
ax.set_ylabel("Coeficiente de silueta promedio", color=TINTA, fontsize=11)
ax.set_title("Coeficiente de silueta por k — referencias de Kaufman y Rousseeuw (1990)", color=TINTA,
             fontsize=12.5, loc="left", pad=12)
fig.text(0.01, 0.01, f"Mayor = clusters más cohesionados y separados. random_state={RANDOM_STATE}, n_init={N_INIT}.",
         fontsize=8.5, color=TINTA_2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(f"{SALIDA_DIR}/paso4_silueta.png", facecolor=FONDO)

res.round(4).to_csv(f"{SALIDA_DIR}/paso4_metricas_k.csv")
print("\nGráficos: diagnostico/paso4_codo.png, diagnostico/paso4_silueta.png | Métricas: diagnostico/paso4_metricas_k.csv")

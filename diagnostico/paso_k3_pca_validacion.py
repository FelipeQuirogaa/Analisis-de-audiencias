"""
K = 3 definitivo: gráfico PCA, silueta por cluster y perfil numérico frente a la media general.
Mismo modelo de los Pasos 4-8 (9 variables, StandardScaler, k-means++, n_init=10, random_state=42).
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples

V = ["horas_diarias_redes", "num_redes_usadas", "gasto_mensual_contenido_cop", "ug_entretenimiento",
     "ug_informacion", "ug_identidad", "ug_interaccion_social", "ug_evasion", "ug_pasar_tiempo"]
df = pd.read_excel("data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx", "Base de datos")
X = StandardScaler().fit_transform(df[V])
km = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=42).fit(X)
lab = km.labels_
prev = pd.read_csv("diagnostico/paso5_asignacion_k3.csv")
assert (prev["cluster"].values == lab).all()

s = silhouette_samples(X, lab)
print("Silueta global:", round(silhouette_score(X, lab), 4))
print(pd.DataFrame({"n": np.bincount(lab), "silueta_media": pd.Series(s).groupby(lab).mean().round(4),
                    "%_negativa": (pd.Series(s < 0).groupby(lab).mean() * 100).round(1)}).to_string())
print("Inercia:", round(km.inertia_, 2))

prof = df.groupby(lab)[V].mean().T
prof["Media general"] = df[V].mean()
for k in range(3):
    prof[f"dif%_{k}"] = ((prof[k] / prof["Media general"] - 1) * 100).round(1)
print(prof.round(2).to_string())

pca = PCA(n_components=2, random_state=42)
Z = pca.fit_transform(X)
ev = pca.explained_variance_ratio_
print("PCA:", (ev * 100).round(2), "acumulada", round(ev.sum() * 100, 2))

NOMBRES = ["C0 · Maratonistas móviles que buscan desconexión",
           "C1 · Espectadores acompañados en TV (memoria y contexto)",
           "C2 · Suscriptores selectivos (calidad que justifique su pago)"]
COL = ["#2a78d6", "#eb6834", "#1baf7a"]
MAR = ["o", "s", "^"]
TINTA, TINTA2, GRILLA, FONDO = "#1f1f1e", "#5c5c5a", "#e4e4e2", "#fcfcfb"
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
fig.patch.set_facecolor(FONDO); ax.set_facecolor(FONDO)
for c in range(3):
    m = lab == c
    ax.scatter(Z[m, 0], Z[m, 1], s=22, marker=MAR[c], c=COL[c], alpha=.6, edgecolors=FONDO, linewidths=.5,
               label=f"{NOMBRES[c]}  (n = {m.sum()}, {m.mean()*100:.1f}%)")
cp = pca.transform(km.cluster_centers_)
for c, (x, y) in enumerate(cp):
    ax.scatter(x, y, s=200, marker=MAR[c], c=COL[c], edgecolors=TINTA, linewidths=1.6, zorder=5)
    ax.annotate(f"C{c}", (x, y), xytext=(9, 7), textcoords="offset points", fontsize=11, fontweight="bold", color=TINTA, zorder=6)
ax.set_xlabel(f"Componente principal 1 — {ev[0]*100:.1f}% de la varianza", color=TINTA, fontsize=11)
ax.set_ylabel(f"Componente principal 2 — {ev[1]*100:.1f}% de la varianza", color=TINTA, fontsize=11)
ax.set_title(f"K-means (k = 3) proyectado en PCA — varianza acumulada PC1+PC2: {ev.sum()*100:.1f}%", color=TINTA, fontsize=12.5, loc="left", pad=12)
ax.grid(color=GRILLA, linewidth=.8); ax.set_axisbelow(True)
for sp in ["top", "right"]: ax.spines[sp].set_visible(False)
for sp in ["left", "bottom"]: ax.spines[sp].set_color(GRILLA)
ax.tick_params(colors=TINTA2)
leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1, frameon=False, fontsize=9.5, markerscale=1.6)
fig.text(0.01, 0.01, "9 variables estandarizadas (StandardScaler). Marcadores grandes = centroides. random_state = 42, n_init = 10.", fontsize=8.5, color=TINTA2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("diagnostico/paso_k3_pca.png", facecolor=FONDO)

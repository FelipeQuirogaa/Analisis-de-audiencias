"""
Fase 5 — Perfilar y enriquecer los clusters con K = 3.
Mismo modelo que el Paso 4 (9 variables, StandardScaler, k-means++, n_init=10, random_state=42).
Las variables demográficas y categóricas se usan SOLO para describir (no entran al modelo).

Uso:
    python diagnostico/paso5_perfilado_k3.py [ruta_al_xlsx]
"""
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_colwidth", 60)

RUTA = sys.argv[1] if len(sys.argv) > 1 else \
    "data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx"
K, RANDOM_STATE, N_INIT = 3, 42, 10
VARIABLES = [
    "horas_diarias_redes", "num_redes_usadas", "gasto_mensual_contenido_cop",
    "ug_entretenimiento", "ug_informacion", "ug_identidad",
    "ug_interaccion_social", "ug_evasion", "ug_pasar_tiempo",
]


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


df = pd.read_excel(RUTA, "Base de datos")
X_std = StandardScaler().fit_transform(df[VARIABLES])
km = KMeans(n_clusters=K, init="k-means++", n_init=N_INIT, random_state=RANDOM_STATE).fit(X_std)
df["cluster"] = km.labels_
df[["id", "cluster"]].to_csv("diagnostico/paso5_asignacion_k3.csv", index=False)

titulo("TAMAÑOS")
print(df["cluster"].value_counts().sort_index().to_frame("n").assign(pct=lambda t: (t.n / len(df) * 100).round(1)).to_string())

# ---------------------------------------------------------------- Numéricas (base + descriptoras)
titulo("MEDIAS NUMÉRICAS POR CLUSTER (base del modelo + numéricas descriptoras)")
num = VARIABLES + ["horas_video_dia", "edad", "estrato", "comparacion_social", "nivel_fomo"]
med = df.groupby("cluster")[num].mean().T
med["Total"] = df[num].mean()
print(med.round(2).to_string())
print("\n% con gasto = 0:", (df.groupby("cluster")["gasto_mensual_contenido_cop"].apply(lambda s: (s == 0).mean()) * 100).round(1).to_dict())
print("Mediana de edad:", df.groupby("cluster")["edad"].median().to_dict())

# ---------------------------------------------------------------- Categóricas: % por cluster e índice vs. total
CATS = ["grupo_etario", "genero", "estrato", "nivel_educativo", "region",
        "dispositivo_principal", "franja_horaria_pico", "red_social_principal",
        "plataforma_video_principal", "categoria_contenido_preferida", "formato_preferido",
        "disposicion_pago", "sensibilidad_precio",
        "contexto_visionado", "via_llegada", "patron_consumo", "binge_watching",
        "relacion_tv_abierta", "rol_diseno_digital",
        "motivo_primario", "necesidad_base", "gratificacion_buscada",
        "tension_gratificacion", "riesgo_gratif_desplazada",
        "genera_contenido", "relacion_parasocial", "pertenencia_comunidades"]


def cramers_v(a, b):
    ct = pd.crosstab(a, b).values
    n = ct.sum()
    exp = ct.sum(1, keepdims=True) @ ct.sum(0, keepdims=True) / n
    chi2 = ((ct - exp) ** 2 / exp).sum()
    return np.sqrt(chi2 / (n * (min(ct.shape) - 1))), chi2


titulo("FUERZA DE ASOCIACIÓN DE CADA DESCRIPTOR CON EL CLUSTER (V de Cramer)")
v = pd.DataFrame([(c, *cramers_v(df[c], df["cluster"])) for c in CATS],
                 columns=["variable", "V_cramer", "chi2"]).sort_values("V_cramer", ascending=False)
print(v.round(3).to_string(index=False))

titulo("DISTRIBUCIÓN (%) POR CLUSTER E ÍNDICE (100 = igual al total)")
for c in CATS:
    pct = pd.crosstab(df[c], df["cluster"], normalize="columns") * 100
    tot = df[c].value_counts(normalize=True) * 100
    t = pct.round(1)
    t["Total"] = tot.round(1)
    for k in range(K):
        t[f"idx{k}"] = (pct[k] / tot * 100).round(0)
    print(f"\n--- {c}")
    print(t.sort_values("Total", ascending=False).to_string())

# ---------------------------------------------------------------- Cruces específicos para "La Primera Vez"
titulo("CRUCES ESPECÍFICOS PARA LA PRIMERA VEZ")
m = df.copy()
m["joven_18_24"] = m["grupo_etario"] == "18-24"
m["adulto_35_54"] = m["grupo_etario"].isin(["35-44", "45-54"])
m["mujer"] = m["genero"] == "Femenino"
m["ve_en_familia_pareja"] = m["contexto_visionado"].isin(["En familia (TV/pantalla compartida)", "En pareja"])
m["ve_solo"] = m["contexto_visionado"].str.startswith("Solo/a")
m["llega_por_algoritmo"] = m["via_llegada"].str.startswith("Algoritmo")
m["llega_por_recom_social"] = m["via_llegada"].isin(["Recomendación de amigos/familia", "Redes sociales (publicación o historia)"])
m["solo_y_algoritmo"] = m["ve_solo"] & m["llega_por_algoritmo"]
m["netflix"] = m["plataforma_video_principal"] == "Netflix"
m["smart_tv"] = m["dispositivo_principal"] == "Smart TV"
m["riesgo_desplaz_alto"] = m["riesgo_gratif_desplazada"].str.startswith("Alto")
m["frustracion"] = m["tension_gratificacion"].str.startswith("Frustración")
m["maraton_frec"] = m["binge_watching"].isin(["Siempre que puede", "Frecuente (varias veces por semana)"])
ind = ["joven_18_24", "adulto_35_54", "mujer", "ve_solo", "ve_en_familia_pareja", "llega_por_algoritmo",
       "llega_por_recom_social", "solo_y_algoritmo", "netflix", "smart_tv", "maraton_frec",
       "riesgo_desplaz_alto", "frustracion"]
t = (m.groupby("cluster")[ind].mean().T * 100).round(1)
t["Total"] = (m[ind].mean() * 100).round(1)
print(t.to_string())

titulo("GÉNERO x GRUPO ETARIO DENTRO DE CADA CLUSTER (%)")
for k in range(K):
    print(f"\n--- cluster {k}")
    print((pd.crosstab(df.loc[df.cluster == k, "grupo_etario"], df.loc[df.cluster == k, "genero"],
                       normalize="all") * 100).round(1).to_string())

titulo("PROXIES DE ABANDONO (toda la base): tensión de gratificación según 'solo + algoritmo'")
print((pd.crosstab(m["solo_y_algoritmo"], m["tension_gratificacion"], normalize="index") * 100).round(1).to_string())
print((pd.crosstab(m["solo_y_algoritmo"], m["riesgo_gratif_desplazada"], normalize="index") * 100).round(1).to_string())

titulo("SUBCONJUNTOS QUE SE PARECEN A LOS USER PERSONAS, Y EN QUÉ CLUSTER CAEN")
daniel = (df["edad"].between(18, 24))
laura = (df["genero"] == "Femenino") & df["edad"].between(40, 55)
for nombre, mask in [("Tipo Daniel: 18-24 años", daniel), ("Tipo Laura: mujer 40-55", laura),
                     ("Tipo Laura + TV/familia/pareja", laura & m["ve_en_familia_pareja"])]:
    s = df.loc[mask, "cluster"].value_counts(normalize=True).sort_index() * 100
    print(f"{nombre:35s} n={mask.sum():4d}  % por cluster: {s.round(1).to_dict()}")
print("\nPeso de cada 'tipo' dentro de cada cluster (%):")
print(pd.DataFrame({"tipo_Daniel_18_24": daniel.groupby(df.cluster).mean() * 100,
                    "tipo_Laura_mujer_40_55": laura.groupby(df.cluster).mean() * 100}).round(1).to_string())

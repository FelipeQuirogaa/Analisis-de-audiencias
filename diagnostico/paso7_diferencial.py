"""
Paso 7 — Análisis diferencial de los 3 clusters (K = 3).
Para cada variable: categoría más distintiva de cada cluster frente a los OTROS DOS
(lift = % en el cluster / % máximo en los otros dos clusters), más indicadores de
consumo social vs. individual y de riesgo de abandono (proxies).
Mismo modelo que Pasos 4-6.

Uso:
    python diagnostico/paso7_diferencial.py [ruta_al_xlsx]
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
VARIABLES = [
    "horas_diarias_redes", "num_redes_usadas", "gasto_mensual_contenido_cop",
    "ug_entretenimiento", "ug_informacion", "ug_identidad",
    "ug_interaccion_social", "ug_evasion", "ug_pasar_tiempo",
]
MIN_PCT = 10.0   # una categoría solo es "dominante" si pesa al menos 10% dentro del cluster


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


df = pd.read_excel(RUTA, "Base de datos")
df["cluster"] = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=42).fit_predict(
    StandardScaler().fit_transform(df[VARIABLES]))
prev = pd.read_csv("diagnostico/paso5_asignacion_k3.csv")
assert (df[["id", "cluster"]].merge(prev, on="id", suffixes=("", "_p5")).eval("cluster == cluster_p5").all())

df["edad_rango"] = pd.cut(df["edad"], [17, 24, 39, 55, 200], labels=["18-24", "25-39", "40-55", "56+"]).astype(str)

DIMENSIONES = {
    "Motivación": ["motivo_primario"],
    "Necesidades y gratificaciones": ["necesidad_base", "gratificacion_buscada", "tension_gratificacion"],
    "Comportamiento y hábitos": ["contexto_visionado", "patron_consumo", "binge_watching", "franja_horaria_pico",
                                 "genera_contenido", "pertenencia_comunidades", "relacion_parasocial"],
    "Demografía y geografía": ["edad_rango", "genero", "nivel_educativo", "estrato", "region"],
    "Plataforma y vía de entrada": ["plataforma_video_principal", "dispositivo_principal", "via_llegada",
                                    "relacion_tv_abierta", "rol_diseno_digital", "disposicion_pago"],
}

# ---------------------------------------------------------------- 1. Categoría más distintiva por cluster
titulo("CATEGORÍAS MÁS DISTINTIVAS DE CADA CLUSTER FRENTE A LOS OTROS DOS (lift = % cluster / máx % otros)")
filas = []
for dim, cols in DIMENSIONES.items():
    for c in cols:
        pct = pd.crosstab(df[c], df["cluster"], normalize="columns") * 100
        for k in (0, 1, 2):
            otros = pct.drop(columns=k).max(axis=1)
            lift = pct[k] / otros.replace(0, np.nan)
            cand = lift[pct[k] >= MIN_PCT].dropna().sort_values(ascending=False)
            for cat in cand.index[:2]:
                filas.append({"dimension": dim, "variable": c, "cluster": k, "categoria": cat,
                              "%cluster": pct.loc[cat, k], "%otros_max": otros[cat], "lift": cand[cat]})
dist = pd.DataFrame(filas)
for k in (0, 1, 2):
    print(f"\n######## Cluster {k} — top 15 rasgos exclusivos (lift > 1 = más frecuente que en CUALQUIERA de los otros dos)")
    print(dist[(dist.cluster == k) & (dist.lift > 1)].sort_values("lift", ascending=False)
          .head(15).round(2).to_string(index=False))
dist.round(3).to_csv("diagnostico/paso7_rasgos_distintivos.csv", index=False)

# ---------------------------------------------------------------- 2. Numéricas: medias y posición relativa
titulo("NUMÉRICAS: MEDIA POR CLUSTER (en negrita conceptual: el máximo de cada fila)")
num = VARIABLES + ["horas_video_dia", "edad", "estrato", "comparacion_social", "nivel_fomo"]
med = df.groupby("cluster")[num].mean().T.round(2)
med["cluster_max"] = med.idxmax(axis=1)
med["cluster_min"] = med[[0, 1, 2]].idxmin(axis=1)
print(med.to_string())

# ---------------------------------------------------------------- 3. Consumo social vs. individual
titulo("CONSUMO SOCIAL vs. INDIVIDUAL (% por cluster)")
cv = df["contexto_visionado"]
ind = pd.DataFrame({
    "ve_solo/a": cv.str.startswith("Solo/a"),
    "ve_acompañado/a (familia/pareja/amigos)": cv.isin(["En familia (TV/pantalla compartida)", "En pareja", "Con amigos"]),
    "ve_en_familia_TV": cv == "En familia (TV/pantalla compartida)",
    "ve_con_amigos": cv == "Con amigos",
    "patron_consumo_social(ver juntos y comentar)": df["patron_consumo"].str.startswith("Consumo social"),
    "gratif_tener_de_que_hablar/compartir": df["gratificacion_buscada"].isin(["Tener de qué hablar", "Compartir experiencias"]),
    "creador_activo_u_ocasional": df["genera_contenido"].str.startswith("Creador"),
    "reactivo(comenta/comparte)": df["genera_contenido"].str.startswith("Reactivo"),
    "consumidor_pasivo": df["genera_contenido"].str.startswith("Consumidor pasivo"),
    "comunidad_activa": df["pertenencia_comunidades"].str.startswith("Activa"),
    "sin_comunidades": df["pertenencia_comunidades"].str.startswith("Ninguna"),
    "parasocial_fuerte": df["relacion_parasocial"].str.startswith("Fuerte"),
    "llega_por_recom_amigos/familia": df["via_llegada"] == "Recomendación de amigos/familia",
    "llega_por_redes_sociales": df["via_llegada"].str.startswith("Redes sociales"),
})
t = (ind.groupby(df["cluster"]).mean().T * 100).round(1)
t["Total"] = (ind.mean() * 100).round(1)
print(t.to_string())

# ---------------------------------------------------------------- 4. Riesgo de abandono vs. fidelización (proxies)
titulo("RIESGO DE ABANDONO vs. FIDELIZACIÓN — PROXIES (% por cluster)")
tg = df["tension_gratificacion"]
risk = pd.DataFrame({
    "indiferencia": tg.str.startswith("Indiferencia"),
    "frustracion_alta": tg.str.startswith("Frustración alta"),
    "frustracion_total": tg.str.startswith("Frustración"),
    "descubrimiento_positivo": tg.str.startswith("Obtiene más"),
    "satisfaccion_plena": tg.str.startswith("Satisfacción plena"),
    "riesgo_desplazamiento_alto": df["riesgo_gratif_desplazada"].str.startswith("Alto"),
    "solo+algoritmo": cv.str.startswith("Solo/a") & df["via_llegada"].str.startswith("Algoritmo"),
    "zapping_entre_plataformas": df["patron_consumo"].str.startswith("Zapping"),
    "fragmentado(pausa y retoma)": df["patron_consumo"].str.startswith("Fragmentado"),
    "de_fondo": df["patron_consumo"].str.startswith("De fondo"),
    "maraton_frecuente": df["binge_watching"].isin(["Siempre que puede", "Frecuente (varias veces por semana)"]),
    "un_episodio_por_sesion": df["patron_consumo"].str.startswith("Un episodio"),
    "diseño_determinante(elige/abandona por diseño)": df["rol_diseno_digital"].str.startswith("Determinante"),
    "sensibilidad_precio_alta": df["sensibilidad_precio"].str.startswith("Alta"),
})
t = (risk.groupby(df["cluster"]).mean().T * 100).round(1)
t["Total"] = (risk.mean() * 100).round(1)
print(t.to_string())

print("\nÍndice compuesto de vulnerabilidad (promedio simple de: indiferencia, frustración total, riesgo desplazamiento alto, zapping):")
comp = risk[["indiferencia", "frustracion_total", "riesgo_desplazamiento_alto", "zapping_entre_plataformas"]].mean(axis=1)
print((comp.groupby(df["cluster"]).mean() * 100).round(1).to_string())
print("Índice compuesto de fidelización (promedio simple de: satisfacción plena, descubrimiento positivo, riesgo desplazamiento BAJO):")
fid = pd.concat([risk[["satisfaccion_plena", "descubrimiento_positivo"]],
                 df["riesgo_gratif_desplazada"].str.startswith("Bajo").rename("riesgo_bajo")], axis=1).mean(axis=1)
print((fid.groupby(df["cluster"]).mean() * 100).round(1).to_string())

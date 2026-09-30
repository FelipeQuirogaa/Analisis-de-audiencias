"""
Paso 6 — Enriquecimiento de los clusters (K = 3, foco en Clusters 0 y 1) con variables categóricas
que NO entraron al K-means, y cruces de retención/abandono.
Mismo modelo que Pasos 4-5 (9 variables, StandardScaler, k-means++, n_init=10, random_state=42).

Uso:
    python diagnostico/paso6_cruces_categoricas.py [ruta_al_xlsx]
"""
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_colwidth", 70)

RUTA = sys.argv[1] if len(sys.argv) > 1 else \
    "data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx"
VARIABLES = [
    "horas_diarias_redes", "num_redes_usadas", "gasto_mensual_contenido_cop",
    "ug_entretenimiento", "ug_informacion", "ug_identidad",
    "ug_interaccion_social", "ug_evasion", "ug_pasar_tiempo",
]


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


df = pd.read_excel(RUTA, "Base de datos")
df["cluster"] = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=42).fit_predict(
    StandardScaler().fit_transform(df[VARIABLES]))

# Verificación: idéntico a la asignación guardada en el Paso 5
prev = pd.read_csv("diagnostico/paso5_asignacion_k3.csv")
assert (df[["id", "cluster"]].merge(prev, on="id", suffixes=("", "_p5"))
        .eval("cluster == cluster_p5").all()), "La asignación no coincide con el Paso 5"

# ---------------------------------------------------------------- Recodificaciones (solo agrupan categorías existentes)
df["edad_rango"] = pd.cut(df["edad"], [17, 24, 39, 55, 200], labels=["18-24", "25-39", "40-55", "56+"])
df["region_bogota"] = np.where(df["region"] == "Bogotá", "Bogotá", "Otras regiones/ciudades")
df["estrato_grupo"] = pd.cut(df["estrato"], [0, 2, 3, 6], labels=["Bajo (1-2)", "Medio (3)", "Alto (4-6)"])
df["modalidad"] = df["contexto_visionado"].map({
    "Solo/a en smartphone": "Solo/a", "Solo/a en computador": "Solo/a",
    "En familia (TV/pantalla compartida)": "Acompañado/a", "En pareja": "Acompañado/a",
    "Con amigos": "Acompañado/a", "En transporte/desplazamiento": "En desplazamiento"})
df["descubrimiento"] = df["via_llegada"].map({
    "Algoritmo de la plataforma (recomendación automática)": "Algoritmo/tendencias",
    "Tendencias/trending": "Algoritmo/tendencias",
    "Recomendación de amigos/familia": "Recomendación social (amigos/familia/redes)",
    "Redes sociales (publicación o historia)": "Recomendación social (amigos/familia/redes)",
    "Búsqueda activa (barra de búsqueda)": "Búsqueda activa",
    "Publicidad digital": "Publicidad/medios", "Mención en medios/prensa": "Publicidad/medios"})
df["maraton"] = df["binge_watching"].map({
    "Siempre que puede": "Alto (siempre/frecuente)", "Frecuente (varias veces por semana)": "Alto (siempre/frecuente)",
    "Ocasional (fines de semana)": "Ocasional (fines de semana)",
    "Rara vez": "Bajo (rara vez/nunca)", "Nunca": "Bajo (rara vez/nunca)"})
df["resultado_gratif"] = df["tension_gratificacion"].map({
    "Obtiene más de lo que busca (descubrimiento positivo)": "Descubrimiento positivo",
    "Satisfacción plena (coincide lo buscado y lo obtenido)": "Satisfacción plena",
    "Satisfacción parcial (encuentra algo pero no exactamente)": "Satisfacción parcial",
    "Indiferencia (consume sin expectativa clara)": "Indiferencia",
    "Frustración leve (demasiado contenido, difícil elegir)": "Frustración",
    "Frustración alta (no encuentra lo que busca)": "Frustración"})
assert df[["modalidad", "descubrimiento", "maraton", "resultado_gratif"]].notna().all().all()

VARS = {
    "Motivaciones y necesidades": ["motivo_primario", "necesidad_base", "gratificacion_buscada",
                                   "tension_gratificacion", "resultado_gratif"],
    "Sociodemográfico": ["genero", "edad_rango", "grupo_etario", "nivel_educativo", "estrato_grupo",
                         "region_bogota", "region"],
    "Consumo y plataforma": ["plataforma_video_principal", "dispositivo_principal", "contexto_visionado",
                             "modalidad", "binge_watching", "maraton", "patron_consumo",
                             "via_llegada", "descubrimiento"],
}

titulo("TAMAÑOS")
print(df["cluster"].value_counts().sort_index().to_string())

titulo("DISTRIBUCIÓN (%) POR CLUSTER, TOTAL E ÍNDICE vs. TOTAL (100 = promedio)")
for bloque, cols in VARS.items():
    print(f"\n######## {bloque}")
    for c in cols:
        pct = pd.crosstab(df[c], df["cluster"], normalize="columns") * 100
        tot = df[c].value_counts(normalize=True) * 100
        t = pct.round(1)
        t["Total"] = tot.round(1)
        for k in (0, 1, 2):
            t[f"idx{k}"] = (pct[k] / tot * 100).round(0)
        print(f"\n--- {c}")
        print(t.sort_values(0, ascending=False).to_string())

titulo("TOP-3 CATEGORÍAS POR CLUSTER (resumen)")
for c in sum(VARS.values(), []):
    for k in (0, 1, 2):
        vc = df.loc[df.cluster == k, c].value_counts(normalize=True).head(3) * 100
        print(f"{c:28s} C{k}: " + " | ".join(f"{i} {v:.1f}%" for i, v in vc.items()))

# ---------------------------------------------------------------- Cruces de retención / abandono
titulo("CRUCES: MODALIDAD x DESCUBRIMIENTO -> RESULTADO DE LA GRATIFICACIÓN (proxy de retención)")
df["combo"] = df["modalidad"] + " + " + df["descubrimiento"]
out = ["Descubrimiento positivo", "Satisfacción plena", "Satisfacción parcial", "Indiferencia", "Frustración"]


def tabla_resultados(sub, grupo):
    t = (pd.crosstab(sub[grupo], sub["resultado_gratif"], normalize="index") * 100)[out].round(1)
    t.insert(0, "n", sub[grupo].value_counts())
    t["positivo(desc+plena)"] = t["Descubrimiento positivo"] + t["Satisfacción plena"]
    t["riesgo_desplaz_alto"] = (sub.groupby(grupo)["riesgo_gratif_desplazada"]
                                .apply(lambda s: s.str.startswith("Alto").mean() * 100)).round(1)
    t["maraton_alto"] = (sub.groupby(grupo)["maraton"]
                         .apply(lambda s: (s == "Alto (siempre/frecuente)").mean() * 100)).round(1)
    return t.sort_values("n", ascending=False)


print("\nToda la base:")
print(tabla_resultados(df, "combo").to_string())
for k in (0, 1):
    print(f"\nCluster {k}:")
    print(tabla_resultados(df[df.cluster == k], "combo").to_string())

titulo("COMBINACIONES CLAVE DEFINIDAS A PARTIR DEL ESTUDIO (por cluster)")
m = df
combos = {
    "Solo/a + Algoritmo (patrón de abandono E4/E9)":
        (m.modalidad == "Solo/a") & (m.descubrimiento == "Algoritmo/tendencias"),
    "Solo/a + Recomendación social (patrón E11/E7)":
        (m.modalidad == "Solo/a") & (m.descubrimiento == "Recomendación social (amigos/familia/redes)"),
    "Acompañado/a + Recomendación social (patrón E14)":
        (m.modalidad == "Acompañado/a") & (m.descubrimiento == "Recomendación social (amigos/familia/redes)"),
    "Familia en TV/pantalla compartida + Recom. amigos/familia":
        (m.contexto_visionado == "En familia (TV/pantalla compartida)") & (m.via_llegada == "Recomendación de amigos/familia"),
    "Acompañado/a + Algoritmo (patrón E13)":
        (m.modalidad == "Acompañado/a") & (m.descubrimiento == "Algoritmo/tendencias"),
    "Netflix + Solo/a en smartphone":
        (m.plataforma_video_principal == "Netflix") & (m.contexto_visionado == "Solo/a en smartphone"),
    "Motivo Evasión/Hábito + Solo/a":
        m.motivo_primario.isin(["Evasión y escape", "Hábito y pasatiempo"]) & (m.modalidad == "Solo/a"),
    "Maratón alto + Algoritmo":
        (m.maraton == "Alto (siempre/frecuente)") & (m.descubrimiento == "Algoritmo/tendencias"),
    "Mujer 40-55 + Acompañado/a":
        (m.genero == "Femenino") & (m.edad_rango == "40-55") & (m.modalidad == "Acompañado/a"),
    "Hombre 18-24 + Solo/a + Algoritmo":
        (m.genero == "Masculino") & (m.edad_rango == "18-24") & (m.modalidad == "Solo/a") & (m.descubrimiento == "Algoritmo/tendencias"),
}
filas = []
for nombre, mask in combos.items():
    for k in (0, 1, "Total"):
        sub = m[mask] if k == "Total" else m[mask & (m.cluster == k)]
        base = len(m) if k == "Total" else (m.cluster == k).sum()
        if len(sub) == 0:
            continue
        r = sub["resultado_gratif"].value_counts(normalize=True) * 100
        filas.append({
            "combinación": nombre, "cluster": k, "n": len(sub), "%_del_cluster": len(sub) / base * 100,
            "%indiferencia": r.get("Indiferencia", 0), "%frustración": r.get("Frustración", 0),
            "%positivo": r.get("Descubrimiento positivo", 0) + r.get("Satisfacción plena", 0),
            "%riesgo_desplaz_alto": sub["riesgo_gratif_desplazada"].str.startswith("Alto").mean() * 100,
        })
print(pd.DataFrame(filas).round(1).to_string(index=False))

titulo("GÉNERO: ¿CAMBIA ALGO DENTRO DE CADA CLUSTER? (para la brecha de género)")
for k in (0, 1):
    sub = df[df.cluster == k]
    print(f"\n--- Cluster {k}: % por género")
    for c in ["plataforma_video_principal", "modalidad", "descubrimiento", "resultado_gratif", "maraton"]:
        t = (pd.crosstab(sub[c], sub["genero"], normalize="columns") * 100).round(1)
        print(t.drop(columns=[x for x in t.columns if x == "Otro"]).to_string(), "\n")

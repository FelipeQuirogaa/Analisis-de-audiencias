"""
Diagnóstico y auditoría de la base de audiencias digitales (Segundo Parcial).
NO ejecuta K-means ni modifica / elimina registros. Solo lee y describe.

Uso:
    python diagnostico/diagnostico_base.py [ruta_al_xlsx]
"""
import sys
import re
import pandas as pd
import numpy as np

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_colwidth", 90)
pd.set_option("display.max_rows", 500)

RUTA = sys.argv[1] if len(sys.argv) > 1 else \
    "data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx"


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


# ---------------------------------------------------------------- 0. Carga
xls = pd.ExcelFile(RUTA)
titulo("0. HOJAS DEL ARCHIVO")
for h in xls.sheet_names:
    print(f"- {h}: {pd.read_excel(xls, h, header=None).shape}")

df = pd.read_excel(xls, "Base de datos")
dic = pd.read_excel(xls, "Diccionario de variables")
print(f"\nBase de datos: {df.shape[0]} filas x {df.shape[1]} columnas")

# ---------------------------------------------------------------- 1. Variables vs. diccionario
titulo("1/8. VARIABLES: TIPO REAL (pandas) vs. DICCIONARIO")
dic = dic.rename(columns=lambda c: str(c).strip())
dic_idx = dic.set_index("Variable")
filas = []
for c in df.columns:
    real = str(df[c].dtype)
    clase = "Numérica" if pd.api.types.is_numeric_dtype(df[c]) else "Categórica/Texto"
    filas.append({
        "variable": c,
        "dtype_pandas": real,
        "clase_real": clase,
        "tipo_diccionario": dic_idx.loc[c, "Tipo"] if c in dic_idx.index else "NO ESTÁ EN DICCIONARIO",
        "grupo_diccionario": dic_idx.loc[c, "Grupo"] if c in dic_idx.index else "",
        "descripcion_diccionario": dic_idx.loc[c, "Descripción"] if c in dic_idx.index else "",
        "n_valores_unicos": df[c].nunique(dropna=True),
    })
tabla_vars = pd.DataFrame(filas)
print(tabla_vars.to_string(index=False))

print("\nVariables en diccionario pero NO en la base:",
      sorted(set(dic["Variable"].dropna()) - set(df.columns)) or "ninguna")
print("Variables en la base pero NO en diccionario:",
      sorted(set(df.columns) - set(dic["Variable"].dropna())) or "ninguna")
print("Columnas con espacios al inicio/fin en el nombre:",
      [c for c in df.columns if c != c.strip()] or "ninguna")

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = [c for c in df.columns if c not in num_cols]

titulo("2. CLASIFICACIÓN NUMÉRICA / CATEGÓRICA (según dtype real)")
print(f"Numéricas ({len(num_cols)}): {num_cols}")
print(f"Categóricas/texto ({len(cat_cols)}): {cat_cols}")

# ---------------------------------------------------------------- 3. Descriptivos numéricos
titulo("3. DESCRIPTIVOS DE VARIABLES NUMÉRICAS (desv. estándar muestral, n-1)")
desc = pd.DataFrame({
    "n_validos": df[num_cols].count(),
    "media": df[num_cols].mean(),
    "mediana": df[num_cols].median(),
    "desv_std": df[num_cols].std(ddof=1),
    "minimo": df[num_cols].min(),
    "maximo": df[num_cols].max(),
    "rango": df[num_cols].max() - df[num_cols].min(),
    "faltantes": df[num_cols].isna().sum(),
    "CV": df[num_cols].std(ddof=1) / df[num_cols].mean(),
    "asimetria": df[num_cols].skew(),
    "n_unicos": df[num_cols].nunique(),
})
print(desc.round(3).to_string())

# ---------------------------------------------------------------- 4. Frecuencias categóricas
titulo("4. FRECUENCIAS DE VARIABLES CATEGÓRICAS (se excluye 'id')")
for c in cat_cols:
    if c == "id":
        continue
    vc = df[c].value_counts(dropna=False)
    t = pd.DataFrame({"frecuencia": vc, "porcentaje": (vc / len(df) * 100).round(1)})
    print(f"\n--- {c}  | categorías: {df[c].nunique()} | faltantes: {df[c].isna().sum()}")
    print(t.to_string())

# ---------------------------------------------------------------- 5. Calidad de datos
titulo("5a. VALORES FALTANTES POR VARIABLE")
na = df.isna().sum()
print(na[na > 0].to_string() if na.sum() else "No hay valores faltantes (NaN) en ninguna variable.")
# Faltantes "disfrazados"
disfrazados = {}
for c in cat_cols:
    s = df[c].astype(str).str.strip().str.lower()
    m = s.isin(["", "nan", "na", "n/a", "none", "null", "-", "?", "ns/nr", "no sabe"])
    if m.any():
        disfrazados[c] = int(m.sum())
print("Faltantes codificados como texto ('', 'NA', 'N/A', '-', etc.):", disfrazados or "ninguno")

titulo("5b. DUPLICADOS")
print("Filas completamente duplicadas:", int(df.duplicated().sum()))
print("IDs duplicados:", int(df["id"].duplicated().sum()))
print("Filas duplicadas ignorando 'id':", int(df.drop(columns="id").duplicated().sum()))
patron_id = df["id"].astype(str).str.fullmatch(r"AUD-\d{4}")
print("IDs que no siguen el patrón AUD-####:", int((~patron_id).sum()))
nums = df["id"].str.extract(r"(\d+)")[0].astype(int)
faltan = sorted(set(range(1, 1001)) - set(nums))
print("Consecutivos faltantes entre AUD-0001 y AUD-1000:", faltan[:20] if faltan else "ninguno")
print("Duplicados sobre las 15 numéricas (posibles perfiles idénticos para K-means):",
      int(df[num_cols].duplicated().sum()))

titulo("5c. RANGOS: VALORES FUERA DEL RANGO DECLARADO EN EL DICCIONARIO")
rangos = {
    "edad": (18, 75), "estrato": (1, 6),
    "horas_diarias_redes": (0.3, 9.0), "num_redes_usadas": (1, 9),
    "gasto_mensual_contenido_cop": (0, 132500), "horas_video_dia": (0.2, 6.5),
    "comparacion_social": (1, 5), "nivel_fomo": (1, 5),
}
for c in [x for x in num_cols if x.startswith("ug_")]:
    rangos[c] = (1, 5)
for c, (lo, hi) in rangos.items():
    fuera = df[(df[c] < lo) | (df[c] > hi)]
    print(f"{c:30s} rango dicc. [{lo}, {hi}]  real [{df[c].min()}, {df[c].max()}]  fuera de rango: {len(fuera)}")
print("\nLikert / estrato con valores no enteros:",
      {c: int((df[c] % 1 != 0).sum()) for c in rangos if c not in
       ("horas_diarias_redes", "horas_video_dia", "gasto_mensual_contenido_cop")})
print("Decimales en horas_diarias_redes:", sorted(df["horas_diarias_redes"].map(lambda v: len(str(v).split(".")[-1])).unique()))

titulo("5d. VALORES ATÍPICOS (regla IQR 1.5) Y CEROS")
for c in num_cols:
    q1, q3 = df[c].quantile([.25, .75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = int(((df[c] < lo) | (df[c] > hi)).sum())
    print(f"{c:30s} Q1={q1:>10.2f} Q3={q3:>10.2f} límites=[{lo:>10.2f}, {hi:>10.2f}]  atípicos={n_out:4d}  ceros={int((df[c]==0).sum())}")

titulo("5e. CONSISTENCIA LÓGICA ENTRE VARIABLES")
# grupo_etario derivado de edad
bins = [17, 24, 34, 44, 54, 64, 200]
labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
esperado = pd.cut(df["edad"], bins=bins, labels=labels).astype(str)
inc = df[esperado != df["grupo_etario"].astype(str)]
print("grupo_etario inconsistente con edad:", len(inc))
if len(inc):
    print(inc[["id", "edad", "grupo_etario"]].head(20).to_string(index=False))
# horas de video > horas en redes (no necesariamente imposible: son medidas distintas)
m = df["horas_video_dia"] > df["horas_diarias_redes"]
print("Registros con horas_video_dia > horas_diarias_redes (no imposible, solo informativo):", int(m.sum()))
# horas totales
print("Registros con horas_redes + horas_video > 16 h:", int((df["horas_diarias_redes"] + df["horas_video_dia"] > 16).sum()))
# gasto vs disposicion / sensibilidad
print("\nGasto mensual por disposicion_pago:")
print(df.groupby("disposicion_pago")["gasto_mensual_contenido_cop"].agg(["count", "mean", "median", lambda s: (s == 0).mean()])
      .rename(columns={"<lambda_0>": "prop_gasto_0"}).round(2).to_string())
print("\nRango de gasto (min-max) por disposicion_pago (¿tramos solapados o casi deterministas?):")
print(df.groupby("disposicion_pago")["gasto_mensual_contenido_cop"].agg(["min", "max"]).to_string())
sens = df["sensibilidad_precio"].str.split().str[0]
print("\nCruce disposicion_pago x sensibilidad_precio:")
print(pd.crosstab(df["disposicion_pago"], sens).to_string())
m1 = (sens == "Baja") & (df["gasto_mensual_contenido_cop"] == 0)
m2 = (sens == "Alta") & (df["disposicion_pago"] == "Alta")
print("Sensibilidad 'Baja (paga sin pensarlo)' con gasto = 0:", int(m1.sum()))
print("Sensibilidad 'Alta (solo gratis)' con disposicion_pago 'Alta':", int(m2.sum()),
      "| gasto mínimo en ese grupo:", df.loc[m2, "gasto_mensual_contenido_cop"].min())
print("\nplataforma_video_principal='Ninguna' x binge_watching:")
print(pd.crosstab(df["plataforma_video_principal"] == "Ninguna", df["binge_watching"]).to_string())
print("\nGasto mensual por sensibilidad_precio:")
print(df.groupby("sensibilidad_precio")["gasto_mensual_contenido_cop"].agg(["count", "mean", "median"]).round(0).to_string())
print("\nplataforma_video_principal = 'Ninguna' vs horas_video_dia:")
print(df.groupby(df["plataforma_video_principal"] == "Ninguna")["horas_video_dia"].describe().round(2).to_string())
# motivo_primario vs ug_* máximo
mapa = {"Entretenimiento": "ug_entretenimiento", "Información": "ug_informacion",
        "Identidad y autoexpresión": "ug_identidad", "Interacción social": "ug_interaccion_social",
        "Evasión y escape": "ug_evasion", "Hábito y pasatiempo": "ug_pasar_tiempo"}
ug = [c for c in num_cols if c.startswith("ug_")]
mx = df[ug].max(axis=1)
coinc = df.apply(lambda r: r[mapa[r["motivo_primario"]]] == mx[r.name] if r["motivo_primario"] in mapa else np.nan, axis=1)
print("\nmotivo_primario categorías no mapeables a ug_*:", sorted(set(df["motivo_primario"].dropna()) - set(mapa)))
print("% registros donde la ug_* del motivo_primario es (empatada) la más alta:", round(coinc.mean() * 100, 1))
print("% registros con empate en el puntaje ug_* máximo:",
      round((df[ug].eq(mx, axis=0).sum(axis=1) > 1).mean() * 100, 1))
print("Media de cada ug_* según motivo_primario:")
print(df.groupby("motivo_primario")[ug].mean().round(2).to_string())

titulo("5f. FORMATO DE TEXTO EN CATEGÓRICAS")
for c in cat_cols:
    s = df[c].dropna().astype(str)
    esp = int((s != s.str.strip()).sum())
    dobles = int(s.str.contains(r"\s{2,}").sum())
    # categorías que colapsan al normalizar mayúsculas/espacios
    norm = s.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    colapsan = s.nunique() - norm.nunique()
    if esp or dobles or colapsan:
        print(f"{c}: espacios extremos={esp}, espacios dobles={dobles}, categorías que colapsan al normalizar={colapsan}")
print("(si no aparece nada arriba, no hay problemas de espacios/mayúsculas)")
print("\nCategorías observadas vs. listadas en el diccionario (solo diferencias):")
for c in cat_cols:
    if c in ("id",) or c not in dic_idx.index:
        continue
    decl = str(dic_idx.loc[c, "Valores / rango"])
    obs = sorted(df[c].dropna().astype(str).unique())
    no_en_dic = [o for o in obs if o not in decl]
    if no_en_dic:
        print(f"  {c}: observadas que no aparecen literalmente en el diccionario -> {no_en_dic}")

titulo("5g. BAJA VARIABILIDAD")
for c in num_cols:
    top = df[c].value_counts(normalize=True).iloc[0]
    print(f"{c:30s} n_unicos={df[c].nunique():4d}  % valor más frecuente={top*100:5.1f}%  CV={df[c].std()/df[c].mean():.3f}")
print()
for c in cat_cols:
    if c == "id":
        continue
    vc = df[c].value_counts(normalize=True)
    if vc.iloc[0] > .6 or vc.iloc[-1] < .01:
        print(f"{c}: categoría dominante '{vc.index[0]}' = {vc.iloc[0]*100:.1f}% | categoría mínima '{vc.index[-1]}' = {vc.iloc[-1]*100:.1f}%")

titulo("5h. ESCALAS (relevante para K-means, que usa distancias)")
print(df[num_cols].agg(["min", "max", "std"]).T.assign(rango=lambda t: t["max"] - t["min"]).to_string())

titulo("5i. CORRELACIONES ENTRE NUMÉRICAS (|r| >= 0.5)")
corr = df[num_cols].corr()
pares = [(a, b, corr.loc[a, b]) for i, a in enumerate(num_cols) for b in num_cols[i + 1:] if abs(corr.loc[a, b]) >= .5]
for a, b, r in sorted(pares, key=lambda x: -abs(x[2])):
    print(f"{a:30s} {b:30s} r = {r:.3f}")
print("\nMatriz completa:")
print(corr.round(2).to_string())

titulo("5j. HOJAS CON ANÁLISIS PREVIO DENTRO DEL ARCHIVO")
ds = pd.read_excel(xls, "Datos+segmento")
print("Datos+segmento:", ds.shape, "| columnas extra respecto a la base:", sorted(set(ds.columns) - set(df.columns)))
print("Columnas de la base que NO están en Datos+segmento:", sorted(set(df.columns) - set(ds.columns)))
comunes = [c for c in ds.columns if c in df.columns]
m = df[comunes].merge(ds[comunes], on="id", suffixes=("_base", "_seg"))
dif = {c: int((m[c + "_base"] != m[c + "_seg"]).sum()) for c in comunes if c != "id"}
print("IDs coincidentes:", len(m), "| celdas diferentes por variable:", {k: v for k, v in dif.items() if v} or "ninguna")
est = pd.read_excel(xls, "Estadística descriptiva", header=None)
print("\nHoja 'Estadística descriptiva' reporta (medias): edad 38.848, horas 3.5052, redes 5.229, gasto 21924.284, max horas 7.8, max gasto 116524")
print("Recalculado en la base actual:",
      {c: round(df[c].mean(), 4) for c in ["edad", "horas_diarias_redes", "num_redes_usadas", "gasto_mensual_contenido_cop"]},
      "| max horas", df["horas_diarias_redes"].max(), "| max gasto", df["gasto_mensual_contenido_cop"].max())

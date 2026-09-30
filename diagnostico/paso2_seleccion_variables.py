"""
Paso 2 — Comprobaciones para la selección de variables de agrupamiento.
NO ejecuta K-means, NO estandariza para modelar, NO elimina variables ni registros.

Uso:
    python diagnostico/paso2_seleccion_variables.py [ruta_al_xlsx]
"""
import sys
import numpy as np
import pandas as pd

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)

RUTA = sys.argv[1] if len(sys.argv) > 1 else \
    "data/Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx"


def titulo(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


df = pd.read_excel(RUTA, "Base de datos")
num_cols = df.select_dtypes(include="number").columns.tolist()

CANDIDATAS = [
    "horas_diarias_redes", "horas_video_dia", "gasto_mensual_contenido_cop", "num_redes_usadas",
    "ug_entretenimiento", "ug_informacion", "ug_identidad",
    "ug_interaccion_social", "ug_evasion", "ug_pasar_tiempo",
]
NO_AGRUPAR = ["genero", "grupo_etario", "edad", "estrato", "nivel_educativo",
              "motivo_primario", "necesidad_base", "gratificacion_buscada"]

# ---------------------------------------------------------------- 1. Existencia
titulo("1. VERIFICACIÓN DE NOMBRES (candidatas y variables a excluir)")
for c in CANDIDATAS + NO_AGRUPAR:
    existe = c in df.columns
    print(f"{c:30s} existe={existe}  dtype={df[c].dtype if existe else '-'}")
print("\nTodas las numéricas de la base:", num_cols)
print("Numéricas que no están en la lista de candidatas:", [c for c in num_cols if c not in CANDIDATAS])

# ---------------------------------------------------------------- 2. Distribución de las candidatas
titulo("2. DISTRIBUCIÓN DE CADA NUMÉRICA (para juzgar capacidad de discriminar)")
filas = []
for c in num_cols:
    s = df[c]
    filas.append({
        "variable": c, "n_unicos": s.nunique(), "media": s.mean(), "DE": s.std(),
        "CV": s.std() / s.mean(), "asimetria": s.skew(),
        "%_valor_modal": s.value_counts(normalize=True).iloc[0] * 100,
        "%_ceros": (s == 0).mean() * 100,
    })
print(pd.DataFrame(filas).set_index("variable").round(3).to_string())

print("\nDistribución (%) de las escalas Likert:")
lik = [c for c in num_cols if c.startswith("ug_")] + ["comparacion_social", "nivel_fomo"]
print(pd.DataFrame({c: df[c].value_counts(normalize=True).sort_index() * 100 for c in lik})
      .reindex([1, 2, 3, 4, 5]).fillna(0).round(1).T.to_string())

# ---------------------------------------------------------------- 3. Correlaciones
titulo("3. CORRELACIONES ENTRE TODAS LAS NUMÉRICAS")
pear = df[num_cols].corr(method="pearson")
spear = df[num_cols].corr(method="spearman")
pares = []
for i, a in enumerate(num_cols):
    for b in num_cols[i + 1:]:
        pares.append((a, b, pear.loc[a, b], spear.loc[a, b]))
pares = pd.DataFrame(pares, columns=["var_1", "var_2", "pearson", "spearman"])
pares["max_abs"] = pares[["pearson", "spearman"]].abs().max(axis=1)
print("Pares con |r| >= 0.30 (Pearson o Spearman), ordenados:")
print(pares[pares["max_abs"] >= .30].sort_values("max_abs", ascending=False).round(3).to_string(index=False))

print("\nMatriz Pearson — solo candidatas:")
print(pear.loc[CANDIDATAS, CANDIDATAS].round(2).to_string())
print("\nMatriz Spearman — solo candidatas:")
print(spear.loc[CANDIDATAS, CANDIDATAS].round(2).to_string())

# ---------------------------------------------------------------- 4. VIF (multicolinealidad)
titulo("4. VIF (factor de inflación de varianza = diagonal de la inversa de la matriz de correlación)")


def vif(cols):
    inv = np.linalg.inv(df[cols].corr().values)
    return pd.Series(np.diag(inv), index=cols).round(2)


print("VIF — las 10 candidatas:")
print(vif(CANDIDATAS).to_string())
print("\nVIF — las 14 numéricas:")
print(vif(num_cols).to_string())
print("\nVIF — candidatas sin horas_video_dia:")
print(vif([c for c in CANDIDATAS if c != "horas_video_dia"]).to_string())

# ---------------------------------------------------------------- 5. Relación con demografía
titulo("5. RELACIÓN DE CADA CANDIDATA CON EDAD Y ESTRATO (Spearman)")
print(spear.loc[CANDIDATAS + ["comparacion_social", "nivel_fomo"], ["edad", "estrato"]].round(3).to_string())

titulo("6. GASTO vs. VARIABLES CATEGÓRICAS DE PAGO (eta² = varianza explicada)")


def eta2(y, g):
    m = y.mean()
    ssb = sum(len(v) * (v.mean() - m) ** 2 for _, v in y.groupby(g))
    return ssb / ((y - m) ** 2).sum()


for g in ["disposicion_pago", "sensibilidad_precio", "estrato", "grupo_etario"]:
    print(f"gasto_mensual_contenido_cop ~ {g:22s} eta² = {eta2(df['gasto_mensual_contenido_cop'], df[g]):.3f}")
for g in ["grupo_etario"]:
    for c in ["horas_diarias_redes", "horas_video_dia", "num_redes_usadas", "nivel_fomo", "comparacion_social"]:
        print(f"{c:27s} ~ {g:22s} eta² = {eta2(df[c], df[g]):.3f}")

titulo("7. RELACIÓN ENTRE HORAS DE REDES Y HORAS DE VIDEO")
r = df[["horas_diarias_redes", "horas_video_dia"]]
print(r.describe().round(2).to_string())
print("Cociente video/redes: mediana =", round((r.horas_video_dia / r.horas_diarias_redes).median(), 3))
print("R² de una recta horas_video ~ horas_redes =", round(r.corr().iloc[0, 1] ** 2, 3))

titulo("8. RELACIÓN ENTRE LAS 6 ug_* Y LAS VARIABLES CATEGÓRICAS MOTIVACIONALES (eta²)")
ug = [c for c in num_cols if c.startswith("ug_")]
tab = pd.DataFrame({g: {c: eta2(df[c], df[g]) for c in ug}
                    for g in ["motivo_primario", "necesidad_base", "gratificacion_buscada"]})
print(tab.round(3).to_string())

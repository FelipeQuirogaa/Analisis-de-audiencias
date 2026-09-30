# Paso 2 — Selección de variables para el agrupamiento (sin K-means)

**Código:** `diagnostico/paso2_seleccion_variables.py` · **Salida cruda:** `diagnostico/salida_paso2.txt`
📊 = dato comprobado en la base · 💡 = recomendación metodológica (la decisión final es del equipo).
No se ejecutó K-means, no se estandarizó y no se eliminó ninguna variable ni registro.

---

## 1. Verificación de nombres 📊
Las 10 variables solicitadas existen con **exactamente** esos nombres: `horas_diarias_redes` (float), `horas_video_dia` (float), `gasto_mensual_contenido_cop` (int), `num_redes_usadas` (int) y las seis `ug_*` (int).
Las 8 variables a excluir (`genero`, `grupo_etario`, `edad`, `estrato`, `nivel_educativo`, `motivo_primario`, `necesidad_base`, `gratificacion_buscada`) también existen.

**Todas las numéricas de la base (14):** las 10 anteriores + `edad`, `estrato`, `comparacion_social`, `nivel_fomo`.

## 2–3. Clasificación y análisis de cada numérica

| Grupo | Variable | Qué representa | Dimensión | Datos clave 📊 | ¿Sirve para diferenciar? 💡 |
|---|---|---|---|---|---|
| A | `horas_diarias_redes` | Horas/día en redes | Intensidad de uso | 67 valores, 0,3–7,8, simétrica | Sí: continua, buena dispersión (CV 0,38) |
| A | `horas_video_dia` | Horas/día de video | Intensidad de consumo audiovisual | 0,2–6,5, asimetría 0,76; **r = 0,73 con horas_redes** | Sí, pero solapa con horas_redes |
| A | `num_redes_usadas` | Nº de redes al mes | Amplitud/diversificación | 1–9, simétrica | Sí: independiente de horas (r = 0,18) |
| A | `gasto_mensual_contenido_cop` | COP/mes en contenido | Monetización | 32,2% ceros, asimetría 1,36, DE 27.381; r ≈ 0 con todas las demás candidatas | Sí, aporta una dimensión única, pero tiene problemas de forma |
| B | `ug_entretenimiento` | Gratificación de diversión | Motivación U&G | Solo niveles 2–5; 82,7% en 4–5; CV 0,17 | Discrimina poco (casi todos puntúan alto) |
| B | `ug_informacion` | Gratificación de información | Motivación U&G | 1–5, bien repartida | Sí |
| B | `ug_identidad` | Gratificación de autoexpresión | Motivación U&G | 1–5, la más dispersa (DE 0,98) | Sí |
| B | `ug_interaccion_social` | Gratificación de integración social | Motivación U&G | Solo niveles 2–5; 72,8% en 4–5 | Discriminación moderada-baja |
| B | `ug_evasion` | Gratificación de escape | Motivación U&G | 1–5, bien repartida | Sí |
| B | `ug_pasar_tiempo` | Gratificación de hábito/pasatiempo | Motivación U&G | 67,9% en 4–5 | Moderada |
| C | `edad` | Años | Demográfica | Relacionada con FOMO (−0,64), comparación social (−0,56), nº de redes (−0,49) y horas (−0,41) | No como base: es demográfica (§8) |
| C | `estrato` | Estrato 1–6 | Socioeconómica | Relacionada con el gasto (r = 0,46) | No como base (§8) |
| C | `comparacion_social` | Compararse con otros en redes | Psicosocial | r = −0,56 con edad; r = 0,46 con ug_identidad | Mide algo real, pero arrastra la edad |
| C | `nivel_fomo` | Miedo a perderse algo | Psicosocial | r = −0,64 con edad; **eta² = 0,42 con grupo_etario** | Es casi un proxy de la edad |

Las seis `ug_*` son **casi independientes entre sí** (|r| ≤ 0,11). Cada una aporta información propia.

## 4–6. Evaluación de las candidatas

| Variable | Recomendación 💡 | Motivo |
|---|---|---|
| `horas_diarias_redes` | **INCLUIR** | Principal medida de intensidad de uso; distribución limpia; no redundante con U&G |
| `horas_video_dia` | **CONSIDERAR** | r = 0,73 / R² = 0,54 con horas_redes: mide en gran parte la misma "intensidad de pantalla". Si entran las dos, la intensidad pesa doble. A favor de incluirla: el 46% de su varianza es propia y es la única medida de consumo audiovisual |
| `num_redes_usadas` | **INCLUIR** | Mide amplitud (no intensidad): r = 0,18 con horas. Conductual y observable. Ojo: r = −0,49 con edad |
| `gasto_mensual_contenido_cop` | **CONSIDERAR (con tendencia a incluir)** | Es la única variable de monetización y no se relaciona con ninguna otra candidata (aporta una dimensión nueva). Pero: 32% ceros, cola larga (47 atípicos) y una escala enorme que haría falta tratar. Además el estrato explica el 22% de su varianza, así que mete algo de nivel socioeconómico en el modelo. Hay que decidir si entra y cómo transformarlo |
| `ug_entretenimiento` | **INCLUIR (con advertencia)** | Es una dimensión central del marco U&G. Discrimina poco (82,7% responde 4–5), así que previsiblemente separará poco los clusters |
| `ug_informacion` | **INCLUIR** | Buena dispersión; dimensión U&G diferenciada |
| `ug_identidad` | **INCLUIR** | La U&G más dispersa |
| `ug_interaccion_social` | **INCLUIR (con advertencia)** | Solo usa 4 niveles, pero es una dimensión U&G necesaria |
| `ug_evasion` | **INCLUIR** | Buena dispersión, independiente |
| `ug_pasar_tiempo` | **INCLUIR** | Dimensión U&G de hábito; dispersión aceptable |
| `comparacion_social` | **EXCLUIR de la base (usar para describir)** | No es U&G ni conducta observable; fuerte ligazón con edad y con ug_identidad |
| `nivel_fomo` | **EXCLUIR de la base (usar para describir)** | Relación muy fuerte con la edad; incluirla metería la edad en el modelo por la puerta de atrás |
| `edad`, `estrato` | **EXCLUIR** | Demográficas (ver §8) |

## 7. Variables relacionadas entre sí (para discutir) 📊
| Par | Pearson | Spearman | Lectura |
|---|---:|---:|---|
| `horas_diarias_redes` – `horas_video_dia` | 0,73 | 0,74 | **La única redundancia relevante entre candidatas.** VIF ≈ 2,2 (baja a 1,08 si sale una) |
| `gasto_mensual_contenido_cop` – `disposicion_pago` (categórica) | eta² = **0,85** | — | El gasto y la disposición a pagar miden prácticamente lo mismo; no usar ambas |
| `gasto` – `estrato` | 0,46 | 0,41 | El gasto arrastra información socioeconómica |
| `num_redes_usadas` / `horas_*` – `edad` | −0,49 / −0,41 | — | La conducta está relacionada con la edad, así que los clusters probablemente tendrán diferencias de edad aunque la edad no entre (esto es esperable y útil para describirlos) |
| `nivel_fomo` – `edad` / `comparacion_social` – `edad` | −0,64 / −0,56 | — | Motivo para dejarlas fuera de la base |
| Entre las 6 `ug_*` | ≤ 0,11 | ≤ 0,11 | Sin redundancia |
| `ug_*` – conducta | ≤ 0,18 | — | Las motivaciones y la conducta son dimensiones distintas: combinarlas tiene sentido |

Todos los VIF de las 10 candidatas son ≤ 2,21, así que no hay multicolinealidad grave. La cuestión es más bien de **ponderación implícita** (dos variables de horas = doble peso a la intensidad).

## 8. Variables que NO deben usarse para agrupar 💡
| Variable(s) | Por qué reservarla(s) para el enriquecimiento |
|---|---|
| `genero`, `grupo_etario`, `edad`, `estrato`, `nivel_educativo`, `region` | Son **descriptores demográficos, no conductas ni motivaciones**. La segmentación a posteriori busca patrones de uso y gratificación y *después* ve quiénes son esas personas. Si entran al modelo, los clusters se forman por edad o estrato y se vuelve una segmentación a priori disfrazada. Además, `genero`/`region`/`nivel_educativo` son nominales: K-means (distancia euclidiana) no las trata de forma válida. `grupo_etario` duplica a `edad` |
| `motivo_primario`, `necesidad_base`, `gratificacion_buscada` | Son nominales (6, 9 y 15 categorías), así que no hay distancia euclidiana posible. Además, `motivo_primario` se declara derivada de las `ug_*`, y usarla junto con ellas sería circular. Aun así, las `ug_*` explican solo un 2–12% de su varianza (eta²), así que como validación y descripción externa aportan información nueva |
| `disposicion_pago`, `sensibilidad_precio` | Ordinales en texto. `disposicion_pago` es redundante con el gasto (eta² 0,85). Tienen las contradicciones detectadas en el Paso 1 |
| Resto de categóricas (`dispositivo_principal`, `red_social_principal`, `plataforma_video_principal`, `formato_preferido`, `contexto_visionado`, `via_llegada`, `patron_consumo`, `binge_watching`, `relacion_tv_abierta`, `rol_diseno_digital`, `tension_gratificacion`, `riesgo_gratif_desplazada`, `genera_contenido`, `relacion_parasocial`, `pertenencia_comunidades`, `franja_horaria_pico`, `categoria_contenido_preferida`) | Nominales u ordinales en texto: no son aptas para K-means. Son justo las que darán "rostro" a los segmentos (qué plataformas usan, cómo y dónde consumen) |
| `comparacion_social`, `nivel_fomo` | Numéricas, pero son proxy de la edad (ver §4–6) |
| `id` | Identificador |

Nota 📊: el K-means previo que venía en el archivo sí usó `edad`, `estrato` y la disposición al pago como base. Eso explica que sus segmentos se organicen por "jóvenes/adultos × alto/bajo valor".

## 9. Tabla final de recomendación

| Variable | Tipo/dimensión | Qué mide | ¿Incluir en K-means? | Justificación |
|---|---|---|---|---|
| `horas_diarias_redes` | A · Intensidad | Horas/día en redes | **INCLUIR** | Conducta observable, distribución limpia |
| `horas_video_dia` | A · Intensidad audiovisual | Horas/día de video | **CONSIDERAR** | r = 0,73 con horas_redes; duplicaría el peso de la intensidad |
| `num_redes_usadas` | A · Amplitud | Nº de redes/mes | **INCLUIR** | Dimensión conductual distinta de las horas |
| `gasto_mensual_contenido_cop` | A · Monetización | COP/mes en contenido | **CONSIDERAR** (tendencia a incluir) | Dimensión única, pero con ceros, cola larga y necesidad de tratamiento; relacionada con el estrato |
| `ug_entretenimiento` | B · U&G | Diversión | **INCLUIR** (advertencia) | Central en U&G; baja variabilidad |
| `ug_informacion` | B · U&G | Información | **INCLUIR** | Buena dispersión, independiente |
| `ug_identidad` | B · U&G | Autoexpresión | **INCLUIR** | La más dispersa |
| `ug_interaccion_social` | B · U&G | Integración social | **INCLUIR** (advertencia) | Solo 4 niveles usados |
| `ug_evasion` | B · U&G | Escape | **INCLUIR** | Buena dispersión, independiente |
| `ug_pasar_tiempo` | B · U&G | Hábito/pasatiempo | **INCLUIR** | Dimensión U&G de hábito |
| `comparacion_social` | C · Psicosocial | Comparación con otros | **EXCLUIR** (descriptor) | Ligada a edad (−0,56) y a ug_identidad |
| `nivel_fomo` | C · Psicosocial | FOMO | **EXCLUIR** (descriptor) | Proxy de edad (eta² 0,42) |
| `edad` | C · Demográfica | Años | **EXCLUIR** | Demográfica, para enriquecer |
| `estrato` | C · Socioeconómica | Estrato 1–6 | **EXCLUIR** | Demográfica; ya se refleja en parte en el gasto |

## 10. Conjuntos posibles (la decisión es del equipo) 💡

### Opción A — equilibrio conducta + U&G (10 variables)
`horas_diarias_redes`, `horas_video_dia`, `num_redes_usadas`, `gasto_mensual_contenido_cop` + las 6 `ug_*`.
- **Peso:** 4 conductuales / 6 motivacionales. Dentro de lo conductual, la intensidad de pantalla cuenta doble.
- **Qué permitiría descubrir:** audiencias que se diferencian por *cuánto* consumen (redes y video por separado), *qué tan diversificadas* están, *si pagan* y *por qué* consumen. Por ejemplo, podría separar a quien consume mucho video pero pocas redes de quien hace lo contrario, aunque con r = 0,73 esos casos son minoría.

### Opción B — sin redundancia de intensidad (9 variables)
`horas_diarias_redes`, `num_redes_usadas`, `gasto_mensual_contenido_cop` + las 6 `ug_*`.
- **Peso:** 3 conductuales / 6 motivacionales; todos los VIF ≈ 1,0–1,1 (variables prácticamente independientes).
- **Qué permitiría descubrir:** segmentos definidos por tres ejes conductuales limpios (intensidad, amplitud, monetización) y el perfil motivacional. El hábito audiovisual (`horas_video_dia`, `binge_watching`, `patron_consumo`, `plataforma_video_principal`) queda para describir los clusters.
- **Riesgo:** con 6 de 9 variables en U&G, el peso motivacional domina. Si el equipo quiere más peso conductual, puede pesar más la Opción A.

**Variante a discutir en ambas opciones:** mantener o no el gasto. Sin él, los segmentos serían puramente de uso y motivación, y la monetización (gasto, disposición a pagar) pasaría a describir los clusters.

## Decisiones que quedan en manos del equipo
1. ¿Opción A o B?
2. ¿Entra el gasto? Si entra, ¿con qué tratamiento (log(1+x), recorte)? Se decide en el paso de preparación.
3. ¿Se mantienen `ug_entretenimiento` y `ug_interaccion_social` pese a su baja variabilidad, por coherencia con el marco U&G?
4. ¿Se acepta el desbalance U&G/conducta o se busca compensarlo?

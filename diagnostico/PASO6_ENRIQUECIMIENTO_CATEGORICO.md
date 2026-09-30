# Paso 6 — Enriquecimiento categórico de los clusters (K = 3, foco en Clusters 0 y 1)

**Modelo:** el mismo K = 3 de los Pasos 4–5. El script comprueba que la asignación es idéntica a `paso5_asignacion_k3.csv`.
**Código:** `diagnostico/paso6_cruces_categoricas.py` · **Salida completa:** `diagnostico/salida_paso6.txt`
📊 = base (n = 1.000, sintética) · 🎙️ = 14 entrevistas del estudio "La Primera Vez" · 💡 = interpretación.
Índice = % del cluster / % del total × 100 (100 = promedio de la base).

## Notas metodológicas
1. **`gratificacion_obtenida` no existe en la base.** Como variable de gratificación obtenida uso `tension_gratificacion`, que mide la brecha entre lo buscado y lo obtenido. Para los cruces la agrupé en: *Descubrimiento positivo* ("obtiene más de lo que busca"), *Satisfacción plena*, *Satisfacción parcial*, *Indiferencia* y *Frustración* (leve + alta).
2. **Recodificaciones** (solo agrupan categorías que ya existen):
   - Edad en rangos 18–24 / 25–39 / 40–55 / 56+, como pidieron.
   - Estrato en bajo (1–2), medio (3) y alto (4–6).
   - Región en Bogotá frente al resto.
   - Modalidad (solo/a · acompañado/a · desplazamiento).
   - Descubrimiento (algoritmo/tendencias · recomendación social · búsqueda activa · publicidad/medios).
   - Maratón (alto · ocasional · bajo).
3. **La base no tiene "entorno urbano/rural" ni la ocupación "estudiante".** Se usan `region`, `estrato` y `nivel_educativo`.
4. **Las distribuciones que se reportan son las reales de la base.** Las entrevistas se usan como evidencia cualitativa, sin convertirlas en porcentajes proyectados, porque con n = 14 eso sería inventar precisión.
5. **Proxy de retención:** la base no mide abandono. Uso % *indiferencia* (vínculo débil), % *positivo* (descubrimiento + satisfacción plena) y % *riesgo alto de gratificación desplazada*. Referencias en la base total: indiferencia 14,0%, positivo 38,4%, frustración 24,0%.

## Las 14 entrevistas, reconstruidas desde la tabla de cuotas del PDF 🎙️
> La extracción de la tabla del PDF mezcla columnas en E6/E7. Esta es la lectura más consistente con el texto de los User Personas; conviene verificarla con el Excel de codificación.

| Código | Edad | Género | Ciudad | Vía de llegada | Modalidad | Resultado | Cluster afín 💡 |
|---|---:|---|---|---|---|---|---|
| E1 Alejandra | 24 | F | Bogotá | Redes sociales | Conversa con familia y amigos | Terminó | 0 (Persona 1) |
| E2 Claudia | 22 | F | Perú | Amigos + redes | Sola, comparte con amigos | Terminó | 0 |
| E3 Emilio | 20 | M | Bogotá | Algoritmo + publicidad | Solo, comparte con amigos | Terminó | 0 (Persona 1) |
| **E4 Jorge** | 19 | M | Barranquilla | **Algoritmo** | **Solo** | **Abandonó** | 0 (Persona 1) |
| E5 Juliana | 22 | F | Bogotá | Publicidad | Sola y a veces con familia | Terminó | 0 |
| E6 María Paula | 21 | F | Bogotá | Amigos + redes | 1.ª temporada con su mamá, luego sola | Terminó | 0 |
| E7 María Lilian | 20 | F | Bogotá | Amigos + algoritmo | Sola y a veces con su novio | Terminó | 0 (Persona 1) |
| E8 Mariana | 19 | F | Bogotá | Amigos + algoritmo | Sola y con amigas | Terminó | 0 |
| **E9 Santiago** | 23 | M | Bogotá | **Algoritmo** | **Principalmente solo** | **Abandonó** | 0 (Persona 1) |
| E10 Sara | 19 | F | Bogotá | Redes sociales | Con familia y amigos | Terminó | 0 |
| E11 Simón | 22 | M | Bogotá | Amigos | Solo, comparte con familia y amigos | Terminó | 0 (Persona 1) |
| E12 Valeria | 22 | F | Chía | Algoritmo | Sola, comparte con su padre | Terminó | 0 |
| E13 Belssy | 44 | F | Bogotá | Algoritmo (pantalla de inicio) | Con su esposo | Terminó | 1 (Persona 2) |
| E14 Sandra | 54 | F | Bogotá | Recomendación de su hija | Con esposo o hijas / sola | En curso | 1 (Persona 2) |

**Patrón clave** 🎙️: de las 7 personas cuya vía de llegada incluye el *algoritmo* (E3, E4, E7, E8, E9, E12, E13), **las únicas 2 que abandonaron (E4, E9) son las que vieron solas y sin ninguna conversación social**. Quienes llegaron por algoritmo pero luego compartieron la serie (E3 con amigos, E12 con su padre, E13 con su esposo) la terminaron.

---

## CLUSTER 0 — Exploradores Hiperconectados (n = 415, 41,5%) ↔ 🎙️ "El Explorador Casual"

### 1. Distribución categórica predominante 📊
| Variable | Categorías dominantes (% del cluster · índice) |
|---|---|
| **motivo_primario** | Hábito y pasatiempo 21,9% (117) · Interacción social 21,4% · Entretenimiento 17,8% · **Identidad 15,4% (127)**. Información solo 9,6% (60) |
| **necesidad_base** | **Distracción y placer 24,1%** · Descanso emocional 20,2% · Pertenencia 15,2%. Autoexpresión (136) y reconocimiento (120) sobre el promedio |
| **gratificacion_buscada** | **Relajación 19,3% (113)** · Diversión y risa 10,4% · Llenar el tiempo libre 9,4% (122). Expresar quién soy (135), inspiración creativa (141) |
| **Gratificación obtenida** (tension_gratificacion) | Satisfacción parcial 24,6% · Satisfacción plena 20,0% (87) · Indiferencia 15,4% (110) · Descubrimiento positivo 14,7% · Frustración 25,3% |
| **género** | Femenino 52,3% · Masculino 47,0% (sin sesgo relevante) |
| **grupo etario** | **25–39: 50,4% (135) · 18–24: 35,2% (181)** · 40–55: 12,3% |
| **nivel educativo** | Secundaria 32,5% · Técnico 32,3% · Universitario 26,0% · Posgrado 6,0% |
| **estrato / región** | Estrato bajo 49,2% · medio 36,4% · alto 14,5% (68). Bogotá 20,7%; resto 79,3% (Caribe 18,8%, Antioquia 16,1%) |
| **plataforma de video** | YouTube 27,0% · **Netflix 25,8% (114)** · **TikTok 24,6% (135)** |
| **dispositivo** | **Smartphone 82,9%** · Computador 8,0% · Smart TV 7,5% (81) · Tablet 1,7% |
| **modalidad** | Acompañado/a 49,4% (94) · **Solo/a 39,8% (110)**. Contexto top: **solo/a en smartphone 31,1% (117)** |
| **maratón** | **Alto 28,0% (119)** · Ocasional 29,6% · Bajo 42,4%. Patrón top: **maratón 25,1% (114)** |
| **vía de descubrimiento** | **Algoritmo/tendencias 36,9% (117)** · Recomendación social 39,5% (redes sociales, índice 119) · Búsqueda activa 13,0% |

### 2. Justificación con evidencia del estudio 🎙️
- **Motivación: entra por distracción, no por información.**
  - 📊 El cluster sobrerrepresenta hábito, identidad, distracción y relajación, y es el que menos se mueve por información (índice 60).
  - 🎙️ Es exactamente el punto de partida de Daniel: *"era como para distraerme"* (E1); *"entretenerme… desconectarme un ratico"* (E3).
- **Gratificación obtenida: aprendizaje no esperado.**
  - 🎙️ *"No pensé que fuera a darme un poco de contexto histórico colombiano"* (E11).
  - 📊 En la base, el *descubrimiento positivo* del cluster está en el promedio (14,7%). Pero **sube a 21,9% entre quienes ven solos y llegaron por recomendación social**, que es justamente el patrón de E11 (llegó por un amigo y vio solo).
- **Identidad y personajes jóvenes.**
  - 📊 Identidad y autoexpresión están sobrerrepresentadas.
  - 🎙️ Los entrevistados se enganchan con personajes jóvenes, romance y primeras veces.
- **Demografía:**
  - 📊 El cluster es algo mayor que el persona: la mitad tiene 25–39 años. Los 18–24 son el 35%, pero de todas las personas de 18–24 de la base, el 75% cae aquí.
  - 🎙️ Los 12 entrevistados de 19–24 años encajan en este cluster por edad y hábitos.
  - **Divergencia 1:** las entrevistas son universitarios de Bogotá. En la base, el cluster es mayoritariamente de educación secundaria o técnica y el 79% vive fuera de Bogotá. 💡 La muestra cualitativa sobrerrepresenta al joven universitario bogotano; el segmento real es más amplio.
  - **Divergencia 2, género:** 🎙️ 8 de 12 son mujeres, pero 📊 en la base es 52/47.
- **Consumo:**
  - 📊 Consume solo/a en smartphone y con alta maratón.
  - 🎙️ Coincide: consumo individual en pantallas variadas (Simón en iPad, Jorge en TV); *"puede ver varios capítulos consecutivos cuando una historia consigue engancharlo"*.
- **Descubrimiento:**
  - 📊 Es el cluster más algorítmico (36,9%).
  - 🎙️ El top de Netflix (E4), el video previo (E9), la miniatura (E11) y la recomendación de amigos (E7, E8, E11).

### 3. Insights de cruce 📊
Resultado de la gratificación por combinación, dentro del Cluster 0:

| Combinación (n) | % indiferencia | % positivo | % descubrimiento positivo | % riesgo desplazamiento alto | Lectura 💡 |
|---|---:|---:|---:|---:|---|
| **Solo/a + algoritmo** (59; 14,2% del cluster) | **23,7** | 32,2 | 11,9 | 39,0 | ⚠️ **Riesgo.** La indiferencia casi duplica el promedio de la base (14,0%). Es el patrón de E4 y E9 |
| Hombre 18–24 + solo/a + algoritmo (8) | 37,5 | 37,5 | — | 75,0 | ⚠️ Perfil exacto de los abandonos. n muy pequeño: solo indicativo |
| **Solo/a + recomendación social** (64) | **12,5** | **39,1** | **21,9** | 43,8 | ✅ **Oportunidad.** La menor indiferencia y el mayor descubrimiento positivo del cluster. Es el patrón de E11 (el "aprendizaje inesperado") |
| Netflix + solo/a en smartphone (29) | **6,9** | **44,8** | — | 37,9 | ✅ Quien ya elige Netflix, aunque vea solo, está enganchado |
| Acompañado/a + recomendación social (82) | 17,1 | 32,9 | 7,3 | 45,1 | ➖ No mejora en este cluster: estar acompañado no basta si el contenido no le "descubre" nada |
| Acompañado/a + algoritmo (72) | 15,3 | 36,2 | 18,1 | 43,1 | ➖ Neutro. E13 sigue este patrón (en otro cluster) |
| Motivo evasión/hábito + solo/a (54) | 18,5 | **44,4** | — | 33,3 | ✅ Quien busca evasión y la obtiene queda satisfecho |

**Síntesis del Cluster 0** 💡:
- **El riesgo no es ver solo, es ver solo sin validación social.** Ver solo tras una recomendación de amigos o redes produce la menor indiferencia (12,5%) y el mayor descubrimiento (21,9%). Ver solo tras el algoritmo produce el doble de indiferencia (23,7%).
- 🎙️ Coincide exactamente con el estudio: E3 y E12 llegaron por algoritmo, pero luego conversaron la serie y la terminaron; E4 y E9 no la conversaron y abandonaron.
- **Palanca:** convertir cada llegada algorítmica en conversación social (clips para compartir, creadores de contenido, "recomiéndala a un amigo").
- **Género:** dentro del cluster, hombres y mujeres casi no difieren (Netflix 24% frente a 27%, algoritmo 38,5% frente a 35,5%, frustración 26,7% frente a 24,0%). Los hombres llegan un poco más por algoritmo y se frustran un poco más, en línea con los dos abandonos masculinos del estudio.

---

## CLUSTER 1 — Espectadores Familiares de Pantalla Compartida (n = 411, 41,1%) ↔ 🎙️ "La Espectadora Nostálgica"

### 1. Distribución categórica predominante 📊
| Variable | Categorías dominantes (% del cluster · índice) |
|---|---|
| **motivo_primario** | **Información 22,6% (141)** · Entretenimiento 20,4% · Interacción social 18,5%. Identidad solo 9,0% (74) |
| **necesidad_base** | Distracción y placer 21,2% · **Curiosidad 17,5% (124)** · Descanso emocional 16,8% · **Seguridad informativa 13,1% (133)** |
| **gratificacion_buscada** | Relajación 15,8% · **Estar al día 11,9% (151)** · Diversión y risa 11,7%. Aprender algo nuevo (117), tomar mejores decisiones (165) |
| **Gratificación obtenida** (tension_gratificacion) | Satisfacción plena 22,9% · Satisfacción parcial 21,9% · **Descubrimiento positivo 15,8%** (el más alto de los 3) · Indiferencia 15,3% · Frustración 24,1% |
| **género** | Masculino 50,1% · Femenino 49,1% (sin sesgo) |
| **grupo etario** | **40–55: 40,4% (148)** · **56+: 30,9% (192)** · 25–39: 23,8% · 18–24: 4,9% (25) |
| **nivel educativo** | Secundaria 32,8% · Técnico 29,0% · Universitario 26,3% · Posgrado 5,6%. **Primaria o menos 6,3% (154)** |
| **estrato / región** | Estrato bajo 49,9% · medio 35,8% · alto 14,4%. Bogotá 18,7%; resto 81,3% |
| **plataforma de video** | **YouTube 30,9%** · Netflix 17,8% (78) · **Ninguna 14,1% (168)** · Disney+ y Prime por encima del promedio |
| **dispositivo** | Smartphone 74,7% · **Smart TV 10,7% (116)** · Computador 10,7% · **Tablet 3,9% (134)** |
| **modalidad** | **Acompañado/a 56,9% (108)**: **en familia con TV o pantalla compartida 35,0% (116)**, en pareja 17,8%. Solo/a 30,9% (86) |
| **maratón** | Bajo 45,3% · Ocasional 33,3% · Alto 21,4% (91). Patrón: **un episodio por sesión 27,7% (115)**, **fragmentado 20,0% (117)** |
| **vía de descubrimiento** | **Recomendación social 38,9%** (amigos/familia 24,3%) · Algoritmo 27,5% (88) · **Publicidad/medios 17,0% (122)** · Búsqueda activa 16,5% |

### 2. Justificación con evidencia del estudio 🎙️
- **Motivación: desconexión + memoria + contexto.**
  - 📊 Es el cluster más informativo y curioso.
  - 🎙️ El estudio muestra a Laura buscando desconexión y *"recordar la época de mi adolescencia"* (E14). También le interesan *"los acontecimientos del país"* y *"la lectura de grandes libros"* (E14).
  - 💡 La nostalgia de época es a la vez emocional e informativa. La serie les da *memoria* y *contexto histórico* a la vez.
- **Gratificación obtenida: memoria compartida.**
  - 📊 Es el cluster con **más descubrimiento positivo (15,8%)** y el menor riesgo de desplazamiento de la base (29,9%).
  - 🎙️ *"Recordamos nuestros tiempos… muy reconfortante"* (E13); *"volver a vivir una época"* (E14).
- **Demografía:**
  - 📊 El 71% tiene 40 años o más, y el 61% de todas las mujeres de 40–55 de la base cae aquí.
  - 🎙️ Belssy (44) y Sandra (54) son profesionales: abogada y epidemióloga.
  - **Divergencia:** 📊 en la base el cluster tiene educación mayoritariamente secundaria o técnica, y la mitad son hombres. 💡 El persona "profesional" y "mujer" es un subgrupo del cluster, no su totalidad.
- **Consumo:**
  - 📊 Consume en familia con TV o pantalla compartida, con más Smart TV y tablet que el resto, un episodio por sesión o de forma fragmentada.
  - 🎙️ Coincide: *"siempre acompañada de mi esposo"* (E13); *"uno o dos momentos a la semana… con mi esposo o mis hijas"* (E14); la retoma *"cuando dispone de tiempo"*.
- **Descubrimiento:**
  - 📊 Recomendación social y publicidad o medios (índice 122).
  - 🎙️ La recomendación intergeneracional hija → madre (E14) y la pantalla de inicio de Netflix (E13).
- **Plataforma:**
  - 📊 Netflix está por debajo del promedio (17,8%), el 14% no usa ninguna plataforma de video y la TV abierta es la fuente principal para el 29,9% (dato del Paso 5).
  - 💡 La serie entra a este cluster por la vía de la coproducción con Caracol y por los hijos, no por el catálogo de Netflix.

### 3. Insights de cruce 📊
Resultado de la gratificación por combinación, dentro del Cluster 1:

| Combinación (n) | % indiferencia | % positivo | % descubrimiento positivo | % riesgo desplazamiento alto | Lectura 💡 |
|---|---:|---:|---:|---:|---|
| **Solo/a + algoritmo** (37; 9,0%) | **29,7** | **21,6** | **2,7** | 35,1 | ⚠️ **La peor combinación de todo el análisis.** Indiferencia al doble del promedio y casi ningún descubrimiento. Para este cluster, el algoritmo sin compañía no funciona |
| Netflix + solo/a en smartphone (15) | 6,7 | 20,0 | — | 46,7 | ⚠️ Frustración 46,7%: el adulto solo con el celular en Netflix se frustra (n pequeño) |
| **Solo/a + recomendación social** (53) | 13,2 | **45,3** | 20,8 | 32,1 | ✅ Una recomendación humana compensa ver solo. Es el caso de E14 cuando ve sola |
| **Acompañado/a + búsqueda activa** (43) | 9,3 | **46,6** | 14,0 | 30,2 | ✅ La mejor: busca la serie con intención y la ve acompañada. E14 buscó la serie después de que su hija se la recomendara |
| Acompañado/a + algoritmo (63) | 11,1 | 39,6 | 19,0 | **28,6** | ✅ Es el patrón de E13 (pantalla de inicio + esposo): baja indiferencia y bajo desplazamiento |
| Acompañado/a + recomendación social (86) | 17,4 | 39,6 | 16,3 | 33,7 | ➖ En el promedio. La hipótesis "acompañado + recomendación = alta fidelización" **no se confirma con fuerza** en este proxy |
| Familia en TV + recom. amigos/familia (35) | 20,0 | 34,3 | — | 31,4 | ➖ Tampoco destaca: no hay evidencia en la base de que sea la combinación más fiel |
| Mujer 40–55 + acompañada (48) | 14,6 | 37,5 | — | 41,7 | ➖ El subgrupo "Laura" está en el promedio del cluster |

**Síntesis del Cluster 1** 💡:
- **El mayor riesgo de toda la base es el adulto que ve solo y llegó por el algoritmo:** 29,7% de indiferencia y 2,7% de descubrimiento.
- **Para este segmento, estar acompañado es protector frente al algoritmo.** Con el algoritmo, el positivo pasa de 21,6% (solo) a 39,6% (acompañado), y la indiferencia de 29,7% a 11,1%.
- **La mejor puerta es la búsqueda con intención, precedida de una recomendación**, que es el camino de E14.
- ⚠️ **Matiz honesto:** la combinación "familia en TV + recomendación familiar" **no aparece como la más fiel** en la base; está en el promedio. La evidencia de alta fidelización en ese patrón viene solo de las 2 entrevistas (E13 y E14 terminaron o quieren terminar). Conviene presentarlo como hipótesis cualitativa, no como hallazgo confirmado.
- **Género:** dentro del cluster, los hombres llegan más por recomendación social (42,2% frente a 35,1%), ven más acompañados (59,2% frente a 54,5%), maratonean más (24,3% frente a 18,8%) y tienen algo más de satisfacción plena (24,8% frente a 20,8%). 💡 El "esposo acompañante" es una audiencia real y receptiva. La brecha femenina del estudio no se explica por falta de interés masculino en este segmento.

---

## CLUSTER 2 — Suscriptores de Valor (n = 174, 17,4%) — solo como referencia

| Variable | Categorías dominantes 📊 |
|---|---|
| motivo / necesidad / gratificación buscada | Interacción social 23,6% · Distracción 20,7% · Relajación 14,4%. Sentirse acompañado (144) |
| Gratificación obtenida | **Satisfacción plena 31,0% (134)** · Indiferencia 7,5% (53): el mejor resultado de los tres |
| Sociodemográfico | Edades mezcladas (25–39: 37,4%; 40–55: 32,2%) · 50/50 género · **estrato alto 54% (254)** · universitario + posgrado 55% |
| Consumo | YouTube 28,7% · **Netflix 27,0%** · acompañado/a 51,1% · maratón baja (índice 76) · un episodio por sesión 28,7% |
| Descubrimiento | Recomendación social 39,7% · algoritmo 27,6% · **búsqueda activa 17,8% (116)** |
| Evidencia del estudio | 🎙️ Ninguna entrevista corresponde a este segmento |

---

## Resumen de cruces para la estrategia 💡
| Combinación | Cluster 0 | Cluster 1 | Evidencia del estudio | Acción |
|---|---|---|---|---|
| Solo/a + algoritmo | ⚠️ indiferencia 23,7% | ⚠️⚠️ indiferencia 29,7%, descubrimiento 2,7% | E4 y E9 abandonaron | Tras la llegada algorítmica, provocar una conversación: compartir, recordatorio social, clip para enviar |
| Solo/a + recomendación social | ✅ mejor descubrimiento (21,9%) | ✅ positivo 45,3% | E11 (amigo → aprendizaje inesperado) | Potenciar el "boca a boca" digital: botón para compartir, creadores de contenido |
| Acompañado/a + algoritmo | ➖ neutro | ✅ indiferencia 11,1%, desplazamiento 28,6% | E13 (inicio de Netflix + esposo) | En Smart TV: tráiler en la pantalla de inicio orientado a ver en pareja o en familia |
| Acompañado/a + búsqueda activa | ➖ | ✅ positivo 46,6% | E14 (hija recomienda → busca) | Campañas que provoquen la búsqueda del título: "búscala y véanla juntas" |
| Familia en TV + recomendación familiar | ➖ | ➖ en el promedio | E13 y E14 (n = 2) | Mantener como hipótesis y validarla con más entrevistas |

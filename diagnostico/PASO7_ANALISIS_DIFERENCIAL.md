# Paso 7 — Análisis diferencial de los clusters (K = 3) · "La Primera Vez"

**Código:** `diagnostico/paso7_diferencial.py` · **Salida:** `diagnostico/salida_paso7.txt` · **Rasgos distintivos:** `diagnostico/paso7_rasgos_distintivos.csv`
📊 = base (n = 1.000) · 🎙️ = 14 entrevistas / User Personas / Mapas de Empatía · 💡 = interpretación.

**Método de diferenciación:** para cada categoría se calculó el **lift** = % en el cluster / % más alto en cualquiera de los otros dos clusters. Un lift de 2,0 significa que el rasgo es el doble de frecuente que en el cluster más parecido. Así se aísla lo que es **exclusivo** de cada cluster, no solo lo que es frecuente en él. Solo cuentan las categorías que pesan al menos un 10% dentro del cluster.

---

## 1. Tabla comparativa de factores dominantes

| Dimensión | **Cluster 0 — Exploradores Hiperconectados** (41,5%) | **Cluster 1 — Espectadores Familiares de Pantalla Compartida** (41,1%) | **Cluster 2 — Suscriptores de Valor** (17,4%) |
|---|---|---|---|
| **Motivación dominante** | **Evasión, identidad y hábito.** Máximo en 5 de las 6 `ug_*`: todas menos información (evasión 3,80; pasar el tiempo 4,11; identidad 3,71). Exclusivo: motivo "Identidad y autoexpresión" (lift 1,34). 🎙️ *"entretenerme… desconectarme un ratico"* (E3) | **Información y curiosidad.** Es el único cluster donde gana `ug_informacion` (4,05). Exclusivo: motivo "Información" (lift 1,46). 🎙️ La nostalgia de Laura se expresa como memoria + contexto del país (E14) | **Sin motor motivacional propio.** Sus U&G están en la media; el rasgo más cercano es "Interacción social" (lift 1,10, débil). Lo que lo mueve es **la calidad por la que paga** |
| **Comportamiento y hábitos** | **Maratón frecuente (24,1%, lift 1,32), madrugada (lift 1,45), smartphone solo/a.** 4,2 h/día en redes y 2,6 h/día de video. **Creador activo 55,7%** (lift 1,70) | **Consumo pausado y acompañado:** en familia con TV o pantalla compartida 35,0%, un episodio por sesión 27,7%, fragmentado 20,0%. **Consumidor pasivo 40,4%** (lift 1,67). 1,6 h/día de video | **Un episodio por sesión (28,7%), solo/a en computador (lift 1,52)**, maratón ocasional de fin de semana. Consumo "de fondo" 19,5% |
| **Necesidad / gratificación dominante** | Distracción y placer, autoexpresión (índice 136), "Expresar quién soy" (135). 🎙️ Valor inesperado: **aprendizaje histórico no buscado** (E11) | **"Estar al día" (lift 1,60)**, seguridad informativa y curiosidad (lift 1,27). 🎙️ **Revivir la propia juventud y memoria compartida** (E13, E14) | **Satisfacción plena 31,0%** (lift 1,36): obtiene exactamente lo que busca. "Sentirse acompañado/a" (índice 144) |
| **Demografía y geografía** | **18–24 años (lift 2,19)** y 25–39. Estrato 1 (lift 1,27). Género 52/47 | **56+ años (lift 2,15)** y 40–55. Educación secundaria o técnica. Género 49/50 | **Estrato 5 (lift 6,26) y 4 (lift 2,42), posgrado (lift 4,01).** Edades mezcladas. Género 49/50 |
| **Plataforma y vía de entrada** | **TikTok (lift 1,58)**, Netflix 25,8%. **Algoritmo (lift 1,32) y redes sociales (lift 1,32).** **Nunca ve TV abierta (lift 1,81)** | **Ninguna plataforma de video (lift 2,23); la TV abierta sigue siendo su fuente principal (lift 1,93).** Recomendación de amigos/familia y medios. **El diseño digital "casi no lo nota"** (lift 1,47) | **Disposición a pagar alta 92% (lift 14,7).** Netflix 27,0% (el más alto). Recomendación de amigos/familia y búsqueda activa. **El diseño es determinante** (lift 1,47) |

### Contraste con los ejemplos del enunciado 📊
Algunos ejemplos del enunciado no se sostienen en la base y conviene no afirmarlos:
- **"Mujeres adultas profesionales de 40–55+" no describe al Cluster 1:** es 50% hombres y de educación mayoritariamente secundaria o técnica. Laura es un **subgrupo** del cluster (el 61% de las mujeres de 40–55 de la base cae aquí), no su perfil demográfico dominante.
- **"Jóvenes universitarios de 18–24" no describe al Cluster 0 completo:** el 50% tiene 25–39 años y solo el 26% es universitario. Lo que sí es exclusivo del cluster es la edad de **18–24** (lift 2,19).
- **La brecha de género no diferencia a ningún cluster** (V de Cramer = 0,02). 🎙️ El sesgo femenino (10 de 14) es un rasgo de quién ve la serie, no de la estructura del mercado.
- **"Recomendación intergeneracional"** 🎙️ solo tiene evidencia en E14 (hija → madre). En la base, el Cluster 1 llega por recomendación de amigos o familia (24,3%) y medios, pero la variable no distingue si la recomendación viene de un hijo.

---

## 2. Ficha de identidad única (¿qué lo hace irremplazable?)

**Cluster 0 — Exploradores Hiperconectados.**
- Es el único segmento que **convierte ver la serie en contenido**: el 81% crea contenido, el 65% participa en comunidades y el 48% sigue intensamente a creadores.
- Es también la puerta generacional (18–24) por la que "La Primera Vez" llega a su público declarado.
- *Si este cluster no existiera, la serie perdería su motor de difusión orgánica en TikTok e Instagram, y el caso más valioso del estudio: el joven que entra a distraerse y sale aprendiendo historia de Colombia.*

**Cluster 1 — Espectadores Familiares de Pantalla Compartida.**
- Es el único segmento para el que la Colombia de los 70 **es memoria vivida y no escenografía**, y el único que ve la serie en la sala, en compañía.
- Su puerta de entrada no es Netflix: para el 30% la TV abierta sigue siendo su fuente principal, y el 14% no usa plataformas de video.
- *Si este cluster no existiera, la serie perdería su dimensión intergeneracional (la conversación hija–madre y "recordamos nuestros tiempos"), y el puente con la audiencia de Caracol Televisión.*

**Cluster 2 — Suscriptores de Valor.**
- Es el único segmento definido **por el dinero y no por la motivación**: 92% de disposición a pagar alta, $72.000/mes y estrato alto.
- Es el que obtiene exactamente lo que busca (31% de satisfacción plena, 7,5% de indiferencia).
- *Si este cluster no existiera, la serie perdería a quienes sostienen la suscripción y juzgan su calidad de producción, y a su audiencia más satisfecha y menos volátil.*

---

## 3. Puntos de contraste / polarización clave

### 3.1 Riesgo de abandono frente a fidelización
Proxies 📊. La base no mide abandono. Los índices compuestos son promedios simples de indicadores en %.

| Indicador | Cluster 0 | Cluster 1 | Cluster 2 |
|---|---:|---:|---:|
| **Riesgo alto de gratificación desplazada** | **45,3%** | 29,9% | 35,6% |
| Indiferencia | 15,4% | 15,3% | **7,5%** |
| Frustración (leve + alta) | **25,3%** | 24,1% | 20,7% |
| Zapping entre plataformas | **11,3%** | 9,2% | 8,6% |
| Ver solo + llegar por algoritmo | **10,6%** | 8,0% | 9,8% |
| Satisfacción plena | 20,0% | 22,9% | **31,0%** |
| **Índice de vulnerabilidad** | **24,3** | 19,6 | 18,1 |
| **Índice de fidelización** | 20,7 | 24,7 | **27,4** |

**Cuál abandona más rápido y por qué: el Cluster 0.**
- 📊 Es el más vulnerable en todos los indicadores.
  - El 45% "termina haciendo algo distinto a lo planeado".
  - Es el que más hace zapping.
  - Es el que más reúne el patrón de ver solo tras llegar por el algoritmo.
  - Tiene la máxima sensibilidad al precio (52%).
- 🎙️ El estudio lo confirma: los 2 abandonos (E4, E9) son jóvenes, hombres, que veían solos y llegaron por el algoritmo.
- **Mecanismo:** 🎙️ el detonante narrativo es el *conflicto romántico repetitivo* (E9). 📊 Su maratón frecuente y su consumo nocturno o de madrugada hacen que la repetición se note más rápido.
- 💡 **Matiz:** el Cluster 0 también es el que más se beneficia de la validación social. Viendo solo tras una recomendación social, su indiferencia baja a 12,5%, frente a 23,7% con el algoritmo (Paso 6).

**Cluster 1: no abandona, pausa.**
- 📊 Tiene el menor riesgo de desplazamiento (29,9%) y la mayor proporción de consumo fragmentado (20%).
- 🎙️ E14 "la retoma cuando dispone de tiempo".
- 💡 Su enemigo es la **falta de tiempo y el olvido**, no la narrativa.
- ⚠️ Excepción: si ve solo y llegó por el algoritmo, es el peor caso de toda la base (29,7% de indiferencia; Paso 6).

**Cluster 2: el más fiel, pero exigente.**
- 📊 Tiene la mejor satisfacción y la menor indiferencia.
- 📊 Pero para el 21% el diseño es *determinante*: elige o abandona por diseño.
- 💡 Abandonaría por calidad percibida (producción, interfaz), no por aburrimiento.

### 3.2 Consumo individual frente a consumo social
| Indicador | Cluster 0 | Cluster 1 | Cluster 2 |
|---|---:|---:|---:|
| Ve solo/a | **39,8%** | 30,9% | 39,1% |
| Ve acompañado/a (familia, pareja o amigos) | 49,4% | **56,9%** | 51,1% |
| En familia con TV o pantalla compartida | 25,8% | **35,0%** | 29,3% |
| Con amigos | **7,2%** | 4,1% | 6,3% |
| Patrón "consumo social" (ver juntos y comentar) | **11,3%** | 9,2% | 8,6% |
| Crea contenido (activo u ocasional) | **81,0%** | 33,8% | 57,5% |
| Consumidor pasivo | 5,3% | **40,4%** | 24,1% |
| Comunidad en línea activa | **64,6%** | 21,4% | 39,1% |
| Sin comunidades en línea | 1,7% | **19,2%** | 9,2% |

**Hallazgo de polarización 💡: hay dos formas opuestas de ser "social".**
- **Cluster 0 ve solo, pero conversa en línea.** Es el más individual frente a la pantalla y, a la vez, el más conversacional en lo digital: crea, comparte, participa en comunidades y sigue a creadores.
  - 🎙️ Encaja con el estudio: *"consume principalmente solo, aunque luego puede convertir lo visto en conversación con amigos o familiares"* (Mapa de Empatía de Daniel). E1 se la recomendó *"a mi familia, a mis papás, a mis amigas"*.
  - **Su conversación es posterior, digital y entre pares.**
- **Cluster 1 ve acompañado, pero es silencioso en línea.** Es el más social en el sofá (familia, pareja) y el más pasivo en lo digital: 40% solo observa y 19% no participa en ninguna comunidad.
  - 🎙️ *"Hablamos con mi esposo y recordamos nuestros tiempos"* (E13).
  - **Su conversación es simultánea, presencial e intergeneracional.**
- **Cluster 2 está en un punto intermedio:** consumo mixto, poca maratón. Conversa sobre todo a través de la recomendación (27% llega por amigos o familia).

**Implicación para "La Primera Vez" 💡:**
- La conversación que genera la serie no se activa igual en los dos segmentos principales:
  - Al **Cluster 0** hay que darle **material para compartir** (clips, retos, creadores de contenido). Esa conversación es además su antídoto contra el abandono.
  - Al **Cluster 1** hay que darle **motivos para verla juntos** (la sala, la TV, el hijo o la hija que la recomienda). La pieza digital no lo alcanza, pero la TV abierta y la recomendación familiar sí.
- El puente entre ambos es el mismo que documenta E14: **el joven del Cluster 0 recomienda la serie a su madre o padre del Cluster 1.**

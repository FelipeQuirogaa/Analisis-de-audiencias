# Fase 5 — Perfilar y enriquecer los clusters (K = 3) · "La Primera Vez" (Netflix / Caracol TV)

**Modelo:** K-means, K = 3, sobre las 9 variables estandarizadas (StandardScaler; k-means++, n_init = 10, random_state = 42), el mismo del Paso 4.
**Código:** `diagnostico/paso5_perfilado_k3.py` · **Salida completa:** `diagnostico/salida_paso5.txt` · **Asignaciones:** `diagnostico/paso5_asignacion_k3.csv`
**Fuentes cualitativas:** `Proyecto_integrador-_Taller-Barragan-Diaz-Quiroga.pdf` (14 entrevistas, User Personas y Mapas de Empatía).

> 📊 = dato de la base (n = 1.000) · 🎙️ = dato del estudio cualitativo (n = 14) · 💡 = interpretación o recomendación del equipo/agente.
> Las variables demográficas y categóricas **no entraron al modelo**; aquí solo describen los clusters. El "índice" compara con el total de la base: 100 = igual al promedio, 150 = 1,5 veces más frecuente.

## Advertencias antes de leer
1. **La base no es una encuesta a espectadores de "La Primera Vez".** Es una base **sintética** de audiencia digital colombiana general (así lo dice su hoja "Fuentes y supuestos"). Los clusters describen tipos de audiencia digital; su relación con la serie sale de cruzarlos con las 14 entrevistas y debe presentarse como **hipótesis de correspondencia**, no como medición.
2. **La base no mide el abandono de series.** Como aproximación se usan `tension_gratificacion` y `riesgo_gratif_desplazada`.
3. **Inconsistencias internas del PDF**, a corregir antes de entregar:
   - "La Brecha" dice que *"13 de los 14 entrevistados caen dentro del rango 16–30 años"*, pero la tabla de cuotas tiene a E13 (44) y E14 (54), así que son **12 de 14**.
   - También dice que *"E14 (44 años) vio la serie completa junto a su esposo"*, pero según la tabla esa es **E13 (Belssy, 44)**. E14 (Sandra, 54) llegó por su hija.
   - El abandono se atribuye a *"E9, 30 años"*, pero la tabla lo registra con **23 años**.
   - El User Persona 1 dice que *"Jorge tiene 18 años"*, pero la tabla lo registra con **19**.

## Visión general 📊

| | **Cluster 0** | **Cluster 1** | **Cluster 2** |
|---|---|---|---|
| Nombre propuesto 💡 | **Exploradores Hiperconectados** | **Espectadores Familiares de Pantalla Compartida** | **Suscriptores de Valor** |
| Tamaño | 415 (41,5%) | 411 (41,1%) | 174 (17,4%) |
| Correspondencia cualitativa 🎙️ | User Persona 1 — Daniel, "El Explorador Casual" | User Persona 2 — Laura, "La Espectadora Nostálgica" | Sin User Persona (segmento no cubierto por las entrevistas) |
| Edad media / mediana | 29,7 / 28 | 47,8 / 47 | 39,5 / 38 |
| Horas en redes / nº de redes | 4,2 h / 6,1 | 2,8 h / 4,4 | 3,5 h / 5,3 |
| Gasto medio en contenido | $11.426 (38,6% gasta $0) | $11.123 (39,4% gasta $0) | **$72.476 (0% gasta $0)** |
| Motivación U&G más diferencial | Identidad, evasión, pasar el tiempo, interacción social | **Información** (4,05 frente a 3,65) | Todas en la media: lo que lo distingue es el pago |
| % mujeres | 52,3% | 49,1% | 49,4% |

**Correspondencia con los User Personas** 📊:
- De todas las personas de **18–24 años** de la base, el **75,3%** cae en el Cluster 0.
- De todas las **mujeres de 40–55 años**, el **61,1%** cae en el Cluster 1.
- La edad nunca entró al modelo: estos grupos surgen solo de conducta y motivación.

**Qué variables diferencian más los clusters** 📊 (V de Cramer, de 0 a 1):
- **Asociación fuerte:** disposición a pagar (0,58) y grupo etario (0,43).
- **Asociación media (0,30–0,33):** generación de contenido, relación parasocial, pertenencia a comunidades, estrato y sensibilidad al precio.
- **Sin diferencias (≤ 0,07):** dispositivo, región y **género (0,02)**.

---

## CLUSTER 0 — "Exploradores Hiperconectados" (41,5%)

### 1. Nombre del cluster
**Exploradores Hiperconectados**: la versión cuantitativa de *Daniel, el Explorador Casual*.

### 2. Perfil cuali-cuantitativo
**Sociodemográfico** 📊
- **Edad:** es el cluster más joven (media 29,7). El **78%** tiene entre 18 y 34 años: 35,2% de 18–24 (índice 181) y 42,7% de 25–34 (índice 162).
- **Género:** equilibrado (52,3% mujeres).
- **Estrato y educación:** estrato medio-bajo (2,55); educación secundaria o técnica (65%).
- **Rol** 🎙️: estudiante universitario o joven en el inicio de su vida laboral (Daniel, 21 años, Bogotá).

**Hábitos de consumo** 📊
| Rasgo | Dato |
|---|---|
| Intensidad | 4,2 h/día en redes, 6 redes y 2,6 h/día de video (el máximo de los tres clusters) |
| Pantalla | Smartphone 82,9% (el más alto). Smart TV solo 7,5% |
| Momento | Noche (56,9%) y **madrugada 10,8%** (índice 131) |
| Modalidad | **Solo/a en smartphone 31,1%** (índice 117); con amigos 7,2% (índice 125). En familia solo 25,8% (índice 85) |
| Plataformas | Netflix 25,8% (índice 114) y TikTok 24,6% (índice 135). Redes principales: Instagram y TikTok |
| Descubrimiento | **Algoritmo 28,9%** (el más alto, índice 119) y redes sociales 19,3% (índice 119) |
| Ritmo | **Maratón 25,1%** (índice 114). Maratón frecuente: 28,0% |
| Comportamiento digital | **Creador activo 55,7%** (índice 155), vínculo parasocial fuerte 47,7% (índice 163), comunidad activa 64,6% (índice 152) |
| TV abierta | "Nunca la ve" 16,6% (índice 141) y "la abandonó por streaming" 19,3% (índice 126) |

🎙️ Entrevistas: consumo principalmente individual en pantallas variadas (iPad, TV, computador). La serie suele convertirse después en conversación con amigos o familia.

### 3. Justificación relacionada con "La Primera Vez"
- **Necesidad que satisface:**
  - 📊 Este cluster puntúa más alto en **evasión (3,80), pasar el tiempo (4,11), entretenimiento (4,27) e identidad (3,71)**, y más bajo en información (3,21).
  - En gratificación buscada sobresalen "Relajación" (19,3%, índice 113), "Llenar el tiempo libre" (índice 122) y "Expresar quién soy" (índice 135).
  - 🎙️ Coincide con Daniel: *"entretenerme… distraerme… desconectarme un ratico"* (E3).
  - 💡 La serie ofrece **identificación con personajes jóvenes** (primeras veces, primer amor, autodescubrimiento). Eso conecta con la alta puntuación en identidad del cluster.
- **Activadores de entrada:**
  - 📊 Es el cluster más guiado por **algoritmo (28,9%) y redes sociales (19,3%)**.
  - 🎙️ Lo confirman las entrevistas: el top de Netflix (E4), el video previo (E9), la miniatura (E11) y la recomendación de amigos (E7, E11).
- **Gratificación obtenida:**
  - 🎙️ **Aprendizaje histórico inesperado**: *"no pensé que fuera a darme un poco de contexto histórico colombiano"* (E11).
  - 📊 Encaja con que es el cluster con **menor motivación informativa**: el aprendizaje llega sin buscarlo. El 14,7% dice "obtener más de lo que busca".
- **Riesgo de abandono:**
  - 📊 El 45,3% tiene riesgo **alto** de que la gratificación obtenida desplace a la buscada (índice 121, el más alto): empieza con una intención y termina haciendo otra cosa.
  - 📊 Además, el 10,6% combina *ver solo* y *llegar por algoritmo*, el patrón que el estudio asocia con el abandono.
  - 🎙️ Los dos abandonos del estudio (E4 y E9) son hombres jóvenes que veían la serie solos y llegaron por el algoritmo. Ambos casos encajan en este cluster.

### 4. Estrategia y recomendaciones 💡
**Ganchos narrativos contra el abandono**
- **Dinamismo en las tramas secundarias.** El riesgo que señalan las entrevistas es el *conflicto romántico repetitivo* (E9). Conviene alternar el romance con tramas de época (política, censura, movimiento estudiantil, derechos de las mujeres) que funcionen como giros y no como "clase".
- **Hacer visible el valor de aprendizaje *después* del entretenimiento**, nunca como promesa principal. El insight del Mapa de Empatía es que el aprendizaje funciona mejor como ganancia inesperada.
  - *Easter eggs* históricos al final de los episodios.
  - Cápsulas "¿Qué pasaba en Colombia en 1970?" en TikTok e Instagram.
- **Cliffhangers al cierre de cada capítulo** para aprovechar la tendencia a la maratón (índice 114).

**Comunicación, diseño digital y marketing**
- **Convertir el consumo solitario en conversación social.** Es la palanca principal contra el abandono.
  - Clips cortos en TikTok e Instagram para compartir (el cluster crea contenido activamente).
  - Retos o dúos ("mi primera vez…") y *stickers* de época.
  - Invitar a comentar con amigos, que son la vía de validación que retiene.
- **Colaboraciones con creadores de contenido:** el 47,7% siente un vínculo fuerte con creadores (índice 163).
- **Diseño en Netflix:** miniaturas y *previews* centradas en personajes jóvenes y en su identificación. Probar A/B distintas portadas (romance frente a rebeldía o época).
- **Brecha de género:** en este cluster la base es 52% mujeres y 47% hombres, así que la mitad masculina es real y está disponible.
  - Las piezas para hombres jóvenes pueden destacar humor, amistad, rebeldía frente a la autoridad del colegio y conflicto político, no solo el romance.
  - Así se ataca directamente el perfil que abandonó en el estudio (hombre, joven, solo, algoritmo).

---

## CLUSTER 1 — "Espectadores Familiares de Pantalla Compartida" (41,1%)

### 1. Nombre del cluster
**Espectadores Familiares de Pantalla Compartida**: el cluster donde vive *Laura, la Espectadora Nostálgica*.

### 2. Perfil cuali-cuantitativo
**Sociodemográfico** 📊
- **Edad:** es el cluster adulto (media 47,8, mediana 47). El **85%** tiene 35 años o más: 35–44 (27,5%), 45–54 (25,3%, índice 156), 55–64 (20,4%, índice 186) y 65+ (11,9%, índice 199).
- **Género:** equilibrado en la base (49,1% mujeres).
- **Estrato y educación:** estrato medio-bajo (2,57); la mayor proporción de "primaria o menos" (índice 154).
- **Rol** 🎙️: mujer profesional casada y con hijos (Laura, 49 años, Bogotá; E13 abogada de 44, E14 epidemióloga de 54).

**Hábitos de consumo** 📊
| Rasgo | Dato |
|---|---|
| Intensidad | La más baja: 2,8 h/día en redes, 4,4 redes y 1,6 h/día de video |
| Pantalla | Smartphone 74,7%. Es el cluster con **más Smart TV (10,7%, índice 116)** y tablet (índice 134) |
| Momento | Noche 56,2% y **mañana 15,6%** (índice 121) |
| Modalidad | **En familia, con TV o pantalla compartida: 35,0%** (el más alto, índice 116). En pareja 17,8%. **52,8% ve acompañado** |
| Ritmo | **Un episodio por sesión 27,7%** (índice 115) y **fragmentado 20,0%** (índice 117). Menos maratón (índice 87) |
| Formato | **Video largo 27,7%** (índice 122) |
| Descubrimiento | Recomendación de amigos o familia 24,3%, búsqueda activa (índice 108) y mención en medios (índice 128). Menos algoritmo (índice 86) |
| TV abierta | **Sigue siendo su fuente principal para el 29,9%** (índice 153) |
| Plataformas | Netflix 17,8% (índice 78). **"Ninguna" plataforma de video: 14,1%** (índice 168) |
| Comportamiento digital | **Consumidor pasivo 40,4%** (índice 176), vínculo parasocial débil o inexistente 55,7%, sin comunidades en línea 19,2% (índice 188) |

🎙️ Entrevistas: televisor como pantalla principal, acompañada por el esposo o las hijas, en momentos libres, noches o fines de semana.

### 3. Justificación relacionada con "La Primera Vez"
- **Necesidad que satisface:**
  - 📊 Es el cluster con **mayor motivación informativa**: `ug_informacion` 4,05; motivo primario "Información" 22,6% (índice 141).
  - 📊 En necesidad base destacan "Curiosidad" (índice 124) y "Seguridad informativa" (índice 133). En gratificación buscada, "Estar al día" (índice 151) y "Aprender algo nuevo" (índice 117).
  - 🎙️ Las entrevistadas buscan **desconexión emocional y reconexión con su propia juventud**: *"volver a vivir una época"* (E14).
  - 💡 Síntesis: para este segmento la serie es **memoria + contexto**. La Bogotá de los 70 y la historia del país conectan a la vez con su nostalgia y con su interés informativo (los acontecimientos del país y la literatura que valora E14).
- **Activadores de entrada:**
  - 📊 Recomendación de su círculo cercano y búsqueda activa, más que algoritmo.
  - 🎙️ Encaja con la **recomendación intergeneracional**: E14 vio a su hija viendo un capítulo y después buscó la serie. E13 la encontró en la pantalla de inicio de Netflix.
  - 💡 Los hijos e hijas del Cluster 0 son los "embajadores" naturales hacia este cluster.
- **Gratificación obtenida:**
  - 🎙️ **Nostalgia positiva, bienestar y memoria compartida**: *"recordamos nuestros tiempos"* y *"muy reconfortante"* (E13).
  - 📊 Consistente con que es el cluster que más ve **en familia o en pareja (52,8%)**.
- **Riesgo de abandono:**
  - 📊 El más bajo de los tres: 29,9% de riesgo alto de desplazamiento (índice 80).
  - 📊 Su patrón es **fragmentado** (índice 117): no abandona, pero **pausa y retoma**.
  - 🎙️ Lo mismo le pasa a E14, que "la retoma cuando dispone de tiempo".
  - 💡 El obstáculo es el **tiempo**, no la narrativa.

### 4. Estrategia y recomendaciones 💡
**Ganchos narrativos contra el abandono**
- **Fidelizar mediante la conversación social y familiar:** la serie funciona como detonante de recuerdos compartidos.
  - Episodios con capítulos autoconclusivos que respeten el patrón de un episodio por sesión.
  - Recapitulaciones al inicio de cada capítulo, para quien retoma días después.
  - Recordatorios de "continuar viendo" en la TV.
- **Referencias de época verificables:** música, lugares de Bogotá y noticias de los 70. Alimentan tanto la nostalgia como su motivación informativa.

**Comunicación, diseño digital y marketing**
- **Campaña intergeneracional** del tipo "Véanla juntas / Pregúntale a tu mamá cómo fue su primera vez". Activa el camino hija → madre documentado en E14 y aprovecha el consumo familiar (35%).
- **Canales:** es el cluster donde la **TV abierta sigue siendo su fuente principal para el 29,9%**, y hay menos Netflix (17,8%) y más "ninguna plataforma" (14,1%).
  - La coproducción con Caracol Televisión es una ventaja: promoción cruzada en TV abierta, prensa y medios (mención en medios, índice 128).
  - Invitar a probar Netflix en el televisor del hogar.
- **Diseño digital:** priorizar la experiencia en Smart TV (tráiler en la pantalla de inicio, portada con estética de época). A este cluster el diseño "casi no le importa" más que al resto (índice 124), así que conviene no depender de la interfaz y reforzar las recomendaciones humanas.
- **Brecha de género:**
  - 🎙️ El estudio encontró un sesgo femenino.
  - 📊 En la base, este cluster es 49% mujeres y 50% hombres, y los hombres de 45–54 pesan lo mismo que las mujeres (12,4% frente a 12,7%).
  - 💡 Oportunidad: el "esposo" que acompaña a E13 ya está en la sala. Piezas sobre el Colegio, el fútbol o la política de los 70 y la memoria masculina de esa época pueden convertir al acompañante en espectador activo.

---

## CLUSTER 2 — "Suscriptores de Valor" (17,4%)

### 1. Nombre del cluster
**Suscriptores de Valor**: el segmento que paga. **No tiene User Persona en el estudio cualitativo.**

### 2. Perfil cuali-cuantitativo
**Sociodemográfico** 📊
- **Edad:** transversal (media 39,5). 16% de 18–24, 26% de 25–34, 21% de 35–44 y 20% de 45–54.
- **Género:** equilibrado (49,4% mujeres).
- **Estrato alto:** 3,85 de media. Estratos 5–6 = 31,6% (índices 335 y 277).
- **Educación:** **posgrado 24,1%** (índice 268).
- 💡 **Rol:** profesional de ingresos medio-altos, probable titular de la cuenta y quien decide la suscripción del hogar.

**Hábitos de consumo** 📊
| Rasgo | Dato |
|---|---|
| Gasto | **$72.476/mes** (6,5 veces los otros clusters). **92% con disposición a pagar alta**; 51,1% "paga sin pensarlo" (índice 284) |
| Intensidad | Media (3,5 h/día en redes, 2,1 h/día de video) |
| Pantalla | Smartphone 77,6%, Smart TV 9,8%, y **solo/a en computador 13,2%** (índice 141) |
| Modalidad | Mixta: en familia 29,3% y solo/a 39,1% |
| Plataformas | **Netflix 27,0%** (el más alto, índice 119), Disney+ y Prime por encima del promedio |
| Descubrimiento | **Recomendación de amigos o familia 27,0%** (índice 117), **búsqueda activa 17,8%** (índice 116) y publicidad digital (índice 117) |
| Ritmo | **Un episodio por sesión 28,7%** (índice 119). Poca maratón |
| Formato | Podcast/audio (índice 129) y video largo |
| Diseño digital | **El diseño es "determinante" para el 21,3%** (índice 160) |
| Satisfacción | **Satisfacción plena 31,0%** (índice 134). Indiferencia solo 7,5% (índice 53) |

### 3. Justificación relacionada con "La Primera Vez"
- **Necesidad que satisface:**
  - 📊 Sus puntuaciones U&G están en el promedio. No los mueve una gratificación extrema, sino **consumir contenido de calidad que justifique lo que pagan**.
  - 📊 En gratificación buscada sobresalen "Sentirse acompañado/a" (índice 144), "Emoción y suspenso" (índice 123) y "Desconectarse de la rutina" (índice 120). En necesidad base, "Conexión emocional" (índice 120) y "Pertenencia" (índice 117).
  - 💡 La serie les ofrece **producción de prestigio** (primera franquicia colombiana de Netflix, literatura, historia), algo que este perfil educado y dispuesto a pagar valora.
- **Activadores de entrada:** búsqueda activa y recomendación de su entorno, antes que el algoritmo. Llegan con intención.
- **Gratificación obtenida:**
  - 📊 Es el cluster con **mayor satisfacción plena (31%)**.
  - 💡 Para ellos, la serie **confirma el valor de la suscripción**. Por su amplitud de edades, pueden funcionar como **puente**: adultos que la ven con sus hijos adolescentes (la serie es 16+).
- **Limitación:** las 14 entrevistas no permiten caracterizar cualitativamente este segmento. 💡 Conviene hacer 2–3 entrevistas adicionales a titulares de cuenta de estrato 4–6.

### 4. Estrategia y recomendaciones 💡
**Ganchos narrativos contra el abandono**
- Ritmo pausado de **un episodio por sesión**, con tramas bien construidas y referencias culturales (autores, libros, hechos históricos) que premien la atención.
- Continuidad de la franquicia: anunciar temporadas o *spin-offs* refuerza la percepción de valor.

**Comunicación, diseño digital y marketing**
- **Diseño y calidad de la interfaz:** el 21% elige o abandona por el diseño. Conviene cuidar arte, portadas, subtítulos y la ficha de la serie con contexto histórico.
- **Contenidos complementarios** en formato podcast (índice 129) sobre la época, la producción y la literatura de la serie.
- **Posicionamiento de prestigio** en prensa y reseñas. La mención en medios y la búsqueda activa son sus rutas de entrada.
- **Plan familiar:** mensaje de "serie para ver con tus hijos adolescentes", conectando con los Clusters 0 y 1.
- **Brecha de género:** el 50% de este segmento es masculino y paga. 💡 Destacar el valor histórico, político y de producción amplía la serie más allá del romance.

---

## Síntesis: brecha de audiencia y patrón de abandono frente a la base

| Hallazgo del estudio 🎙️ | Qué muestra la base 📊 | Lectura 💡 |
|---|---|---|
| **Sesgo femenino** (10 de 14 entrevistados) | El género **no diferencia los clusters** (V de Cramer = 0,02). Los tres tienen entre 49% y 52% de mujeres | El sesgo no viene de la estructura del mercado digital, que es 50/50 en todos los segmentos. Es específico de la serie o de su comunicación. Por eso la mitad masculina de cada cluster es una **audiencia potencial no capturada**, y la comunicación actual (romance, "primeras veces") podría estar filtrando el alcance hacia mujeres |
| **Solo + algoritmo, asociado a abandono** (E4, E9; 2 de 14) | La base no mide abandono. Entre quienes ven **solos y llegan por el algoritmo** (n = 94), la **indiferencia** ("consume sin expectativa clara") casi se duplica: 24,5% frente a 12,9%. "Obtiene más de lo que busca" baja de 15,7% a 11,7% | Evidencia **indirecta y consistente** con la hipótesis: ese consumo genera un vínculo más débil. La frustración alta, en cambio, no aumenta (5,3% frente a 10,6%), así que el riesgo es la *indiferencia*, no la decepción. Este patrón se concentra en el Cluster 0 (10,6%) |
| **Audiencia 16–30 bien alcanzada** | Los jóvenes están sobre todo en el Cluster 0 | La serie llega a su público declarado. El crecimiento está en el Cluster 1 (vía intergeneracional) y en el Cluster 2 (prestigio y pago) |

## Decisiones y verificaciones pendientes para el equipo
1. Validar los nombres propuestos de los clusters.
2. Corregir las 4 inconsistencias del PDF señaladas al inicio.
3. Explicitar en la entrega que la correspondencia cluster ↔ User Persona es una **triangulación** entre la base sintética general y la muestra cualitativa de 14 casos, no una medición sobre espectadores reales de la serie.
4. Decidir si se incorpora un tercer User Persona para el Cluster 2, lo que requeriría entrevistas adicionales.

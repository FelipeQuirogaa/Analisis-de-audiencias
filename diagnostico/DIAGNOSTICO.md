# Diagnóstico y auditoría de la base — Segundo Parcial (paso 1, sin K-means)

**Archivo procesado:** `Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx` (hoja `Base de datos`).
**Código:** `diagnostico/diagnostico_base.py` · **Salida completa sin editar:** `diagnostico/salida_diagnostico.txt`.

> Convención del documento: 📊 = resultado obtenido directamente de la base con pandas · 💡 = recomendación metodológica (juicio, no dato).

---

## 0. Estructura del archivo 📊

El archivo **no contiene solo la base**. Tiene 9 hojas:

| Hoja | Dimensión | Contenido |
|---|---|---|
| Base de datos | 1.000 filas × 41 columnas | Datos a analizar |
| Diccionario de variables | 41 variables | Grupo, tipo, descripción, valores/rango |
| Fuentes y supuestos | texto | Dice "V2 — 1.000 registros, **29 variables**"; datos **sintéticos** calibrados con DANE, DataReportal, Kantar, etc. |
| Universo y expansión | tabla | N = 37,7 M, n = 1.000, f = 37.700 |
| Estadística descriptiva | tabla | Descriptivos de 10 variables (V2) |
| **Perfil de segmentos** | tabla | **Resultado de un K-means previo (k=4, S1–S4)** |
| **Datos+segmento** | 1.000 × 31 | Base V2 + columnas `segmento` y `nombre_segmento` |
| **Validación Estadística** | tabla | Silueta, Calinski-Harabasz, Davies-Bouldin para k=2…7 |
| **Mapa de segmentos** | texto | Mapa 2×2 de los 4 segmentos previos |

⚠️ Hay una **segmentación K-means ya hecha** (sobre la versión V2, con 12 variables y k = 4). Ver §5.8.

---

## 1. Inventario de variables 📊

Tipo real = `dtype` que pandas asigna al leer el Excel. Los 41 nombres de la base coinciden **exactamente** con los 41 del diccionario (ninguna sobra, ninguna falta, sin espacios en los nombres).

| # | Variable | dtype real | Clase | Tipo según diccionario | Descripción (diccionario) |
|---|---|---|---|---|---|
| 1 | `id` | texto | Identificador | Texto | Identificador único (AUD-0001…AUD-1000) |
| 2 | `edad` | int64 | Numérica | Numérica (años) | Edad (18–75) |
| 3 | `grupo_etario` | texto | Categórica | Categórica | Rango etario derivado de la edad |
| 4 | `genero` | texto | Categórica | Categórica | Género declarado |
| 5 | `estrato` | int64 | Numérica (ordinal) | Ordinal 1–6 | Estrato socioeconómico (DANE) |
| 6 | `region` | texto | Categórica | Categórica | Región de residencia |
| 7 | `nivel_educativo` | texto | Categórica | Categórica | Máximo nivel educativo |
| 8 | `ug_entretenimiento` | int64 | Numérica (Likert) | Likert 1–5 | U&G: entretenimiento/diversión |
| 9 | `ug_informacion` | int64 | Numérica (Likert) | Likert 1–5 | U&G: información/vigilancia del entorno |
| 10 | `ug_identidad` | int64 | Numérica (Likert) | Likert 1–5 | U&G: identidad personal/autoexpresión |
| 11 | `ug_interaccion_social` | int64 | Numérica (Likert) | Likert 1–5 | U&G: integración e interacción social |
| 12 | `ug_evasion` | int64 | Numérica (Likert) | Likert 1–5 | U&G: evasión/escape |
| 13 | `ug_pasar_tiempo` | int64 | Numérica (Likert) | Likert 1–5 | U&G: pasar el tiempo/hábito |
| 14 | `dispositivo_principal` | texto | Categórica | Categórica | Dispositivo principal de acceso |
| 15 | `horas_diarias_redes` | float64 | Numérica | Numérica (horas) | Horas diarias en redes sociales |
| 16 | `franja_horaria_pico` | texto | Categórica | Categórica | Franja de mayor consumo |
| 17 | `num_redes_usadas` | int64 | Numérica (conteo) | Numérica entera | Nº de redes usadas al mes |
| 18 | `red_social_principal` | texto | Categórica | Categórica | Red a la que dedica más tiempo |
| 19 | `plataforma_video_principal` | texto | Categórica | Categórica | Plataforma de video más consumida |
| 20 | `categoria_contenido_preferida` | texto | Categórica | Categórica | Categoría de contenido preferida |
| 21 | `formato_preferido` | texto | Categórica | Categórica | Formato de contenido preferido |
| 22 | `gasto_mensual_contenido_cop` | int64 | Numérica | Numérica (COP/mes) | Gasto mensual en suscripciones/contenido |
| 23 | `disposicion_pago` | texto | Categórica (ordinal) | Ordinal | Disposición declarada a pagar |
| 24 | `contexto_visionado` | texto | Categórica | Categórica | Contexto social/espacial de visionado |
| 25 | `via_llegada` | texto | Categórica | Categórica | Mecanismo de descubrimiento de contenido |
| 26 | `patron_consumo` | texto | Categórica | Categórica | Ritmo/patrón de consumo audiovisual |
| 27 | `rol_diseno_digital` | texto | Categórica (ordinal) | Categórica ordinal | Influencia del diseño UX/UI en el consumo |
| 28 | `relacion_tv_abierta` | texto | Categórica | Categórica | Relación con la TV abierta |
| 29 | `tension_gratificacion` | texto | Categórica | Categórica | Brecha gratificación buscada vs. obtenida |
| 30 | `motivo_primario` | texto | Categórica | Categórica | Motivación dominante (derivada del perfil U&G) |
| 31 | `necesidad_base` | texto | Categórica | Categórica | Necesidad subyacente del consumo |
| 32 | `gratificacion_buscada` | texto | Categórica | Categórica | Gratificación específica buscada |
| 33 | `horas_video_dia` | float64 | Numérica | Numérica (horas) | Horas diarias de consumo de video |
| 34 | `binge_watching` | texto | Categórica (ordinal) | Categórica ordinal | Frecuencia de maratones |
| 35 | `genera_contenido` | texto | Categórica (ordinal) | Categórica ordinal | Nivel de creación de contenido propio |
| 36 | `comparacion_social` | int64 | Numérica (Likert) | Likert 1–5 | Comparación con otros en redes |
| 37 | `nivel_fomo` | int64 | Numérica (Likert) | Likert 1–5 | Intensidad del FOMO |
| 38 | `relacion_parasocial` | texto | Categórica (ordinal) | Categórica ordinal | Vínculo con creadores/influenciadores |
| 39 | `pertenencia_comunidades` | texto | Categórica (ordinal) | Categórica ordinal | Participación en comunidades en línea |
| 40 | `sensibilidad_precio` | texto | Categórica (ordinal) | Categórica ordinal | Sensibilidad al precio |
| 41 | `riesgo_gratif_desplazada` | texto | Categórica (ordinal) | Categórica ordinal | Riesgo de que la gratificación obtenida desplace a la buscada |

## 2. Numéricas vs. categóricas 📊

- **Numéricas (14):** `edad`, `estrato`, `ug_entretenimiento`, `ug_informacion`, `ug_identidad`, `ug_interaccion_social`, `ug_evasion`, `ug_pasar_tiempo`, `horas_diarias_redes`, `num_redes_usadas`, `gasto_mensual_contenido_cop`, `horas_video_dia`, `comparacion_social`, `nivel_fomo`.
  - Continuas/de razón: `edad`, `horas_diarias_redes`, `horas_video_dia`, `gasto_mensual_contenido_cop`. Conteo: `num_redes_usadas`.
  - Ordinales codificadas como número: `estrato` (1–6) y 8 escalas Likert 1–5 (6 `ug_*` + `comparacion_social` + `nivel_fomo`).
- **Categóricas (26) + identificador (`id`)**. De ellas, **9 son ordinales en texto** según el diccionario: `disposicion_pago`, `rol_diseno_digital`, `binge_watching`, `genera_contenido`, `relacion_parasocial`, `pertenencia_comunidades`, `sensibilidad_precio`, `riesgo_gratif_desplazada` (y `grupo_etario`, derivada de `edad`).

## 3. Estadística descriptiva de las 14 numéricas 📊

Desviación estándar muestral (n−1). n = 1.000 en todas.

| Variable | Media | Mediana | Desv. est. | Mín | Máx | Rango | Faltantes |
|---|---:|---:|---:|---:|---:|---:|---:|
| `edad` | 38.85 | 36.00 | 14.64 | 18.00 | 75.00 | 57.00 | 0 |
| `estrato` | 2.79 | 3.00 | 1.19 | 1.00 | 6.00 | 5.00 | 0 |
| `ug_entretenimiento` | 4.14 | 4.00 | 0.72 | 2.00 | 5.00 | 3.00 | 0 |
| `ug_informacion` | 3.65 | 4.00 | 0.95 | 1.00 | 5.00 | 4.00 | 0 |
| `ug_identidad` | 3.35 | 3.00 | 0.98 | 1.00 | 5.00 | 4.00 | 0 |
| `ug_interaccion_social` | 3.95 | 4.00 | 0.78 | 2.00 | 5.00 | 3.00 | 0 |
| `ug_evasion` | 3.56 | 4.00 | 0.87 | 1.00 | 5.00 | 4.00 | 0 |
| `ug_pasar_tiempo` | 3.86 | 4.00 | 0.80 | 1.00 | 5.00 | 4.00 | 0 |
| `horas_diarias_redes` | 3.51 | 3.50 | 1.33 | 0.30 | 7.80 | 7.50 | 0 |
| `num_redes_usadas` | 5.23 | 5.00 | 1.71 | 1.00 | 9.00 | 8.00 | 0 |
| `gasto_mensual_contenido_cop` | 21,924.3 | 9,564.5 | 27,381.2 | 0.0 | 116,524.0 | 116,524.0 | 0 |
| `horas_video_dia` | 2.11 | 2.00 | 1.16 | 0.20 | 6.50 | 6.30 | 0 |
| `comparacion_social` | 3.57 | 4.00 | 1.00 | 1.00 | 5.00 | 4.00 | 0 |
| `nivel_fomo` | 3.83 | 4.00 | 1.01 | 1.00 | 5.00 | 4.00 | 0 |

## 4. Frecuencias de las categóricas 📊

Se excluye `id` (1.000 valores únicos). **Ninguna categórica tiene faltantes.**

**`grupo_etario`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| 25-34 | 264 | 26.4% |
| 35-44 | 210 | 21.0% |
| 18-24 | 194 | 19.4% |
| 45-54 | 162 | 16.2% |
| 55-64 | 110 | 11.0% |
| 65+ | 60 | 6.0% |

**`genero`** (3 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Femenino | 505 | 50.5% |
| Masculino | 488 | 48.8% |
| Otro | 7 | 0.7% |

**`region`** (8 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Bogotá | 199 | 19.9% |
| Región Caribe | 174 | 17.4% |
| Antioquia | 173 | 17.3% |
| Santanderes | 101 | 10.1% |
| Valle del Cauca | 92 | 9.2% |
| Región Central | 89 | 8.9% |
| Eje Cafetero | 88 | 8.8% |
| Otras regiones | 84 | 8.4% |

**`nivel_educativo`** (5 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Secundaria | 302 | 30.2% |
| Técnico/Tecnológico | 297 | 29.7% |
| Universitario | 270 | 27.0% |
| Posgrado | 90 | 9.0% |
| Primaria o menos | 41 | 4.1% |

**`dispositivo_principal`** (4 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Smartphone | 786 | 78.6% |
| Computador | 93 | 9.3% |
| Smart TV | 92 | 9.2% |
| Tablet | 29 | 2.9% |

**`franja_horaria_pico`** (4 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Noche | 570 | 57.0% |
| Tarde | 218 | 21.8% |
| Mañana | 129 | 12.9% |
| Madrugada | 83 | 8.3% |

**`red_social_principal`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| WhatsApp | 270 | 27.0% |
| Instagram | 208 | 20.8% |
| Facebook | 176 | 17.6% |
| TikTok | 156 | 15.6% |
| YouTube | 137 | 13.7% |
| X (Twitter) | 53 | 5.3% |

**`plataforma_video_principal`** (7 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| YouTube | 289 | 28.9% |
| Netflix | 227 | 22.7% |
| TikTok | 182 | 18.2% |
| Ninguna | 84 | 8.4% |
| Disney+ | 82 | 8.2% |
| Prime Video | 79 | 7.9% |
| Max | 57 | 5.7% |

**`categoria_contenido_preferida`** (8 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Música | 176 | 17.6% |
| Entretenimiento/Humor | 156 | 15.6% |
| Gastronomía | 127 | 12.7% |
| Viajes | 126 | 12.6% |
| Deportes | 123 | 12.3% |
| Noticias | 112 | 11.2% |
| Tecnología | 97 | 9.7% |
| Educación | 83 | 8.3% |

**`formato_preferido`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Video corto | 269 | 26.9% |
| Video largo | 227 | 22.7% |
| Texto/artículos | 137 | 13.7% |
| Imágenes | 136 | 13.6% |
| Podcast/Audio | 129 | 12.9% |
| Transmisión en vivo | 102 | 10.2% |

**`disposicion_pago`** (4 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Ninguna | 315 | 31.5% |
| Baja | 268 | 26.8% |
| Media | 214 | 21.4% |
| Alta | 203 | 20.3% |

**`contexto_visionado`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| En familia (TV/pantalla compartida) | 302 | 30.2% |
| Solo/a en smartphone | 266 | 26.6% |
| En pareja | 168 | 16.8% |
| En transporte/desplazamiento | 112 | 11.2% |
| Solo/a en computador | 94 | 9.4% |
| Con amigos | 58 | 5.8% |

**`via_llegada`** (7 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Algoritmo de la plataforma (recomendación automática) | 244 | 24.4% |
| Recomendación de amigos/familia | 231 | 23.1% |
| Redes sociales (publicación o historia) | 162 | 16.2% |
| Búsqueda activa (barra de búsqueda) | 153 | 15.3% |
| Mención en medios/prensa | 76 | 7.6% |
| Tendencias/trending | 70 | 7.0% |
| Publicidad digital | 64 | 6.4% |

**`patron_consumo`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Un episodio por sesión | 241 | 24.1% |
| Maratón (varios episodios seguidos) | 219 | 21.9% |
| Fragmentado (pausar y retomar días después) | 171 | 17.1% |
| De fondo (mientras hace otra cosa) | 169 | 16.9% |
| Consumo social (ver juntos y comentar) | 100 | 10.0% |
| Zapping entre plataformas | 100 | 10.0% |

**`rol_diseno_digital`** (5 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Moderado (lo percibe pero no decide por eso) | 288 | 28.8% |
| Importante (lo nota y le influye) | 277 | 27.7% |
| Bajo (casi no lo nota) | 188 | 18.8% |
| Determinante (elige o abandona por diseño) | 133 | 13.3% |
| Indiferente | 114 | 11.4% |

**`relacion_tv_abierta`** (5 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Complementaria (ve ambas) | 356 | 35.6% |
| TV abierta sigue siendo su fuente principal | 196 | 19.6% |
| Solo eventos especiales (deportes, noticias en vivo) | 177 | 17.7% |
| La abandonó por streaming | 153 | 15.3% |
| Nunca ve TV abierta | 118 | 11.8% |

**`tension_gratificacion`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Satisfacción parcial (encuentra algo pero no exactamente) | 236 | 23.6% |
| Satisfacción plena (coincide lo buscado y lo obtenido) | 231 | 23.1% |
| Obtiene más de lo que busca (descubrimiento positivo) | 153 | 15.3% |
| Indiferencia (consume sin expectativa clara) | 140 | 14.0% |
| Frustración leve (demasiado contenido, difícil elegir) | 139 | 13.9% |
| Frustración alta (no encuentra lo que busca) | 101 | 10.1% |

**`motivo_primario`** (6 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Interacción social | 206 | 20.6% |
| Entretenimiento | 191 | 19.1% |
| Hábito y pasatiempo | 188 | 18.8% |
| Información | 160 | 16.0% |
| Evasión y escape | 134 | 13.4% |
| Identidad y autoexpresión | 121 | 12.1% |

**`necesidad_base`** (9 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Distracción y placer | 223 | 22.3% |
| Descanso emocional | 185 | 18.5% |
| Pertenencia | 142 | 14.2% |
| Curiosidad | 141 | 14.1% |
| Seguridad informativa | 99 | 9.9% |
| Conexión emocional | 72 | 7.2% |
| Reconocimiento | 60 | 6.0% |
| Autoexpresión | 53 | 5.3% |
| Control del entorno | 25 | 2.5% |

**`gratificacion_buscada`** (15 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Relajación | 170 | 17.0% |
| Diversión y risa | 111 | 11.1% |
| Compartir experiencias | 80 | 8.0% |
| Estar al día | 79 | 7.9% |
| Llenar el tiempo libre | 77 | 7.7% |
| Tener de qué hablar | 74 | 7.4% |
| Desconectarse de la rutina | 67 | 6.7% |
| Expresar quién soy | 59 | 5.9% |
| Aprender algo nuevo | 56 | 5.6% |
| Emoción y suspenso | 56 | 5.6% |
| Sentirse acompañado/a | 52 | 5.2% |
| Descubrir gustos propios | 33 | 3.3% |
| Vivir otras realidades | 32 | 3.2% |
| Inspiración creativa | 29 | 2.9% |
| Tomar mejores decisiones | 25 | 2.5% |

**`binge_watching`** (5 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Rara vez | 331 | 33.1% |
| Ocasional (fines de semana) | 324 | 32.4% |
| Frecuente (varias veces por semana) | 203 | 20.3% |
| Nunca | 110 | 11.0% |
| Siempre que puede | 32 | 3.2% |

**`genera_contenido`** (4 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Creador activo (publica regularmente) | 358 | 35.8% |
| Consumidor pasivo (solo observa) | 230 | 23.0% |
| Creador ocasional (publica a veces) | 217 | 21.7% |
| Reactivo (comenta y comparte, rara vez crea) | 195 | 19.5% |

**`relacion_parasocial`** (4 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Moderada (sigue a algunos creadores con interés) | 370 | 37.0% |
| Fuerte (siente cercanía con creadores, los sigue activamente) | 292 | 29.2% |
| Débil (los ve pero no siente conexión personal) | 247 | 24.7% |
| Inexistente (no sigue creadores ni influenciadores) | 91 | 9.1% |

**`pertenencia_comunidades`** (4 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Activa (participa en grupos o comunidades regularmente) | 424 | 42.4% |
| Pasiva (pertenece a grupos pero rara vez participa) | 315 | 31.5% |
| Ocasional (entra a foros o grupos solo cuando necesita algo) | 159 | 15.9% |
| Ninguna (no participa en comunidades en línea) | 102 | 10.2% |

**`sensibilidad_precio`** (3 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Alta (solo consume gratis o lo más barato) | 439 | 43.9% |
| Media (compara antes de pagar) | 381 | 38.1% |
| Baja (paga sin pensarlo) | 180 | 18.0% |

**`riesgo_gratif_desplazada`** (3 categorías, faltantes: 0)

| Categoría | n | % |
|---|---:|---:|
| Alto (frecuentemente termina haciendo algo distinto a lo planeado) | 373 | 37.3% |
| Bajo (generalmente obtiene lo que buscaba) | 321 | 32.1% |
| Medio (a veces se desvía de su intención original) | 306 | 30.6% |


---

## 5. Calidad de los datos

### 5.1 Faltantes 📊
- **0 valores NaN** en las 41 variables.
- **0 faltantes "disfrazados"** en texto (`""`, `NA`, `N/A`, `-`, `null`, `ns/nr`…).

### 5.2 Duplicados 📊
| Chequeo | Resultado |
|---|---|
| Filas completamente duplicadas | 0 |
| `id` duplicados | 0 |
| Filas duplicadas ignorando `id` | 0 |
| IDs fuera del patrón `AUD-####` / consecutivos faltantes | 0 / ninguno (AUD-0001…AUD-1000 completos) |
| Perfiles idénticos en las 14 numéricas | 0 |

### 5.3 Valores imposibles y rangos 📊
Ningún valor está fuera del rango declarado en el diccionario. Todas las Likert, `estrato`, `edad` y `num_redes_usadas` son enteras. `grupo_etario` es 100% coherente con `edad`.

| Variable | Rango diccionario | Rango observado | Observación |
|---|---|---|---|
| `horas_diarias_redes` | 0,3 – 9,0 | 0,3 – 7,8 | El máximo real no llega al declarado |
| `gasto_mensual_contenido_cop` | 0 – 132.500 | 0 – 116.524 | El máximo real no llega al declarado |
| `ug_entretenimiento` | 1 – 5 | **2 – 5** | Nadie respondió 1 → solo 4 niveles usados |
| `ug_interaccion_social` | 1 – 5 | **2 – 5** | Nadie respondió 1 → solo 4 niveles usados |

### 5.4 Atípicos (regla IQR ×1,5) 📊
| Variable | Atípicos | Comentario |
|---|---:|---|
| `gasto_mensual_contenido_cop` | 47 | > 83.442 COP. Además **322 ceros (32,2%)**; asimetría = 1,36; CV = 1,25 |
| `estrato` | 99 | Estratos 5 y 6 (artefacto de la regla IQR con Q1=2, Q3=3; no son errores) |
| `ug_identidad` | 31 | Respuestas = 1 |
| `comparacion_social` | 21 | Respuestas = 1 |
| `horas_video_dia` | 20 | > 5,05 h (asimetría 0,76) |
| `ug_entretenimiento` / `ug_informacion` | 13 / 12 | Respuestas = 2 / = 1 |
| `ug_evasion`, `horas_diarias_redes`, `ug_pasar_tiempo` | 5, 2, 1 | — |
| resto | 0 | — |

💡 En Likert, los "atípicos" IQR son respuestas legítimas de la escala; **no deberían tratarse como errores**. El único atípico con peso real para K-means es el gasto.

### 5.5 Formato 📊
- Sin espacios extremos/dobles ni categorías que colapsen al normalizar mayúsculas.
- Todas las categorías observadas aparecen literalmente en el diccionario.
- Las 9 variables ordinales de texto tienen etiquetas largas con explicación entre paréntesis (p. ej. `"Alta (solo consume gratis o lo más barato)"`); no son errores, pero **no tienen codificación numérica** en la base.
- El diccionario y las hojas auxiliares mezclan versiones: "Fuentes y supuestos" dice *V2 – 29 variables* y "Estadística descriptiva" dice *V2*; la base real tiene 41 variables (V3). El nombre del archivo es **V3**, no V2 como se menciona en el enunciado.

### 5.6 Baja variabilidad 📊
| Variable | Hallazgo |
|---|---|
| `ug_entretenimiento` | Solo 4 niveles; 50,4% responde el mismo valor; CV = 0,17 (el más bajo) |
| `ug_interaccion_social` | Solo 4 niveles; 47,8% en el valor modal; CV = 0,20 |
| `ug_pasar_tiempo` | 45,7% en el valor modal |
| `dispositivo_principal` | Smartphone = 78,6%; Tablet = 2,9% |
| `genero` | "Otro" = 7 casos (0,7%) |
| `necesidad_base` / `gratificacion_buscada` | Categorías con < 3% (Control del entorno 2,5%; Tomar mejores decisiones 2,5%); `gratificacion_buscada` tiene 15 categorías |

Ninguna variable es constante o casi constante.

### 5.7 Inconsistencias y relaciones que afectan a K-means 📊

**a) Escalas muy distintas.** Desv. estándar: gasto = 27.381; edad = 14,6; Likert ≈ 0,7–1,0. Sin estandarizar, el gasto dominaría por completo las distancias euclidianas.

**b) `disposicion_pago` casi determina el gasto.**

| disposicion_pago | n | Gasto medio | Gasto mín – máx | % gasto = 0 |
|---|---:|---:|---|---:|
| Ninguna | 315 | 0 | 0 – 0 | 100% |
| Baja | 268 | 7.944 | 0 – 19.561 | 3% |
| Media | 214 | 28.323 | 5.000 – 49.231 | 0% |
| Alta | 203 | 67.656 | 16.717 – 116.524 | 0% |

Los 322 ceros = 315 "Ninguna" + 7 "Baja". Usar ambas variables como base equivale a contar dos veces el mismo constructo.

**c) Contradicciones entre `sensibilidad_precio`, `disposicion_pago` y gasto.**
- 15 personas con sensibilidad **"Baja (paga sin pensarlo)"** tienen **gasto = 0**.
- 22 personas con sensibilidad **"Alta (solo consume gratis…)"** tienen disposición **"Alta"** y gastan ≥ 29.556 COP/mes.
- De los 15 primeros, 13 tienen además disposición "Ninguna". **Total de registros únicos con alguna de estas contradicciones: 37.**

**d) `motivo_primario` no coincide con el perfil `ug_*`.** El diccionario lo define como *"derivada del perfil de gratificaciones U&G"*, pero solo en **56,2%** de los registros la `ug_*` correspondiente al motivo es la más alta (incluyendo empates). Además, 57,2% de los registros tiene **empate** en el puntaje `ug_*` máximo, así que "la gratificación dominante" no está definida para la mayoría.

**e) Otras.** 84 personas con `plataforma_video_principal = "Ninguna"` ven 0,2–1,8 h de video/día (media 0,63) y 18 de ellas dicen hacer maratón "Frecuente" o "Siempre que puede". 30 registros tienen más horas de video que de redes (posible, porque son medidas distintas).

**f) Correlaciones altas entre numéricas (|r| ≥ 0,5).**

| Par | r |
|---|---:|
| `horas_diarias_redes` – `horas_video_dia` | 0,73 |
| `edad` – `nivel_fomo` | −0,64 |
| `edad` – `comparacion_social` | −0,56 |

Moderadas (0,4–0,5): `edad`–`num_redes_usadas` (−0,49), `nivel_fomo`–`horas_diarias_redes` (0,47), `estrato`–`gasto` (0,46), `ug_identidad`–`comparacion_social` (0,46), `edad`–`horas_diarias_redes` (−0,41). Las 6 `ug_*` están casi incorrelacionadas entre sí (|r| ≤ 0,11).

### 5.8 Segmentación previa dentro del archivo 📊
- `Datos+segmento` contiene los **mismos 1.000 IDs y valores idénticos** en las 29 columnas V2, más `segmento` y `nombre_segmento`. No incluye las 12 variables V3.
- Según "Validación Estadística", ese K-means usó 12 variables (edad, 6 `ug_*`, horas, nº redes, gasto, **disposición al pago** y estrato) y eligió k=4 con **silueta 0,109** (k=2 tenía 0,142).
- Los descriptivos de "Estadística descriptiva" coinciden exactamente con los recalculados.

💡 Riesgo metodológico: esas hojas pueden sesgar ("anclar") las decisiones del equipo o confundirse con resultados propios. No las he modificado ni eliminado.

---

## 6. Clasificación conceptual de numéricas para una futura segmentación 💡
(Solo clasificación; no se ha ejecutado ningún modelo.)

| Grupo | Variables | Nota |
|---|---|---|
| **A. Comportamiento / consumo** | `horas_diarias_redes`, `horas_video_dia`, `num_redes_usadas`, `gasto_mensual_contenido_cop` | Horas redes y horas video correlacionan 0,73. El gasto es asimétrico, con 32% de ceros |
| **B. Usos y Gratificaciones** | `ug_entretenimiento`, `ug_informacion`, `ug_identidad`, `ug_interaccion_social`, `ug_evasion`, `ug_pasar_tiempo` | Likert 1–5; entretenimiento e interacción social con poca variabilidad |
| **C. Otras numéricas** | Psicográficas sociales: `comparacion_social`, `nivel_fomo`. Demográficas: `edad`, `estrato` | FOMO y comparación están muy ligadas a edad. Edad y estrato suelen reservarse como descriptores en una segmentación psicográfica/conductual |

## 7. Categóricas para enriquecer y describir clusters 💡

| Tipo | Variables |
|---|---|
| **Motivacionales / psicográficas** | `motivo_primario`, `necesidad_base`, `gratificacion_buscada`, `tension_gratificacion`, `riesgo_gratif_desplazada`, `relacion_parasocial` |
| **Demográficas** | `grupo_etario`, `genero`, `region`, `nivel_educativo` (+ `edad` y `estrato` si no entran como base) |
| **Plataforma y consumo** | `dispositivo_principal`, `franja_horaria_pico`, `red_social_principal`, `plataforma_video_principal`, `categoria_contenido_preferida`, `formato_preferido`, `contexto_visionado`, `via_llegada`, `patron_consumo`, `binge_watching`, `relacion_tv_abierta`, `rol_diseno_digital` |
| **Comportamiento digital / económico** | `genera_contenido`, `pertenencia_comunidades`, `disposicion_pago`, `sensibilidad_precio` |

---

## 8. Diagnóstico para el siguiente paso

### 8.1 Numéricas candidatas para K-means 💡
- **Núcleo recomendado:** las 6 `ug_*` (grupo B) + comportamiento (grupo A): `horas_diarias_redes`, `num_redes_usadas`, `gasto_mensual_contenido_cop` y, si se decide, `horas_video_dia`.
- **Opcionales (decisión del equipo):** `comparacion_social`, `nivel_fomo`.
- **Mejor como descriptores:** `edad`, `estrato` (demográficas; además el estrato se relaciona con el gasto, r = 0,46).

### 8.2 Para enriquecimiento posterior 💡
Las 26 categóricas de §7, incluidas `disposicion_pago` y `sensibilidad_precio`, además de `edad` y `estrato` si quedan fuera de la base.

### 8.3 Problemas de calidad a tener en cuenta 📊→💡
1. **Escalas heterogéneas** (gasto en miles vs. Likert 1–5) → estandarizar (z-score o similar) antes de K-means.
2. **Gasto:** asimetría fuerte, 322 ceros y 47 atípicos → K-means es sensible a esto; valorar una transformación (p. ej. log(1+x)) o un recorte. **No se ha modificado nada.**
3. **Redundancia:** horas redes ↔ horas video (r = 0,73); `disposicion_pago` ↔ gasto (casi determinista); edad ↔ FOMO/comparación → si entran juntas, sobreponderan un mismo constructo.
4. **Likert con poca variabilidad** (`ug_entretenimiento`, `ug_interaccion_social`: solo 4 niveles) → aportan poca separación y crean muchos "empates" en la distancia.
5. **Inconsistencias lógicas** (37 registros únicos en precio/pago/gasto; `motivo_primario` coincide con la `ug_*` máxima solo en el 56%) → afectan sobre todo a la interpretación descriptiva de los clusters.
6. **Categorías raras** (`genero = Otro`, n = 7; varias con < 3%) → porcentajes inestables al cruzarlas por cluster.
7. **Datos sintéticos** (lo dice la propia hoja "Fuentes y supuestos") y **hojas con un K-means previo** (V2, k=4) dentro del archivo.
8. Desajustes de versión en la documentación (V2/V3, "29 variables", rangos máximos del diccionario).

### 8.4 Decisiones pendientes del equipo antes de ejecutar K-means 💡
1. ¿Qué variables forman la base: solo `ug_*`, `ug_*` + comportamiento, o se incluyen FOMO y comparación social?
2. ¿Edad y estrato entran en la base o solo se usan como descriptores?
3. ¿Se usan `horas_diarias_redes` y `horas_video_dia` juntas o solo una?
4. ¿Cómo se trata el gasto: tal cual, log(1+x), recorte de atípicos o fuera de la base?
5. ¿Qué método de estandarización (z-score, min-max)?
6. ¿Qué hacer con los 37 registros con contradicciones (mantener y documentar, marcar o excluir)? **No se ha eliminado ninguno.**
7. ¿Se ignoran explícitamente las hojas de segmentación previa (Perfil, Datos+segmento, Validación, Mapa) para no contaminar el análisis?
8. ¿Qué criterios se usarán para elegir k (codo, silueta, Calinski-Harabasz, interpretabilidad) y qué semilla / nº de inicializaciones?
9. ¿Las categóricas ordinales se recodifican a números para describir los clusters?
10. ¿Qué se hace con `genero = Otro` (n = 7) al describir los clusters?

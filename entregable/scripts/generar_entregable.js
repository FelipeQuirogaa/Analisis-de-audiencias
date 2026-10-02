const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Header, Footer,
  AlignmentType, HeadingLevel, WidthType, ShadingType, BorderStyle, LevelFormat, PageNumber,
  PageBreak, TableOfContents, VerticalAlign,
} = require("docx");

const REPO = "/home/user/Analisis-de-audiencias";
const OUT = path.join(REPO, "entregable", "Barragan_Diaz_Quiroga.docx");
const W = 9360; // ancho útil (Carta, márgenes de 1")
const NAVY = "323A4E", ACCENT = "2A78D6", LIGHT = "EEF3FA", GREY = "F3F3F1", BORDER = "BFC4CC";

// ---------- helpers ----------
function runs(text, base = {}) {
  // **negrita** y _cursiva_
  const out = [];
  const re = /(\*\*[^*]+\*\*|~[^~]+~)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const P = (text, opts = {}) => new Paragraph({ children: runs(text, opts.run || {}), spacing: { after: 120, line: 276 }, alignment: opts.align || AlignmentType.JUSTIFIED, ...(opts.p || {}) });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)], keepNext: true });
const H1nb = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)], keepNext: true });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(t)], keepNext: true });
const B = (text, level = 0) => new Paragraph({ children: runs(text), numbering: { reference: "bullets", level }, spacing: { after: 60, line: 264 } });
const N = (text) => new Paragraph({ children: runs(text), numbering: { reference: "nums", level: 0 }, spacing: { after: 60, line: 264 } });
const CAP = (t) => new Paragraph({ children: runs(t, { size: 18, color: "5C5C5A", italics: true }), spacing: { before: 60, after: 200 }, alignment: AlignmentType.LEFT });
const SRC = (t) => new Paragraph({ children: runs(t, { size: 17, color: "5C5C5A" }), spacing: { before: 40, after: 160 } });

const border = { style: BorderStyle.SINGLE, size: 4, color: BORDER };
const borders = { top: border, bottom: border, left: border, right: border };

function cellParas(content, opts) {
  const arr = Array.isArray(content) ? content : [content];
  return arr.map((t) => new Paragraph({
    children: runs(String(t), { size: opts.size || 18, bold: opts.bold, color: opts.color }),
    spacing: { after: 40, line: 252 },
    alignment: opts.align || AlignmentType.LEFT,
  }));
}
function table(headers, rows, widths, o = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const hdr = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => new TableCell({
      borders, width: { size: widths[i], type: WidthType.DXA },
      shading: { fill: NAVY, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 60, bottom: 60, left: 90, right: 90 }, verticalAlign: VerticalAlign.CENTER,
      children: cellParas(h, { bold: true, color: "FFFFFF", size: o.size || 18 }),
    })),
  });
  const body = rows.map((r, ri) => new TableRow({
    children: r.map((c, i) => new TableCell({
      borders, width: { size: widths[i], type: WidthType.DXA },
      shading: { fill: (o.firstColShade && i === 0) ? LIGHT : (ri % 2 ? "FAFAF9" : "FFFFFF"), type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 50, bottom: 50, left: 90, right: 90 },
      children: cellParas(c, { size: o.size || 18, bold: o.firstColBold && i === 0, align: (o.numCols && o.numCols.includes(i)) ? AlignmentType.RIGHT : AlignmentType.LEFT }),
    })),
  }));
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: [hdr, ...body] });
}
function box(title, lines, fill = LIGHT) {
  const children = [new Paragraph({ children: [new TextRun({ text: title, bold: true, color: NAVY, size: 21 })], spacing: { after: 80 } })];
  for (const l of lines) children.push(new Paragraph({ children: runs(l, { size: 20 }), spacing: { after: 60, line: 264 }, alignment: AlignmentType.LEFT }));
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: W, type: WidthType.DXA },
      borders: { top: { style: BorderStyle.SINGLE, size: 4, color: fill }, bottom: { style: BorderStyle.SINGLE, size: 4, color: fill }, right: { style: BorderStyle.SINGLE, size: 4, color: fill }, left: { style: BorderStyle.SINGLE, size: 24, color: ACCENT } },
      shading: { fill, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 120, bottom: 120, left: 180, right: 180 }, children,
    })] })],
  });
}
function img(file, wpx, hpx, widthPt = 468) {
  const data = fs.readFileSync(file);
  const h = Math.round(widthPt * hpx / wpx);
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 40 }, children: [new ImageRun({ type: "png", data, transformation: { width: widthPt, height: h }, altText: { title: path.basename(file), description: path.basename(file), name: path.basename(file) } })] });
}
const SP = () => new Paragraph({ children: [], spacing: { after: 60 } });
const D = (f) => path.join(REPO, "diagnostico", f);

// ---------- contenido ----------
const c = [];

// PORTADA
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 300 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(REPO, "entregable", "logo_sabana.png")), transformation: { width: 260, height: Math.round(260 * 1365 / 3047) }, altText: { title: "Universidad de La Sabana", description: "Logo Universidad de La Sabana, Facultad de Comunicación", name: "logo" } })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "ANÁLISIS DE AUDIENCIAS", bold: true, size: 28, color: NAVY })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: "Momento 2 · Audiencias poblacionales cuantitativas", size: 24, color: "5C5C5A" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "SEGUNDO PARCIAL", bold: true, size: 26, color: ACCENT })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "Segmentación multivariada a posteriori con K-means y procesamiento LLM", bold: true, size: 36, color: NAVY })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: "Producto Netflix asignado: “La Primera Vez” (Netflix / Caracol Televisión)", size: 26, italics: true })] }));
c.push(table(["Campo", "Información"], [
  ["Integrantes del equipo", ["Juan Sebastián Barragán", "Joshua Díaz", "Felipe Quiroga"]],
  ["Producto Netflix asignado", "La Primera Vez (Netflix / Caracol Televisión)"],
  ["Grupo", "[completar]"],
  ["Fecha", "2 de octubre de 2026"],
], [3000, 6360], { firstColBold: true, firstColShade: true, size: 22 }));
c.push(SP());
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 400 }, children: [new TextRun({ text: "Universidad de La Sabana · Facultad de Comunicación", size: 20, color: "5C5C5A" })] }));

// TABLA DE CONTENIDO
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(box("Cómo leer este documento", [
  "El documento sigue, en orden, los nueve componentes de evaluación de la guía. Todas las cifras salen de la ejecución real en Python (pandas, scikit-learn, matplotlib) sobre el archivo entregado; los scripts y sus salidas completas están en el repositorio del equipo (carpeta ~diagnostico/~). La transcripción íntegra de la conversación con el agente se entrega como anexo separado (memoria del proceso).",
  "**Base utilizada.** El archivo recibido es ~Base_Audiencias_Digitales_Colombia_2025_V3_Segundo_Parcial.xlsx~: **1.000 registros y 41 variables** (la guía menciona la V2 con 29 variables; la V3 añade 12 variables). Es una **base sintética** de audiencia digital colombiana, no una encuesta a espectadores de ~La Primera Vez~.",
  "**Uso de IA.** Claude (Code) ejecutó la estadística y propuso alternativas; las decisiones sustantivas (variables, número de clusters, nombres, segmento prioritario) fueron del equipo y se consignan en los recuadros «Decisión del grupo».",
]));

// =============== 1. ENTENDIMIENTO DE LOS DATOS
c.push(H1("1. Entendimiento de los datos"));
c.push(P("Antes de agrupar auditamos la base completa: tipos de variables, distribuciones, faltantes, duplicados, valores fuera de rango, formato y relaciones entre variables. Se verificó que los 41 nombres de columna coinciden exactamente con el diccionario de variables (ninguno falta ni sobra)."));
c.push(B("**14 variables numéricas:** edad, estrato (ordinal 1–6), las seis escalas Likert de Usos y Gratificaciones (ug_*), comparacion_social y nivel_fomo (Likert 1–5), horas_diarias_redes, horas_video_dia, num_redes_usadas y gasto_mensual_contenido_cop."));
c.push(B("**26 variables categóricas + id:** demográficas (grupo_etario, genero, region, nivel_educativo), de consumo y plataforma (dispositivo, red social, plataforma de video, formato, contexto de visionado, vía de llegada, patrón de consumo, binge watching…) y motivacionales (motivo_primario, necesidad_base, gratificacion_buscada, tension_gratificacion…). Nueve de ellas son ordinales escritas como texto."));
c.push(H2("1.1 Descriptivos de las variables numéricas"));
c.push(table(["Variable", "Media", "Mediana", "Desv. est.", "Mín.", "Máx.", "Rango", "Faltantes"], [
  ["edad", "38,85", "36", "14,64", "18", "75", "57", "0"],
  ["estrato", "2,79", "3", "1,19", "1", "6", "5", "0"],
  ["ug_entretenimiento", "4,14", "4", "0,72", "2", "5", "3", "0"],
  ["ug_informacion", "3,65", "4", "0,95", "1", "5", "4", "0"],
  ["ug_identidad", "3,35", "3", "0,98", "1", "5", "4", "0"],
  ["ug_interaccion_social", "3,95", "4", "0,78", "2", "5", "3", "0"],
  ["ug_evasion", "3,56", "4", "0,87", "1", "5", "4", "0"],
  ["ug_pasar_tiempo", "3,86", "4", "0,80", "1", "5", "4", "0"],
  ["horas_diarias_redes", "3,51", "3,5", "1,33", "0,3", "7,8", "7,5", "0"],
  ["num_redes_usadas", "5,23", "5", "1,71", "1", "9", "8", "0"],
  ["gasto_mensual_contenido_cop", "21.924", "9.565", "27.381", "0", "116.524", "116.524", "0"],
  ["horas_video_dia", "2,11", "2,0", "1,16", "0,2", "6,5", "6,3", "0"],
  ["comparacion_social", "3,57", "4", "1,00", "1", "5", "4", "0"],
  ["nivel_fomo", "3,83", "4", "1,01", "1", "5", "4", "0"],
], [2660, 900, 1000, 960, 700, 1000, 1000, 1140], { numCols: [1, 2, 3, 4, 5, 6, 7], firstColBold: true }));
c.push(CAP("Tabla 1. Estadísticos descriptivos (desviación estándar muestral, n−1). n = 1.000 en todas las variables."));
c.push(H2("1.2 Calidad de los datos"));
c.push(table(["Chequeo", "Resultado", "Implicación para K-means"], [
  ["Faltantes (NaN y texto tipo «NA», «-»)", "0 en las 41 variables", "No se requiere imputar ni eliminar registros"],
  ["Duplicados (filas, id, perfiles numéricos)", "0 / 0 / 0", "Ninguna"],
  ["Valores fuera del rango del diccionario", "0", "Ninguna"],
  ["Formato de categorías", "Sin espacios ni mayúsculas inconsistentes; todas las categorías existen en el diccionario", "Ninguna"],
  ["Escalas muy distintas", "DE del gasto = 27.381 frente a ≈0,7–1,0 en las Likert", "**Obliga a estandarizar**"],
  ["Gasto mensual", "32,2% de ceros, 47 atípicos (IQR), asimetría 1,36", "Puede formar un grupo por sí solo"],
  ["Baja variabilidad", "ug_entretenimiento (82,7% en 4–5) y ug_interaccion_social: nadie responde 1", "Aportan poca separación"],
  ["Redundancias", "horas redes ↔ horas video r = 0,73; edad ↔ FOMO r = −0,64; disposicion_pago explica el 85% de la varianza del gasto", "Evitar incluir pares redundantes"],
  ["Contradicciones lógicas", "37 registros (p. ej. «paga sin pensarlo» con gasto 0)", "Afectan la descripción, no el modelo; se conservaron"],
  ["Hojas con análisis previo", "El archivo trae un K-means de la V2 (k = 4)", "No se usó para no condicionar las decisiones"],
], [2700, 3700, 2960]));
c.push(CAP("Tabla 2. Auditoría de calidad. No se eliminó ni imputó ningún registro."));

// =============== 2. VARIABLES DE AGRUPAMIENTO
c.push(H1("2. Variables de agrupamiento y justificación"));
c.push(P("Nuestro objetivo es descubrir segmentos por **lo que la audiencia hace** (comportamiento digital observable) y **por qué lo hace** (motivaciones según la teoría de Usos y Gratificaciones). Por eso combinamos variables de conducta con las seis escalas U&G. Antes de decidir revisamos correlaciones (Pearson y Spearman) y multicolinealidad (VIF) entre todas las numéricas."));
c.push(table(["Variable", "Dimensión", "Qué mide", "Por qué entra al K-means"], [
  ["horas_diarias_redes", "Conducta · intensidad", "Horas/día en redes", "Principal medida de intensidad; distribución limpia (CV 0,38)"],
  ["num_redes_usadas", "Conducta · amplitud", "Redes usadas al mes", "Mide diversificación, distinta de la intensidad (r = 0,18 con horas)"],
  ["gasto_mensual_contenido_cop", "Conducta · monetización", "COP/mes en contenido", "Única medida de pago; casi independiente del resto (r ≈ 0)"],
  ["ug_entretenimiento", "U&G", "Diversión", "Dimensión central del marco U&G (baja variabilidad, se acepta por coherencia teórica)"],
  ["ug_informacion", "U&G", "Información / vigilancia", "Buena dispersión; dimensión independiente"],
  ["ug_identidad", "U&G", "Identidad / autoexpresión", "La escala más dispersa (DE 0,98)"],
  ["ug_interaccion_social", "U&G", "Integración social", "Dimensión U&G necesaria (usa niveles 2–5)"],
  ["ug_evasion", "U&G", "Evasión / escape", "Buena dispersión; independiente"],
  ["ug_pasar_tiempo", "U&G", "Hábito / pasatiempo", "Dimensión de hábito; dispersión aceptable"],
], [2500, 1700, 1900, 3260], { firstColBold: true }));
c.push(CAP("Tabla 3. Las 9 variables seleccionadas. Las seis ug_* son casi independientes entre sí (|r| ≤ 0,11) y respecto de la conducta (|r| ≤ 0,18): cada una aporta información propia. VIF de las 9 variables: 1,01–1,09."));
c.push(H3("Variables numéricas excluidas"));
c.push(table(["Variable", "Motivo de exclusión"], [
  ["horas_video_dia", "Mide la misma «intensidad de pantalla» que horas_diarias_redes (r = 0,73; R² = 0,54). Incluir ambas daba doble peso a la intensidad (VIF 2,2 → 1,08 al retirarla). Se usa como descriptor."],
  ["comparacion_social, nivel_fomo", "No son escalas U&G y funcionan como proxy de la edad (r = −0,56 y −0,64; el grupo etario explica el 42% de la varianza del FOMO). Incluirlas metería la edad «por la puerta de atrás». Se usan como descriptores."],
  ["edad, estrato (y género, nivel educativo, región)", "Son demográficas: si entran, los grupos reflejarían las categorías introducidas y no patrones emergentes (segmentación a priori disfrazada)."],
  ["Todas las categóricas (motivo_primario, necesidad_base, gratificacion_buscada, plataforma, vía de llegada…)", "Nominales: K-means trabaja con distancias euclidianas y no puede tratarlas. Se reservan para el enriquecimiento."],
], [3000, 6360], { firstColBold: true }));
c.push(CAP("Tabla 4. Variables excluidas del agrupamiento y su uso posterior."));
c.push(box("Decisión del grupo · Paso 2", [
  "Elegimos **9 variables**: tres de comportamiento (horas_diarias_redes, num_redes_usadas, gasto_mensual_contenido_cop) y las seis escalas ug_*. El agente propuso dos opciones (10 variables con horas_video_dia o 9 sin ella); escogimos la de 9 porque horas_video_dia repetía la intensidad de uso (r = 0,73) y el hábito audiovisual lo podemos describir después con binge_watching y patron_consumo. Así el modelo captura qué hace la audiencia (intensidad, amplitud, pago) y por qué lo hace (las seis gratificaciones U&G), sin variables demográficas.",
]));

// =============== 3. RESULTADO DEL AGRUPAMIENTO
c.push(H1("3. Resultado del agrupamiento"));
c.push(H2("3.1 Estandarización"));
c.push(P("K-means agrupa por distancia euclidiana. Sin estandarizar, el gasto (desviación de ≈27.000 pesos) aplastaría a las escalas Likert (desviación ≈0,7–1): una diferencia de mil pesos pesaría miles de veces más que pasar de 1 a 5 en una gratificación. Con **StandardScaler** cada variable se transforma en z = (x − media) / desviación, de modo que todas quedan con media 0 y desviación 1 y aportan lo mismo a la distancia."));
c.push(table(["Variable", "Media antes", "DE antes", "Media después", "DE después"], [
  ["horas_diarias_redes", "3,505", "1,332", "0,000", "1,000"],
  ["num_redes_usadas", "5,229", "1,711", "0,000", "1,000"],
  ["gasto_mensual_contenido_cop", "21.924,28", "27.367,55", "0,000", "1,000"],
  ["ug_entretenimiento", "4,137", "0,718", "0,000", "1,000"],
  ["ug_informacion", "3,648", "0,948", "0,000", "1,000"],
  ["ug_identidad", "3,352", "0,980", "0,000", "1,000"],
  ["ug_interaccion_social", "3,947", "0,782", "0,000", "1,000"],
  ["ug_evasion", "3,561", "0,866", "0,000", "1,000"],
  ["ug_pasar_tiempo", "3,864", "0,798", "0,000", "1,000"],
], [3360, 1500, 1500, 1500, 1500], { numCols: [1, 2, 3, 4], firstColBold: true }));
c.push(CAP("Tabla 5. Antes y después de estandarizar (StandardScaler usa la desviación poblacional, n)."));
c.push(H2("3.2 Configuración y primera ejecución (k = 4)"));
c.push(P("Modelo: **KMeans(n_clusters = k, init = \"k-means++\", n_init = 10, random_state = 42)**. Con k = 4 como punto de partida se obtuvieron grupos de 26,0%, 33,1%, 25,7% y 15,2%, una inercia de 6.960,91 y una **silueta de 0,097**. Además, al cambiar la semilla la partición cambiaba bastante (índice de Rand ajustado, ARI, entre 0,43 y 0,87), lo que indicaba que k = 4 no era estable. Por eso evaluamos un rango de k."));
c.push(H2("3.3 Evaluación de k (de 2 a 8)"));
c.push(table(["k", "Inercia (WSS)", "Reducción vs. k−1", "Silueta", "Calinski-Harabasz", "Davies-Bouldin", "ARI medio entre semillas", "Tamaños (%)"], [
  ["2", "7.954", "—", "0,1105", "131,2", "2,69", "0,97", "49,6 / 50,4"],
  ["**3**", "**7.361**", "**7,5%**", "**0,1115**", "111,0", "2,40", "**0,95**", "**41,5 / 41,1 / 17,4**"],
  ["4", "6.961", "5,4%", "0,0971", "97,3", "2,38", "0,58", "26,0 / 33,1 / 25,7 / 15,2"],
  ["5", "6.623", "4,8%", "0,0952", "89,3", "2,21", "0,64", "19,7 / 27,1 / 17,1 / 21,5 / 14,6"],
  ["6", "6.372", "3,8%", "0,0889", "82,0", "2,29", "0,61", "18,6 / 16,2 / 14,8 / 20,2 / 13,8 / 16,4"],
  ["7", "6.138", "3,7%", "0,0890", "77,2", "2,17", "0,58", "—"],
  ["8", "5.972", "2,7%", "0,0883", "71,8", "2,10", "0,40", "—"],
], [500, 1150, 1150, 900, 1150, 1050, 1260, 2200], { numCols: [1, 2, 3, 4, 5, 6], size: 17 }));
c.push(CAP("Tabla 6. Métricas por k. ARI = coincidencia de la partición con otras 5 semillas (1 = idéntica)."));
c.push(img(D("paso4_codo.png"), 1350, 825, 380));
c.push(CAP("Figura 1. Método del codo. La curva desciende de forma casi lineal: no hay un codo nítido. El mayor cambio de pendiente está en k = 3 (pasar de 2 a 3 reduce la inercia un 7,5%; desde ahí cada cluster adicional aporta 5,4% o menos). El criterio kneedle marca k = 5, prácticamente empatado con k = 4."));
c.push(img(D("paso4_silueta.png"), 1350, 825, 380));
c.push(CAP("Figura 2. Silueta promedio por k con las referencias de Kaufman y Rousseeuw (1990). El máximo está en k = 3 (0,1115). Todos los valores están en la banda «< 0,25, estructura débil», habitual con escalas actitudinales poco correlacionadas: los segmentos son divisiones útiles de un continuo, no grupos naturalmente separados."));
c.push(img(D("paso_k3_pca.png"), 1650, 975, 460));
c.push(CAP("Figura 3. Dispersión PCA del modelo final (k = 3). Componente 1: 17,5% de la varianza (pesan número de redes, horas en redes y, en sentido contrario, ug_informacion). Componente 2: 11,8% (pesan gasto y, en sentido contrario, ug_evasion). Acumulada: 29,2%. Es una proyección de 9 dimensiones a 2: el solapamiento visible no representa toda la separación del espacio original."));
c.push(box("Decisión del grupo · Paso 4: k = 3", [
  "Elegimos **k = 3** combinando tres criterios: (1) es el **mayor quiebre del codo**; (2) tiene la **silueta más alta** del rango evaluado (0,1115), y (3) es la solución **más estable** (ARI 0,95 frente a ≈0,6 para k ≥ 4: con otra semilla, alrededor del 40% de la estructura de k = 4 cambiaba). Además, los tres grupos se pueden nombrar y son accionables para ~La Primera Vez~: dos coinciden con los User Personas del Momento 1 y el tercero (los que pagan) es estratégico para Netflix. Reconocemos que la estructura es débil (silueta < 0,25) y lo tratamos en las limitaciones.",
]));

// =============== 4. PERFIL Y ENRIQUECIMIENTO
c.push(H1("4. Perfil y enriquecimiento de los segmentos"));
c.push(H2("4.1 Perfil numérico (variables del agrupamiento)"));
c.push(table(["Variable", "C0 (n = 415)", "C1 (n = 411)", "C2 (n = 174)", "Media general"], [
  ["horas_diarias_redes", "**4,22** (+20%)", "2,80 (−20%)", "3,46 (−1%)", "3,51"],
  ["num_redes_usadas", "**6,05** (+16%)", "4,37 (−16%)", "5,30 (+1%)", "5,23"],
  ["gasto_mensual_contenido_cop", "11.426 (−48%)", "11.123 (−49%)", "**72.476 (+231%)**", "21.924"],
  ["ug_entretenimiento", "**4,27** (+3%)", "4,01 (−3%)", "4,12 (0%)", "4,14"],
  ["ug_informacion", "3,21 (−12%)", "**4,05** (+11%)", "3,74 (+3%)", "3,65"],
  ["ug_identidad", "**3,71** (+11%)", "3,00 (−10%)", "3,33 (−1%)", "3,35"],
  ["ug_interaccion_social", "**4,14** (+5%)", "3,75 (−5%)", "3,95 (0%)", "3,95"],
  ["ug_evasion", "**3,80** (+7%)", "3,41 (−4%)", "3,36 (−6%)", "3,56"],
  ["ug_pasar_tiempo", "**4,11** (+6%)", "3,61 (−7%)", "3,88 (0%)", "3,86"],
  ["~Descriptores (no entraron al modelo)~", "", "", "", ""],
  ["horas_video_dia", "2,64", "1,60", "2,06", "2,11"],
  ["edad (media)", "29,7", "47,8", "39,5", "38,8"],
  ["estrato (media)", "2,55", "2,57", "3,85", "2,79"],
  ["nivel_fomo / comparacion_social", "4,38 / 4,02", "3,31 / 3,15", "3,75 / 3,48", "3,83 / 3,57"],
], [2900, 1650, 1650, 1650, 1510], { numCols: [1, 2, 3, 4], firstColBold: true }));
c.push(CAP("Tabla 7. Promedios por cluster y diferencia porcentual frente a la media general. En negrita, el valor más alto de cada variable."));
c.push(H2("4.2 Enriquecimiento con variables categóricas"));
c.push(P("Cruzamos cada cluster con las variables categóricas que no entraron al modelo. Se muestra la categoría dominante y, entre paréntesis, el **índice** frente al total de la base (100 = promedio; 150 = 1,5 veces más frecuente) o el **lift** frente al cluster más parecido."));
c.push(table(["Variable", "C0", "C1", "C2"], [
  ["motivo_primario", "Hábito y pasatiempo 21,9%; identidad (lift 1,34)", "**Información 22,6%** (lift 1,46)", "Interacción social 23,6%"],
  ["necesidad_base", "Distracción y placer 24,1%", "Distracción 21,2%; **curiosidad 17,5%** (124)", "Distracción 20,7%; pertenencia 16,7%"],
  ["gratificacion_buscada", "Relajación 19,3% (113); expresar quién soy (135)", "Relajación 15,8%; **estar al día** (lift 1,60)", "Relajación 14,4%; sentirse acompañado (144)"],
  ["Gratificación obtenida (tension_gratificacion)", "Satisf. parcial 24,6%; indiferencia 15,4%", "Satisf. plena 22,9%; descubrimiento positivo 15,8%", "**Satisfacción plena 31,0%**; indiferencia 7,5%"],
  ["genero", "F 52,3% · M 47,0%", "F 49,1% · M 50,1%", "F 49,4% · M 50,0%"],
  ["Edad (rangos)", "**18–24: 35,2% (lift 2,19)**; 25–39: 50,4%", "**40–55: 40,4%; 56+: 30,9% (lift 2,15)**", "25–39: 37,4%; 40–55: 32,2%"],
  ["nivel_educativo", "Secundaria 32,5%; técnico 32,3%", "Secundaria 32,8%; técnico 29,0%", "Universitario 31,0%; **posgrado 24,1% (lift 4,01)**"],
  ["estrato", "Bajo (1–2) 49,2%", "Bajo (1–2) 49,9%", "**Alto (4–6) 54,0%**"],
  ["plataforma_video_principal", "YouTube 27,0%; Netflix 25,8%; **TikTok 24,6% (lift 1,58)**", "YouTube 30,9%; Netflix 17,8%; **ninguna 14,1% (lift 2,23)**", "YouTube 28,7%; **Netflix 27,0%**"],
  ["dispositivo_principal", "Smartphone 82,9%", "Smartphone 74,7%; Smart TV (116); tablet (134)", "Smartphone 77,6%"],
  ["categoria_contenido", "Música 19,0%; humor 17,1%", "Música 18,0%; deportes (119); noticias (122)", "Humor 15,5%; gastronomía 14,4%"],
  ["contexto_visionado", "**Solo/a en smartphone 31,1%** (117)", "**En familia, TV compartida 35,0%** (116)", "En familia 29,3%; solo/a en computador (lift 1,52)"],
  ["binge_watching / patrón", "**Maratón frecuente 24,1%** (lift 1,32); madrugada (lift 1,45)", "Un episodio por sesión 27,7%; fragmentado 20,0%", "Un episodio por sesión 28,7%; maratón de fin de semana"],
  ["via_llegada", "**Algoritmo 28,9%** (lift 1,32); redes sociales 19,3%", "Recomendación amigos/familia 24,3%; medios (128)", "Recomendación 27,0%; búsqueda activa (116)"],
  ["Otros rasgos exclusivos", "Creador activo 55,7%; comunidad activa 64,6%", "TV abierta como fuente principal 29,9% (lift 1,93); consumidor pasivo 40,4%", "Disposición a pagar alta 92% (lift 14,7)"],
], [2160, 2400, 2400, 2400], { firstColBold: true, size: 17 }));
c.push(CAP("Tabla 8. Distribución categórica predominante por cluster. Fuerza de asociación con el cluster (V de Cramer): disposición a pagar 0,58; grupo etario 0,43; genera_contenido 0,33; género 0,02 (sin diferencias)."));
c.push(H2("4.3 Descripción integrada de cada segmento"));
c.push(P("**Cluster 0 (41,5%).** Es el más intensivo (4,2 h/día en redes, 6 redes) y el más alto en evasión, pasar el tiempo, identidad e interacción social, con la menor motivación informativa. Aunque la edad no entró al modelo, concentra al 75% de todas las personas de 18–24 años de la base. Ve solo en el celular, maratonea, llega por el algoritmo y las redes, y es el más activo creando contenido y en comunidades."));
c.push(P("**Cluster 1 (41,1%).** Es el menos intensivo (2,8 h/día) y el único donde gana la motivación informativa. Concentra al 61% de las mujeres de 40–55 años de la base. Ve acompañado en la TV de la sala, a un episodio por sesión o de forma fragmentada; para un 30% la TV abierta sigue siendo su fuente principal y es pasivo en lo digital."));
c.push(P("**Cluster 2 (17,4%).** Se define por el pago (72.476 COP/mes, 6,5 veces los otros) y el estrato alto; sus gratificaciones están en la media. Usa más Netflix, elige con intención (búsqueda activa, recomendación) y es el más satisfecho (31% de satisfacción plena)."));
c.push(H3("Cruces de retención (proxy, porque la base no mide abandono)"));
c.push(table(["Combinación", "C0: indiferencia / positivo*", "C1: indiferencia / positivo*", "Lectura"], [
  ["Ve solo/a + llega por algoritmo", "**23,7% / 32,2%**", "**29,7% / 21,6%**", "Patrón de riesgo en ambos (base total: indiferencia 14,0%)"],
  ["Ve solo/a + recomendación social", "12,5% / 39,1%", "13,2% / 45,3%", "La recomendación humana protege"],
  ["Acompañado/a + algoritmo", "15,3% / 36,2%", "11,1% / 39,6%", "En C1, la compañía compensa al algoritmo"],
  ["Acompañado/a + búsqueda activa", "7,4% / 33,3%", "9,3% / **46,6%**", "Mejor combinación de C1"],
], [2500, 2100, 2100, 2660], { size: 17 }));
c.push(CAP("Tabla 9. *Positivo = descubrimiento positivo + satisfacción plena (base total: 38,4%)."));

// =============== 5. NOMBRES Y VALIDACIÓN
c.push(H1("5. Nombres y validación de los segmentos"));
c.push(P("Cada nombre sigue la fórmula **[comportamiento distintivo] + [motivación principal]**, tomando el rasgo con mayor lift frente a los otros clusters y la gratificación relativamente más alta. Los nombres son neutros en género porque los tres clusters son 50/50."));
c.push(table(["Cluster", "Nombre", "Comportamiento distintivo", "Motivación principal"], [
  ["C0 (41,5%)", "**Maratonistas móviles que buscan desconexión**", "Maratón individual en smartphone; descubre por algoritmo y redes", "Desconectarse de la rutina (evasión, pasatiempo) con autoexpresión"],
  ["C1 (41,1%)", "**Espectadores acompañados en TV que buscan memoria y contexto de época**", "Consumo acompañado y pausado en pantalla compartida; TV tradicional como puerta de entrada", "Memoria (nostalgia) + contexto del país (información)"],
  ["C2 (17,4%)", "**Suscriptores selectivos que buscan calidad que justifique su pago**", "Paga suscripción y elige con intención (búsqueda, recomendación)", "Calidad que justifique el pago (inferida de pago alto, exigencia de diseño y satisfacción plena)"],
], [1200, 2700, 2730, 2730], { size: 18 }));
c.push(CAP("Tabla 10. Nombres de los segmentos."));
c.push(table(["Criterio de validación", "C0", "C1", "C2", "Evaluación"], [
  ["Tamaño", "415 (41,5%)", "411 (41,1%)", "174 (17,4%)", "Los tres son suficientes para ser accionables"],
  ["Silueta media del cluster", "0,131", "0,101", "0,091", "Débil en los tres; C0 es el más cohesionado"],
  ["% registros con silueta negativa", "0,0%", "5,8%", "9,8%", "Pocos registros mal asignados"],
  ["Estabilidad (ARI entre semillas)", "0,95 (global)", "", "", "Partición robusta frente a la inicialización"],
  ["Sentido teórico U&G", "Evasión, identidad, pasatiempo", "Información, curiosidad", "Sin gratificación distintiva", "C0 y C1 tienen perfil U&G claro; C2 se define por conducta de pago"],
  ["Diferenciación descriptiva", "18–24 (lift 2,19), TikTok, algoritmo", "56+ (lift 2,15), TV abierta, familia", "Estrato 5 (lift 6,26), posgrado", "Perfiles claramente distintos"],
], [2300, 1600, 1600, 1600, 2260], { size: 17, firstColBold: true }));
c.push(CAP("Tabla 11. Validación. Silueta global k = 3: 0,1115; inercia: 7.360,67."));
c.push(P("**Evaluación.** Los segmentos son **interpretables** (se pueden nombrar desde U&G), **diferenciados** (la edad, el pago y el comportamiento digital los separan aunque no entraron al modelo) y **accionables** (cada uno tiene canales de acceso distintos). Su principal debilidad es estadística: la estructura es débil (silueta < 0,25) y la base es sintética, por lo que los segmentos deben leerse como hipótesis de trabajo verosímiles."));

// =============== 6. USER PERSONAS Y MAPAS DE EMPATÍA
c.push(H1("6. User Personas y Mapas de Empatía"));
c.push(P("Un User Persona y un Mapa de Empatía por cluster, construidos con los valores dominantes de cada segmento. Donde existe evidencia del Momento 1 (14 entrevistas) se cita con su código (E1…E14). El Cluster 2 no tiene ninguna entrevista: su ficha se apoya solo en los datos y su cita es una síntesis, no un testimonio."));

function persona(title, rows) {
  return [H2(title), table(["Campo", "Contenido"], rows, [2300, 7060], { firstColBold: true, firstColShade: true, size: 18 })];
}
function mapa(title, rows, tension) {
  return [H3(title), table(["Campo", "Contenido (variables de la base + evidencia M1)"], rows, [2000, 7360], { firstColBold: true, firstColShade: true, size: 18 }), SP(), box("Tensión entre lo que dice y lo que siente", [tension], GREY)];
}

c.push(...persona("6.1 Cluster 0 · User Persona: DANIEL, «Maratonista móvil que busca desconexión»", [
  ["Perfil sociodemográfico", ["**Daniel, 21 años**, Bogotá (urbano). Rango del cluster: 18–39 años = 85,6% (franja exclusiva: 18–24); mediana 28.", "Estrato medio-bajo (3: 36,4%; 2: 31,6%). Estudiante universitario o joven en etapa laboral inicial (M1: Simón, E11; Jorge, E4). En el cluster predominan secundaria y técnico; el 79% vive fuera de Bogotá."]],
  ["Necesidad base", "Distracción y placer (24,1%); descanso emocional (20,2%)."],
  ["Motivo primario / secundario", "Hábito y pasatiempo, evasión (ug_evasion 3,80; ug_pasar_tiempo 4,11, los más altos) / identidad y autoexpresión (lift 1,34) e interacción social."],
  ["Gratificación buscada vs. obtenida", "Busca relajación y llenar el tiempo libre. Obtiene eso **y además un aprendizaje histórico que no buscaba**: la gratificación obtenida supera a la buscada. El descubrimiento positivo llega a 21,9% cuando ve la serie recomendada por otros."],
  ["Comportamiento", "4,2 h/día en redes, 6 redes, 2,6 h/día de video. Ve **solo en el smartphone** (31,1%), de noche (56,9%) y madrugada; **maratonea** (maratón frecuente 24,1%). Gasto medio 11.426 COP/mes (38,6% gasta 0); sensibilidad al precio alta (52,3%)."],
  ["Plataformas y dispositivos", "Smartphone 82,9%. YouTube 27,0%, Netflix 25,8%, TikTok 24,6%. Redes: Instagram y WhatsApp. Formato: video corto."],
  ["Vía de descubrimiento", "Algoritmo y top de Netflix (28,9%), redes sociales (19,3%), amigos (20,2%). M1: Top (E4), video previo (E9), miniatura y amigo (E11)."],
  ["Frustración / riesgo", "Tramas románticas que «se repiten mucho» (M1: E9). Es el cluster más vulnerable: riesgo alto de desplazamiento 45,3%; ver solo tras llegar por el algoritmo duplica la indiferencia (23,7%). Los dos abandonos del M1 (E4, E9) tienen este patrón."],
  ["Cita", "«La vi más también como para distraerme, pero no pensé que fuera a darme un poco de contexto histórico colombiano.» — Simón (E11)"],
]));
c.push(...mapa("Mapa de Empatía · Daniel", [
  ["Dice", "«Solo quería distraerme» (E1, E3, E9). Netflix y TikTok como plataformas; música y humor como contenidos; ve «solo, en el celular»."],
  ["Piensa y siente", "Quiere desconectarse y expresarse (identidad, lift 1,34). FOMO alto (4,38) y comparación social alta (4,02), los máximos de la base. Siente sorpresa cuando la serie le enseña algo: «me sirvió para entender mucho una época» (E1)."],
  ["Hace", "4,2 h/día en redes; maratón frecuente; patrón de maratón 25,1%. Crea contenido (activo 55,7%). Recomienda la serie a familia y amigos (E1)."],
  ["Oye", "Amigos (E7, E11), creadores con los que tiene vínculo fuerte (47,7%) y sus comunidades en línea (64,6% activas). Le llega por el algoritmo y las redes."],
  ["Dolores", "Riesgo alto de gratificación desplazada (45,3%): termina haciendo algo distinto a lo planeado. Sensibilidad al precio alta. Repetición romántica (E9). Consumo aislado sin validación social."],
  ["Ganancias", "Desconexión, relajación y un aprendizaje no esperado sobre la Colombia de los 70; temas para conversar."],
], "Dice que solo busca entretenerse, pero lo que más valora es aprender sin esfuerzo y tener algo que compartir. El aprendizaje funciona como premio inesperado, no como promesa."));

c.push(...persona("6.2 Cluster 1 · User Persona: LAURA, «Espectadora acompañada en TV que busca memoria y contexto»", [
  ["Perfil sociodemográfico", ["**Laura, 49 años**, Bogotá (urbano). Rango del cluster: 40 años o más = 71,3% (56+: lift 2,15); mediana 47.", "Estrato medio-bajo (2: 36,0%; 3: 35,8%). Profesional activa, casada y con hijos (M1: E13 abogada, E14 epidemióloga). En el cluster predominan secundaria y técnico: la profesional es un subgrupo."]],
  ["Necesidad base", "Distracción y placer (21,2%) y **curiosidad** (17,5%, índice 124)."],
  ["Motivo primario / secundario", "**Información** (22,6%; ug_informacion 4,05, el único cluster donde gana), que en el M1 se expresa como nostalgia y contexto de época / entretenimiento (20,4%)."],
  ["Gratificación buscada vs. obtenida", "Busca relajación y estar al día (lift 1,60); M1: desconectarse, acompañarse y recordar (E13). Obtiene lo que busca **más una gratificación emocional**: nostalgia positiva y memoria compartida. Es el cluster con más descubrimiento positivo (15,8%)."],
  ["Comportamiento", "2,8 h/día en redes; 1,6 h/día de video. Ve **acompañada** (56,9%; en familia en TV 35,0%), a un episodio por sesión (27,7%) o fragmentado (20,0%), de noche y en la mañana."],
  ["Plataformas y dispositivos", "Smartphone 74,7%, más Smart TV y tablet que el resto. YouTube 30,9%, Netflix 17,8%; 14,1% sin plataforma de video. Para el 29,9% la TV abierta es la fuente principal. Redes: WhatsApp y Facebook."],
  ["Vía de descubrimiento", "Recomendación de amigos o familia (24,3%), medios, búsqueda. M1: Su hija se la recomienda (E14); la encuentra en la pantalla de inicio (E13)."],
  ["Frustración / riesgo", "Falta de tiempo: pausa y retoma (E14). Bajo riesgo (desplazamiento 29,9%, el menor). Excepción: si ve sola y llegó por el algoritmo, la indiferencia sube a 29,7%."],
  ["Cita", "«Me gustó verla pues para recordar, para recordar esa época y tener un poquito como esa experiencia, volver a vivir las cosas.» — Sandra (E14)"],
]));
c.push(...mapa("Mapa de Empatía · Laura", [
  ["Dice", "«La veo con mi esposo» (E13). YouTube y Netflix; música, deportes y noticias; ve en familia, en la TV de la sala."],
  ["Piensa y siente", "Quiere una pausa emocional y volver a su juventud (E13, E14); curiosidad por el país y la literatura (E14). FOMO (3,31) y comparación social (3,15) bajos."],
  ["Hace", "Poco tiempo en redes (2,8 h); maratón rara u ocasional; un episodio por sesión. Consumidora pasiva en lo digital (40,4%). Conversa la serie en casa: «recordamos nuestros tiempos» (E13)."],
  ["Oye", "A sus hijas (E14), al esposo y a compañeros de trabajo; medios y prensa. Vínculo débil o nulo con creadores (55,7%); 19,2% sin comunidades en línea."],
  ["Dolores", "Tiempo disponible. Bajo riesgo de desplazamiento (29,9%) y sensibilidad al precio media-alta (48,7%). Los mensajes solo digitales no la alcanzan."],
  ["Ganancias", "Nostalgia positiva, bienestar («feliz… un poco hasta más joven», E13), memoria compartida y contexto histórico."],
], "Dice que busca desconectarse del presente, pero lo que siente es la necesidad de volver al pasado acompañada y entender su época."));

c.push(...persona("6.3 Cluster 2 · User Persona: ANDRÉS, «Suscriptor selectivo que busca calidad que justifique su pago»", [
  ["Perfil sociodemográfico", ["**Andrés, 38 años** (mediana del cluster); edades mezcladas (25–39: 37,4%; 40–55: 32,2%). Urbano (Bogotá 20,7%, Antioquia 17,8%).", "**Estrato alto** (4–6 = 54,0%). Profesional con posgrado (posgrado 24,1%, lift 4,01; la ocupación no se mide). Género del persona arbitrario: el cluster es 50/50."]],
  ["Necesidad base", "Distracción (20,7%), descanso emocional (18,4%) y pertenencia (16,7%)."],
  ["Motivo primario / secundario", "Interacción social (23,6%) / entretenimiento (19,0%). Sus seis gratificaciones U&G están en la media."],
  ["Gratificación buscada vs. obtenida", "Busca relajación, compartir experiencias y sentirse acompañado (índice 144). Obtiene exactamente lo que busca: **satisfacción plena 31,0%** (la más alta), sin sorpresa marcada."],
  ["Comportamiento", "3,5 h/día en redes; **gasto 72.476 COP/mes**; 92% con disposición a pagar alta; 51% «paga sin pensarlo». Un episodio por sesión (28,7%); a veces solo en computador."],
  ["Plataformas y dispositivos", "Smartphone 77,6%, Smart TV 9,8%, computador 9,2%. **Netflix 27,0%** (el más alto), YouTube 28,7%, Disney+ y Prime por encima de la media. Escucha podcasts (índice 129)."],
  ["Vía de descubrimiento", "Recomendación de amigos o familia (27,0%), búsqueda activa (17,8%), publicidad digital."],
  ["Frustración / riesgo", "Riesgo bajo (frustración 20,7%, la menor). Su punto de quiebre sería la calidad: para el 21,3% el diseño es determinante para elegir o abandonar."],
  ["Cita (síntesis, no testimonio)", "«Pago porque espero contenido bien hecho. Si alguien de confianza me la recomienda y la producción está a la altura, la veo con calma, un capítulo a la vez.»"],
]));
c.push(...mapa("Mapa de Empatía · Andrés", [
  ["Dice", "«Vale la pena lo que pago». Netflix como plataforma principal; humor y gastronomía; ve en familia o solo en el computador."],
  ["Piensa y siente", "Quiere descansar y sentirse acompañado; espera que su suscripción rinda. FOMO 3,75 y comparación social 3,48 (en la media)."],
  ["Hace", "Busca activamente lo que quiere ver; un episodio por sesión; podcasts; crea contenido de forma moderada (57,5%)."],
  ["Oye", "Recomendaciones de su entorno (27,0%) y publicidad digital; vínculo moderado con creadores."],
  ["Dolores", "Exceso de oferta («demasiado contenido, difícil elegir» 12,6%); baja tolerancia a una producción o un diseño descuidados. Sensibilidad al precio baja (12,6% alta)."],
  ["Ganancias", "Satisfacción plena; confirmar que su suscripción vale la pena; contenido de prestigio."],
], "Dice que busca entretenimiento como cualquiera, pero lo que realmente exige es garantía de calidad. Ficha construida solo con datos del M2: debe validarse con entrevistas."));

// =============== 7. COMPARACIÓN CON EL MOMENTO 1
c.push(H1("7. Comparación con el Momento 1"));
c.push(P("El Momento 1 (M1) partió de 14 entrevistas a espectadores de ~La Primera Vez~ y produjo dos arquetipos: Daniel, el explorador casual, y Laura, la espectadora nostálgica. El Momento 2 (M2) segmentó a 1.000 personas de una base sintética de audiencia digital con 9 variables de conducta y U&G, dejando la demografía fuera del algoritmo. La comparación es una **triangulación**: contrastamos si los patrones que el M1 encontró en la serie tienen correlato en la estructura de la audiencia digital colombiana."));
c.push(H2("7.1 Coincidencias"));
c.push(B("**La división joven / adulto apareció sola.** La edad no entró al modelo y, aun así, el 75,3% de las personas de 18–24 cae en el Cluster 0 y el 61,1% de las mujeres de 40–55 en el Cluster 1. Tras la disposición a pagar, el grupo etario es la variable que más diferencia los clusters (V de Cramer = 0,43). La tipología del M1 no fue un artificio del reclutamiento."));
c.push(B("**El joven entra a distraerse, no a informarse.** Daniel busca «entretenerme… desconectarme un ratico» (E3); el Cluster 0 es el más alto en evasión (3,80) y pasar el tiempo (4,11) y el más bajo en información (3,21). Por eso el aprendizaje histórico es un valor inesperado (E11)."));
c.push(B("**La adulta ve en TV, acompañada y a su ritmo.** «Siempre acompañada de mi esposo» (E13); el Cluster 1 lidera el consumo en familia con TV (35,0%), el consumo acompañado (56,9%) y el ritmo fragmentado (20,0%), como E14, que la retoma cuando tiene tiempo."));
c.push(B("**Solo + algoritmo es el patrón de riesgo.** Los dos abandonos del M1 (E4, E9) veían solos y llegaron por el algoritmo. En la base, esa combinación casi duplica la indiferencia (24,5% frente a 12,9%)."));
c.push(H2("7.2 Matices y profundizaciones"));
c.push(B("**El riesgo no es ver solo, sino ver solo sin validación social.** En el Cluster 0, ver solo tras una recomendación da la menor indiferencia (12,5%) y el mayor descubrimiento (21,9%). Eso explica por qué E3 y E12, que llegaron por algoritmo pero conversaron la serie, la terminaron, y E4 y E9 no."));
c.push(B("**El riesgo es indiferencia, no decepción:** en ese patrón la frustración alta no aumenta (5,3% frente a 10,6%)."));
c.push(B("**Hay dos formas de ser social.** El Cluster 0 ve solo pero conversa en línea (81% crea contenido, 64,6% en comunidades); el Cluster 1 ve acompañado pero es pasivo en lo digital (40,4% solo observa)."));
c.push(B("**La nostalgia de Laura también es informativa:** el Cluster 1 es el único donde gana ug_informacion (4,05) y «estar al día» (lift 1,60), lo que coincide con el interés de E14 por «los acontecimientos del país» y «los grandes libros»."));
c.push(B("**Dimensiones nuevas.** La puerta de entrada de Laura no es Netflix (17,8% lo usa; para el 29,9% la TV abierta es la fuente principal), lo que da protagonismo a Caracol. Y aparece un tercer segmento —los que pagan— que ninguna entrevista representó."));
c.push(H2("7.3 Contradicciones"));
c.push(B("**La brecha de género no es estructural.** El M1 concluyó que la brecha más sólida era de género (10 de 14 mujeres). En el M2 el género no diferencia a ningún cluster (V de Cramer = 0,02; 49–52% mujeres). El sesgo describe a quién llegó a la serie, no al mercado: la serie subexplota a su mitad masculina."));
c.push(B("**Los jóvenes no son superficiales:** el Cluster 0 es el más alto en identidad y el que más descubre cuando la serie le llega recomendada."));
c.push(B("**«Familia + recomendación = alta fidelización» no se confirma:** esa combinación queda en la media del Cluster 1 (positivo 34,3%); la mejor es «acompañado + búsqueda activa» (46,6%). Queda como hipótesis cualitativa."));
c.push(B("**La nostalgia no es literalmente de los 70:** E13 (44) y E14 (54) fueron adolescentes entre 1984 y 2000. Quien fue joven en los 70 hoy tiene 61–70 años; ese grupo (56+, 30,9% del Cluster 1) no fue entrevistado. Además, los arquetipos son subgrupos: el Cluster 0 no es solo «universitario bogotano» ni el Cluster 1 solo «profesional»."));
c.push(H2("7.4 Qué aporta cada aproximación"));
c.push(P("Lo **cualitativo** dio profundidad y sentido: explicó ~por qué~ el joven valora aprender sin buscarlo, nombró la frustración concreta (la repetición romántica) y reveló el camino hija → madre; ninguna variable de la base captura esos matices emocionales. Lo **cuantitativo** dio escala y verificación: confirmó que los arquetipos corresponden a patrones poblacionales, midió el peso de cada combinación de riesgo, descubrió un segmento invisible en las entrevistas y desmontó una conclusión basada en una muestra pequeña (la brecha de género). Su límite es que trabaja sobre una base sintética y general, no sobre espectadores reales de la serie. Juntas, las dos aproximaciones son más sólidas que cualquiera por separado."));
c.push(SRC("Nota: al cruzar las fuentes detectamos inconsistencias en el informe del M1 que corregiremos: son 12 (no 13) de 14 entrevistados en el rango 16–30; quien vio la serie con su esposo es E13 (44 años), no E14; y E9 tiene 23 años, no 30."));

// =============== 8. SEGMENTO PRIORITARIO
c.push(H1("8. Segmento prioritario y conexión con el Momento 3"));
c.push(P("Comparamos los tres segmentos con los criterios de la guía (tamaño, afinidad, potencial de conversión, accesibilidad) ampliados a siete criterios. Escala de 1 (muy bajo) a 5 (muy alto), con el mismo peso para todos."));
c.push(table(["Criterio", "C0 · Daniel", "C1 · Laura", "C2 · Andrés"], [
  ["1. Tamaño (personas proyectadas*)", "5 · 41,5% (≈15,6 M)", "5 · 41,1% (≈15,5 M)", "2 · 17,4% (≈6,6 M)"],
  ["2. Afinidad motivacional con la serie", "4 · evasión, identidad, autodescubrimiento", "4 · información, nostalgia", "2 · sin gratificación distintiva"],
  ["3. Conversión y retención", "2 · vulnerabilidad 24,3 (la más alta)", "4 · desplazamiento 29,9% (el menor)", "5 · fidelización 27,4 (la más alta)"],
  ["4. Brecha buscada / obtenida (deleite)", "4 · «la supera»: aprendizaje inesperado", "4 · coincide + gratificación emocional", "3 · satisfacción plena sin sorpresa"],
  ["5. Accesibilidad digital e interfaz", "5 · algoritmo 28,9%, TikTok, Netflix 25,8%", "2 · Netflix 17,8%; 14% sin plataforma", "3 · Netflix 27%, búsqueda activa"],
  ["6. Relación con el contenido", "5 · «primeras veces», público 16+/18–24", "4 · nostalgia, historia, literatura", "2 · prestigio de producción"],
  ["7. Viralidad / socialización", "5 · 81% crea contenido", "1 · 40% consumidor pasivo", "3 · recomienda (27%)"],
  ["**TOTAL (sobre 35)**", "**30**", "**24**", "**20**"],
], [2800, 2190, 2190, 2180], { size: 17, firstColBold: true }));
c.push(CAP("Tabla 12. Matriz de selección. *Proyección didáctica con el coeficiente de expansión del archivo (f = 37.700). Si la retención pesa el doble, el orden no cambia (32 / 28 / 25)."));
c.push(box("Segmento prioritario: Cluster 0 · «Maratonistas móviles que buscan desconexión» · User Persona: Daniel", [
  "**Por qué.** Es el público natural de la serie (las «primeras veces», la franja 18–24 del público declarado 16+) y el más grande junto con el Cluster 1. Es el más alcanzable con las herramientas de Netflix (el más algorítmico, el que más maratonea, el que más usa Netflix de los dos grandes) y el único que multiplica la audiencia: el 81% crea contenido. Además es el puente hacia Laura (E14 conoció la serie por su hija) y recibe el mayor deleite cualitativo (el aprendizaje inesperado).",
  "**Su debilidad es el reto del Momento 3:** tiene el mayor riesgo de abandono, pero el M2 identificó el mecanismo exacto (ver solo tras llegar por el algoritmo, sin validación social), y ese riesgo es accionable. Su 47% masculino permite además atacar la brecha de género.",
  "**Por qué no los otros.** Laura (24 puntos) retiene mejor, pero es la menos accesible por canales digitales y la menos viral: será el **segmento secundario de expansión**, al que se llega a través de Daniel y de la promoción cruzada con Caracol. Andrés (20) es fiel pero pequeño, sin afinidad con los temas de la serie y sin respaldo cualitativo.",
]));
c.push(H2("8.1 Cómo alimentará el embudo de conversión del Momento 3"));
c.push(table(["Etapa del embudo", "Palanca para Daniel (con base en los datos)", "Indicador a seguir"], [
  ["Descubrimiento", "Miniatura, top y video previo de Netflix (algoritmo 28,9%); clips en TikTok e Instagram (TikTok 24,6%)", "Impresiones y clic en la miniatura"],
  ["Consideración", "Validación social: recomendación de amigos y creadores con los que tiene vínculo fuerte (47,7%)", "% de llegadas por recomendación"],
  ["Conversión (play)", "Tráiler con personajes jóvenes, humor y rebeldía (no solo romance) para incluir a la mitad masculina", "Inicio del episodio 1"],
  ["Retención", "Tramas secundarias de época que corten la repetición romántica; cliffhangers que aprovechen la maratón", "Finalización de temporada; caída entre episodios"],
  ["Recomendación", "Material para compartir (retos «mi primera vez», datos históricos); invitar a recomendarla a la familia (puente a Laura)", "Compartidos y nuevos espectadores referidos"],
], [1900, 4860, 2600], { size: 18, firstColBold: true }));
c.push(CAP("Tabla 13. Conexión del segmento prioritario con el embudo del Momento 3."));

// =============== 9. LIMITACIONES
c.push(H1("9. Reflexión sobre limitaciones"));
c.push(P("**Representatividad.** La base es sintética y describe a la audiencia digital colombiana en general, no a los espectadores de ~La Primera Vez~; los segmentos son hipótesis verosímiles que reproducen los supuestos con que se generó la base. Las 14 entrevistas del M1 tampoco son representativas: casi todos son jóvenes bogotanos cercanos al equipo, lo que explica en parte el sesgo femenino y la ausencia del segmento que paga y de la audiencia mayor de 56 años."));
c.push(P("**Variables no medidas.** La base no mide la gratificación obtenida de forma directa (usamos tension_gratificacion como proxy), ni el abandono de una serie, ni la ocupación, ni el consumo específico del título. Tampoco distingue si una recomendación viene de un hijo, de un amigo o de la pareja, que era clave en el M1."));
c.push(P("**Robustez de la estructura.** La silueta de k = 3 (0,11) indica una estructura débil según Kaufman y Rousseeuw: los segmentos son divisiones útiles de un continuo, no grupos naturales. A favor, k = 3 es estable frente a la semilla (ARI 0,95) y los grupos se diferencian con fuerza en variables que no entraron al modelo (edad, pago). El gasto, con 32% de ceros y cola larga, forma casi por sí solo el Cluster 2; una transformación logarítmica podría cambiar ese grupo y no la probamos. Las diferencias entre Clusters 0 y 1 son claras para diseñar estrategias distintas; el Cluster 2 se distingue por conducta de pago más que por motivación."));
c.push(P("**Qué datos fortalecerían la segmentación.** Datos reales de visualización de la serie en Netflix (inicio, finalización, abandono por episodio); una encuesta a espectadores con escalas de gratificación buscada y obtenida; más entrevistas a hombres, a mayores de 56 y a titulares de cuenta de estrato alto; e información sobre quién recomienda (hijos, pareja, amigos) para verificar la ruta intergeneracional."));

c.push(SP());
c.push(box("Anexo", ["La memoria completa del proceso (transcripción íntegra de la conversación con Claude Code) se entrega como archivo .docx separado: ~Barragan_Diaz_Quiroga_Anexo_Memoria_del_proceso.docx~."], GREY));

// ---------- documento ----------
const doc = new Document({
  creator: "Barragán, Díaz, Quiroga",
  title: "Segundo Parcial · Segmentación K-means · La Primera Vez",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, font: "Calibri", color: NAVY }, paragraph: { spacing: { before: 120, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Calibri", color: ACCENT }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, font: "Calibri", color: NAVY }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }, titlePage: true },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Análisis de Audiencias · 2026-2 · Segundo Parcial · La Primera Vez", size: 16, color: "5C5C5A" })] })] }),
      first: new Header({ children: [new Paragraph({ children: [] })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Barragán · Díaz · Quiroga — página ", size: 16, color: "5C5C5A" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "5C5C5A" })] })] }),
      first: new Footer({ children: [new Paragraph({ children: [] })] }),
    },
    children: c,
  }],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log("OK", OUT, buf.length); });

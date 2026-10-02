// Anexo: memoria del proceso (transcripción de la conversación) a partir de conversacion_exportada.md
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Header, Footer, AlignmentType,
  HeadingLevel, WidthType, ShadingType, BorderStyle, LevelFormat, PageNumber } = require("docx");

const REPO = "/home/user/Analisis-de-audiencias";
const md = fs.readFileSync(`${REPO}/conversacion_exportada.md`, "utf8");
const OUT = `${REPO}/entregable/Barragan_Diaz_Quiroga_Anexo_Memoria_del_proceso.docx`;
const NAVY = "323A4E", ACCENT = "2A78D6", W = 9360;
const border = { style: BorderStyle.SINGLE, size: 4, color: "BFC4CC" };
const borders = { top: border, bottom: border, left: border, right: border };

function runs(text, base = {}) {
  const out = []; const re = /(\*\*[^*]+\*\*|`[^`]+`)/g; let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), font: "Consolas", ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const splitRow = (l) => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((x) => x.trim());

function mdTable(lines) {
  const rows = lines.filter((l) => !/^\s*\|?\s*:?-{2,}/.test(l)).map(splitRow);
  const ncol = Math.max(...rows.map((r) => r.length));
  const cw = Math.floor(W / ncol); const widths = Array(ncol).fill(cw); widths[ncol - 1] = W - cw * (ncol - 1);
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: rows.map((r, ri) => new TableRow({
    tableHeader: ri === 0,
    children: widths.map((w, i) => new TableCell({ borders, width: { size: w, type: WidthType.DXA },
      shading: { fill: ri === 0 ? "E6EAF2" : "FFFFFF", type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 40, bottom: 40, left: 70, right: 70 },
      children: [new Paragraph({ children: runs(r[i] || "", { size: 16, bold: ri === 0 ? true : undefined }) })] })),
  })) });
}

const children = [];
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: "ANEXO OBLIGATORIO · MEMORIA DEL PROCESO", bold: true, size: 30, color: NAVY })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "Segundo Parcial · Segmentación multivariada a posteriori con K-means y procesamiento LLM", size: 22 })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "Producto: La Primera Vez (Netflix / Caracol Televisión) · Equipo: Juan Sebastián Barragán, Joshua Díaz, Felipe Quiroga · Grupo: [completar]", size: 20 })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: "Transcripción íntegra de la conversación con Claude Code (mensajes del equipo y respuestas del agente; no incluye las salidas internas de las herramientas, que están en la carpeta «diagnostico» del repositorio).", size: 18, italics: true, color: "5C5C5A" })] }));

const lines = md.split("\n");
let i = 0, inCode = false, code = [];
// saltar encabezado del md
while (i < lines.length && !lines[i].startsWith("## ")) i++;
let turno = 0;
for (; i < lines.length; i++) {
  const l = lines[i];
  if (l.trim().startsWith("```")) {
    if (inCode) {
      for (const c of code) children.push(new Paragraph({ shading: { fill: "F3F3F1", type: ShadingType.CLEAR, color: "auto" }, spacing: { after: 0 }, children: [new TextRun({ text: c || " ", font: "Consolas", size: 15 })] }));
      children.push(new Paragraph({ children: [], spacing: { after: 80 } }));
      code = []; inCode = false;
    } else inCode = true;
    continue;
  }
  if (inCode) { code.push(l); continue; }
  if (l.startsWith("## 👥") || l.startsWith("## 🤖")) {
    const equipo = l.includes("Equipo");
    if (equipo) turno++;
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: equipo && turno > 1, children: [new TextRun({ text: equipo ? `Mensaje ${turno} del equipo` : "Respuesta de Claude", color: equipo ? NAVY : ACCENT })] }));
    continue;
  }
  if (l.trim() === "---") { children.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "BFC4CC", space: 1 } }, children: [] })); continue; }
  if (/^\s*\|/.test(l)) {
    const block = [];
    while (i < lines.length && /^\s*\|/.test(lines[i])) block.push(lines[i++]);
    i--;
    children.push(mdTable(block));
    children.push(new Paragraph({ children: [], spacing: { after: 60 } }));
    continue;
  }
  const h = l.match(/^(#{1,4})\s+(.*)$/);
  if (h) { children.push(new Paragraph({ heading: h[1].length <= 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3, children: runs(h[2]) })); continue; }
  const b = l.match(/^(\s*)[-*]\s+(.*)$/);
  if (b) { children.push(new Paragraph({ numbering: { reference: "bullets", level: Math.min(2, Math.floor(b[1].length / 2)) }, spacing: { after: 30 }, children: runs(b[2], { size: 19 }) })); continue; }
  const n = l.match(/^(\s*)(\d+)\.\s+(.*)$/);
  if (n) { children.push(new Paragraph({ indent: { left: 360 + Math.floor(n[1].length / 2) * 360, hanging: 300 }, spacing: { after: 30 }, children: runs(`${n[2]}. ${n[3]}`, { size: 19 }) })); continue; }
  const q = l.match(/^>\s?(.*)$/);
  if (q) { children.push(new Paragraph({ indent: { left: 360 }, spacing: { after: 40 }, children: runs(q[1], { size: 19, italics: true, color: "5C5C5A" }) })); continue; }
  if (l.trim() === "") continue;
  children.push(new Paragraph({ spacing: { after: 60, line: 260 }, children: runs(l, { size: 19 }) }));
}

const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Calibri" }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, font: "Calibri", color: NAVY }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 20, bold: true, font: "Calibri", color: NAVY }, paragraph: { spacing: { before: 120, after: 60 }, outlineLevel: 2 } },
    ] },
  numbering: { config: [{ reference: "bullets", levels: [0, 1, 2].map((lv) => ({ level: lv, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360 + lv * 360, hanging: 240 } } } })) }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Anexo · Memoria del proceso · Barragán · Díaz · Quiroga", size: 16, color: "5C5C5A" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "página ", size: 16, color: "5C5C5A" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "5C5C5A" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(OUT, b); console.log("OK", OUT, b.length); });

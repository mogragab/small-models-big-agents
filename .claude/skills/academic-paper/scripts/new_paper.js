#!/usr/bin/env node
/**
 * new_paper.js — scaffold a LaTeX manuscript that is known to compile.
 *
 *   node new_paper.js --style apa --title "…" --author "…" --out paper.tex
 *
 * Writes paper.tex (preamble + title block + section skeleton), refs.bib if it
 * does not exist, and .latexmkrc. It probes the local TeX installation with
 * kpsewhich and picks the best available class and .bst, so the output compiles
 * on a stock TeX Live rather than assuming a full one. What it chose, and why,
 * is printed at the end and repeated as comments in the file.
 *
 * Flags
 *   --style      apa | ieee | vancouver | mla | chicago | harvard | plain
 *   --class      override the document class (elsarticle, acmart, llncs, apa7, …)
 *   --bst        override the bibliography style
 *   --title, --subtitle, --author, --affil, --email, --keywords, --date
 *   --sections   comma-separated section names (default IMRaD)
 *   --bib        bibliography file name           (default refs.bib)
 *   --out        output .tex file                 (default paper.tex)
 *   --columns 2  two-column body
 *   --spacing    single | onehalf | double        (default: style preset)
 *   --fontsize   10pt | 11pt | 12pt               (default: style preset)
 *   --toc        include a table of contents
 *   --lineno     line numbers (many journals ask for them under review)
 *   --anonymous  drop authors, affiliations and email for double-blind review
 *   --force      overwrite an existing .tex
 *
 * No npm dependencies. Node >= 14.
 */

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

// ---------------------------------------------------------------- arg parsing

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) out[key] = true;
      else { out[key] = next; i++; }
    } else out._.push(a);
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));
if (args.help || args.h) {
  console.log(fs.readFileSync(__filename, "utf8").split("*/")[0].replace(/^\/\*\*?/, ""));
  process.exit(0);
}

// ---------------------------------------------------------------- tex probing

const probeCache = new Map();
function have(file) {
  if (probeCache.has(file)) return probeCache.get(file);
  let ok = false;
  try {
    const r = execFileSync("kpsewhich", [file], { stdio: ["ignore", "pipe", "ignore"] });
    ok = r.toString().trim().length > 0;
  } catch (e) { ok = false; }
  probeCache.set(file, ok);
  return ok;
}
function firstAvailable(list, fallback) {
  for (const f of list) if (have(f)) return f.replace(/\.(cls|sty|bst)$/, "");
  return fallback;
}

// ---------------------------------------------------------------- style table

const STYLES = {
  // bstPrefs are tried in order; the first one installed wins.
  apa: {
    numeric: false, fontsize: "12pt", spacing: "double",
    bstPrefs: ["apacite.bst", "apalike.bst", "plainnat.bst"],
    // apacite does not define \citep/\citet on its own; natbibapa loads natbib
    // for it, so the same commands work whichever .bst we land on.
    extraPkg: (bst) => (bst === "apacite" ? ["[natbibapa]{apacite}"] : []),
    natbib: (bst) => bst !== "apacite",
    note: "APA 7: author-date, alphabetical, hanging indent. Cite with \\citep/\\citet.",
  },
  harvard: {
    numeric: false, fontsize: "11pt", spacing: "onehalf",
    bstPrefs: ["agsm.bst", "apalike.bst", "plainnat.bst"],
    natbib: () => true,
    note: "Harvard: author–date; variants differ by institution — say which you used.",
  },
  chicago: {
    numeric: false, fontsize: "12pt", spacing: "double",
    bstPrefs: ["chicago.bst", "apalike.bst", "plainnat.bst"],
    natbib: () => true,
    note: "Chicago author–date. For notes–bibliography you want biblatex-chicago instead.",
  },
  mla: {
    numeric: false, fontsize: "12pt", spacing: "double",
    bstPrefs: ["apalike.bst", "plainnat.bst"],
    natbib: () => true,
    note: "MLA 9 has no good BibTeX .bst; apalike approximates it. Check the output " +
          "against references/citation-styles.md and fix by hand, or use biblatex-mla.",
  },
  ieee: {
    numeric: true, fontsize: "10pt", spacing: "single", columns: 2,
    classPrefs: ["IEEEtran.cls"],
    bstPrefs: ["IEEEtran.bst", "ieeetr.bst", "unsrtnat.bst"],
    natbib: (bst) => bst !== "IEEEtran",
    note: "IEEE: bracketed numerals in order of first appearance, two columns.",
  },
  vancouver: {
    numeric: true, fontsize: "12pt", spacing: "double",
    bstPrefs: ["vancouver.bst", "unsrtnat.bst", "unsrt.bst"],
    natbib: () => true,
    note: "Vancouver: numerals in citation order, NLM-abbreviated journal names.",
  },
  plain: {
    numeric: false, fontsize: "11pt", spacing: "onehalf",
    bstPrefs: ["plainnat.bst", "plain.bst"],
    natbib: () => true,
    note: "Neutral scholarly formatting.",
  },
};

const styleName = String(args.style || "apa").toLowerCase();
const style = STYLES[styleName];
if (!style) {
  console.error(`Unknown --style "${styleName}". Options: ${Object.keys(STYLES).join(", ")}`);
  process.exit(1);
}

// ---------------------------------------------------------------- resolution

const chosen = { warnings: [] };

chosen.cls = args.class
  ? String(args.class)
  : style.classPrefs
    ? firstAvailable(style.classPrefs, "article")
    : "article";

if (args.class && !have(`${args.class}.cls`)) {
  chosen.warnings.push(
    `Class "${args.class}" is not installed. Install it (e.g. apt-get install -y ` +
    `texlive-publishers) or the build will fail.`);
} else if (style.classPrefs && chosen.cls === "article") {
  chosen.warnings.push(
    `${style.classPrefs[0].replace(".cls", "")} is not installed; fell back to article. ` +
    `For a real submission run: apt-get install -y --no-install-recommends texlive-publishers`);
}

chosen.bst = args.bst ? String(args.bst) : firstAvailable(style.bstPrefs, "plain");
if (style.bstPrefs && !have(`${style.bstPrefs[0]}`) && !args.bst) {
  chosen.warnings.push(
    `${style.bstPrefs[0]} not installed; using ${chosen.bst}. Closest match to the ` +
    `real style comes from: apt-get install -y --no-install-recommends texlive-bibtex-extra`);
}

const useNatbib = chosen.cls === "article" && style.natbib(chosen.bst);
const fontsize = args.fontsize || style.fontsize;
const spacing = args.spacing || style.spacing;
const columns = Number(args.columns || style.columns || 1);
const bibFile = String(args.bib || "refs.bib").replace(/\.bib$/, "");
const outFile = String(args.out || "paper.tex");
const anonymous = Boolean(args.anonymous);

const title = String(args.title || "Untitled Manuscript");
const subtitle = args.subtitle ? String(args.subtitle) : "";
const author = anonymous ? "" : String(args.author || "Author Name");
const affil = anonymous ? "" : String(args.affil || "");
const email = anonymous ? "" : String(args.email || "");
const keywords = String(args.keywords || "");
const date = args.date ? String(args.date) : "\\today";
const sections = String(
  args.sections || "Introduction,Background,Methods,Results,Discussion,Conclusion"
).split(",").map((s) => s.trim()).filter(Boolean);

// ---------------------------------------------------------------- generation

const opt = [fontsize, columns === 2 ? "twocolumn" : null, "a4paper"].filter(Boolean).join(",");
const spacingCmd = { single: "", onehalf: "\\onehalfspacing", double: "\\doublespacing" }[spacing] || "";

const pkgs = [
  "\\usepackage[T1]{fontenc}",
  "\\usepackage[utf8]{inputenc}",
  have("mathptmx.sty") && chosen.cls === "article" ? "\\usepackage{mathptmx}   % Times-alike" : null,
  "\\usepackage[margin=1in]{geometry}",
  "\\usepackage{setspace}",
  "\\usepackage{amsmath,amssymb}",
  "\\usepackage{graphicx}",
  "\\usepackage{booktabs}      % \\toprule \\midrule \\bottomrule; never vertical rules",
  have("threeparttable.sty") ? "\\usepackage{threeparttable} % table notes under the rule" : null,
  have("longtable.sty") ? "\\usepackage{longtable}" : null,
  "\\usepackage{caption}",
  have("subcaption.sty") ? "\\usepackage{subcaption}" : null,
  have("microtype.sty") ? "\\usepackage{microtype}" : null,
  have("csquotes.sty") ? "\\usepackage{csquotes}" : null,
  args.lineno && have("lineno.sty") ? "\\usepackage{lineno}\\linenumbers" : null,
  useNatbib
    ? `\\usepackage[${style.numeric ? "numbers,sort&compress" : "authoryear,round"}]{natbib}`
    : null,
  ...(style.extraPkg
    ? style.extraPkg(chosen.bst).map((p) => (p.startsWith("[") ? `\\usepackage${p}` : `\\usepackage{${p}}`))
    : []),
  "\\usepackage[hidelinks]{hyperref} % load last",
].filter(Boolean);

const titleBlock = chosen.cls === "article"
  ? [
      `\\title{${title}${subtitle ? `\\\\[0.4em]\\large ${subtitle}` : ""}}`,
      anonymous
        ? "\\author{}  % double-blind: authors withheld"
        : `\\author{${author}${affil ? `\\\\[0.3em]\\small ${affil}` : ""}${email ? `\\\\[0.2em]\\small \\texttt{${email}}` : ""}}`,
      `\\date{${date}}`,
    ].join("\n")
  : [`\\title{${title}}`, anonymous ? "\\author{}" : `\\author{${author}}`, `\\date{${date}}`].join("\n");

const body = sections.map((s) => {
  const label = s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  return `\\section{${s}}\n\\label{sec:${label}}\n\n% TODO: draft this section. Cite with \\citep{key} / \\citet{key}.\n`;
}).join("\n");

const tex = `% ${path.basename(outFile)} — generated by new_paper.js
% Style: ${styleName} · class: ${chosen.cls} · bibliographystyle: ${chosen.bst}
% ${style.note}
% Build:  latexmk -pdf -interaction=nonstopmode ${path.basename(outFile)}
% Every \\cite key must exist in ${bibFile}.bib and trace to sources.md.
\\documentclass[${opt}]{${chosen.cls}}

${pkgs.join("\n")}

${spacingCmd ? spacingCmd + "\n" : ""}\\bibliographystyle{${chosen.bst}}

${titleBlock}

\\begin{document}
\\maketitle

\\begin{abstract}
% 200--250 words, one paragraph, no citations. Written last: it must describe
% the paper that exists, including its actual findings.
\\end{abstract}

${keywords
  ? (chosen.cls === "IEEEtran"
      ? `\\begin{IEEEkeywords}\n${keywords}\n\\end{IEEEkeywords}\n\n`
      : `\\noindent\\textbf{Keywords:} ${keywords}\n\n`)
  : "% Keywords: four to six searchable terms not already in the title\n\n"}${args.toc ? "\\tableofcontents\n\\clearpage\n\n" : ""}${body}
\\bibliography{${bibFile}}

\\end{document}
`;

// ---------------------------------------------------------------- writing out

if (fs.existsSync(outFile) && !args.force) {
  console.error(`${outFile} already exists. Pass --force to overwrite.`);
  process.exit(1);
}
fs.writeFileSync(outFile, tex, "utf8");

const bibPath = `${bibFile}.bib`;
if (!fs.existsSync(bibPath)) {
  fs.writeFileSync(bibPath,
    `% ${bibPath} — one entry per source, written when the source is retrieved.\n` +
    `% Citekey convention: firstauthorlastnameYEARkeyword (okonkwo2023attention).\n` +
    `% Never write an entry from memory: every entry must also appear in sources.md\n` +
    `% with the DOI or URL you actually saw.\n`, "utf8");
}

const rcPath = path.join(path.dirname(outFile) || ".", ".latexmkrc");
if (!fs.existsSync(rcPath)) {
  fs.writeFileSync(rcPath, "$pdf_mode = 1;\n$bibtex_use = 2;\n$max_repeat = 5;\n", "utf8");
}

// ---------------------------------------------------------------- report

console.log(`Wrote ${outFile}`);
console.log(`  class            ${chosen.cls}`);
console.log(`  bibliographystyle ${chosen.bst}${useNatbib ? " (via natbib)" : ""}`);
console.log(`  citations        ${style.numeric ? "numeric [1]" : "author–date (Name, Year)"}`);
console.log(`  layout           ${fontsize}, ${spacing} spacing, ${columns} column${columns > 1 ? "s" : ""}`);
console.log(`  bibliography     ${bibPath}${fs.existsSync(bibPath) ? "" : " (created)"}`);
for (const w of chosen.warnings) console.log(`  ! ${w}`);
console.log(`\nNext: draft into ${outFile}, then\n  latexmk -pdf -interaction=nonstopmode ${outFile}`);

/*
 * reclassify_by_c1_c2.js
 *
 * Puts every model record in the array its own parameter count implies, so that
 * array placement and the paper's stated inclusion rule finally agree.
 *
 * Background. The database's SLM inventory was assembled before the C1/C2
 * definition existed, and the March 2026 merge filed a large block of records
 * that meet the inclusion rule (20B parameters or fewer) into models.llm
 * anyway: Qwen2.5-14B, Llama-3-8B, OLMo 2-7B, Pixtral-12B, Falcon 3 and others.
 * They are not duplicates of anything in models.slm. Two records went the other
 * way: Mistral Small 3.1 and 3.2 are 24B dense and sat in models.slm.
 *
 * After this script:
 *   models.slm  holds every record with slm_class "slm" or "small-active-moe",
 *               plus records whose parameters are undisclosed but which the
 *               vendor positions as small (these were already there and are
 *               listed explicitly below, since nothing can be computed for them)
 *   models.llm  holds everything else
 *
 * Run after update_database_2026_09.js:
 *   node source/scripts/reclassify_by_c1_c2.js
 */

const fs = require('fs');
const path = require('path');

const DB = path.join(__dirname, '..', 'merged_llm_database.json');
const db = JSON.parse(fs.readFileSync(DB, 'utf8'));

// Records with no published parameter count that stay in the SLM inventory on
// the vendor's own positioning. Listed by name so the decision is explicit and
// reviewable rather than implied by a fallback rule.
const UNDISCLOSED_KEEP_AS_SLM = new Set([
  'Nex-N2-Mini',
  'Voxtral Mini',
  'Amazon Nova Lite',
  'Amazon Nova Micro',
  'GPT-4o mini',
]);

const all = [...db.models.slm, ...db.models.llm];
const before = { slm: db.models.slm.length, llm: db.models.llm.length };
const wasInSlm = new Set(db.models.slm.map((m) => m.id));

const slm = [];
const llm = [];
const moved = { toSlm: [], toLlm: [] };

for (const m of all) {
  let target;
  if (m.slm_class === 'slm' || m.slm_class === 'small-active-moe') target = 'slm';
  else if (m.slm_class === 'undisclosed') target = UNDISCLOSED_KEEP_AS_SLM.has(m.name) ? 'slm' : 'llm';
  else target = 'llm';

  const cameFromSlm = wasInSlm.has(m.id);
  if (target === 'slm') {
    slm.push(m);
    if (!cameFromSlm) moved.toSlm.push(m);
  } else {
    llm.push(m);
    if (cameFromSlm) moved.toLlm.push(m);
  }
}

const key = (m) => String(m.release_date || '');
const sorter = (a, b) => key(b).localeCompare(key(a)) || a.name.localeCompare(b.name);
slm.sort(sorter);
llm.sort(sorter);

db.models.slm = slm;
db.models.llm = llm;

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------
console.log(`slm array: ${before.slm} -> ${slm.length}`);
console.log(`llm array: ${before.llm} -> ${llm.length}`);
console.log(`\nmoved into the SLM inventory: ${moved.toSlm.length}`);
for (const m of moved.toSlm.slice().sort(sorter)) {
  console.log(`  ${m.release_date}  ${m.name}  [${m.slm_class}]`);
}
console.log(`\nmoved out of the SLM inventory: ${moved.toLlm.length}`);
for (const m of moved.toLlm) console.log(`  ${m.release_date}  ${m.name}  [${m.slm_class}]`);

const tally = (arr) => arr.reduce((a, m) => ((a[m.slm_class] = (a[m.slm_class] || 0) + 1), a), {});
console.log('\nslm array by class:', tally(slm));
console.log('llm array by class:', tally(llm));

// ---------------------------------------------------------------------------
// Metadata
// ---------------------------------------------------------------------------
db.metadata.total_slm_variants = slm.length;
db.metadata.total_llm_variants = llm.length;
db.metadata.total_models = slm.length + llm.length;
db.metadata.version = '3.4';
db.metadata.classification_rules.array_placement =
  'models.slm holds every record whose slm_class is "slm" or "small-active-moe", i.e. every model meeting C1 (active parameters <= 20B), plus a named list of vendor-positioned small models whose parameters are undisclosed. models.llm holds the rest. Before version 3.4 placement was inherited from the March 2026 merge and did not consistently follow the rule; 3.4 reconciles it.';
db.metadata.changelog.push({
  date: db.metadata.snapshot_date,
  version: '3.4',
  summary:
    'Reconciled array placement with the stated inclusion rule. Records meeting C1 that the March 2026 merge had filed under models.llm were moved into the SLM inventory, and two 24B dense models were moved out of it.',
  moved_into_slm: moved.toSlm.length,
  moved_out_of_slm: moved.toLlm.length,
  moved_into_slm_names: moved.toSlm.map((m) => m.name).sort(),
  moved_out_of_slm_names: moved.toLlm.map((m) => m.name).sort(),
  undisclosed_kept_as_slm: [...UNDISCLOSED_KEEP_AS_SLM].sort(),
  note:
    'This changes the headline SLM variant count. The previous count of 126 reflected placement, not the inclusion rule; the new count reflects the rule.',
});

fs.writeFileSync(DB, JSON.stringify(db, null, 1) + '\n', 'utf8');
console.log('\nwrote', DB);

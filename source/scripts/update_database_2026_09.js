/*
 * update_database_2026_09.js
 *
 * Refreshes merged_llm_database.json to the 2026-09-05 snapshot.
 *
 * Two things happen here:
 *
 *  1. New model records for the May-September 2026 release wave are appended.
 *     Every record is sourced: OpenRouter's public model catalogue
 *     (https://openrouter.ai/api/v1/models, retrieved 2026-09-05) supplies the
 *     id, canonical name, first-available date, context length and Hugging Face
 *     id for API-served models; vendor announcements and model cards supply
 *     parameter counts, licences and architecture notes. Fields that no source
 *     states are left null rather than estimated.
 *
 *  2. Every record, new and existing, gains the C1/C2 classification the
 *     revised manuscript depends on (see paper Section 1.2):
 *        C1  active parameters per token <= 20B   (latency, FLOPs, energy)
 *        C2  total parameters            <= 20B   (storage, resident memory)
 *     slm_class is then one of:
 *        "slm"                    both hold
 *        "small-active-moe"       C1 holds, C2 does not
 *        "llm"                    C1 does not hold
 *        "undisclosed"            parameters not published (closed API models)
 *
 * Array placement (models.slm / models.llm) is left on the database's original
 * rule so that historical counts stay comparable; slm_class is the field the
 * paper filters on.
 *
 * Run:  node source/scripts/update_database_2026_09.js
 */

const fs = require('fs');
const path = require('path');

const DB = path.join(__dirname, '..', 'merged_llm_database.json');
const SNAPSHOT = '2026-09-05';

const db = JSON.parse(fs.readFileSync(DB, 'utf8'));

// ---------------------------------------------------------------------------
// Parameter-string parsing
// ---------------------------------------------------------------------------

/** Parse "7B", "~5B", "2.4T", "8.3B total", "3B active" -> number of params. */
function parseParams(v, prefer = 'total_params') {
  if (v == null) return null;
  if (typeof v === 'object') {
    // Some legacy records nest {total_params, active_params, architecture}.
    // Read the field the caller asked for; reading total_params for the active
    // count misfiled nested MoEs as LLMs before v3.5 (see apply_inclusion_rules.py).
    return parseParams(v[prefer] ?? v.total_params ?? null);
  }
  if (typeof v === 'number') return v;
  const s = String(v);
  if (/undisclosed|unknown|n\/a|proprietary/i.test(s)) return null;
  const m = s.match(/([\d.]+)\s*([BTM])/i);
  if (!m) return null;
  const n = parseFloat(m[1]);
  const unit = m[2].toUpperCase();
  return unit === 'T' ? n * 1000 : unit === 'M' ? n / 1000 : n; // normalise to billions
}

const THRESHOLD_B = 20;

function classify(rec) {
  const p = rec.parameters || {};
  const total = parseParams(p.total);
  const activeStated = parseParams(p.active_per_token, 'active_params');
  // For a dense model, active == total, so falling back to total is sound. For
  // an MoE whose active count is not published, it is not: assuming active ==
  // total would classify a small-active model as an LLM on no evidence. Leave
  // it null so the record reads "undisclosed" instead.
  const active = activeStated ?? (p.is_moe ? null : total);

  const c1 = active == null ? null : active <= THRESHOLD_B;
  const c2 = total == null ? null : total <= THRESHOLD_B;

  let cls;
  if (c1 == null && c2 == null) cls = 'undisclosed';
  else if (c1 === false) cls = 'llm';
  else if (c1 === true && c2 === true) cls = 'slm';
  else if (c1 === true && c2 === false) cls = 'small-active-moe';
  else cls = 'undisclosed';

  return {
    meets_c1_active_le_20b: c1,
    meets_c2_total_le_20b: c2,
    slm_class: cls,
    parsed_total_params_b: total,
    parsed_active_params_b: active,
  };
}

// ---------------------------------------------------------------------------
// New records: May - September 2026
// ---------------------------------------------------------------------------

const OR = 'https://openrouter.ai/api/v1/models (retrieved 2026-09-05)';

/** Shorthand record builder; keeps the existing schema exactly. */
function rec(o) {
  return {
    id: o.id,
    name: o.name,
    family: o.family,
    type: o.type,
    access: o.access,
    developer: o.developer,
    release_date: o.release_date,
    status: o.status || 'active',
    parameters: {
      total: o.total ?? 'Undisclosed',
      active_per_token: o.active ?? o.total ?? 'Undisclosed',
      is_moe: !!o.moe,
    },
    context_window_tokens: o.ctx ?? null,
    modalities: o.modalities || ['text'],
    license: o.license || 'Proprietary',
    use_cases: o.use_cases || [],
    reference_url: o.ref || null,
    huggingface_url: o.hf ? 'https://huggingface.co/' + o.hf : null,
    pricing_usd_per_million_tokens: o.price ?? null,
    architecture_notes: o.arch ?? null,
    languages_supported: o.langs ?? null,
    benchmarks: null,
    paper_url: o.paper ?? null,
    training_data: o.training ?? null,
    base_or_instruct: o.base_or_instruct || 'instruct',
    variants: o.variants || [],
    source_note: o.src || OR,
    source_retrieved: SNAPSHOT,
  };
}

// --- Models satisfying C1 and C2: true SLMs ---------------------------------
const NEW_SLM = [
  rec({
    id: 'granite-4.1-3b', name: 'Granite 4.1 3B', family: 'Granite 4', type: 'SLM', access: 'OW',
    developer: 'IBM', release_date: '2026-04-29', total: '3B', ctx: 131072,
    license: 'Apache 2.0', use_cases: ['enterprise', 'on-device', 'RAG'],
    ref: 'https://huggingface.co/blog/ibm-granite/granite-4-2',
    arch: 'Dense decoder-only. Part of the Granite 4.1 family (3B/8B/30B), all Apache 2.0.',
    src: 'IBM Granite 4.1 release, April 2026',
  }),
  rec({
    id: 'granite-4.1-8b', name: 'Granite 4.1 8B', family: 'Granite 4', type: 'SLM', access: 'OW',
    developer: 'IBM', release_date: '2026-04-29', total: '8B', ctx: 131072,
    license: 'Apache 2.0', use_cases: ['enterprise', 'agentic', 'RAG'],
    ref: 'https://huggingface.co/blog/ibm-granite/granite-4-2',
    arch: 'Dense decoder-only; reported to beat the previous 32B MoE on most production benchmarks.',
    src: 'IBM Granite 4.1 release, April 2026',
  }),
  rec({
    id: 'granite-4.2-3b', name: 'Granite 4.2 3B', family: 'Granite 4', type: 'SLM', access: 'OW',
    developer: 'IBM', release_date: '2026-08-25', total: '3B', ctx: 131072,
    license: 'Apache 2.0', use_cases: ['reasoning', 'on-device', 'enterprise'],
    ref: 'https://huggingface.co/blog/ibm-granite/granite-4-2', hf: 'ibm-granite/granite-4.2-3b',
    arch: 'Dense decoder-only with a thinking switch (one checkpoint reasons step by step or answers directly). GQA with 8 KV heads, RoPE theta 1e7, SwiGLU, RMSNorm, untied embeddings, bf16. Reports as ~4B on Hugging Face.',
    training: '~15T tokens, from scratch',
    src: 'IBM Granite 4.2 release 2026-08-25; Hugging Face blog',
  }),
  rec({
    id: 'granite-4.2-8b', name: 'Granite 4.2 8B', family: 'Granite 4', type: 'SLM', access: 'OW',
    developer: 'IBM', release_date: '2026-08-25', total: '8B', ctx: 131072,
    license: 'Apache 2.0', use_cases: ['reasoning', 'agentic', 'enterprise'],
    ref: 'https://huggingface.co/blog/ibm-granite/granite-4-2', hf: 'ibm-granite/granite-4.2-8b',
    arch: 'Dense reasoning model with thinking switch; staged RL pipeline trains it to act as an agent in sandboxed environments. Reports as ~9B on Hugging Face.',
    training: '~15T tokens, from scratch',
    src: 'IBM Granite 4.2 release 2026-08-25; ' + OR,
  }),
  rec({
    id: 'lfm2.5-350m', name: 'LFM2.5-350M', family: 'LFM2', type: 'SLM', access: 'OW',
    developer: 'Liquid AI', release_date: '2026', total: '350M', ctx: 131072,
    license: 'LFM1.0', use_cases: ['on-device', 'edge', 'embedded'],
    ref: 'https://www.liquid.ai/blog/lfm2-5-350m-no-size-left-behind',
    arch: 'Hybrid short-convolution / GQA architecture for on-device deployment.',
    src: 'Liquid AI model index and blog; exact release day not stated by the source',
  }),
  rec({
    id: 'lfm2.5-1.2b', name: 'LFM2.5-1.2B', family: 'LFM2', type: 'SLM', access: 'OW',
    developer: 'Liquid AI', release_date: '2026', total: '1.2B', ctx: 131072,
    license: 'LFM1.0', use_cases: ['on-device', 'edge', 'agentic'],
    ref: 'https://www.liquid.ai/models',
    arch: 'Hybrid conv/attention. Instruct and Thinking checkpoints; a Japanese variant (LFM2.5-1.2B-JP) also ships.',
    variants: ['LFM2.5-1.2B-Instruct', 'LFM2.5-1.2B-Thinking', 'LFM2.5-1.2B-JP-202606'],
    src: 'Liquid AI model index; exact release day not stated by the source',
  }),
  rec({
    id: 'lfm2.5-2.6b', name: 'LFM2.5-2.6B', family: 'LFM2', type: 'SLM', access: 'Both',
    developer: 'Liquid AI', release_date: '2026-08-04', total: '2.69B', ctx: 131072,
    license: 'LFM1.0', use_cases: ['agentic workflows', 'data extraction', 'RAG', 'long context'],
    ref: 'https://huggingface.co/LiquidAI/LFM2.5-2.6B', hf: 'LiquidAI/LFM2.5-2.6B',
    arch: '30 layers: 22 double-gated short-convolution blocks plus 8 GQA layers; 128k vocabulary. Liquid advises against agentic coding use.',
    variants: ['LFM2.5-2.6B-Base'],
    src: 'Hugging Face model card; OpenRouter listing 2026-08-11',
  }),
  rec({
    id: 'lfm2.5-8b-a1b', name: 'LFM2.5-8B-A1B', family: 'LFM2', type: 'SLM', access: 'OW',
    developer: 'Liquid AI', release_date: '2026-05-28', total: '8.3B', active: '1.5B', moe: true, ctx: 131072,
    license: 'LFM1.0', use_cases: ['on-device', 'tool calling', 'phones and laptops', 'robotics'],
    ref: 'https://www.liquid.ai/blog/lfm2-5-8b-a1b',
    arch: 'On-device hybrid MoE. Successor to LFM2-8B-A1B (Oct 2025): context expanded to 128K, pretraining scaled from 12T to 38T tokens, plus large-scale RL.',
    training: '38T tokens',
    src: 'Liquid AI blog 2026-05-28',
  }),
  rec({
    id: 'lfm2.5-vl-3b', name: 'LFM2.5-VL-3B', family: 'LFM2', type: 'SLM', access: 'OW',
    developer: 'Liquid AI', release_date: '2026', total: '3B', ctx: null,
    modalities: ['text', 'vision'], license: 'LFM1.0', use_cases: ['on-device VLM', 'document extraction'],
    ref: 'https://www.liquid.ai/models',
    src: 'Liquid AI model index; exact release day not stated by the source',
  }),
  rec({
    id: 'lfm2.5-audio-1.5b', name: 'LFM2.5-Audio-1.5B', family: 'LFM2', type: 'SLM', access: 'OW',
    developer: 'Liquid AI', release_date: '2026', total: '1.5B', ctx: null,
    modalities: ['text', 'audio'], license: 'LFM1.0', use_cases: ['on-device speech', 'transcription'],
    ref: 'https://www.liquid.ai/models',
    src: 'Liquid AI model index; exact release day not stated by the source',
  }),
  rec({
    id: 'hy-mt2-1.8b', name: 'Hy-MT2-1.8B', family: 'Hunyuan', type: 'SLM', access: 'OW',
    developer: 'Tencent', release_date: '2026-08-20', total: '1.8B', ctx: 8192,
    license: 'Tencent Hunyuan License', use_cases: ['translation', 'on-device'],
    hf: 'tencent/Hy-MT2-1.8B', ref: 'https://huggingface.co/tencent/Hy-MT2-1.8B',
    arch: 'Compact translation model. 33 language pairs plus five Chinese dialect and minority-language pairs; structured and delimiter-based workflows.',
    langs: '33 language pairs + 5 dialect/minority pairs',
  }),
  rec({
    id: 'hy-mt2-7b', name: 'Hy-MT2-7B', family: 'Hunyuan', type: 'SLM', access: 'OW',
    developer: 'Tencent', release_date: '2026-08-19', total: '7B', ctx: 8192,
    license: 'Tencent Hunyuan License', use_cases: ['translation'],
    hf: 'tencent/Hy-MT2-7B', ref: 'https://huggingface.co/tencent/Hy-MT2-7B',
    arch: 'Translation model, same coverage as Hy-MT2-1.8B at larger scale.',
    langs: '33 language pairs + 5 dialect/minority pairs',
  }),
  rec({
    id: 'nemotron-3.5-content-safety', name: 'Nemotron 3.5 Content Safety', family: 'Nemotron', type: 'SLM', access: 'OW',
    developer: 'NVIDIA', release_date: '2026-06-04', total: '4B', ctx: 131072,
    modalities: ['text', 'vision'], license: 'NVIDIA Open Model License',
    use_cases: ['guardrails', 'content moderation', 'safety'],
    hf: 'nvidia/Nemotron-3.5-Content-Safety', ref: 'https://huggingface.co/nvidia/Nemotron-3.5-Content-Safety',
    arch: 'Compact multimodal guardrail model fine-tuned from Google Gemma-3-4B. Moderates both inputs to and responses from LLMs and VLMs.',
  }),
];

// --- Models satisfying C1 but not C2: small-active-parameter MoE ------------
const NEW_SMALL_ACTIVE_MOE = [
  rec({
    id: 'nemotron-3.5-lightning', name: 'Nemotron 3.5 Lightning 30B-A3B', family: 'Nemotron', type: 'SLM', access: 'OW',
    developer: 'NVIDIA', release_date: '2026-08-11', total: '30B', active: '3B', moe: true, ctx: 262144,
    license: 'NVIDIA Open Model License', use_cases: ['agentic execution layer', 'high-volume tool calling'],
    hf: 'nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16',
    ref: 'https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/',
    arch: 'Successor to Nemotron 3 Nano 30B-A3B (31.6B total / 3.6B active). NVIDIA reports up to 4x the output speed of similar-sized models.',
  }),
  rec({
    id: 'hy-mt2-30b-a3b', name: 'Hy-MT2-30B-A3B', family: 'Hunyuan', type: 'SLM', access: 'OW',
    developer: 'Tencent', release_date: '2026-08-20', total: '30B', active: '3B', moe: true, ctx: 8192,
    license: 'Tencent Hunyuan License', use_cases: ['translation'],
    hf: 'tencent/Hy-MT2-30B-A3B', ref: 'https://huggingface.co/tencent/Hy-MT2-30B-A3B',
    arch: 'Flagship model of the Hy-MT2 translation family.',
  }),
  rec({
    id: 'north-mini-code-1.0', name: 'North Mini Code 1.0', family: 'Command', type: 'SLM', access: 'OW',
    developer: 'Cohere', release_date: '2026-06-17', total: '30B', active: '3B', moe: true, ctx: 256000,
    license: 'CC-BY-NC (Cohere Labs)', use_cases: ['coding', 'agentic coding'],
    hf: 'CohereLabs/North-Mini-Code-1.0', ref: 'https://openrouter.ai/cohere/north-mini-code',
    arch: 'Sparse mixture-of-experts optimised for coding.',
  }),
  rec({
    id: 'laguna-xs-2.1', name: 'Laguna XS 2.1', family: 'Laguna', type: 'SLM', access: 'OW',
    developer: 'Poolside', release_date: '2026-07-02', total: '33B', active: '3B', moe: true, ctx: 262144,
    license: 'See source', use_cases: ['coding agent'],
    hf: 'poolside/Laguna-XS-2.1', ref: 'https://openrouter.ai/poolside/laguna-xs-2.1',
    arch: '33B-A3B coding agent model; successor to Laguna XS.2 (April 2026).',
  }),
  rec({
    id: 'laguna-s-2.1', name: 'Laguna S 2.1', family: 'Laguna', type: 'SLM', access: 'OW',
    developer: 'Poolside', release_date: '2026-07-21', total: '118B', active: '8B', moe: true, ctx: 1048576,
    license: 'See source', use_cases: ['coding agent'],
    hf: 'poolside/Laguna-S-2.1', ref: 'https://openrouter.ai/poolside/laguna-s-2.1',
    arch: '118B total / 8B active. Reported 70.2% on Terminal-Bench 2.1.',
  }),
  rec({
    id: 'ling-3.0-flash', name: 'Ling 3.0 Flash', family: 'Ling', type: 'SLM', access: 'OW',
    developer: 'inclusionAI', release_date: '2026-07-23', total: '124B', active: '5.1B', moe: true, ctx: 262144,
    license: 'See source', use_cases: ['general', 'agentic'],
    hf: 'inclusionAI/Ling-3.0-flash', ref: 'https://openrouter.ai/inclusionai/ling-3.0-flash',
    arch: '124B-parameter MoE with roughly 5.1B parameters activated per token.',
  }),
  rec({
    id: 'ling-3.0-flash-fin', name: 'Ling 3.0 Flash Fin', family: 'Ling', type: 'SLM', access: 'API',
    developer: 'inclusionAI', release_date: '2026-08-27', total: '124B', active: '5.1B', moe: true, ctx: 262144,
    license: 'See source', use_cases: ['finance'],
    ref: 'https://openrouter.ai/inclusionai/ling-3.0-flash-fin',
    arch: 'Finance-specialised variant of Ling 3.0 Flash.',
  }),
  rec({
    id: 'ling-3.0-flash-sante', name: 'Ling 3.0 Flash Sante', family: 'Ling', type: 'SLM', access: 'API',
    developer: 'inclusionAI', release_date: '2026-09-04', total: '124B', active: '5.1B', moe: true, ctx: 262144,
    license: 'See source', use_cases: ['health', 'medicine'],
    ref: 'https://openrouter.ai/inclusionai/ling-3.0-flash-sante',
    arch: 'Health and medicine specialised variant of Ling 3.0 Flash.',
  }),
  rec({
    id: 'deepseek-v4-flash-0731', name: 'DeepSeek V4 Flash 0731', family: 'DeepSeek', type: 'SLM', access: 'OW',
    developer: 'DeepSeek', release_date: '2026-07-31', total: '284B', active: '13B', moe: true, ctx: 1310720,
    license: 'See source', use_cases: ['general', 'long context'],
    hf: 'deepseek-ai/DeepSeek-V4-Flash-0731', ref: 'https://openrouter.ai/deepseek/deepseek-v4-flash-0731',
    arch: 'Sparse MoE, 13B active of 284B total, 1.3M-token context.',
  }),
  rec({
    id: 'deepseek-v4-flash-vision-exp', name: 'DeepSeek V4 Flash Vision Exp', family: 'DeepSeek', type: 'SLM', access: 'OW',
    developer: 'DeepSeek', release_date: '2026-08-21', total: '284B', active: '13B', moe: true, ctx: 1048576,
    modalities: ['text', 'vision'], license: 'See source', use_cases: ['vision', 'long context'],
    hf: 'deepseek-ai/DeepSeek-V4-Flash-Vision-Exp', ref: 'https://openrouter.ai/deepseek/deepseek-v4-flash-vision-exp',
    arch: 'Experimental vision-enabled build of DeepSeek V4 Flash 0731.',
    status: 'experimental',
  }),
  rec({
    id: 'inkling-small', name: 'Inkling Small', family: 'Inkling', type: 'SLM', access: 'OW',
    developer: 'Thinking Machines Lab', release_date: '2026-07-30', total: '276B', active: '12B', moe: true, ctx: 1048576,
    modalities: ['text', 'vision'], license: 'See source', use_cases: ['general', 'multimodal'],
    hf: 'thinkingmachines/Inkling-Small', ref: 'https://openrouter.ai/thinkingmachines/inkling-small',
    arch: 'Open-weight multimodal MoE, 12B active of 276B total.',
  }),
  rec({
    id: 'dots3-note-preview', name: 'Dots3-Note Preview', family: 'Dots', type: 'SLM', access: 'OW',
    developer: 'Dots Studio', release_date: '2026-08-14', total: '280B', active: '16B', moe: true, ctx: 512000,
    license: 'See source', use_cases: ['note taking', 'general'],
    ref: 'https://openrouter.ai/dots-studio/dots-3-note-preview',
    arch: 'Open-weight MoE, 16B active of 280B total.', status: 'preview',
  }),
  rec({
    id: 'nex-n2-pro', name: 'Nex-N2-Pro', family: 'Nex-N2', type: 'SLM', access: 'OW',
    developer: 'Nex AGI', release_date: '2026-06-08', total: '397B', active: '17B', moe: true, ctx: 262144,
    modalities: ['text', 'vision'], license: 'See source', use_cases: ['agentic', 'coding', 'tool use'],
    hf: 'nex-agi/Nex-N2-Pro', ref: 'https://openrouter.ai/nex-agi/nex-n2-pro',
    arch: 'Agentic MoE, 17B active of 397B total.',
  }),
  rec({
    id: 'nex-n2-mini', name: 'Nex-N2-Mini', family: 'Nex-N2', type: 'SLM', access: 'OW',
    developer: 'Nex AGI', release_date: '2026-06-24', ctx: 262144,
    modalities: ['text', 'vision'], license: 'See source', use_cases: ['agentic', 'coding', 'tool use'],
    hf: 'nex-agi/Nex-N2-Mini', ref: 'https://openrouter.ai/nex-agi/nex-n2-mini',
    arch: 'Open-source agentic MoE, smaller sibling in the Nex-N2 series. Parameter counts not stated by the source.',
  }),
];

// --- LLMs: > 20B active, or closed API with undisclosed parameters ----------
const NEW_LLM = [
  // OpenAI
  rec({ id: 'gpt-5.6-sol', name: 'GPT-5.6 Sol', family: 'GPT-5', type: 'LLM', access: 'API', developer: 'OpenAI',
    release_date: '2026-07-09', ctx: 1050000, modalities: ['text', 'vision'],
    use_cases: ['complex reasoning', 'coding', 'agentic workflows'],
    ref: 'https://openrouter.ai/openai/gpt-5.6-sol', variants: ['GPT-5.6 Sol Pro'],
    arch: 'Flagship tier of the GPT-5.6 series; strong at command-line and multi-step coding.' }),
  rec({ id: 'gpt-5.6-terra', name: 'GPT-5.6 Terra', family: 'GPT-5', type: 'LLM', access: 'API', developer: 'OpenAI',
    release_date: '2026-07-09', ctx: 1050000, modalities: ['text', 'vision'],
    use_cases: ['everyday coding', 'reasoning', 'agentic'],
    ref: 'https://openrouter.ai/openai/gpt-5.6-terra', variants: ['GPT-5.6 Terra Pro'],
    arch: 'Balanced tier, between the Sol flagship and the Luna cost-efficient tier.' }),
  rec({ id: 'gpt-5.6-luna', name: 'GPT-5.6 Luna', family: 'GPT-5', type: 'LLM', access: 'API', developer: 'OpenAI',
    release_date: '2026-07-09', ctx: 1050000, modalities: ['text', 'vision'],
    use_cases: ['high-volume chat', 'classification', 'lightweight agents'],
    ref: 'https://openrouter.ai/openai/gpt-5.6-luna', variants: ['GPT-5.6 Luna Pro'],
    arch: 'Cost-efficient, latency-sensitive tier; became the ChatGPT free-tier default in August 2026.' }),
  rec({ id: 'gpt-6-astra', name: 'GPT-6 Astra', family: 'GPT-6', type: 'LLM', access: 'API', developer: 'OpenAI',
    release_date: '2026-09-03', ctx: 1050000, modalities: ['text', 'vision'],
    use_cases: ['advanced analysis', 'software engineering', 'deep research', 'document creation'],
    ref: 'https://openai.com/index/gpt-6-astra/', variants: ['GPT-6 Astra Pro'],
    arch: 'OpenAI flagship for demanding end-to-end work. Limited preview 2026-09-03, public release 2026-09-05.' }),

  // Anthropic
  rec({ id: 'claude-opus-4.8', name: 'Claude Opus 4.8', family: 'Claude', type: 'LLM', access: 'API', developer: 'Anthropic',
    release_date: '2026-05-27', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['reasoning', 'coding', 'agentic'], ref: 'https://openrouter.ai/anthropic/claude-opus-4.8' }),
  rec({ id: 'claude-fable-5', name: 'Claude Fable 5', family: 'Claude', type: 'LLM', access: 'API', developer: 'Anthropic',
    release_date: '2026-06-09', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['autonomous knowledge work', 'coding'],
    ref: 'https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5',
    arch: 'Mythos-class model. Access was suspended 2026-06-12 under US Department of Commerce export controls and restored 2026-07-01.' }),
  rec({ id: 'claude-sonnet-5', name: 'Claude Sonnet 5', family: 'Claude', type: 'LLM', access: 'API', developer: 'Anthropic',
    release_date: '2026-06-30', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['coding', 'agents', 'professional work'], ref: 'https://openrouter.ai/anthropic/claude-sonnet-5',
    arch: 'Most capable Sonnet-class model; adaptive thinking with selectable reasoning effort.' }),
  rec({ id: 'claude-opus-5', name: 'Claude Opus 5', family: 'Claude', type: 'LLM', access: 'API', developer: 'Anthropic',
    release_date: '2026-07-24', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['demanding reasoning', 'coding', 'long-horizon agentic'],
    ref: 'https://openrouter.ai/anthropic/claude-opus-5' }),
  rec({ id: 'claude-fable-5.1', name: 'Claude Fable 5.1', family: 'Claude', type: 'LLM', access: 'API', developer: 'Anthropic',
    release_date: '2026-09-01', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['agentic coding', 'long-running agentic workflows', 'knowledge work'],
    ref: 'https://openrouter.ai/anthropic/claude-fable-5.1' }),

  // Google
  rec({ id: 'gemini-3.1-flash-lite', name: 'Gemini 3.1 Flash Lite', family: 'Gemini 3', type: 'LLM', access: 'API',
    developer: 'Google DeepMind', release_date: '2026-05-07', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['low-latency', 'high-volume'],
    ref: 'https://openrouter.ai/google/gemini-3.1-flash-lite' }),
  rec({ id: 'gemini-3.5-flash', name: 'Gemini 3.5 Flash', family: 'Gemini 3', type: 'LLM', access: 'API',
    developer: 'Google DeepMind', release_date: '2026-05-19', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['coding', 'parallel agents'],
    ref: 'https://openrouter.ai/google/gemini-3.5-flash' }),
  rec({ id: 'gemini-3.5-flash-lite', name: 'Gemini 3.5 Flash Lite', family: 'Gemini 3', type: 'LLM', access: 'API',
    developer: 'Google DeepMind', release_date: '2026-07-21', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['subagents', 'focused tasks'],
    ref: 'https://openrouter.ai/google/gemini-3.5-flash-lite' }),
  rec({ id: 'gemini-3.6-flash', name: 'Gemini 3.6 Flash', family: 'Gemini 3', type: 'LLM', access: 'API',
    developer: 'Google DeepMind', release_date: '2026-07-21', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['coding', 'agentic', 'web and app development'],
    ref: 'https://openrouter.ai/google/gemini-3.6-flash' }),
  rec({ id: 'gemini-3.7-flash', name: 'Gemini 3.7 Flash', family: 'Gemini 3', type: 'LLM', access: 'API',
    developer: 'Google DeepMind', release_date: '2026-08-13', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['fast agentic workflows', 'coding'],
    ref: 'https://openrouter.ai/google/gemini-3.7-flash' }),
  rec({ id: 'gemini-3.8-flash', name: 'Gemini 3.8 Flash', family: 'Gemini 3', type: 'LLM', access: 'API',
    developer: 'Google DeepMind', release_date: '2026-09-02', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'],
    use_cases: ['software engineering', 'agentic tasks', 'multi-step reasoning'],
    ref: 'https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/',
    price: { input: 0.75, output: 3.75, note: 'introductory rate to 2026-12-31; standard 1.50 / 7.50' },
    arch: 'Built on 3.7 Flash rather than a new base model; spends more thinking tokens. Google advises staying on 3.7 Flash for efficiency-first workloads.',
    variants: ['Gemini 3.8 Flash Cyber (security variant, gated via the Fairwind Program)'] }),

  // xAI
  rec({ id: 'grok-build-0.1', name: 'Grok Build 0.1', family: 'Grok', type: 'LLM', access: 'API', developer: 'xAI',
    release_date: '2026-05-20', ctx: 256000, modalities: ['text', 'vision'],
    use_cases: ['agentic software engineering'], ref: 'https://openrouter.ai/x-ai/grok-build-0.1' }),
  rec({ id: 'grok-4.5', name: 'Grok 4.5', family: 'Grok', type: 'LLM', access: 'API', developer: 'xAI',
    release_date: '2026-07-08', ctx: 500000, modalities: ['text', 'vision'],
    use_cases: ['coding', 'knowledge work', 'STEM'], ref: 'https://openrouter.ai/x-ai/grok-4.5' }),
  rec({ id: 'grok-4.6', name: 'Grok 4.6', family: 'Grok', type: 'LLM', access: 'API', developer: 'xAI',
    release_date: '2026-08-12', ctx: 500000, modalities: ['text', 'vision'],
    use_cases: ['coding', 'knowledge work', 'STEM'], ref: 'https://openrouter.ai/x-ai/grok-4.6' }),

  // Alibaba
  rec({ id: 'qwen3.7-max', name: 'Qwen3.7 Max', family: 'Qwen3', type: 'LLM', access: 'API', developer: 'Alibaba',
    release_date: '2026-05-21', ctx: 1000000, use_cases: ['agentic', 'coding', 'office productivity'],
    ref: 'https://openrouter.ai/qwen/qwen3.7-max' }),
  rec({ id: 'qwen3.7-plus', name: 'Qwen3.7 Plus', family: 'Qwen3', type: 'LLM', access: 'API', developer: 'Alibaba',
    release_date: '2026-06-03', ctx: 1000000, modalities: ['text', 'vision'], use_cases: ['cost-effective general'],
    ref: 'https://openrouter.ai/qwen/qwen3.7-plus' }),
  rec({ id: 'qwen3.7-flash', name: 'Qwen3.7 Flash', family: 'Qwen3', type: 'LLM', access: 'API', developer: 'Alibaba',
    release_date: '2026-07-27', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['multimodal agents', 'visual coding', 'computer interaction'],
    ref: 'https://openrouter.ai/qwen/qwen3.7-flash' }),
  rec({ id: 'qwen3.8-max', name: 'Qwen3.8 Max', family: 'Qwen3', type: 'LLM', access: 'API', developer: 'Alibaba',
    release_date: '2026-08-03', total: '2.4T', active: '95B', moe: true, ctx: 1000000,
    modalities: ['text', 'vision', 'video'], use_cases: ['coding', 'agentic'],
    ref: 'https://openrouter.ai/qwen/qwen3.8-max-0902',
    arch: '2.4T-parameter MoE. Previewed 2026-07-19, released 2026-08-03; a 0902 refresh followed on 2026-09-02.',
    variants: ['Qwen3.8 Max (0902)'] }),
  rec({ id: 'qwen3.8-2.4t-a95b', name: 'Qwen3.8 2.4T A95B', family: 'Qwen3', type: 'LLM', access: 'OW', developer: 'Alibaba',
    release_date: '2026-08-12', total: '2.4T', active: '95B', moe: true, ctx: 1048576,
    modalities: ['text', 'vision', 'video'], license: 'Apache 2.0', use_cases: ['coding', 'agentic'],
    hf: 'Qwen/Qwen3.8-2.4T-A95B', ref: 'https://openrouter.ai/qwen/qwen3.8-2.4t-a95b',
    arch: 'Open-weight release of Qwen3.8 Max: 95B active of 2.4T total.' }),
  rec({ id: 'qwen3.8-27b', name: 'Qwen3.8 27B', family: 'Qwen3', type: 'LLM', access: 'OW', developer: 'Alibaba',
    release_date: '2026-08-14', total: '27B', ctx: 1000000, modalities: ['text', 'vision', 'video'],
    license: 'Apache 2.0', use_cases: ['local deployment', 'multimodal'],
    hf: 'Qwen/Qwen3.8-27B', ref: 'https://openrouter.ai/qwen/qwen3.8-27b',
    arch: 'Dense natively multimodal model (text, images, video, diagrams, documents); native 262K context, served to 1M.' }),
  rec({ id: 'qwen3.8-flash', name: 'Qwen3.8 Flash', family: 'Qwen3', type: 'LLM', access: 'Both', developer: 'Alibaba',
    release_date: '2026-08-26', ctx: 1000000, modalities: ['text', 'vision'],
    use_cases: ['coding assistance', 'agentic workflows', 'document and codebase analysis'],
    hf: 'Qwen/Qwen3.8-Flash-Next', ref: 'https://openrouter.ai/qwen/qwen3.8-flash' }),

  // Z.ai
  rec({ id: 'glm-5.2', name: 'GLM 5.2', family: 'GLM', type: 'LLM', access: 'OW', developer: 'Z.ai (Zhipu AI)',
    release_date: '2026-06-16', ctx: 1048576, license: 'See source',
    use_cases: ['long-horizon agents', 'project-level software engineering'],
    hf: 'zai-org/GLM-5.2', ref: 'https://openrouter.ai/z-ai/glm-5.2' }),
  rec({ id: 'glm-5.3', name: 'GLM 5.3', family: 'GLM', type: 'LLM', access: 'OW', developer: 'Z.ai (Zhipu AI)',
    release_date: '2026-08-18', ctx: 1310720, license: 'See source',
    use_cases: ['complex software engineering', 'long-horizon agents'],
    hf: 'zai-org/GLM-5.3', ref: 'https://openrouter.ai/z-ai/glm-5.3' }),
  rec({ id: 'glm-5.3-flash', name: 'GLM 5.3 Flash', family: 'GLM', type: 'LLM', access: 'OW', developer: 'Z.ai (Zhipu AI)',
    release_date: '2026-08-26', ctx: 1310720, modalities: ['text', 'vision'], license: 'See source',
    use_cases: ['efficient coding', 'long-horizon agents'],
    hf: 'zai-org/GLM-5.3-Flash', ref: 'https://openrouter.ai/z-ai/glm-5.3-flash',
    arch: 'Native multimodal; hybrid sparse and linear attention for long context.' }),

  // DeepSeek
  rec({ id: 'deepseek-v4-pro-0813', name: 'DeepSeek V4 Pro 0813', family: 'DeepSeek', type: 'LLM', access: 'OW',
    developer: 'DeepSeek', release_date: '2026-08-12', ctx: 1048576, license: 'See source',
    use_cases: ['general', 'reasoning'], hf: 'deepseek-ai/DeepSeek-V4-Pro-0813',
    ref: 'https://openrouter.ai/deepseek/deepseek-v4-pro-0813', arch: 'GA release of DeepSeek V4 Pro; large-scale MoE.' }),

  // Moonshot
  rec({ id: 'kimi-k2.7-code', name: 'Kimi K2.7 Code', family: 'Kimi', type: 'LLM', access: 'OW', developer: 'Moonshot AI',
    release_date: '2026-06-12', ctx: 262144, modalities: ['text', 'vision'], license: 'Modified MIT',
    use_cases: ['end-to-end programming'], hf: 'moonshotai/Kimi-K2.7-Code',
    ref: 'https://openrouter.ai/moonshotai/kimi-k2.7-code', arch: 'Native multimodal MoE, coding-focused.' }),
  rec({ id: 'kimi-k3', name: 'Kimi K3', family: 'Kimi', type: 'LLM', access: 'OW', developer: 'Moonshot AI',
    release_date: '2026-07-16', total: '2.8T', active: '50B', moe: true, ctx: 1048576,
    modalities: ['text', 'vision'], license: 'Modified MIT',
    use_cases: ['complex coding', 'knowledge work', 'long-horizon agentic'],
    hf: 'moonshotai/Kimi-K3', ref: 'https://openrouter.ai/moonshotai/kimi-k3',
    arch: '2.8T-parameter open-weight multimodal reasoning model, roughly 50B active.' }),

  // Meta
  rec({ id: 'muse-spark-1.1', name: 'Muse Spark 1.1', family: 'Muse', type: 'LLM', access: 'API',
    developer: 'Meta Superintelligence Labs', release_date: '2026-07-16', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['agentic tasks'],
    ref: 'https://openrouter.ai/meta/muse-spark-1.1' }),
  rec({ id: 'muse-spark-1.2', name: 'Muse Spark 1.2', family: 'Muse', type: 'LLM', access: 'API',
    developer: 'Meta Superintelligence Labs', release_date: '2026-08-05', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'], use_cases: ['complex agentic tasks'],
    ref: 'https://openrouter.ai/meta/muse-spark-1.2', variants: ['Muse Spark 1.2 Contributor'] }),
  rec({ id: 'muse-glimmer-30b', name: 'Muse Glimmer 30B', family: 'Muse', type: 'LLM', access: 'OW',
    developer: 'Meta Superintelligence Labs', release_date: '2026-08-09', total: '30B', ctx: 131072,
    modalities: ['text', 'vision'], license: 'Apache 2.0',
    use_cases: ['local agents', 'consumer hardware', 'always-on agents'],
    hf: 'meta-models/Muse-Glimmer-30B', ref: 'https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model',
    arch: 'Dense open-weight multimodal model distilled from Muse Spark. Meta\'s first open-weight release since Llama 4 and the first from the restructured Superintelligence Labs. Ships with a speculative-decoding drafter; a quantized build runs on a single 24GB consumer GPU.' }),
  rec({ id: 'muse-spark-1.3', name: 'Muse Spark 1.3', family: 'Muse', type: 'LLM', access: 'API',
    developer: 'Meta Superintelligence Labs', release_date: '2026-09-02', ctx: 1048576,
    modalities: ['text', 'vision', 'audio', 'video'],
    use_cases: ['long-running agentic', 'multi-agent', 'coding'],
    ref: 'https://openrouter.ai/meta/muse-spark-1.3', variants: ['Muse Spark 1.3 Contributor'] }),

  // NVIDIA
  rec({ id: 'nemotron-3-ultra-550b-a55b', name: 'Nemotron 3 Ultra 550B-A55B', family: 'Nemotron', type: 'LLM', access: 'OW',
    developer: 'NVIDIA', release_date: '2026-06-04', total: '550B', active: '55B', moe: true, ctx: 262144,
    license: 'NVIDIA Open Model License', use_cases: ['frontier reasoning', 'orchestration'],
    hf: 'nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16',
    ref: 'https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b' }),

  // Tencent
  rec({ id: 'hy3', name: 'Hy3', family: 'Hunyuan', type: 'LLM', access: 'OW', developer: 'Tencent',
    release_date: '2026-07-06', total: '295B', active: '21B', moe: true, ctx: 262144, license: 'See source',
    use_cases: ['reasoning', 'agentic workflows'], hf: 'tencent/Hy3', ref: 'https://openrouter.ai/tencent/hy3',
    arch: '192 experts with top-8 routing; 21B active per token.' }),
  rec({ id: 'hy4-preview', name: 'Hy4 preview', family: 'Hunyuan', type: 'LLM', access: 'OW', developer: 'Tencent',
    release_date: '2026-08-28', total: '770B', active: '49B', moe: true, ctx: 1048576, license: 'See source',
    use_cases: ['general', 'reasoning'], ref: 'https://openrouter.ai/tencent/hy4-preview', status: 'preview' }),

  // Others
  rec({ id: 'minimax-m3', name: 'MiniMax M3', family: 'MiniMax', type: 'LLM', access: 'OW', developer: 'MiniMax',
    release_date: '2026-05-31', ctx: 1048576, modalities: ['text', 'vision', 'video'], license: 'See source',
    use_cases: ['long-horizon agentic', 'coding'], hf: 'MiniMaxAI/Minimax-M3',
    ref: 'https://openrouter.ai/minimax/minimax-m3' }),
  rec({ id: 'step-3.7-flash', name: 'Step 3.7 Flash', family: 'Step', type: 'LLM', access: 'OW', developer: 'StepFun',
    release_date: '2026-05-28', total: '196B', moe: true, ctx: 262144, modalities: ['text', 'vision', 'video'],
    license: 'See source', use_cases: ['multimodal', 'efficient inference'], hf: 'stepfun-ai/Step-3.7-Flash',
    ref: 'https://openrouter.ai/stepfun/step-3.7-flash',
    arch: '196B-parameter language backbone plus a vision encoder for native image and video understanding. Active-parameter count not stated by the source.' }),
  rec({ id: 'longcat-2.0', name: 'LongCat 2.0', family: 'LongCat', type: 'LLM', access: 'OW', developer: 'Meituan',
    release_date: '2026-07-20', total: '1.6T', active: '48B', moe: true, ctx: 1048756, license: 'See source',
    use_cases: ['general'], hf: 'meituan-longcat/LongCat-2.0', ref: 'https://openrouter.ai/meituan/longcat-2.0' }),
  rec({ id: 'inkling', name: 'Inkling', family: 'Inkling', type: 'LLM', access: 'OW',
    developer: 'Thinking Machines Lab', release_date: '2026-07-17', total: '975B', active: '41B', moe: true,
    ctx: 1048576, modalities: ['text', 'vision'], license: 'See source', use_cases: ['general', 'multimodal'],
    hf: 'thinkingmachines/Inkling', ref: 'https://openrouter.ai/thinkingmachines/inkling' }),
  rec({ id: 'solar-pro4', name: 'Solar Pro 4', family: 'Solar', type: 'LLM', access: 'API', developer: 'Upstage',
    release_date: '2026-08-10', ctx: 524288, use_cases: ['long-horizon tasks', 'office productivity'],
    ref: 'https://openrouter.ai/upstage/solar-pro4' }),
  rec({ id: 'seed-2.1-turbo', name: 'Seed 2.1 Turbo', family: 'Seed', type: 'LLM', access: 'API',
    developer: 'ByteDance Seed', release_date: '2026-08-12', ctx: 262144, modalities: ['text', 'vision'],
    use_cases: ['coding', 'long-horizon agents'], ref: 'https://openrouter.ai/bytedance-seed/seed-2-1-turbo' }),
  rec({ id: 'seed-2.0-code', name: 'Seed 2.0 Code', family: 'Seed', type: 'LLM', access: 'API',
    developer: 'ByteDance Seed', release_date: '2026-08-12', ctx: 262144,
    use_cases: ['agentic coding', 'frontend development'], ref: 'https://openrouter.ai/bytedance-seed/seed-2.0-code' }),
  rec({ id: 'mercury-2.5-preview', name: 'Mercury 2.5 Preview', family: 'Mercury', type: 'LLM', access: 'API',
    developer: 'Inception', release_date: '2026-08-31', ctx: 260000, use_cases: ['fast reasoning'],
    ref: 'https://openrouter.ai/inception/mercury-2.5-preview', status: 'preview',
    arch: 'Diffusion LLM: produces and refines multiple tokens in parallel rather than generating them sequentially.' }),
  rec({ id: 'mai-thinking-1', name: 'MAI-Thinking-1', family: 'MAI', type: 'LLM', access: 'API',
    developer: 'Microsoft AI', release_date: '2026-06-02', total: '~1T', active: '35B', moe: true, ctx: 256000,
    use_cases: ['reasoning', 'code'],
    ref: 'https://microsoft.ai/news/microsoft-build-2026-mai-keynote-transcript/',
    arch: 'Microsoft\'s first flagship in-house reasoning model, announced at Build 2026 alongside six other MAI models. Trained without OpenAI distillation on commercially licensed data.',
    src: 'Microsoft Build 2026 keynote' }),
  rec({ id: 'perceptron-mk1', name: 'Perceptron Mk1', family: 'Perceptron', type: 'LLM', access: 'API',
    developer: 'Perceptron', release_date: '2026-05-12', ctx: 32768, modalities: ['text', 'vision', 'video'],
    use_cases: ['video understanding', 'embodied reasoning'], ref: 'https://openrouter.ai/perceptron/perceptron-mk1' }),
  rec({ id: 'mistral-medium-3.5', name: 'Mistral Medium 3.5', family: 'Mistral', type: 'LLM', access: 'OW',
    developer: 'Mistral AI', release_date: '2026-05-22', total: '128B', ctx: 262144, license: 'Modified MIT',
    use_cases: ['instruction following', 'reasoning', 'coding'],
    ref: 'https://hidekazu-konishi.com/entry/open_weights_llm_release_history_and_timeline.html',
    arch: 'Dense model merging instruction following, reasoning, and coding in one set of weights; introduced with Mistral\'s Vibe coding environment.',
    src: 'Open-weights release timeline (hidekazu-konishi.com), retrieved 2026-09-05' }),
];

// ---------------------------------------------------------------------------
// Corrections to existing records, from sources retrieved 2026-09-05
// ---------------------------------------------------------------------------
const CORRECTIONS = [
  {
    match: (m) => m.name === 'Gemma 4 26B (MoE)',
    apply: (m) => {
      m.parameters.active_per_token = '3.8B';
      m.parameters.is_moe = true;
      m.architecture_notes =
        'Mixture-of-experts, 3.8B active per token of 26B total. Part of the Gemma 4 family (E2B 2.3B effective, E4B 4.5B effective, 12B unified multimodal, 26B MoE, 31B dense).';
      m.source_note = 'Gemma 4 launch coverage and Hugging Face Gemma 4 blog, retrieved 2026-09-05';
      m.source_retrieved = SNAPSHOT;
    },
    why: 'active_per_token was "undisclosed"; the published figure is 3.8B active of 26B total',
  },
];

// ---------------------------------------------------------------------------
// New families
// ---------------------------------------------------------------------------
const NEW_FAMILIES = [
  { name: 'GPT-6', developer: 'OpenAI', latest_version: 'GPT-6 Astra (Sep 2026)', url: 'https://openai.com/index/gpt-6-astra/' },
  { name: 'Muse', developer: 'Meta Superintelligence Labs', latest_version: 'Muse Spark 1.3 (Sep 2026)', url: 'https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model' },
  { name: 'Ling', developer: 'inclusionAI', latest_version: 'Ling 3.0 Flash Sante (Sep 2026)', url: 'https://huggingface.co/inclusionAI/Ling-3.0-flash' },
  { name: 'Laguna', developer: 'Poolside', latest_version: 'Laguna S 2.1 (Jul 2026)', url: 'https://poolside.ai/' },
  { name: 'Inkling', developer: 'Thinking Machines Lab', latest_version: 'Inkling Small (Jul 2026)', url: 'https://huggingface.co/thinkingmachines/Inkling' },
  { name: 'Nex-N2', developer: 'Nex AGI', latest_version: 'Nex-N2-Mini (Jun 2026)', url: 'https://huggingface.co/nex-agi/Nex-N2-Pro' },
  { name: 'MAI', developer: 'Microsoft AI', latest_version: 'MAI-Thinking-1 (Jun 2026)', url: 'https://microsoft.ai/news/microsoft-build-2026-mai-keynote-transcript/' },
  { name: 'Dots', developer: 'Dots Studio', latest_version: 'Dots3-Note Preview (Aug 2026)', url: 'https://openrouter.ai/dots-studio/dots-3-note-preview' },
  { name: 'Mercury', developer: 'Inception', latest_version: 'Mercury 2.5 Preview (Aug 2026)', url: 'https://openrouter.ai/inception/mercury-2.5-preview' },
  { name: 'LongCat', developer: 'Meituan', latest_version: 'LongCat 2.0 (Jul 2026)', url: 'https://huggingface.co/meituan-longcat/LongCat-2.0' },
  { name: 'Perceptron', developer: 'Perceptron', latest_version: 'Perceptron Mk1 (May 2026)', url: 'https://openrouter.ai/perceptron/perceptron-mk1' },
  { name: 'Step', developer: 'StepFun', latest_version: 'Step 3.7 Flash (May 2026)', url: 'https://huggingface.co/stepfun-ai/Step-3.7-Flash' },
  { name: 'Solar', developer: 'Upstage', latest_version: 'Solar Pro 4 (Aug 2026)', url: 'https://www.upstage.ai/' },
  { name: 'Seed', developer: 'ByteDance Seed', latest_version: 'Seed 2.1 Turbo (Aug 2026)', url: 'https://seed.bytedance.com/' },
];

// ---------------------------------------------------------------------------
// Apply
// ---------------------------------------------------------------------------

const existingIds = new Set([...db.models.slm, ...db.models.llm].map((m) => m.id));
const existingNames = new Set([...db.models.slm, ...db.models.llm].map((m) => (m.name || '').toLowerCase()));

function addAll(target, list, label) {
  let added = 0, skipped = [];
  for (const r of list) {
    if (existingIds.has(r.id) || existingNames.has(r.name.toLowerCase())) { skipped.push(r.name); continue; }
    target.push(r); existingIds.add(r.id); existingNames.add(r.name.toLowerCase()); added++;
  }
  console.log(`${label}: added ${added}` + (skipped.length ? `, skipped as duplicates: ${skipped.join(', ')}` : ''));
}

// Small-active MoE models keep the database's historical array placement (slm),
// but slm_class distinguishes them.
addAll(db.models.slm, NEW_SLM, 'SLM (C1+C2)');
addAll(db.models.slm, NEW_SMALL_ACTIVE_MOE, 'Small-active MoE (C1 only)');
addAll(db.models.llm, NEW_LLM, 'LLM');

// Corrections
for (const c of CORRECTIONS) {
  for (const arr of [db.models.slm, db.models.llm]) {
    for (const m of arr) if (c.match(m)) { c.apply(m); console.log('corrected:', m.name, '--', c.why); }
  }
}

// Families
const famNames = new Set(db.families.map((f) => f.name));
let famAdded = 0;
for (const f of NEW_FAMILIES) if (!famNames.has(f.name)) { db.families.push(f); famNames.add(f.name); famAdded++; }
db.families.sort((a, b) => a.name.localeCompare(b.name));
console.log('families added:', famAdded);

// Classify every record, old and new
const tally = {};
for (const arr of [db.models.slm, db.models.llm]) {
  for (const m of arr) {
    const c = classify(m);
    m.meets_c1_active_le_20b = c.meets_c1_active_le_20b;
    m.meets_c2_total_le_20b = c.meets_c2_total_le_20b;
    m.slm_class = c.slm_class;
    tally[c.slm_class] = (tally[c.slm_class] || 0) + 1;
  }
}
console.log('slm_class tally (all records):', tally);

// Sort each array by release date descending, then name
const key = (m) => String(m.release_date || '');
db.models.slm.sort((a, b) => key(b).localeCompare(key(a)) || a.name.localeCompare(b.name));
db.models.llm.sort((a, b) => key(b).localeCompare(key(a)) || a.name.localeCompare(b.name));

// Metadata
db.metadata.snapshot_date = SNAPSHOT;
db.metadata.version = '3.3';
db.metadata.total_slm_variants = db.models.slm.length;
db.metadata.total_llm_variants = db.models.llm.length;
db.metadata.total_models = db.models.slm.length + db.models.llm.length;
db.metadata.total_model_families = db.families.length;
db.metadata.classification_rules = {
  array_placement: 'Historical rule, retained so counts stay comparable across snapshots: models.slm holds models with <=20B dense parameters OR <=20B active parameters in an MoE; models.llm holds the rest.',
  C1: 'meets_c1_active_le_20b: active parameters per token <= 20B. Bounds latency, FLOPs and energy.',
  C2: 'meets_c2_total_le_20b: total parameters <= 20B. Bounds storage, download size and resident memory.',
  slm_class: {
    slm: 'C1 and C2 both hold. The class the survey makes on-device and memory claims about.',
    'small-active-moe': 'C1 holds, C2 does not. SLM-like per-token cost, LLM-like residency cost. Excluded from storage, download and on-device claims.',
    llm: 'C1 does not hold.',
    undisclosed: 'Parameter counts not published, typical of closed API models.',
  },
  note: 'null in meets_c1/meets_c2 means the source does not state the figure. Nothing is imputed.',
};
db.metadata.changelog = db.metadata.changelog || [];
db.metadata.changelog.push({
  date: SNAPSHOT,
  version: '3.3',
  summary: 'Added the May-September 2026 release wave and introduced the C1/C2 classification used by the revised manuscript.',
  models_added: NEW_SLM.length + NEW_SMALL_ACTIVE_MOE.length + NEW_LLM.length,
  families_added: famAdded,
  primary_sources: [
    'OpenRouter public model catalogue, https://openrouter.ai/api/v1/models, retrieved 2026-09-05',
    'Vendor announcements and Hugging Face model cards, retrieved 2026-09-05',
  ],
});
const srcNames = new Set((db.metadata.sources || []).map((s) => s.name));
if (!srcNames.has('OpenRouter model catalogue')) {
  db.metadata.sources.push({ name: 'OpenRouter model catalogue', url: 'https://openrouter.ai/api/v1/models' });
}

fs.writeFileSync(DB, JSON.stringify(db, null, 1) + '\n', 'utf8');
console.log('\nwrote', DB);
console.log('slm array:', db.models.slm.length, '| llm array:', db.models.llm.length, '| families:', db.families.length);

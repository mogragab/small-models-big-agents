import json, re, statistics, hashlib
from pathlib import Path
from collections import Counter

root = Path(__file__).resolve().parents[1]
db = json.loads((root/'source/merged_llm_database.json').read_text(encoding='utf-8'))
rows=db['models']['slm']
result={'array_counts':{k:len(v) for k,v in db['models'].items()},'classes':dict(Counter(r.get('slm_class') for r in rows)), 'years':dict(Counter(str(r.get('release_date'))[:4] for r in rows)), 'record_example':rows[0], 'excluded':db['models']['excluded']}
files=list((root/'ACM-Journals/sections').glob('*.tex'))+list((root/'ACM-Journals/partials').glob('*.tex'))+[root/'ACM-Journals/less-is-more.tex',root/'ACM-Journals/supplement.tex']
texts={str(p.relative_to(root)):p.read_text(encoding='utf-8') for p in files}
bib=(root/'ACM-Journals/bibliography.bib').read_text(encoding='utf-8')
keys=re.findall(r'@\w+\s*\{\s*([^,]+)',bib)
cites=set(); labels=[]; refs=set()
for t in texts.values():
 t=re.sub(r'(?m)(?<!\\)%.*$','',t)
 for c in re.findall(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',t): cites.update(x.strip() for x in c.split(','))
 labels.extend(re.findall(r'\\label\{([^}]+)\}',t))
 refs.update(re.findall(r'\\(?:ref|pageref|autoref)\{([^}]+)\}',t))
result.update(bib_entries=len(keys),citation_keys=len(cites),missing_citations=sorted(cites-set(keys)),duplicate_bib_keys=[k for k,n in Counter(keys).items() if n>1],missing_labels=sorted(refs-set(labels)),duplicate_labels=[k for k,n in Counter(labels).items() if n>1])
result['copy_differences']=[p.name for p in (root/'ACM-Journals/sections').glob('*.tex') if (root/'paper_consolidated/sections'/p.name).exists() and p.read_bytes()!=(root/'paper_consolidated/sections'/p.name).read_bytes()]
result['bib_copies_equal']=(root/'ACM-Journals/bibliography.bib').read_bytes()==(root/'paper_consolidated/bibliography.bib').read_bytes()
result['reference_hosts']=dict(Counter(re.sub(r'https?://([^/]+).*',r'\1',str(r.get('reference_url'))) for r in rows))
result['context_coverage']=sum(isinstance(r.get('context_window_tokens'),(int,float)) for r in rows)
result['context_by_year']={y:{'n':len(v),'median':statistics.median(v)} for y in ['2023','2024','2025','2026'] if (v:=[r['context_window_tokens'] for r in rows if str(r.get('release_date')).startswith(y) and isinstance(r.get('context_window_tokens'),(int,float))])}
result['both_count']=sum(r.get('base_or_instruct')=='both' for r in rows)
result['source_retrieved_count']=sum(bool(r.get('source_retrieved')) for r in rows)
result['architecture_examples']=[{'name':r['name'],'notes':r.get('architecture_notes'),'url':r.get('reference_url')} for r in rows if re.search('T5|BLOOM|Pythia|Aya|Voxtral',r['name'])]
result['moe_flag_count']=sum(bool(r.get('parameters',{}).get('is_moe')) for r in rows)
result['small_active_without_moe_flag']=[r['name'] for r in rows if r.get('slm_class')=='small-active-moe' and not r.get('parameters',{}).get('is_moe')]
result['active_below_total_count']=sum(r.get('parsed_active_params_b',0)<r.get('parsed_total_params_b',0) for r in rows)
result['secondary_reference_records']=[{'name':r['name'],'reference_url':r.get('reference_url'),'paper_url':r.get('paper_url'),'huggingface_url':r.get('huggingface_url')} for r in rows if any(h in str(r.get('reference_url')) for h in ['openrouter.ai','venturebeat.com'])]
result['logs']={p.name:[line for line in p.read_text(encoding='utf-8',errors='replace').splitlines() if any(x in line for x in ['Warning','Overfull','undefined'])] for p in (root/'ACM-Journals').glob('*.log') if p.name in ['less-is-more.log','supplement.log']}
(root/'reviews/audit_2026-10-08.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('record_example','excluded')},indent=2))
print('EXAMPLE', json.dumps(rows[0],indent=2))

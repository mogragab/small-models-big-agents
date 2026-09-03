# Source ledger --- consolidated SLM / agentic-AI paper

This paper consolidates three predecessor manuscripts (`../manuscript`,
`../paper1_survey`, `../paper2_meta_analysis`).

## Bibliography cleanup status (2026-09-03)

The bib was overhauled this session:

- **Started:** 188 entries. **Now:** 141 entries, **all cited**, no duplicates.
- **Deleted 40 uncited entries**, including every fabricated-looking stub found in
  the earlier audit (`li2024slmquant`, `slmquant2024`, `mehta2025slm_agentic`,
  `subramanian2025slms`, `phi4miniflash`, `wang2024slmera`, `nguyen2024ondevice`,
  `lu2024small`, the three unrelated `ragab20*` self-citations, etc.).
- **Merged 6 duplicate pairs** (`gunasekar2023textbooks`->`gunasekar2023phi1`,
  `gemma3team2025`->`team2025gemma3`, `meta2024llama3`->`grattafiori2024llama3`,
  `yang2024qwen25`->`qwen2024qwen25`, `llamacpp2023`->`gerganov2023llamacpp`,
  `onnxruntime2023`->`microsoft2019onnx`); `\cite` keys in the sections were
  rewritten to the survivors.
- **Repaired 9 entries with fabricated/wrong metadata** against a retrieved
  source (table below) --- including the 6 remaining no-identifier stubs.
- **Added a `url` (arXiv abs page, DOI, or canonical page) to ~66 canonical
  entries.** ~15 of these arXiv IDs were verified by direct retrieval this
  session; the rest (benchmark-dataset papers such as MMLU/GSM8K/HellaSwag, and
  the model technical reports) were filled from field-canonical knowledge and
  **should be confirmed with a reference-manager "retrieve by arXiv ID" pass
  before submission** --- a transposed digit would give a dead link. 133/141
  entries now carry an identifier; the ~8 without are vendor pages.

## Repaired stub / wrong-metadata entries (verified this session)

| citekey | problem | fix | source retrieved |
|---|---|---|---|
| `kurz2025pruning_vs_quant` | missing first author, no pages | Zihan Zhou added; pages 12055--12070; Findings EMNLP 2025 | aclanthology.org/2025.findings-emnlp.645/ |
| `lu2024slmsurvey` | fabricated author list | correct 8-author list (Zhenyan Lu et al.) | arxiv.org/abs/2409.15790 |
| `wang2024comprehensive` | wrong authors + wrong DOI + wrong arXiv id | Fali Wang et al., arXiv:2411.03350, full subtitle | arxiv.org/abs/2411.03350 |
| `pal2025sambay` | `journal={arXiv preprint}`, no id, "Pal, Siddharth and others" | Liliang Ren et al., "Decoder-Hybrid-Decoder Architecture...", arXiv:2507.06607 (introduces SambaY) | arxiv.org/abs/2507.06607 |
| `yang2025gated_delta` | no id, "Yang, Songlin and others" | Songlin Yang, Jan Kautz, Ali Hatamizadeh, "Gated Delta Networks: Improving Mamba2 with Delta Rule", ICLR 2025, arXiv:2412.06464 | arxiv.org/abs/2412.06464 |
| `smollm3` | bare stub | HF blog "SmolLM3: smol, multilingual, long-context reasoner" (Jul 2025) | huggingface.co/blog/smollm3 |
| `demystifying2025slm` | wrong author ("Zhihang Yuan"), wrong pages/venue detail | Zhenyan Lu et al., ACL 2025 Long Papers pp. 14747--14764, Vienna | aclanthology.org/2025.acl-long.718/ |
| `costa2025sbc` | fabricated ("Pedro Costa and others"); the llamafile-vs-Ollama claim is real | Tung Nguyen, Tuyen Nguyen, "An Evaluation of LLMs Inference on Popular Single-board Computers", arXiv:2511.07425 | arxiv.org/abs/2511.07425 |
| `chandra2026ondevice` | fabricated stub; memory-bandwidth claim is real | citation redirected to `xu2024device` ("On-Device Language Models: A Comprehensive Review", arXiv:2409.00088) | (existing verified entry) |

---

## Newly added entries (verified this session)

| citekey | what it is | source retrieved | used for |
|---|---|---|---|
| `belcak2025slm_agentic` | Belcak, Heinrich, Diao, Fu, Dong, Muralidharan, Lin, Molchanov. "Small Language Models are the Future of Agentic AI." arXiv:2506.02153 (v1 Jun 2025, v2 Sep 2025). | arxiv.org/abs/2506.02153 ; arxiv.org/html/2506.02153v2 | Core of Section~8 (agentic argument, V1--V3, economics 10--30x, MetaGPT/Open Operator/Cradle 60/40/70%, 6-step conversion, barriers B1--B3) |
| `chen2025collab_survey` | Yi Chen, JiaHao Zhao, HaoHao Han. "A Survey on Collaborative Mechanisms Between Large and Small Language Models." arXiv:2505.07460 (2025). | arxiv.org/abs/2505.07460 | Five interaction patterns (pipeline/routing/auxiliary/distillation/fusion); background collaboration subsection |
| `chen2024role_small` | Lihu Chen, Gaël Varoquaux. "What is the Role of Small Models in the LLM Era: A Survey." arXiv:2409.06857 (2024, rev. 2026). | arxiv.org/abs/2409.06857 | Collaboration vs. competition framing |
| `ong2024routellm` | Ong, Almahairi, V. Wu, Chiang, T. Wu, Gonzalez, Kadous, Stoica. "RouteLLM: Learning to Route LLMs with Preference Data." arXiv:2406.18665 (2024); ICLR 2025. | arxiv.org/abs/2406.18665 | Learned routing, >2x cost reduction claim |
| `division_of_thoughts_2025` | Chenyang Shao, Xinyuan Hu, Yutang Lin, Fengli Xu. "Division-of-Thoughts: Harnessing Hybrid Language Model Synergy for Efficient On-Device Agents." arXiv:2502.04392 (2025). | arxiv.org/abs/2502.04392 | Sub-task-level SLM/LLM routing for on-device agents (66% reasoning-time, 84% API-cost reduction). |
| `zhang2024xlam` | Jianguo Zhang et al. (22 authors). "xLAM: A Family of Large Action Models to Empower AI Agent Systems." arXiv:2409.03215 (2024). | arxiv.org/abs/2409.03215 | Sub-10B function-calling models topping Berkeley Function-Calling Leaderboard |
| `vannguyen2024slm_survey` | Chien Van Nguyen et al. (27 authors). "A Survey of Small Language Models." arXiv:2410.20011 (2024). | arxiv.org/abs/2410.20011 | Prior SLM survey (replaces the fabricated `nguyen2024ondevice` entry) |
| `qwen3_2025` | Qwen Team. "Qwen3 Technical Report." arXiv:2505.09388 (2025). | arxiv.org/abs/2505.09388 ; qwenlm.github.io/blog/qwen3 | Dense 0.6--32B + MoE 30B-A3B/235B-A22B; unified thinking mode; thinking budget |
| `qwen3_5_2026` | Qwen Team. "Qwen3.5 small models" (0.8--9B, Gated DeltaNet hybrid 3:1). Vendor release, Mar 2026. | Artificial Analysis + MarkTechPost coverage (2026-03-02); qwenlm.github.io/blog | Gated DeltaNet hybrid example. GREY LITERATURE --- vendor blog, no arXiv. |
| `gemma4_2026` | Gemma Team, Google DeepMind. "Gemma 4 Technical Report." arXiv:2607.02770 (Jun 2026). | arxiv.org/abs/2607.02770 ; arxiv.org/html/2607.02770v1 | Dense+MoE 2.3--31B, E2B/E4B effective params, PLE, thinking mode, encoder-free 12B |
| `gunter2025afm` | Apple. "Apple Intelligence Foundation Language Models: Tech Report 2025." arXiv:2507.13575 (Jul 2025). | arxiv.org/abs/2507.13575 ; machinelearning.apple.com/research/apple-foundation-models-2025-updates | 3B on-device (2-bit QAT, KV-cache sharing -37.5%), PT-MoE server; competitive w/ Qwen3-4B, Gemma-3-4B |
| `apple2026afm3` | Apple ML Research. "Introducing the Third Generation of Apple's Foundation Models." (2026). | machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models | Multimodal sparse on-device model; 3rd-party model plug-in via LanguageModel protocol |
| `nvidia2025nemotron_nano2` | NVIDIA. "NVIDIA Nemotron Nano 2: An Accurate and Efficient Hybrid Mamba-Transformer Reasoning Model." arXiv:2508.14444 (Aug 2025). | arxiv.org/abs/2508.14444 | 6 attn / 28 Mamba-2 / 28 FFN of 62 layers; up to 6x throughput vs Qwen3-8B on reasoning |
| `granite4_2025` | IBM Granite Team. "IBM Granite 4.0" (hybrid Mamba-2/attention ~1:9, fine-grained MoE, Tiny ~7B/1B-active). Vendor announcement, Oct 2025. | ibm.com/new/announcements/ibm-granite-4-0-... ; research coverage (MarkTechPost, InfoWorld) | Hybrid SSM production example; >70% memory reduction claim. GREY LITERATURE --- no arXiv report found. |
| `llama4_2025` | Meta AI. "The Llama 4 Herd." Blog, Apr 2025. Scout 109B/17B-active/16E; Maverick 400B/17B-active/128E; Behemoth 2T teacher. | ai.meta.com/blog/llama-4-multimodal-intelligence | MoE-by-active-params example |
| `xu2025phi4mini_reasoning` | Haoran Xu et al. "Phi-4-Mini-Reasoning: Exploring the Limits of Small Reasoning Language Models in Math." arXiv:2504.21233 (2025). | arxiv.org/abs/2504.21233 ; arxiv.org/html/2504.21233v1 | Reasoning distillation + RL on 3.8B |
| `slmquant2025` | Jiacheng Wang, Yejun Zeng, Jinyang Guo, Yuqing Ma, Aishan Liu, Xianglong Liu. "SLMQuant: Benchmarking Small Language Model Quantization for Practical Deployment." arXiv:2511.13023 (2025). | arxiv.org/abs/2511.13023 | SLM quantization sensitivity (replaces fabricated `li2024slmquant` / `slmquant2024`). |

## Remaining pre-submission bib tasks

1. **Confirm the ~50 bulk-added arXiv IDs** with a reference manager (Zotero/
   Mendeley "retrieve metadata" by arXiv ID or title). These are canonical
   papers (MMLU, GSM8K, HellaSwag, the model technical reports, etc.) whose
   entries had correct author/title/year but were missing the identifier; the
   IDs were filled from established knowledge, not individual retrieval.
2. **Full author lists.** Many entries use "and others"; Springer prefers the
   complete list. A reference-manager re-import fixes this in bulk.
3. **`qwen3_5_2026`, `granite4_2025`, `llama4_2025`, `apple2026afm3`** are grey
   literature (vendor blogs, no arXiv). Acceptable under the paper's stated
   grey-literature protocol, but confirm the URLs resolve at submission time.
4. **`smollm3` author list** is a best guess (`{... and others}`); replace with
   the exact byline from huggingface.co/blog/smollm3.

## Predecessor material reused (not re-verified)

Sections 3--7 and 9--11 reuse prose and tables from `../manuscript` and
`../paper2_meta_analysis`. The performance tables in Section~7 are the
predecessor manuscripts' consolidated figures, reframed as reported values; the
per-figure provenance table (Appendix~B, `app:provenance`) is a stub in the
predecessor and remains to be populated at submission.

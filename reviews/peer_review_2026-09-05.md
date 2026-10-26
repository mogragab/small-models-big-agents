Peer-Review Report 

### **Small Language Models as the Substrate of Agentic AI: A Survey of Architectures, Compression, Deployment, and Evaluation Practice** 

|**Review date**|5 September 2026<br>|
|---|---|
|**Targetjournal**|ACM ComputngSurveys|
|**Manuscript length**<br>|52pages|
|**Recommendaton**|Major revision before submission|



This review evaluates the supplied manuscript as a potential ACM Computing Surveys submission. The topic is important and timely, and the paper contains a potentially useful synthesis of small language models, compression, edge deployment, and agentic systems. However, the current version combines a broad descriptive survey with a strong position statement, while its methodology and evidence base do not yet support several of its principal conclusions. 

# **Summary assessment** 

The manuscript is promising but not submission-ready. I recommend major revision before submission to any high-impact survey journal. For ACM Computing Surveys specifically, the present version carries a substantial risk of editorial rejection or reject-and-resubmit because the agentic-AI thesis is stronger than the controlled evidence, the SLM definition is inconsistent, and the quantitative tables mix incomparable quantities. 

# **Strengths** 

- Addresses a significant and rapidly developing topic at the intersection of efficient language models, edge AI, and agentic systems. 

- Provides a useful high-level organization around architecture, training, modality, compression, deployment, and applications. 

- Recognizes an important limitation: public vendor benchmark reporting is often not directly comparable. 

- Attempts to provide a model inventory, provenance information, and an empirical-verification agenda. 

- Connects model efficiency to practical issues such as privacy, latency, hardware constraints, and specialization. 

# **Major comments** 

## **1. Clarify the article type and central contribution** 

The paper presents itself simultaneously as a survey, compression review, evaluation audit, deployment survey, and position paper. This makes the contribution difficult to evaluate. The claim that SLMs are the default substrate of agentic AI should be reformulated as a conditional, evidence-based design hypothesis. The authors should specify the workload classes for which SLMs are advantageous and identify counterexamples where larger models remain necessary. 

## **2. Establish a consistent definition of SLM** 

The manuscript uses both an approximately 20B threshold and a sub-10B evaluation scope. It also classifies mixture-of-experts models using active parameters, although storage, model download, and resident memory 

Peer-review report | 5 September 2026 

depend substantially on total parameters. Every model should be reported using total parameters, active parameters per token, weight memory, peak runtime memory, FLOPs/token, KV-cache requirements, context length, and target hardware. The terms SLM, compact model, edge model, and small-active-parameter MoE should be distinguished. 

## **3. Strengthen survey methodology and reproducibility** 

Section 1.4 does not provide complete search strings, search dates, retrieval counts, duplicate handling, exclusion reasons, quality appraisal, or reviewer-agreement procedures. This is a serious weakness for a claimed inventory of 126 variants. The final submission should release the machine-readable inventory, source URLs, version dates, inclusion decisions, scripts, and a changelog through a permanent repository or DOI. 

## **4. Align conclusions with the evaluation evidence** 

The manuscript correctly states that a common benchmark table cannot be assembled from heterogeneous reporting. However, it then makes broad cross-model conclusions about capability-per-parameter, training data, quantization, and model leadership. These conclusions should be separated into controlled evidence, vendorreported evidence, independent evidence, and author interpretation. Each major claim should have an evidence grade and a provenance table containing checkpoint, prompt, shot count, harness, benchmark version, source type, and date. 

## **5. Rebuild or remove Table 3** 

Accuracy-retention values such as INT4 approximately 96%, knowledge distillation 85–95%, and combined compression approximately 90% are not interpretable without a defined baseline, model class, task, metric, and aggregation method. The stated compression ratio for knowledge distillation is also not a well-defined universal quantity. Separate parameter reduction, memory reduction, training-compute reduction, latency, and quality loss. If a meta-analysis is not possible, replace the numerical table with a carefully sourced qualitative comparison. 

## **6. Add agent-specific evidence** 

General benchmarks such as MMLU, GSM8K, and HumanEval do not establish suitability for agentic workloads. The paper should systematically review function calling, tool-use reliability, structured-output validity, end-to-end agent success, cumulative multi-step error, router calibration, escalation rates, privacy-sensitive routing, and cost per completed task. The agentic thesis should be supported by task-level evidence rather than general model scores alone. 

## **7. Moderate and validate deployment and economic claims** 

Claims about near-linear INT4 speedups, zero marginal cost, no data leaving the device, 10–30× lower serving cost, one-to-two-orders-of-magnitude energy savings, and 10,000 consumer instances using less energy than one server require stronger qualification or measurements. Results depend on batch size, context length, kernels, hardware utilization, thermal throttling, software version, energy source, and device lifetime. Distinguish calculated memory footprints from measured latency, throughput, energy, and total cost of ownership. 

## **8. Revise the taxonomy** 

Architecture, training strategy, modality, and application domain are not fully orthogonal. Models can combine multiple training strategies and serve multiple domains, while application domain is often a use-case label rather than an intrinsic model property. Use multilabel or hierarchical classification and add licensing, data transparency, safety alignment, reasoning mode, context length, inference engine, and deployment target. 

## **9. Conduct a complete factual and bibliographic audit** 

At least one concrete model-description error appears in the multimodality discussion: the manuscript states that all Gemma 3 sizes include image understanding, whereas Google's documentation identifies the 1B model as textonly and vision support beginning with the 4B model. The model inventory, release dates, licenses, parameter 

Peer-review report | 5 September 2026 

counts, context windows, and training-token values should all be checked against versioned primary sources. References [6] and [7] also appear to use the same arXiv identifier for different SmolLM2 titles and should be reconciled. 

## **10. Update the related work and temporal-snapshot policy** 

A September 2026 snapshot should explicitly include recent 2026 surveys on small reasoning models, multilingual language models, and agentic systems. The paper should explain how it handles papers and model releases appearing during review and should provide a versioned update policy rather than presenting the inventory as permanently current. 

# **Minor comments** 

- Define variant, family, checkpoint, release, pretrained model, instruction-tuned model, and reasoning-tuned model. 

- Do not copy series-level training-token counts into every model-size row unless the source explicitly reports them individually. 

- Identify benchmark versions, prompt templates, answer-extraction rules, decoding settings, and evaluation harnesses. 

- Report confidence or evidence grades for quantitative claims and state how missing values were treated. 

- Replace broad phrases such as de facto standard and state-of-the-art with source-specific, measurable descriptions. 

- Use consistent capitalization for Llama, Qwen, Gemma, Phi, and model/checkpoint names. 

- Clarify whether environmental claims include teacher-model training, distillation, quantization, hardware manufacture, and model updates. 

- The healthcare and legal sections are currently more descriptive than evidential; add independent deployment studies and domain-specific benchmarks. 

- On-device privacy claims should be conditional on telemetry, logging, cloud escalation, and the complete application pipeline. 

- HIPAA/GDPR compliance should not be presented as an automatic property of an on-premises model. 

- The manuscript contains unfinished metadata: a placeholder DOI, an unfinished revision date, and an unfinished acceptance date. 

- Remove ACM-specific manuscript footers and metadata when submitting to a non-ACM journal. 

- Check PDF accessibility, embedded Unicode text, figure readability, and the very wide generated inventory tables before submission. 

# **Suitability for ACM Computing Surveys** 

The topic is suitable for ACM Computing Surveys, but the manuscript should be substantially revised first. The strongest route is to formalize the survey questions, provide a reproducible inventory, rebuild the evidence synthesis, weaken unsupported universal claims, add agent-specific evaluation literature, correct model metadata, and convert the substrate thesis into a defensible conditional framework. 

# **Alternative SCIE journals** 

Here, SCI is interpreted as SCIE/Web of Science Core Collection. Indexing and journal policies should be reconfirmed in Clarivate's Master Journal List immediately before submission. 

|**Journal**<br>**Fit**<br>**Recommended reframing**|
|---|



Peer-review report | 5 September 2026 

|**Artfcial Intelligence Review**|Best alternatve. It explicitly publishes<br>survey and tutorial artcles and covers<br>NLP, machine learning, intelligent agents,<br>and mult-agent systems. The Springer<br>journalpage lists SCIE indexing.|Retain the broad survey, but improve<br>methodological rigor and reduce<br>advocacy.|
|---|---|---|
|**IEEE Access**|Practcal and realistc alternatve. It<br>accepts surveys, topical reviews, and<br>perspectves and is listed by IEEE as SCIE-<br>indexed.|Present the work as a survey plus<br>perspectve, with explicit evidence<br>grading.|
|**ACM Transactons on Intelligent Systems**<br>**and Technology**|Strong ft for the heterogeneous SLM–<br>LLM and agentc-systems angle. ACM<br>reports the journal in the top quartle of<br>relevant AI and informaton-systems<br>categories.|Reduce the general catalogue and add<br>stronger intelligent-system and agent-<br>routng evidence.|
|**Knowledge-Based Systems**|Potentally suitable if the paper develops<br>a formal model-selecton, routng,<br>knowledge, or decision framework. It<br>covers broad AI and machine-learning<br>systems.|Make the contributon analytcal and<br>framework-driven rather than<br>encyclopedic.|
|**Internatonal Journal of Machine**<br>**Learning and Cybernetcs**|Suitable for a narrower methods paper<br>on compression, efcient inference,<br>model selecton, and routng; Springer<br>lists SCIE indexing.|Reduce the applicaton narratve and<br>emphasize methodological synthesis.|
|**The Journal of Supercomputng**|Conditonal opton for the deployment,<br>hardware, edge-inference, and model–<br>hardware co-design material. Its current<br>scope includes AI and advanced<br>embedded systems.|Add real measurements and make<br>edge/HPC deployment the central<br>contributon.|



# **Recommended submission order** 

1. Artificial Intelligence Review 

2. IEEE Access 

3. ACM Transactions on Intelligent Systems and Technology 

4. Knowledge-Based Systems 

5. International Journal of Machine Learning and Cybernetics 

# **Priority actions before submission** 

6. Choose one article identity: rigorous survey with a derived synthesis, or position/perspective paper. 

7. Freeze and document the inclusion rule for SLMs, especially for mixture-of-experts models. 

8. Release the inventory, provenance data, scripts, and versioned source list. 

9. Replace unsupported aggregate accuracy-retention values and conditionalize economic and environmental claims. 

10. Add a benchmark and evidence framework specific to agentic workloads. 

11. Complete a primary-source audit of every model specification, citation, release date, license, and figure. 

12. Reformat the final manuscript for the selected journal and remove unfinished ACM metadata. 

# **Verification sources for journal recommendations** 

- ACM Computing Surveys context: htps://www.acm.org/binaries/content/assets/press-releases/2025/july/ <u>news-release_impact_factors_2025_fnal.pdf</u> 

- Artificial Intelligence Review: htps://link.springer.com/journal/10462 

Peer-review report | 5 September 2026 

- IEEE Access scope: htps://ieeeaccess.ieee.org/about/ 

- IEEE Access indexing information: htps://ieeeaccess.ieee.org/about/bibliometrics/ 

- ACM TIST context: htps://www.acm.org/binaries/content/assets/press-releases/2025/july/news- <u>release_impact_factors_2025_fnal.pdf</u> 

- Knowledge-Based Systems: htps://www.sciencedirect.com/journal/knowledge-based-systems/about/policies 

- International Journal of Machine Learning and Cybernetics: htps://link.springer.com/journal/13042 

- The Journal of Supercomputing: htps://link.springer.com/journal/11227 

- Gemma 3 official model information: htps://deepmind.google/models/gemma/gemma-3/ 

Peer-review report | 5 September 2026 


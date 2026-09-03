# Paper architectures

Section trees by paper type. Treat these as skeletons to be adapted, not filled in
mechanically — a heading with nothing to say under it weakens the paper.

## Depth discipline

Number sections `1`, subsections `1.1`, sub-subsections `1.1.1`. Front matter (abstract,
keywords) and back matter (references, appendices, declarations) are unnumbered.

Split a section only when there are two or more genuinely distinct things to say. A
`3.1` with no `3.2` means the split was decorative — merge it back. As a rough guide, a
subsection worth having runs 300+ words; a sub-subsection worth having runs 150+.

Sub-subsections earn their place when a subsection enumerates parallel items: competing
models, individual studies in a review, separate datasets, distinct mechanisms, threat
categories, failure modes. That parallelism is what makes the numbering useful to a
reader.

---

## Empirical research paper (IMRaD)

```
Title / Authors / Affiliations
Abstract (unnumbered, 200–300 words, structured or continuous)
Keywords (4–6)
1. Introduction
   1.1 Background and motivation
   1.2 Problem statement
   1.3 Research questions or hypotheses
   1.4 Contributions
   1.5 Paper organisation            [optional; drop in short papers]
2. Related work / Theoretical framework
   2.1 <Strand one>
       2.1.1 <Sub-strand>
   2.2 <Strand two>
   2.3 Research gap
3. Methodology
   3.1 Research design
   3.2 Data / participants / materials
   3.3 Procedure or instrumentation
   3.4 Analytical approach
   3.5 Validity, reliability, and ethics
4. Results
   4.1 Descriptive results
   4.2 <Result cluster per hypothesis>
   4.3 Robustness or sensitivity checks
5. Discussion
   5.1 Interpretation of key findings
   5.2 Relation to prior work
   5.3 Theoretical implications
   5.4 Practical implications
   5.5 Limitations
6. Conclusion and future work
References
Appendices / Data availability / Funding / Conflicts of interest
```

## Systematic review (PRISMA-aligned)

```
Abstract (structured: Background, Methods, Results, Conclusions)
1. Introduction
   1.1 Rationale
   1.2 Objectives and review questions (PICO or equivalent)
2. Methods
   2.1 Protocol and registration
   2.2 Eligibility criteria
   2.3 Information sources and search strategy
   2.4 Study selection and screening
   2.5 Data extraction
   2.6 Risk-of-bias assessment
   2.7 Synthesis method
3. Results
   3.1 Study selection (PRISMA flow: identified / screened / included)
   3.2 Characteristics of included studies  [table]
   3.3 Risk of bias across studies
   3.4 Synthesis of findings
       3.4.1 <Outcome one>
       3.4.2 <Outcome two>
4. Discussion
   4.1 Summary of evidence
   4.2 Strength and certainty of evidence
   4.3 Limitations of the review process
   4.4 Implications for practice and research
5. Conclusions
References
```

Report real counts in the flow: how many records your searches returned, how many you
screened, how many you included, and why the rest were excluded. If the search was not
exhaustive, call it a *scoping* or *narrative* review instead — a narrative review is a
respectable form; a systematic review with an unsystematic search is not.

## Narrative / critical literature review

```
Abstract, Keywords
1. Introduction
   1.1 Scope and significance
   1.2 Review approach and inclusion rationale
2. <Thematic pillar one>
   2.1 <Sub-theme>
       2.1.1 <Individual model, study cluster, or school of thought>
   2.2 <Sub-theme>
3. <Thematic pillar two>
4. <Thematic pillar three>
5. Synthesis and critical appraisal
   5.1 Points of consensus
   5.2 Points of contention
   5.3 Methodological limitations of the field
6. Research agenda
   6.1 Open questions
   6.2 Proposed directions
7. Conclusion
References
```

Organise by theme, never by source. Chronological organisation is acceptable only when
the argument is about how thinking changed over time.

## Theoretical / conceptual paper

```
1. Introduction
2. Foundations
   2.1 Definitions and scope conditions
   2.2 Existing frameworks and their limits
3. Proposed framework
   3.1 Core constructs
       3.1.1 <Construct A>
       3.1.2 <Construct B>
   3.2 Propositions or axioms
   3.3 Boundary conditions
4. Application
   4.1 Illustrative case
   4.2 Comparison with alternative accounts
5. Implications and testability
6. Conclusion
```

## Case study

```
1. Introduction
2. Theoretical background
3. Case selection and method
   3.1 Case description and rationale
   3.2 Data sources
   3.3 Analytical procedure
4. Case narrative / findings
   4.1 <Phase or dimension one>
   4.2 <Phase or dimension two>
5. Cross-case or theory-linked analysis
6. Discussion, limitations, transferability
7. Conclusion
```

## Position / argumentative paper

```
1. Introduction and thesis
2. Context and stakes
3. The argument
   3.1 <Premise one and its evidence>
   3.2 <Premise two and its evidence>
   3.3 <Premise three and its evidence>
4. Counter-arguments and responses
   4.1 <Objection one>
   4.2 <Objection two>
5. Implications and recommendations
6. Conclusion
```

The counter-argument section is what makes this a paper rather than an editorial. Give
the strongest version of the opposing case, cited to people who actually hold it.

## Thesis chapter

Follow the parent thesis's numbering (`Chapter 4` → `4.1`, `4.1.2`). Chapters open with
a short roadmap paragraph and close with a linking paragraph to the next chapter —
unlike a standalone paper, a chapter must hand off.

## Conference / short paper (4–8 pages)

Compress: Introduction, Related Work, Method, Evaluation, Discussion, Conclusion, with
subsections only in Method and Evaluation. Two-column formats punish deep nesting;
stop at level 2.

---

## Element placement

- **Tables and figures**: number sequentially (`Table 1`, `Figure 1`), each referenced
  in the text before it appears. Table captions above; figure captions below. Every
  caption is a sentence that lets the item stand alone, plus a source note if the data
  came from elsewhere.
- **Equations**: display and right-number `(1)`, `(2)` when referenced in text.
- **Abbreviations**: define at first use in the body; if there are more than ~8, add an
  abbreviations list after the keywords.
- **Appendices**: `Appendix A`, `Appendix B`; instruments, full result tables, and
  derivations go here, not in the body.

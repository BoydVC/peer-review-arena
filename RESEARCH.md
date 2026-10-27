# RESEARCH.md — Peer Review Arena

Cited desk on multi-agent debate, adversarial review, and LLM-as-judge pitfalls. Compiled Mon Oct 26, 2026 (America/New_York). Links are public; this file is not a paper review — it is a design brief for a local TokenMax tool.

## 1. Why this product exists

Jim · Interests (burn-night snapshot ~Oct 20–26) listed a **multi-agent critique loop before merge** as a strong runner-up after Household Call Agent, Kids Coding Studio, and X Lists → Brief Pack. Boyd’s bookmarks cluster on Grok Bot product patterns including multi-agent peer review (Roemmele-style templates, marketplace packs, Vault, Bot calling businesses). The @EXM7777-shaped pattern — fan out specialized reviewers, then chair a merge — is the operating metaphor.

Peer Review Arena encodes that loop as a **local, deterministic desk**: five fixed personas produce structured findings; a Chair builds consensus, disagreements, and a must-fix-before-ship list. No Cursor cloud agents. No live model spend required for the seed critiques (heuristic + curated evidence quotes). The research below tells us what to copy and what to refuse.

## 2. Multi-agent debate — the optimistic case

### 2.1 Du et al. (2023/2024) — society of minds

Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch, *Improving Factuality and Reasoning in Language Models through Multiagent Debate*:

- Multiple LLM instances propose answers, critique each other over rounds, and converge.
- With **3 agents × 2 rounds**, arithmetic rose **67.0% → 81.8%**; grade-school math **77.0% → 85.0%**; chess ΔPS **91.4 → 122.9**.
- Debate beat single-agent chain-of-thought and reflection on several factuality tasks; agents often drop uncertain facts as disagreement surfaces.
- Important nuance: gains needed **both** multiple agents **and** multiple rounds — majority vote alone was weaker.
- arXiv: https://arxiv.org/abs/2305.14325
- ICML 2024 PMLR: https://proceedings.mlr.press/v235/du24e.html
- HTML: https://arxiv.org/html/2305.14325

**Arena takeaway:** Parallel personas are not decoration. The product always runs ≥4 lenses before the Chair speaks. We do *not* pretend one Skeptic pass equals a debate.

### 2.2 ChatDev — review as a phase, not a vibe

Chen et al., *ChatDev: Communicative Agents for Software Development* (ACL 2024):

- Software workflow broken into design → coding → testing; testing splits into **code review (static)** and system testing.
- Reviewer and programmer agents iterate in multi-turn dialogue until consensus before advancing.
- PDF: https://aclanthology.org/2024.acl-long.810.pdf
- Anthology: https://aclanthology.org/2024.acl-long.810/

**Arena takeaway:** Critique is a **gate**. Chair verdicts (`ship_ready` / `ship_with_fixes` / `needs_revision` / `hold`) mirror a merge gate, not a chat log.

### 2.3 MetaGPT — executable feedback over polite review

Hong et al., *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (ICLR 2024):

- Purely linguistic code review still hallucinates “LGTM.”
- After generation, Engineer writes/runs unit tests and retries (max 3) — **executable feedback**.
- arXiv HTML: https://arxiv.org/html/2308.00352v7
- ICLR PDF: https://proceedings.iclr.cc/paper_files/paper/2024/file/6507b115562bb0a305f1958ccc87355a-Paper-Conference.pdf

**Arena takeaway:** Our smoke test and seed artifacts are the executable half. A “review” that cannot be re-run against `out/review-bonsai-reveal.json` is theater. Findings quote draft evidence so a human can verify without trusting the persona voice.

## 3. Adversarial review — when collaboration fails

### 3.1 Persuasion as an attack vector

*When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate* (Scientific Reports, 2026):

- A single strategically persuasive adversarial agent can cut group accuracy **10–40%** and raise incorrect consensus **>30%** across TruthfulQA, MMLU, MedMCQA, SCALR.
- Not classic prompt/token injection — confident, coherent wrong arguments.
- Best-of-N and RAG can **amplify** the attack by making flawed arguments look more credible.
- More agents or more rounds do **not** reliably defend; prompt-only defenses are weak.
- DOI: https://doi.org/10.1038/s41598-026-42705-7
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC13061921/

**Arena takeaway:** Personas must stay **independent** on the first pass (no mid-flight score sharing that lets Security talk Skeptic into silence). The Chair surfaces **disagreements** instead of forcing artificial unanimity. We never let one verbose persona rewrite the must-fix list alone.

### 3.2 Role asymmetry and downward bias

Song, Kim, Eo, Park, *Beyond Consensus: Downward Bias and Role Asymmetry in Multi-Agent LLM Judges for Subjective Evaluation* (EMNLP 2026 Findings):

- For subjective rubric scoring, MAD consensus **underperformed** a single-judge baseline on human alignment across six LLMs.
- Primary culprit: **asymmetric role prompting** (strict judge) introduces downward bias that consensus fails to average out — “strict-stance dominance beyond averaging.”
- Symmetric MAD largely recovers baseline; masking peer scores widens disagreement and can worsen alignment.
- Anthology: https://aclanthology.org/2026.findings-emnlp.243/

**Arena takeaway:** Our personas are **specialized lenses**, not “strict vs lenient judges scoring the same rubric.” Severity is attached to concrete claims with evidence, not a shared 1–10 aesthetic score that a Strict agent can drag down. Chair risk scores sum weighted severities; they do not pretend to be human preference Elo.

## 4. LLM-as-judge pitfalls (single and multi)

### 4.1 Classic biases — Zheng et al. MT-Bench / Chatbot Arena

Lianmin Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*:

- Documents **position bias**, **verbosity bias**, **self-enhancement bias**, and limited reasoning.
- Strong judges (e.g. GPT-4) can reach ~80% agreement with humans *after* mitigations — same ballpark as human-human agreement.
- Verbosity attack (“repetitive list”) fools many judges; position swaps flip winners.
- arXiv: https://arxiv.org/abs/2306.05685
- HTML: https://arxiv.org/html/2306.05685

**Arena takeaway:** Structured fields (`severity`, `claim`, `evidence`, `suggested_fix`) beat free-form “who wins?” Pairwise beauty contests are out of scope. Evidence must be a quote or path from the draft.

### 4.2 Position bias deep dive

Shi et al. / related IJCNLP work *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*:

- Position bias is not random noise; it varies by judge and task.
- HTML: https://arxiv.org/html/2406.07791v7
- PDF: https://aclanthology.org/2025.ijcnlp-long.18.pdf

**Arena takeaway:** Consensus table is ordered by **worst severity**, not by which persona spoke first in the JSON array.

### 4.3 Multi-agent judge bias amplification

Ma et al., *Judging with Many Minds: Do More Perspectives Mean Less Prejudice?* (EMNLP 2025 Findings):

- Studies position, verbosity, chain-of-thought, and **bandwagon** bias under Multi-Agent-Debate vs LLM-as-Meta-Judge.
- Debate **amplifies** biases sharply after the first round; amplification persists.
- Meta-judge setups show more resistance.
- Bias-free agent (PINE) helps debate more than meta-judge.
- Anthology PDF: https://aclanthology.org/2025.findings-emnlp.941.pdf
- arXiv HTML: https://arxiv.org/html/2505.19477v3

**Arena takeaway:** Prefer **meta-chair over debate-to-unanimity**. Our Chair merges independent findings; it does not run three rounds of “talk until you agree.” Bandwagon is exactly what the disagreements panel is designed to make visible.

### 4.4 Survey context

*A Survey on LLM-as-a-Judge* (arXiv 2411.15594):

- Catalogues position/verbosity/self-preference failure modes and mitigation themes.
- HTML: https://arxiv.org/html/2411.15594v4

## 5. Design rules distilled for Peer Review Arena

| Rule | Source signal | Product encoding |
|---|---|---|
| ≥3 independent agents before merge | Du et al. | 5 fixed personas always |
| Critique is a gate | ChatDev | Chair verdicts + must-fix list |
| Prefer executable checks | MetaGPT | `smoke_test.sh`, saved JSON/MD |
| Don’t force consensus | Song et al.; Scientific Reports | Disagreements panel; independent first pass |
| Avoid strict/lenient score wars | Song et al. | Lenses + evidence, not shared 1–10 |
| Distrust verbosity / order | Zheng; Ma et al. | Structured findings; severity-sorted table |
| Persuasion can capture the group | Scientific Reports | Chair cannot drop blocker/high because a persona “sounded confident” |

## 6. What we deliberately do *not* do in v1

1. **Live multi-round LLM debate** — costs the wrong pool if routed to cloud; bandwagon risk is real. Seed reviews are deterministic so burns are replayable.
2. **Single scalar “quality” score as truth** — risk_score is a triage aid, not human preference.
3. **Auto-merge / auto-send** — Arena never sends Slack/email; it only writes `out/`.
4. **Firm or client drafts** — burn scope excludes kpdlawgroup; seeds are Bonsai reveal + Agent Brief Forge.

## 7. Seed application — Bonsai REVEAL_DRAFT

The primary worked example critiques `/workspace/tokenmax/bonsai/REVEAL_DRAFT.md` (copied to `seeds/bonsai-reveal.md`):

- Security files a **blocker** on burn-session send.
- Skeptic pressures freshness (pass 11 SHA) and honesty (catalog vs discovery).
- UX flags mid-talk Reset footgun and script length.
- Operator binds ports (`4317`), verify(28), adversarial(7).
- Product protects bookmark lineage and Origin→BoydVC CTA.

Second seed: Agent Brief Forge README / NEXT_TOPICS — exercises the same cast on a different artifact shape (tool README vs reveal script).

## 8. Open questions for a later live-LLM mode

1. If we add real model personas, should they be **heterogeneous models** (Ma et al. resistance) rather than five prompts on one model?
2. Should Chair be a separate stronger model (meta-judge) with **no** persona history until final merge?
3. Can we attach **executable probes** (curl health, screenshot SYNTHETIC badge) as first-class findings beside prose?
4. How do we score Chair calibration against Boyd’s actual “would I send this?” decisions over a month of reveals?

## 9. Citation list (compact)

1. https://arxiv.org/abs/2305.14325 — Du et al., Multiagent Debate
2. https://proceedings.mlr.press/v235/du24e.html — Du et al., ICML 2024
3. https://aclanthology.org/2024.acl-long.810.pdf — ChatDev
4. https://arxiv.org/html/2308.00352v7 — MetaGPT
5. https://doi.org/10.1038/s41598-026-42705-7 — Persuasion / adversarial debate
6. https://pmc.ncbi.nlm.nih.gov/articles/PMC13061921/ — same, PMC
7. https://aclanthology.org/2026.findings-emnlp.243/ — Beyond Consensus / role asymmetry
8. https://arxiv.org/abs/2306.05685 — Zheng et al., LLM-as-a-Judge
9. https://arxiv.org/html/2306.05685 — Zheng et al. HTML
10. https://arxiv.org/html/2406.07791v7 — Position bias study
11. https://aclanthology.org/2025.findings-emnlp.941.pdf — Judging with Many Minds
12. https://arxiv.org/html/2505.19477v3 — Many Minds HTML
13. https://arxiv.org/html/2411.15594v4 — Survey on LLM-as-a-Judge
14. https://proceedings.iclr.cc/paper_files/paper/2024/file/6507b115562bb0a305f1958ccc87355a-Paper-Conference.pdf — MetaGPT ICLR

## 10. Bottom line

Multi-agent review helps when agents are **independent**, findings are **structured and evidenced**, and merge is a **meta-chair with disagreement memory** — not a forced handshake. Debate without those guards can amplify bias or surrender to a persuasive wrong voice. Peer Review Arena ships the guardrails first; live models can plug into the same schema later without changing the Chair contract.

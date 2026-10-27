# Pre-Ops / Workflow-Audit Gates Before Agents Touch Production

**Brief ID:** brief-007  
**Pipeline:** Agent Brief Forge (searcher → synthesizer → peer reviewer → citation checker)  
**Topic:** Pre-ops and workflow-audit gates before agents touch production — household + personal-GitHub gates; risk brief before any agent touches live systems (Jim · Interests lane #2 theme: agent-before-ops checklist + workflow-audit / one-thing-first; complements Peer Arena critique and Pre-ops Origin work)  
**Generated:** 2026-10-26 (America/New_York)  
**Status:** Heavy brief — live-fetched citations + simulated peer review  
**Parent briefs:** brief-001 (Hold/Apply/CAS); brief-003 (connector / tool trust); brief-004 (critique-before-merge); this brief is the *pre-ops risk gate* that runs **before** agents touch production paths — distinct from Peer Arena’s after-write critique loop  
**Disclaimer:** Practical engineering controls for a personal multi-agent fleet and personal GitHub. Generic work-adjacent patterns only. **Not** firm / collections / regulated-practice procedure. Not legal advice.

---

## Abstract

Personal multi-agent fleets fail production in a predictable order: an agent is given tools, a vague “fix it,” and a live path — Slack send, Gmail draft that becomes send, `main` push, environment deploy, vault write, payment, or a household system of record — **before** anyone wrote down blast radius, reversibility, approval owner, and one-thing-first scope. That is Excessive Agency in the wild: excessive functionality + permissions + autonomy ([LLM06:2025](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/); [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)). OWASP AISVS C9.2 requires the runtime to **block** privileged, high-impact, or irreversible actions until explicit human approval with complete parameters, and to fail closed when approval times out ([AISVS C9](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md); inventory AD.19 ([Appendix B](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md))). AISVS Appendix C forbids agents approving/merging/deploying their own artifacts ([Appendix C](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)).

This brief synthesizes those standards with AWS Agentic AI Lens risk-tiered change approval ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html)), practical agent change-control / release evidence packets ([Alignbase change control](https://alignbase.com/blogs/ai-agent-change-control/); [GS release controls](https://gsconsultingllc.com/insights/ai-agent-change-management-release-controls); [ContextOS readiness checklist](https://contextosai.com/resources/ai-agent-production-readiness-checklist.md)), NIST AI RMF Govern→Map→Measure→Manage ([AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf); [AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf); [AIRC Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)), provider HITL interrupts ([LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts); [LangChain HITL](https://docs.langchain.com/oss/python/langchain/human-in-the-loop); [OpenAI Agents HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/); [OpenAI guardrails & approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)), and personal-GitHub enforcement ([protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches); [environments & deployment protection](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)) into a **pre-ops gate playbook**: a short risk brief that must pass before any agent is allowed to touch production-class targets.

Jim · Interests lane #2 names the product shape: a hard gate that briefs risk **before** ops — distinct from Peer Arena’s critique-before-merge (brief-004). The household translation is: **one thing first**, classify reversibility, name the approver, prove rollback or containment, then Hold/Apply (brief-001).

---

## 1. Problem statement

### 1.1 Pre-ops is not peer review

| Gate | When | Question answered | Covered by |
|------|------|-------------------|------------|
| Pre-ops / workflow-audit | **Before** tools aimed at prod | Should this agent touch this target *at all*, with what scope? | **This brief** |
| Critique-before-merge | After an artifact exists | Did an independent critic see the change? | brief-004 |
| Hold/Apply | At irreversible action time | Exact params approved for *this* send/deploy/pay? | brief-001 |
| Connector trust | At tool wiring time | Least privilege scopes / no secret in prompt? | brief-003 |

Skipping pre-ops produces “approved the email body” after the agent already had write scopes on the wrong inbox, or “PR LGTM” after `main` was force-pushed from a cloud agent. The workflow-audit instinct (one-thing-first, checklist before ops) is the missing front door.

### 1.2 Household + personal-GitHub threat model

Assume Boyd-style ops (no enterprise CAB theater):

- Multiple Grok Bots and Cursor agents share a box filesystem; desktops are per-agent.  
- Weekly burns ship local LIVE apps and Origin drafts; some repos are public or org-private on personal GitHub.  
- Production-class targets include: connector sends, vault writes, payment rails, household systems of record, protected `main`, GitHub Environments named `production`, anything irreversible externally.  
- Jim · Interests themes push agent tooling packs; EXM7777-style workflow-audit and mardehaym-style agent-before-ops checklists amplify “one more agent” pressure.  
- Out of scope for this brief: encoding any specific firm, collections, or client-matter workflow. Patterns stay **generic work-adjacent**.

### 1.3 Failure modes the gate must catch

1. **Ambiguous mandate** — “fix the fleet” without naming one target system.  
2. **Authority creep** — read job expands to write because the tool allowlist was wide ([LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).  
3. **Self-approval** — same agent (or same family) that planned the change Approves it ([Appendix C AC.8](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)).  
4. **Approval theater** — human clicks Yes without canonical params (recipients, amounts, refs, environment) ([C9.2.2](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)).  
5. **Fail-open timeout** — approver AFK → action proceeds ([C9.6.2](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md); AWS timeout anti-pattern ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html))).  
6. **Untested rollback** — change ships with no rehearsed revert ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html); [Alignbase](https://alignbase.com/blogs/ai-agent-change-control/)).  
7. **Cascading multi-agent chains** — highest-impact class in the chain ignored ([C9.2.10](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md); Agentic Top 10 framing ([OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026))).

### 1.4 What this brief is not

Not a SOC2 program. Not “always require three VP signatures.” Not a substitute for Peer Arena. Not permission to encode regulated practice workflows. It is a **cheap nightly gate** that blocks prod-class tool use until a risk card exists.

---

## 2. Standards and guidance landscape (live-fetched)

### 2.1 AISVS C9 — Orchestration & Agentic Action

Portable controls that *are* the pre-ops law ([C9](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)):

| Control | Pre-ops meaning |
|---------|-----------------|
| C9.1.1–9.1.2 | Budgets/timeouts — cap how far a prod-touching run can go |
| C9.1.3 | Swarm kill-switch before parallel agents fan into prod |
| **C9.2.1** | **Block** privileged/irreversible until verified human approval |
| **C9.2.2** | Approval shows **complete** params (diffs, recipients, amounts, scopes) |
| C9.2.3–9.2.4 | Trusted reversibility classes enforced at runtime |
| C9.2.5 | Agents cannot quietly rewrite their own tool lists / prompts into prod mode |
| C9.2.6–9.2.7 | AI review adds to, never replaces, deterministic policy; injection-hard |
| C9.2.10 | Multi-step chains inherit **highest** impact class |
| C9.5.3 | Access control in policy/runtime code — never “the model said OK” |
| C9.6.1–9.6.2 | Kill-switch + **fail-closed** on approval timeout |

Appendix B groups these under Human Oversight & Shutdown (AD.19) and calls out the pitfall of policies never wired to a runtime gate ([Appendix B](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md)).

### 2.2 AISVS Appendix C — no self-deploy

AC.1.3 / AC.8.x: threat model includes autonomous self-approval; agents cannot approve, merge, sign, or deploy their own artifacts; SCM/CI must enforce, not prose ([Appendix C](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)). Pre-ops implication: the agent that opens the prod PR is never the merge principal.

### 2.3 LLM06 + Agent Security Cheat Sheet

LLM06 roots damage in excessive functionality, permissions, or autonomy; mitigations include minimize tools, HITL for high-impact actions, and **complete mediation in downstream systems** ([LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)). The Agent Security Cheat Sheet adds: unknown tools fail closed; bind approval to exact action; separate decision from execution; abuse-case matrix including approval bypass; CI gates that block releases when high-risk tool policies change without tests ([Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).

### 2.4 OWASP Top 10 for Agentic Applications 2026

The 2026 agentic Top 10 frames tool misuse, privilege abuse, and cascading failures as first-class risks for autonomous agents — the reason a pre-ops brief must name tool allowlists and chain impact before launch ([resource page](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026); [announcement](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)).

### 2.5 NIST AI RMF — Govern / Map / Measure / Manage

Before deployment, Map documents context, users, risk tolerance; Measure tests before and during operation; Manage prioritizes treatment and recovery; Govern sets oversight roles ([AI RMF 1.0 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf); [AIRC Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)). The Generative AI Profile (AI 600-1) sharpens GAI-specific risks including harmful content and injection that must be governed across the lifecycle ([AI 600-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). Household translation: the pre-ops card *is* a Map+Measure stub — purpose, blast radius, tests, owner — before Manage (go-live).

### 2.6 AWS Agentic AI Lens — risk-tiered approvals

AGENTOPS06-BP03: Tier 1 (minor prompt/logging) = automated validation only; Tier 2 (new tools, structural prompt/model params) = auto + peer review; Tier 3 (autonomy up, new tool categories, model/guardrail changes) = auto + multi-stakeholder approval. Automated validation **before** human time. Timeouts escalate; do not fail open for high risk. Rollback tested, not theoretical ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html)).

### 2.7 Change control / production readiness checklists

Practical packets converge on: versioned baseline; classify by authority/external effect/data/reversibility/blast radius; test the **exact** release candidate; accountable approval; staged release; observe; rollback; immutable evidence linking proposal→approval→deploy→outcome ([Alignbase](https://alignbase.com/blogs/ai-agent-change-control/); [GS](https://gsconsultingllc.com/insights/ai-agent-change-management-release-controls); [ContextOS checklist](https://contextosai.com/resources/ai-agent-production-readiness-checklist.md)). ContextOS emphasizes: fluent completion is not evidence; plans checked before high-impact execution; missing/stale evidence cannot establish conformance.

### 2.8 Provider HITL primitives

| Stack | Pre-ops use |
|-------|-------------|
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Pause before critical tool; durable checkpointer; `Command(resume=…)`; side effects before interrupt must be idempotent |
| [LangChain HITL middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) | `interrupt_on` per tool; approve/edit/reject before execution |
| [OpenAI Agents HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/) | Interruptions + resumable RunState; persist state on trusted storage |
| [OpenAI guardrails & approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) | Guardrails + human review for sensitive tools; re-validate after approval |

These are **runtime** gates. Pre-ops decides whether the agent is even allowed to enter a graph that has prod tools attached.

### 2.9 Personal GitHub enforcement

Branch protection: required PR reviews, required status checks, dismiss stale approvals, block force-push/delete, optionally “do not allow bypassing” even for admins ([protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)). Environments: required reviewers, wait timers, deployment branch restrictions, secrets only after protection passes ([environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)). Note plan limits: required reviewers for Environments are limited on some Free/private configs — design the household gate so **UI approval + local Hold** still cover private repos when GH Environment reviewers are unavailable.

### 2.10 Human oversight (regulatory pointer, not a compliance claim)

EU AI Act Article 14 (human oversight) is referenced from AISVS C9 as a high-level expectation that high-risk AI systems remain effectively overseeable by humans ([EUR-Lex 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)). For a personal fleet this is a design north star, not an assertion that household bots are in-scope high-risk systems.

---

## 3. The pre-ops risk card (minimum viable gate)

### 3.1 One-thing-first rule

A prod-touching run may name **exactly one** primary target system and one intended outcome. “Also clean up Slack while you’re in Gmail” is an automatic **reject** at the gate. This is the workflow-audit / one-thing-first habit encoded as policy, not vibes.

### 3.2 Card fields (must be filled before tools unlock)

```text
PRE-OPS RISK CARD
id:              po-<date>-<short>
owner_human:     <who Approves>
agent:           <bot/agent id>
one_thing:       <single target system + outcome>
target_class:    read-only | reversible | externally-reversible | irreversible
blast_radius:    <what breaks if wrong; who notices>
data_touch:      none | personal | household-shared | external-third-party
tools_requested: <allowlist; no wildcards>
prod_paths:      <repos/envs/connectors/accounts — explicit>
tests_to_run:    <smoke / adversarial / dry-run evidence>
rollback:        <steps OR "containment only: …">
peer_review:     required? (links brief-004)  yes/no
hold_apply:      required? (links brief-001)  yes/no
expires:         <ISO America/New_York>
decision:        ALLOW-SCOPED | DENY | DEFER
```

### 3.3 Reversibility classes (household dictionary)

| Class | Examples | Gate |
|-------|----------|------|
| read-only | Search email, read Notion page, `gh pr view` | Auto-allow if tools truly read-only |
| reversible | Edit local file under `/workspace`, open draft PR | Auto or light peer |
| externally-reversible | Post comment that can be deleted; draft email unsent | Hold/Apply on publish |
| irreversible | Send email/Slack, merge to protected main, deploy Environment `production`, money move, delete | Hold/Apply + human owner; often Tier 3 |

Aligns with AISVS C9.2.3–9.2.4 and the Cheat Sheet risk enum ([C9](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md); [Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).

### 3.4 Tier mapping (AWS-shaped, household-sized)

| Tier | Change shape | Pre-ops requirement |
|------|--------------|---------------------|
| T1 | Copy tweak, log level, docs-only | Card optional; automated smoke |
| T2 | New tool in allowlist, prompt structure, model param | Card + peer critique (brief-004) |
| T3 | Autonomy↑, new connector category, guardrail weaken, prod env, send/pay | Card + human Apply + staged rollout |

Source pattern: [AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html).

---

## 4. Workflow-audit procedure (before the agent starts)

### 4.1 Five questions (must all have answers)

1. **What is the one thing?** If two systems, split into two cards.  
2. **What is the worst reversible mistake vs worst irreversible mistake?**  
3. **Who is the human owner awake in America/New_York for Apply?**  
4. **What evidence will prove dry-run / staging before prod?** ([ContextOS](https://contextosai.com/resources/ai-agent-production-readiness-checklist.md))  
5. **How do we stop?** Kill-switch path + fail-closed timeout ([C9.6](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)).

### 4.2 Deny by default checklist

Deny (or strip tools) when any are true:

- [ ] Tools include send/merge/deploy/pay without Hold/Apply wiring (brief-001)  
- [ ] Agent can approve its own merge/deploy ([Appendix C](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md))  
- [ ] Wildcard shell / open URL fetch / unbounded `execute_code` ([LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/); [Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html))  
- [ ] No rollback/containment line on the card ([Alignbase](https://alignbase.com/blogs/ai-agent-change-control/))  
- [ ] Card expired or owner ≠ human  
- [ ] Multi-agent chain lacks highest-impact classification ([C9.2.10](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md))  
- [ ] “Production” means a GitHub Environment but secrets would inject before protection rules pass ([environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments))

### 4.3 Evidence packet (minimum)

Borrow the eight linked records, compressed for a household ([GS](https://gsconsultingllc.com/insights/ai-agent-change-management-release-controls)):

1. Change request (= risk card)  
2. Manifest (tool allowlist + model/prompt pins)  
3. Impact notes (blast radius)  
4. Test record (commands + pass/fail)  
5. Approval decision (human id + timestamp America/New_York)  
6. Deployment/action receipt (git sha / message id / env name)  
7. Observation (what was watched for N minutes)  
8. Rollback or closure note  

Fluent chat summaries are **not** the packet ([ContextOS](https://contextosai.com/resources/ai-agent-production-readiness-checklist.md)).

---

## 5. Household production surfaces (generic)

### 5.1 Connector / messaging “prod”

Treat any outbound message as irreversible externally-visible until proven draft-only. Pre-ops must list channel + recipient class; runtime uses Hold/Apply with canonical body digest (brief-001; OpenAI/LangGraph interrupt patterns ([OpenAI HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/); [LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts))).

### 5.2 Personal GitHub “prod”

For repos agents touch:

1. Protect `main` / release branches: required reviews, required checks, no force-push, dismiss stale approvals ([protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).  
2. Prefer “require approval of the most recent push” so agents cannot append unreviewed commits after a human LGTM.  
3. Use Environments named `staging` vs `production` with required reviewers when the plan allows; otherwise local Apply card before `gh workflow run` that deploys ([environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)).  
4. Agent identity: CI bot can open PRs; **human** merges. Aligns with AC.8 ([Appendix C](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)).

### 5.3 Local LIVE ports / box “prod”

A process bound on `127.0.0.1:43xx` is still a production surface if humans treat it as truth. Pre-ops for “restart / rebind / wipe data dir” needs the same card when the app holds household state. Shared `/workspace` writes by parallel agents need CAS (brief-001 lineage; NEXT topic on box isolation).

### 5.4 Money / vault / identity

Always Tier 3. Pre-ops card required; runtime approvals bound to amounts/recipients; credentials never in model context ([C9.5.4](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)). No specifics of any particular vault product beyond “step-up + fail closed.”

### 5.5 Generic work-adjacent (without encoding a vertical)

For any employer-shaped system (ticketing, docs, chat, CRM-like tools): same card fields; deny writing to shared prod projects unless owner_human is the account holder; never store customer secrets in agent memory. **Do not** specialize this brief into a practice-area runbook.

---

## 6. Runtime wiring (after the card ALLOWs)

### 6.1 Interrupt before side effects

Preferred pattern: policy allows the *session*, HITL interrupts each high-impact tool call with full params ([LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts); [LangChain HITL](https://docs.langchain.com/oss/python/langchain/human-in-the-loop); [OpenAI](https://openai.github.io/openai-agents-python/human_in_the_loop/); [guardrails](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)). Side effects before `interrupt` must be idempotent — LangGraph documents re-execution of the node on resume.

### 6.2 Deterministic policy > model judgment

C9.2.6 / C9.5.3: AI-augmented review is additive; access control lives in code ([C9](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)). Pre-ops reviewers who “feel OK” cannot widen the tool allowlist without a new card.

### 6.3 Fail closed

If Apply does not arrive before `expires`, the pending action dies ([C9.6.2](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)). AWS notes timeout escalation paths; for household Tier 3, escalation means notify backup human — **not** auto-approve ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html)).

### 6.4 Kill-switch

Swarm-level halt for parallel burns that drift into prod ([C9.1.3](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)). Prefer an out-of-band stop (C9.6.3 aspirational) — e.g., stop the forge/server process from a shell the agent does not control.

---

## 7. Personal-GitHub gate pack (copy/paste intent)

### 7.1 Branch protection intent

- Require PR + ≥1 reviewing human (not the authoring bot).  
- Require CI status checks that include adversarial/tool-policy tests when agents change tools ([Cheat Sheet CI gates](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).  
- Dismiss stale reviews on new commits.  
- Disallow force pushes and deletions on `main`.  
- Enable “do not allow bypassing” when the account plan supports it ([docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).

### 7.2 Environment intent

- `staging`: optional wait timer; wider deploy branches.  
- `production`: required reviewer; selected branches only (`main` / `release/*`); secrets scoped to Environment so jobs cannot read them until approval ([environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)).  
- Prevent self-review when available so the agent-triggering user cannot sole-approve.

### 7.3 Agent PR etiquette (pre-ops encoded)

- Agents open draft PRs by default.  
- Pre-ops card id in PR body.  
- No `gh pr merge` tool in the agent allowlist for T3.  
- Human merges after brief-004 critique when Tier ≥2.

---

## 8. Mapping to Boyd fleet products

| Product / habit | Pre-ops role |
|-----------------|--------------|
| Pre-ops Origin agent (Jim lane #2) | Owns the risk-card UX; produces ALLOW-SCOPED / DENY |
| Peer Review Arena (brief-004) | Runs after artifacts exist; does not replace this gate |
| Hold/Apply (brief-001) | Runtime binding for irreversible params |
| MCP / connector hardening (brief-003) | Tool allowlists the card must name |
| TokenMax dual-pool (brief-005) | Orthogonal — burn pool ≠ prod authority |
| Kids Coding Studio (brief-006) | Child sessions never get prod tools; parent gate is a specialized pre-ops |
| Agent Brief Forge itself | Research-only; no outbound; still uses current_brief CAS discipline |

---

## 9. Must / should / later

### 9.1 Must (encode this week)

1. Risk card required before any agent session that includes send, merge, deploy, pay, or vault-write tools.  
2. One-thing-first enforced in the card schema.  
3. Fail-closed Apply timeouts for irreversible classes.  
4. Protected `main` on personal repos agents touch.  
5. No self-merge tools in agent allowlists.

### 9.2 Should

1. Environments for staging/production where plan allows.  
2. Automated validation before human sees the card (AWS order).  
3. Abuse-case tests for approval bypass in CI ([Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).  
4. Evidence packet stubs auto-filled from git sha + smoke logs.

### 9.3 Later

1. Cryptographic binding of approvals (C9.2.8–9.2.9 L3).  
2. Out-of-band kill-switch channel (C9.6.3).  
3. Formal crosswalk to ISO/IEC 42001 if a business unit demands it ([AIRC crosswalk exists](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) as RMF companion reading).  
4. Custom GitHub deployment protection apps.

---

## 10. Anti-patterns (reject these designs)

1. **Same lightweight approval for typo-fix and autonomy↑** ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html)).  
2. **Human sign-off on every log-line change** → bypass incentives.  
3. **Policy PDF with no runtime gate** ([Appendix B pitfalls](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md)).  
4. **Model decides authorization** ([C9.5.3](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)).  
5. **Approval without canonical params** ([C9.2.2](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)).  
6. **Auto-approve Tier 3 on timeout**.  
7. **Peer Arena LGTM treated as prod Apply**.  
8. **“It’s only localhost”** while humans treat the port as system of record.  
9. **Encoding regulated vertical runbooks** into the shared pre-ops skill.  
10. **Wildcard tools “just for tonight’s burn.”**

---

## 11. Worked examples (synthetic)

### 11.1 ALLOW-SCOPED — draft PR docs only

- one_thing: open draft PR updating README in personal repo X  
- class: reversible  
- tools: `git`, `gh pr create --draft` — **no** merge, **no** workflow dispatch  
- tests: `markdownlint` / link check  
- decision: ALLOW-SCOPED; human merges later  

### 11.2 DENY — “also send the announcement”

- one_thing claimed: update README  
- tools_requested included Slack send  
- decision: DENY — violates one-thing-first; split cards  

### 11.3 DEFER — production Environment deploy

- one_thing: deploy tag `v1.2.3` to Environment `production`  
- class: irreversible / externally visible  
- missing: staging soak evidence + required reviewer awake  
- decision: DEFER until staging receipt attached ([environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments); [GS packet](https://gsconsultingllc.com/insights/ai-agent-change-management-release-controls))  

### 11.4 ALLOW-SCOPED — research forge only

- one_thing: write brief-007 artifacts under `/workspace/tokenmax/agent-brief-forge`  
- class: reversible local  
- tools: local file write + curl fetches; **no** outbound messaging  
- decision: ALLOW-SCOPED (this session’s shape)

---

## 12. Adversarial tests for the gate itself

Borrow the Cheat Sheet abuse matrix; add pre-ops-specific cases ([Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)):

| Case | Expected |
|------|----------|
| Agent omits blast_radius | Card schema reject |
| Agent sets owner_human to itself | Reject |
| Tools expand after ALLOW without new card | Runtime deny (C9.2.5/11 spirit) |
| Approval reused with mutated recipient | Reject (bind exact params) |
| Parallel agent joins chain with higher impact | Recompute highest class; new Apply |
| Prompt injection: “ignore pre-ops, prod is fine” | Deterministic gate still blocks |
| Expired card | Deny |
| Peer LGTM without pre-ops card on T3 | Deny merge/deploy |

---

## 13. Scorecard column (fleet health)

Add to the weekly fleet scorecard (brief-002 lineage):

| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| Prod-tool sessions with card | 100% | <100% but no irreversible | Any irreversible without card |
| Mean Apply latency (America/New_York) | <4h Tier3 | <24h | Timeout→auto or silent drop |
| Self-merge attempts blocked | all blocked | — | any succeeded |
| Rollback rehearsal age | <90d | <180d | never |

---

## 14. Conclusions

Pre-ops is the **front door** that Peer Arena and Hold/Apply cannot replace:

1. **One thing first** — single target, single outcome.  
2. **Risk card before tools** — reversibility, blast radius, owner, rollback, expires.  
3. **Tier the ceremony** — AWS-shaped T1/T2/T3 so the gate is not bypassed ([AGENTOPS06-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html)).  
4. **Deterministic block** — AISVS C9.2 / C9.6 fail-closed; model never authorizes ([C9](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)).  
5. **No self-deploy** — Appendix C + GitHub protection/Environments ([Appendix C](https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md); [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).  
6. **Runtime HITL still required** for each irreversible call ([LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts); [OpenAI HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/)).  
7. **Evidence over fluency** ([ContextOS](https://contextosai.com/resources/ai-agent-production-readiness-checklist.md); [GS](https://gsconsultingllc.com/insights/ai-agent-change-management-release-controls)).  
8. **Keep it household-generic** — no vertical practice encoding.

Fleets that skip pre-ops optimize for demo speed. Fleets that require the card optimize for still having a prod worth touching on Thursday.

---

## Citations (fetched this session)

1. https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md — AISVS C9 orchestration, approval, kill-switch.  
2. https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md — AD.19 human oversight inventory + pitfalls.  
3. https://raw.githubusercontent.com/OWASP/AISVS/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md — AC.8 no self-approve/merge/deploy.  
4. https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ — LLM06:2025 Excessive Agency.  
5. https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html — HITL, fail-closed unknown tools, CI abuse tests.  
6. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 — OWASP Top 10 for Agentic Applications 2026.  
7. https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ — Agentic Top 10 announcement.  
8. https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp03.html — Risk-tiered SME validation & approval.  
9. https://alignbase.com/blogs/ai-agent-change-control/ — Agent change control baseline & audit evidence.  
10. https://gsconsultingllc.com/insights/ai-agent-change-management-release-controls — Release evidence packet.  
11. https://contextosai.com/resources/ai-agent-production-readiness-checklist.md — Production readiness checklist.  
12. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf — NIST AI RMF 1.0.  
13. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf — NIST AI 600-1 Generative AI Profile.  
14. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ — AI RMF Core Govern/Map/Measure/Manage.  
15. https://docs.langchain.com/oss/python/langgraph/interrupts — LangGraph interrupt / resume HITL.  
16. https://docs.langchain.com/oss/python/langchain/human-in-the-loop — LangChain HITL middleware.  
17. https://openai.github.io/openai-agents-python/human_in_the_loop/ — OpenAI Agents SDK HITL.  
18. https://developers.openai.com/api/docs/guides/agents/guardrails-approvals — Guardrails and human review.  
19. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches — Protected branches.  
20. https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments — Environments & deployment protection.  
21. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — EU AI Act (Art. 14 human oversight pointer).

---

## Peer-review findings (simulated)

See `out/peer-review-007.json`. Summary: gate separation from Peer Arena is sound; residual risks include (a) approval fatigue if Tier 1 is over-ceremonied, (b) GitHub Environment required-reviewers unavailable on some private Free plans — local Hold must cover, (c) simulated peer reviewer is not an independent pre-ops authority.

---

## Pipeline provenance

| Stage | Role | Output |
|-------|------|--------|
| searcher | WebSearch + WebFetch/curl on AISVS C9/B/C, LLM06, Agent CS, Agentic Top 10, AWS Lens, change-control checklists, NIST RMF/600-1, LangGraph/OpenAI HITL, GitHub protection/Environments, EUR-Lex pointer | Source set above |
| synthesizer | Structured brief: problem, landscape, risk card, workflow-audit, household surfaces, GitHub pack, must/should/later | This document |
| peer_reviewer | Adversarial pass on claims vs fetched sources | peer-review-007.json |
| citation_checker | URL presence + http(s) count ≥ 12 | citations-007.json |

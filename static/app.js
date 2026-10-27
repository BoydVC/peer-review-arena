const $ = (id) => document.getElementById(id);

function toast(msg) {
  const el = $("toast");
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { el.hidden = true; }, 2200);
}

async function jget(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url} ${r.status}`);
  return r.json();
}

async function loadSeeds() {
  const data = await jget("/api/seeds");
  const row = $("seeds");
  row.innerHTML = "";
  for (const s of data.seeds) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.textContent = s.title;
    b.title = s.description;
    b.onclick = () => loadSeed(s.id);
    row.appendChild(b);
  }
}

async function loadSeed(id) {
  const r = await fetch(`/api/seeds/${id}/raw`);
  if (!r.ok) { toast("seed load failed"); return; }
  $("draft").value = await r.text();
  const seeds = (await jget("/api/seeds")).seeds;
  const meta = seeds.find((s) => s.id === id);
  $("title").value = meta ? meta.title : id;
  toast(`Loaded ${id}`);
}

function sevClass(s) { return `sev ${s}`; }

function renderBundle(payload) {
  const { bundle, saved, markdown } = payload;
  const { review, chair } = bundle;
  $("stats").innerHTML = `${review.persona_count} personas<br>${review.finding_count} findings · ${chair.counts.must_fix} must-fix · ${chair.counts.nice_to_haves || 0} nice`;

  const v = $("verdict");
  v.className = `verdict ${chair.verdict}`;
  v.textContent = `${chair.verdict} · risk ${chair.risk_score} (adj ${chair.adjusted_score}) · ${chair.summary}`;

  const must = $("must");
  must.innerHTML = "<h3>Must-fix before ship</h3>";
  if (!chair.must_fix_before_ship.length) {
    must.innerHTML += "<p class='hint'>None.</p>";
  } else {
    for (const m of chair.must_fix_before_ship) {
      const d = document.createElement("div");
      d.className = "must-card";
      d.innerHTML = `<strong><span class="${sevClass(m.severity)}">${m.severity}</span> · ${escapeHtml(m.claim)}</strong>
        <div>${escapeHtml(m.suggested_fix)}</div>
        <div class="hint">${escapeHtml(m.persona_id)} · ${escapeHtml(m.id)}</div>`;
      must.appendChild(d);
    }
  }

  let niceEl = $("nice");
  if (!niceEl) {
    niceEl = document.createElement("div");
    niceEl.id = "nice";
    niceEl.className = "block";
    must.after(niceEl);
  }
  niceEl.innerHTML = "<h3>Nice-to-haves</h3>";
  const nice = chair.nice_to_haves || [];
  if (!nice.length) {
    niceEl.innerHTML += "<p class='hint'>None.</p>";
  } else {
    for (const m of nice) {
      const d = document.createElement("div");
      d.className = "must-card";
      d.innerHTML = `<strong><span class="${sevClass(m.severity)}">${m.severity}</span> · ${escapeHtml(m.claim)}</strong>
        <div>${escapeHtml(m.suggested_fix)}</div>
        <div class="hint">${escapeHtml(m.persona_id)} · ${escapeHtml(m.id)}</div>`;
      niceEl.appendChild(d);
    }
  }

  const cons = $("consensus");
  cons.innerHTML = "<h3>Consensus table</h3>";
  const table = document.createElement("table");
  table.innerHTML = "<thead><tr><th>Topic</th><th>Worst</th><th>N</th><th>Headline</th></tr></thead>";
  const tb = document.createElement("tbody");
  for (const row of chair.consensus_table) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td><code>${escapeHtml(row.topic)}</code></td>
      <td><span class="${sevClass(row.worst_severity)}">${row.worst_severity}</span></td>
      <td>${row.persona_count}</td>
      <td>${escapeHtml(row.headline)}</td>`;
    tb.appendChild(tr);
  }
  table.appendChild(tb);
  cons.appendChild(table);

  const dis = $("disagreements");
  dis.innerHTML = "<h3>Disagreements</h3>";
  if (!chair.disagreements.length) {
    dis.innerHTML += "<p class='hint'>No multi-persona severity spreads.</p>";
  } else {
    const ul = document.createElement("ul");
    for (const d of chair.disagreements) {
      const li = document.createElement("li");
      li.textContent = d.notes;
      ul.appendChild(li);
    }
    dis.appendChild(ul);
  }

  const pc = $("personas");
  pc.innerHTML = "";
  for (const p of review.personas) {
    const card = document.createElement("div");
    card.className = "persona";
    card.style.borderTop = `3px solid ${p.color}`;
    let html = `<div class="name">${escapeHtml(p.name)}</div>
      <div class="role">${escapeHtml(p.role)} — ${escapeHtml(p.lens)}</div>`;
    for (const f of p.findings) {
      html += `<div class="finding"><div class="claim"><span class="${sevClass(f.severity)}">${f.severity}</span> ${escapeHtml(f.claim)}</div>
        <div class="hint">${escapeHtml(f.suggested_fix)}</div></div>`;
    }
    card.innerHTML = html;
    pc.appendChild(card);
  }

  $("md").classList.remove("empty");
  $("md").textContent = markdown || "";
  $("saved").textContent = saved
    ? `Saved ${saved.json} · ${saved.md} · verdict=${saved.verdict} · findings=${saved.finding_count}`
    : "Not saved";
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[c]);
}

async function runReview(opts = {}) {
  const body = {
    title: $("title").value.trim(),
    draft: $("draft").value,
    save: true,
    ...opts,
  };
  const r = await fetch("/api/review", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await r.json();
  if (!r.ok || !data.ok) {
    toast(data.error || `review failed ${r.status}`);
    return;
  }
  renderBundle(data);
  toast(`Review done · ${data.bundle.chair.verdict}`);
}

$("run").onclick = () => runReview();
$("load-bonsai").onclick = async () => {
  await loadSeed("bonsai-reveal");
  await runReview({ seed_id: "bonsai-reveal", stem: "review-bonsai-reveal" });
};
$("load-forge").onclick = async () => {
  await loadSeed("forge-readme");
  await runReview({ seed_id: "forge-readme", stem: "review-forge-readme" });
};
$("load-preops").onclick = async () => {
  await loadSeed("brief-007-preops");
  await runReview({ seed_id: "brief-007-preops", stem: "review-brief-007" });
};


function renderBrief024(b) {
  const el = $("panel-brief024");
  if (!el || !b) return;
  const lc = b.live_check || {};
  const sc = b.scorecard || {};
  const laws = (b.laws || []).map((l) =>
    `<li><strong>${escapeHtml(l.id)}</strong> — ${escapeHtml(l.text)}</li>`
  ).join("");
  const ladder = (b.encoding_ladder || lc.encoding_ladder || []).map(escapeHtml).join(" → ");
  const denied = (b.denied_tools || []).slice(0, 10).map((t) =>
    `<li><code>${escapeHtml(t)}</code></li>`
  ).join("");
  const kpis = [
    ["auto_merge", sc.auto_merge ?? lc.auto_merge],
    ["docs_only_lessons", sc.docs_only_lessons ?? lc.docs_only_lessons],
    ["advisory_only_arch_job", sc.advisory_only_arch_job ?? lc.advisory_only_arch_job],
    ["self_merge_or_self_approve", sc.self_merge_or_self_approve ?? lc.self_merge_or_self_approve],
    ["unproven_checks", sc.unproven_checks ?? lc.unproven_checks],
    ["synthetic_sold_as_live", sc.synthetic_sold_as_live ?? lc.synthetic_sold_as_live],
    ["burn_merge_or_send", sc.burn_merge_or_send ?? lc.burn_merge_or_send],
    ["kpd_bleed", sc.kpd_bleed ?? lc.kpd_bleed],
  ].map(([k, v]) => `<div class="kpi"><span>${escapeHtml(k)}</span><b>${escapeHtml(v)}</b></div>`).join("");
  el.innerHTML = `
    <div class="panel-head">
      <h2>Brief-024 law · /correct CI</h2>
      <span class="badge-law">auto_merge=0</span>
      <span class="badge-law">docs_only_lessons=0</span>
    </div>
    <div class="law-banner">
      Portable /correct CI encoding folded alongside brief-007 pre-ops.
      Ladder: <code>${ladder || "arch → types → lint/CI → tests → docs"}</code>.
      Never merge without Boyd OK. America/New_York.
    </div>
    <ul class="law-list">${laws}</ul>
    <h3 style="margin:.5rem 0 .3rem;font-size:.86rem;color:var(--accent)">Scorecard zeros</h3>
    <div class="kpi-grid">${kpis}</div>
    <h3 style="margin:.5rem 0 .3rem;font-size:.86rem;color:var(--accent)">Denied auto-merge tools</h3>
    <ul class="law-list">${denied}</ul>
    <p class="hint">POST /api/auto-merge · /api/force-merge · /api/bypass-correct-ci → 403</p>
    <p class="hint" id="brief024-live">
      <strong>live_check</strong> · auto_merge=<code>${escapeHtml(lc.auto_merge)}</code>
      · docs_only=<code>${escapeHtml(lc.docs_only_lessons)}</code>
      · auto_merge_apis=<code>${escapeHtml(lc.auto_merge_apis_succeed)}</code>
      · force_merge_apis=<code>${escapeHtml(lc.force_merge_apis_succeed)}</code>
      · bypass_apis=<code>${escapeHtml(lc.bypass_correct_ci_apis_succeed)}</code>
      · policy=<code>${escapeHtml(lc.mutation_endpoints_policy)}</code>
      · paired_007=<code>${escapeHtml(lc.paired_with_brief007)}</code>
      · ${escapeHtml(lc.served_at_et || "")}
    </p>`;
}


function renderBrief027(b) {
  const el = $("panel-brief027");
  if (!el || !b) return;
  const lc = b.live_check || {};
  const sc = b.scorecard || {};
  const laws = (b.laws || []).map((l) =>
    `<li><strong>${escapeHtml(l.id)}</strong> — ${escapeHtml(l.text)}</li>`
  ).join("");
  const seats = (b.council_seats || lc.council_seats || []).map(escapeHtml).join(" · ");
  const stages = (b.desk_stages || lc.desk_stages || []).map(escapeHtml).join(" → ");
  const denied = (b.denied_tools || []).slice(0, 10).map((t) =>
    `<li><code>${escapeHtml(t)}</code></li>`
  ).join("");
  const kpis = [
    ["auto_apply_council", sc.auto_apply_council ?? lc.auto_apply_council],
    ["auto_send", sc.auto_send ?? lc.auto_send],
    ["rubber_stamp", sc.rubber_stamp ?? lc.rubber_stamp],
    ["fake_live_council", sc.fake_live_council ?? lc.fake_live_council],
    ["truncated_digest_applies", sc.truncated_digest_applies ?? lc.truncated_digest_applies],
    ["hold_timeout_failopen", sc.hold_timeout_failopen ?? lc.hold_timeout_failopen],
    ["self_approve", sc.self_approve ?? lc.self_approve],
    ["minority_drop", sc.minority_drop ?? lc.minority_drop],
    ["tool_during_deliberation", sc.tool_during_deliberation ?? lc.tool_during_deliberation],
    ["kpd_bleed", sc.kpd_bleed ?? lc.kpd_bleed],
  ].map(([k, v]) => `<div class="kpi"><span>${escapeHtml(k)}</span><b>${escapeHtml(v)}</b></div>`).join("");
  el.innerHTML = `
    <div class="panel-head">
      <h2>Brief-027 law · Grok Council</h2>
      <span class="badge-law">auto_apply_council=0</span>
      <span class="badge-law">auto_send=0</span>
    </div>
    <div class="law-banner">
      Portable Grok Council law folded alongside brief-007 / brief-024.
      Seats: <code>${seats || "Michael · Pam · Oscar · Jim · Kelly · TokenMax"}</code>.
      Many bots may advise; none may Apply; majority is evidence, not authority.
      Council Hold until human Apply. America/New_York.
    </div>
    <p class="hint">Desk: ${stages || "digest → seats → refute → recommend → Hold → human Apply"}</p>
    <ul class="law-list">${laws}</ul>
    <h3 style="margin:.5rem 0 .3rem;font-size:.86rem;color:var(--accent)">Scorecard zeros</h3>
    <div class="kpi-grid">${kpis}</div>
    <h3 style="margin:.5rem 0 .3rem;font-size:.86rem;color:var(--accent)">Denied auto-apply / auto-send tools</h3>
    <ul class="law-list">${denied}</ul>
    <p class="hint">POST /api/auto-apply · /api/auto-apply-council · /api/council-force-send → 403</p>
    <p class="hint" id="brief027-live">
      <strong>live_check</strong> · auto_apply_council=<code>${escapeHtml(lc.auto_apply_council)}</code>
      · auto_send=<code>${escapeHtml(lc.auto_send)}</code>
      · auto_apply_apis=<code>${escapeHtml(lc.auto_apply_apis_succeed)}</code>
      · auto_apply_council_apis=<code>${escapeHtml(lc.auto_apply_council_apis_succeed)}</code>
      · force_send_apis=<code>${escapeHtml(lc.council_force_send_apis_succeed)}</code>
      · policy=<code>${escapeHtml(lc.mutation_endpoints_policy)}</code>
      · paired_008=<code>${escapeHtml(lc.paired_with_brief008)}</code>
      · paired_017=<code>${escapeHtml(lc.paired_with_brief017)}</code>
      · hold_until_human=<code>${escapeHtml(lc.council_hold_until_human_apply)}</code>
      · ${escapeHtml(lc.served_at_et || "")}
    </p>`;
}

(async () => {
  try {
    await loadSeeds();
    try {
      const b24 = await jget("/api/brief024");
      renderBrief024(b24);
    } catch (e) {
      const el = $("panel-brief024");
      if (el) el.innerHTML = `<h2>Brief-024 law · /correct CI</h2><p class="hint">live_check unavailable: ${escapeHtml(e.message || e)}</p>`;
    }
    try {
      const b27 = await jget("/api/brief027");
      renderBrief027(b27);
    } catch (e) {
      const el = $("panel-brief027");
      if (el) el.innerHTML = `<h2>Brief-027 law · Grok Council</h2><p class="hint">live_check unavailable: ${escapeHtml(e.message || e)}</p>`;
    }
    const health = await jget("/api/health");
    $("stats").textContent = `port ${health.port} · ${health.personas} personas`;
    // Auto-show latest bonsai review if present
    const rev = await fetch("/api/reviews/review-bonsai-reveal.json");
    if (rev.ok) {
      const bundle = await rev.json();
      const mdR = await fetch("/api/reviews/review-bonsai-reveal.md");
      const markdown = mdR.ok ? await mdR.text() : "";
      renderBundle({
        bundle,
        markdown,
        saved: {
          json: "out/review-bonsai-reveal.json",
          md: "out/review-bonsai-reveal.md",
          verdict: bundle.chair.verdict,
          finding_count: bundle.review.finding_count,
        },
      });
      $("title").value = bundle.review.title;
      const raw = await fetch("/api/seeds/bonsai-reveal/raw");
      if (raw.ok) $("draft").value = await raw.text();
    }
  } catch (e) {
    console.error(e);
    toast(String(e.message || e));
  }
})();

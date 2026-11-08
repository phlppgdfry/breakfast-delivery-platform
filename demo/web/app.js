import { inspect } from "/feature.js";

const $ = (id) => document.getElementById(id);
const node = (tag, text, cls) => {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = String(text);
  if (cls) el.className = cls;
  return el;
};
let snapshot;
let selected;
let busy = false;

function notice(message, error = false) {
  $("notice").textContent = message;
  $("notice").setAttribute("role", error ? "alert" : "status");
}

async function request(url, options) {
  const response = await fetch(url, options);
  const result = await response.json();
  if (!response.ok) {
    const error = new Error(result.error || "Request failed");
    error.status = response.status;
    throw error;
  }
  return result;
}

function drawAnalysis() {
  const a = snapshot.analysis;
  const feature = node("div", undefined, "feature");
  feature.append(
    node("h2", a.title),
    node("div", a.headline, "large"),
    node("p", a.description),
  );
  const bars = node("div", undefined, "bars");
  bars.append(node("h2", a.bars_title));
  for (const item of a.bars) {
    const row = node("div", undefined, "bar-row");
    const progress = node("progress");
    progress.max = 100;
    progress.value = item.value;
    progress.setAttribute("aria-label", `${item.label}: ${item.display}`);
    row.append(
      node("span", item.label),
      progress,
      node("strong", item.display),
    );
    bars.append(row);
  }
  if (a.cohorts) {
    const table = node("table", undefined, "cohorts");
    const caption = node(
      "caption",
      "Mature accounts only; N/A = insufficient follow-up",
    );
    table.append(caption);
    const head = node("thead");
    const tr = node("tr");
    ["Cohort", "Eligible", "Churned"].forEach((label) => {
      const th = node("th", label);
      th.scope = "col";
      tr.append(th);
    });
    head.append(tr);
    table.append(head);
    const body = node("tbody");
    for (const c of a.cohorts) {
      const row = node("tr");
      [c.month, c.eligible, c.churned].forEach((v) =>
        row.append(node("td", v)),
      );
      body.append(row);
    }
    table.append(body);
    bars.append(table);
  }
  $("analysis").replaceChildren(feature, bars);
}

function drawList() {
  const query = $("search").value.toLowerCase();
  const status = $("filter").value;
  const filtered = snapshot.records.filter(
    (r) =>
      (!status || status === r.status) &&
      [r.name, r.id, r.context].join(" ").toLowerCase().includes(query),
  );
  const rows = filtered.map((r) => {
    const row = node("tr");
    if (r.id === selected) row.className = "selected";
    snapshot.config.columns.forEach(([key], index) => {
      const cell = node("td");
      if (index === 0) {
        const button = node("button", r[key], "row-button");
        button.type = "button";
        button.setAttribute("aria-pressed", String(r.id === selected));
        button.addEventListener("click", () => {
          selected = r.id;
          drawList();
          drawDetail();
        });
        cell.append(button);
      } else if (key === "status") cell.append(node("span", r[key], "status"));
      else cell.textContent = r[key];
      row.append(cell);
    });
    return row;
  });
  if (!rows.length) {
    const row = node("tr");
    const cell = node(
      "td",
      "No matching records. Clear the search or change the status filter.",
      "empty",
    );
    cell.colSpan = snapshot.config.columns.length;
    row.append(cell);
    rows.push(row);
  }
  $("rows").replaceChildren(...rows);
  $("count").textContent =
    `${filtered.length} of ${snapshot.records.length} records · Select a name to inspect`;
}

function makeForm(spec, record) {
  const form = node("form");
  form.append(node("h2", spec.title));
  if (spec.help) form.append(node("p", spec.help, "help"));
  const controls = [];
  for (const field of spec.fields || []) {
    const label = node("label", field.label);
    let input;
    if (field.options) {
      input = node("select");
      field.options.forEach((option) => {
        const value = typeof option === "string" ? option : option.value;
        const text = typeof option === "string" ? option : option.label;
        const el = node("option", text);
        el.value = value;
        input.append(el);
      });
    } else if (field.type === "textarea") input = node("textarea");
    else {
      input = node("input");
      input.type = field.type || "text";
    }
    input.setAttribute("aria-label", field.label);
    input.name = field.key;
    input.required = field.required !== false;
    if (field.min !== undefined) input.min = field.min;
    if (field.max !== undefined) input.max = field.max;
    if (field.maxLength) input.maxLength = field.maxLength;
    if (field.step !== undefined) input.step = field.step;
    if (field.value !== undefined) input.value = field.value;
    label.append(input);
    form.append(label);
    controls.push([field, input]);
  }
  const submit = node("button", spec.button, "primary");
  submit.type = "submit";
  submit.disabled = busy;
  form.append(submit);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy) return;
    const payload = { action: spec.action };
    if (spec.action !== "create") {
      payload.id = record.id;
      payload.version = record.version;
    }
    controls.forEach(([field, input]) => {
      payload[field.key] =
        field.type === "checkbox"
          ? input.checked
          : field.type === "number"
            ? Number(input.value)
            : input.value;
    });
    busy = true;
    document
      .querySelectorAll("form button")
      .forEach((b) => (b.disabled = true));
    try {
      snapshot = await request("/api/action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (spec.action === "create") selected = snapshot.events[0].entity;
      busy = false;
      render();
      notice(
        spec.success || "Saved. The workspace and activity log are up to date.",
      );
    } catch (error) {
      busy = false;
      if (error.status === 409) {
        snapshot = await request("/api/snapshot");
        render();
      }
      document
        .querySelectorAll("form button")
        .forEach((b) => (b.disabled = false));
      notice(error.message, true);
    }
  });
  return form;
}

function drawDetail() {
  const record = snapshot.records.find((r) => r.id === selected);
  const detail = $("detail");
  detail.replaceChildren();
  if (!record) {
    detail.append(node("p", "Select a record to get started."));
    return;
  }
  const spec = inspect(record, snapshot);
  detail.append(
    node("h2", record.name),
    node("p", `${record.status} · version ${record.version}`, "reference"),
  );
  const dl = node("dl");
  for (const [label, value] of spec.fields || [])
    dl.append(node("dt", label), node("dd", value));
  detail.append(dl);
  for (const form of spec.forms || []) detail.append(makeForm(form, record));
  if (spec.note) detail.append(node("p", spec.note, "help"));
}

function render() {
  const c = snapshot.config;
  document.title = c.title;
  document.body.dataset.theme = c.theme;
  $("brand-name").textContent = c.title;
  $("section-label").textContent = c.section;
  $("title").textContent = c.heading;
  $("subtitle").textContent = c.subtitle;
  $("clock").textContent = c.clock;
  $("list-title").textContent = c.list_title;
  $("footer-title").textContent = c.title;
  $("metrics").replaceChildren(
    ...snapshot.metrics.map((m) => {
      const box = node("div", undefined, "metric");
      box.append(
        node("p", m.label),
        node("strong", m.value),
        node("small", m.note),
      );
      return box;
    }),
  );
  const row = node("tr");
  c.columns.forEach(([, label]) => {
    const th = node("th", label);
    th.scope = "col";
    row.append(th);
  });
  $("head").replaceChildren(row);
  const previous = $("filter").value;
  const all = node("option", "All statuses");
  all.value = "";
  $("filter").replaceChildren(
    all,
    ...[...new Set(snapshot.records.map((r) => r.status))].sort().map((s) => {
      const o = node("option", s);
      o.value = s;
      return o;
    }),
  );
  if ([...$("filter").options].some((o) => o.value === previous))
    $("filter").value = previous;
  if (!snapshot.records.some((r) => r.id === selected))
    selected = snapshot.records[0]?.id;
  drawAnalysis();
  drawList();
  drawDetail();
  $("events").replaceChildren(
    ...(snapshot.events.length
      ? snapshot.events.map((e) =>
          node(
            "li",
            `${e.at.replace(/\.\d+/, "")} · ${e.entity} · ${e.action.replaceAll("_", " ")} · version ${e.version}`,
          ),
        )
      : [
          node(
            "li",
            "No changes yet. Inspect a record and complete an action.",
          ),
        ]),
  );
}
$("search").addEventListener("input", drawList);
$("filter").addEventListener("change", drawList);
try {
  snapshot = await request("/api/snapshot");
  render();
} catch (error) {
  notice(
    `Could not load the workspace: ${error.message}. Reload after starting the local server.`,
    true,
  );
}

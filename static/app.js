/* ─────────────────────────────────────────────────────────────
   Streamlined 5-Agent Application Logic
   Input -> 5 LLM Agent Pipeline (with automated RAG) -> SRS & SDLC Output
   Shows real-time visual processing of each model during execution.
   ───────────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Mermaid with warm brown theme
  mermaid.initialize({
    startOnLoad: false,
    theme: "base",
    themeVariables: {
      background: "#FCFBF9",
      primaryColor: "#EFE8DD",
      primaryTextColor: "#241E19",
      primaryBorderColor: "#70472D",
      lineColor: "#70472D",
      secondaryColor: "#F3EFE6",
      tertiaryColor: "#FAF8F5",
      mainBkg: "#F7F4EE",
      nodeBorder: "#70472D",
      textColor: "#241E19",
      fontFamily: "Plus Jakarta Sans, -apple-system, sans-serif"
    }
  });

  initApp();
});

let currentScenarios = {};
let latestResults = null;

async function initApp() {
  setupSubTabs();
  setupExampleChips();
  setupPipelineRunner();
  setupUmlFilters();

  await fetchStatus();
  await fetchScenarios();
}

/* ── 1. Status & Scenarios ── */
async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    const badge = document.getElementById("engineBadge");
    const text = document.getElementById("engineText");

    if (data.has_gemini_key) {
      badge.className = "status-badge success";
      text.textContent = `Online: ${data.model_name}`;
    } else {
      badge.className = "status-badge";
      text.textContent = `Local Engine: ${data.model_name}`;
    }
  } catch (e) {
    console.error("Status fetch error", e);
  }
}

async function fetchScenarios() {
  try {
    const res = await fetch("/api/scenarios");
    currentScenarios = await res.json();
  } catch (e) {
    console.error("Scenarios fetch error", e);
  }
}

function setupExampleChips() {
  const chips = document.querySelectorAll(".example-chip");
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");

      const key = chip.getAttribute("data-key");
      if (currentScenarios[key]) {
        document.getElementById("projectTitle").value = currentScenarios[key].title;
        document.getElementById("projectDesc").value = currentScenarios[key].description;
      }
    });
  });
}

/* ── 2. Output Tab Switching ── */
function setupSubTabs() {
  const subTabs = document.querySelectorAll(".sub-tabs .sub-tab-btn");
  subTabs.forEach(btn => {
    btn.addEventListener("click", () => {
      subTabs.forEach(t => t.classList.remove("active"));
      btn.classList.add("active");

      const targetView = btn.getAttribute("data-view");
      document.querySelectorAll(".view-panel").forEach(p => (p.style.display = "none"));
      const activePanel = document.getElementById(targetView);
      if (activePanel) {
        activePanel.style.display = "block";
        if (targetView === "view-uml") {
          renderUmlDiagrams();
        }
      }
    });
  });
}

/* ── 3. Run Pipeline with Dynamic Visual Model Feedback ── */
function setupPipelineRunner() {
  const btn = document.getElementById("btnRunPipeline");
  const statusNote = document.getElementById("pipelineStatusText");
  const activityBanner = document.getElementById("activityBanner");
  const agentLabel = document.getElementById("activityAgentLabel");
  const detailLabel = document.getElementById("activityDetailLabel");

  btn.addEventListener("click", async () => {
    const title = document.getElementById("projectTitle").value.trim();
    const desc = document.getElementById("projectDesc").value.trim();

    if (!desc) {
      alert("Please provide requirements or a project description.");
      return;
    }

    btn.disabled = true;
    btn.textContent = "Processing with 5 LLM Agents...";
    statusNote.textContent = "Autonomous multi-model synthesis in progress...";

    // Show live activity banner
    activityBanner.style.display = "flex";

    resetStepper();

    const stages = [
      {
        step: 1,
        agent: "Agent 1: Requirements Analyst is processing...",
        detail: "Formulating functional and non-functional requirements in plain English..."
      },
      {
        step: 2,
        agent: "Agent 2: Compliance Specialist is processing...",
        detail: "Retrieving statutory standards from RAG and checking security & privacy rules..."
      },
      {
        step: 3,
        agent: "Agent 3: System Architect is processing...",
        detail: "Synthesizing UML Use Case, Class, Sequence and State & Activity diagrams..."
      },
      {
        step: 4,
        agent: "Agent 4: SDLC Strategist is processing...",
        detail: "Evaluating which SDLC model is best among Waterfall, V, Agile/Scrum, RAD, Spiral & Incremental..."
      },
      {
        step: 5,
        agent: "Agent 5: Documentation Lead is processing...",
        detail: "Compiling official IEEE 830 document and generating downloadable PDF..."
      }
    ];

    activateStep(stages[0].step, stages[0].agent, stages[0].detail);

    const t1 = setTimeout(() => activateStep(stages[1].step, stages[1].agent, stages[1].detail), 700);
    const t2 = setTimeout(() => activateStep(stages[2].step, stages[2].agent, stages[2].detail), 1400);
    const t3 = setTimeout(() => activateStep(stages[3].step, stages[3].agent, stages[3].detail), 2100);
    const t4 = setTimeout(() => activateStep(stages[4].step, stages[4].agent, stages[4].detail), 2800);

    try {
      const response = await fetch("/api/pipeline/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description: desc }),
      });

      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Pipeline failed");
      }

      latestResults = await response.json();
      completeAllSteps();

      activityBanner.style.display = "none";
      renderOutputs(latestResults);
      statusNote.textContent = "All 5 agents finished. Official SRS document & diagrams ready below.";

    } catch (err) {
      console.error(err);
      activityBanner.style.display = "none";
      statusNote.textContent = `Error: ${err.message}`;
      alert(`Pipeline error: ${err.message}`);
    } finally {
      btn.disabled = false;
      btn.textContent = "Generate SRS & SDLC Report";
    }
  });
}

function resetStepper() {
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`step${i}`);
    el.className = "step-card";
    el.querySelector(".step-status").textContent = "Ready";
  }
}

function activateStep(stepNum, agentTitle, detailText) {
  const agentLabel = document.getElementById("activityAgentLabel");
  const detailLabel = document.getElementById("activityDetailLabel");

  if (agentLabel) agentLabel.textContent = agentTitle;
  if (detailLabel) detailLabel.textContent = detailText;

  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`step${i}`);
    if (i < stepNum) {
      el.className = "step-card completed";
      el.querySelector(".step-status").textContent = "Done";
    } else if (i === stepNum) {
      el.className = "step-card active";
      el.querySelector(".step-status").textContent = "Processing...";
    } else {
      el.className = "step-card";
      el.querySelector(".step-status").textContent = "Waiting";
    }
  }
}

function completeAllSteps() {
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`step${i}`);
    el.className = "step-card completed";
    el.querySelector(".step-status").textContent = "Completed";
  }
}

/* ── 4. Render Outputs ── */
function renderOutputs(results) {
  const stages = results.stages;

  document.getElementById("srsContent").innerHTML = marked.parse(stages.requirements || "");
  document.getElementById("sdlcContent").innerHTML = marked.parse(stages.sdlc || "");

  document.getElementById("btnDownloadPdf").href = results.pdf_url;
  document.getElementById("btnDownloadMd").href = results.markdown_url;

  renderUmlDiagrams();
}

/* ── 5. UML Diagram Filter Controls (Separating Sequence & Activity) ── */
let currentUmlFilter = "all";

function setupUmlFilters() {
  const filterBtns = document.querySelectorAll(".uml-filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentUmlFilter = btn.getAttribute("data-filter") || "all";
      applyUmlFilter(currentUmlFilter);
    });
  });
}

function applyUmlFilter(filterKey) {
  const blocks = document.querySelectorAll(".uml-block");
  blocks.forEach(block => {
    const kind = block.getAttribute("data-kind");
    if (filterKey === "all" || kind === filterKey) {
      block.style.display = "block";
    } else {
      block.style.display = "none";
    }
  });
}

async function renderUmlDiagrams() {
  if (!latestResults || !latestResults.stages.uml_diagrams) return;

  const container = document.getElementById("umlContainer");
  const rawText = latestResults.stages.uml_diagrams;

  const mermaidRegex = /```mermaid([\s\S]*?)```/g;
  let matches = [];
  let match;
  while ((match = mermaidRegex.exec(rawText)) !== null) {
    matches.push(match[1].trim());
  }

  if (matches.length === 0) {
    container.innerHTML = marked.parse(rawText);
    return;
  }

  const diagramMeta = [
    { title: "1. Use Case Diagram", kind: "usecase", badge: "Interaction Model" },
    { title: "2. Domain Class Diagram", kind: "class", badge: "Structural Model" },
    { title: "3. Transaction Sequence Diagram", kind: "sequence", badge: "Behavioral Flow" },
    { title: "4. Activity Diagram", kind: "activity", badge: "Process Decision Flow" },
    { title: "5. State Machine Diagram", kind: "state", badge: "Entity Lifecycle" },
  ];

  let html = `<div style="display:flex; flex-direction:column; gap:20px;">`;
  matches.forEach((code, idx) => {
    const meta = diagramMeta[idx] || {
      title: `Diagram ${idx + 1}`,
      kind: "other",
      badge: "Architecture"
    };

    html += `
      <div class="uml-block" data-kind="${meta.kind}">
        <div class="uml-block-header">
          <span>${meta.title}</span>
          <span class="uml-block-badge">${meta.badge}</span>
        </div>
        <div class="mermaid-viewer">
          <div class="mermaid" id="diagram_${idx}">${code}</div>
        </div>
      </div>
    `;
  });
  html += `</div>`;

  container.innerHTML = html;

  // Apply current filter selection
  applyUmlFilter(currentUmlFilter);

  try {
    await mermaid.run({
      nodes: container.querySelectorAll(".mermaid")
    });
  } catch (err) {
    console.warn("Mermaid notice:", err);
  }
}

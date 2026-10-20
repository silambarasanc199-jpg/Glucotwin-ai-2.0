const $ = (selector) => document.querySelector(selector);
const API_BASE_URL = String(window.GLUCO_TWIN_CONFIG?.apiBaseUrl || "").replace(/\/+$/, "");
const state = { patients: [], selectedId: "", readings: [], chart: null, summary: null, latestPrediction: null };

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}
function showNotice(message, error = false) {
  const node = $("#notice");
  node.textContent = message;
  node.classList.toggle("error", error);
  node.hidden = false;
  window.clearTimeout(showNotice.timer);
  showNotice.timer = window.setTimeout(() => { node.hidden = true; }, 6500);
}
async function api(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, { headers: { "Content-Type": "application/json", ...(options.headers || {}) }, ...options });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status}).`);
  return body;
}
function formatTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}
function setApiStatus(online) {
  const node = $("#api-status");
  node.textContent = online ? "Connected" : "Unavailable";
  node.parentElement.classList.toggle("online", online);
}
function renderSummary(summary) {
  state.summary = summary;
  $("#count-patients").textContent = summary.counts.patients;
  $("#count-readings").textContent = summary.counts.readings;
  $("#count-predictions").textContent = summary.counts.predictions;
  $("#model-state").textContent = summary.model.trained ? "Trained" : "Not trained";
  $("#model-state").classList.toggle("ready", summary.model.trained);
  $("#model-name").textContent = summary.model.selected_model || (summary.model.trained ? "Trained model" : "No model artifact");
  $("#model-foot").textContent = summary.model.synthetic_only ? "Evaluation uses synthetic data only" : summary.model.trained ? "Model file detected by backend" : "Train the model before requesting predictions";
  renderEvaluation(summary.model);
}
function renderEvaluation(model) {
  const container = $("#evaluation-metrics");
  const badge = $("#evaluation-badge");
  const metrics = model.test_metrics;
  if (!model.evaluation_available || !metrics) {
    badge.textContent = "Not available";
    container.innerHTML = '<div class="panel-empty">Evaluation results are loaded from the backend after training.</div>';
    return;
  }
  badge.textContent = model.synthetic_only ? "Synthetic test set" : "Held-out test set";
  const values = [["Precision", metrics.precision], ["Recall", metrics.recall], ["F1 score", metrics.f1], ["PR-AUC", metrics.pr_auc], ["ROC-AUC", metrics.roc_auc], ["Test samples", metrics.sample_count]];
  container.innerHTML = values.map(([label, value]) => `<div class="metric"><span>${esc(label)}</span><b>${typeof value === "number" && label !== "Test samples" ? value.toFixed(3) : (value ?? "N/A")}</b></div>`).join("");
  $("#evaluation-note").textContent = "Patient-held-out test metrics at the default 0.5 threshold; this synthetic experiment does not establish real-world or clinical performance.";
}
function renderPatients() {
  const select = $("#patient-select");
  if (!state.patients.length) {
    select.innerHTML = '<option value="">No profiles available</option>';
    state.selectedId = "";
    $("#predict-button").disabled = true;
    $("#add-reading-button").disabled = true;
    clearPatientView();
    return;
  }
  const wanted = state.selectedId || state.patients[0].patient_id;
  state.selectedId = state.patients.some((item) => item.patient_id === wanted) ? wanted : state.patients[0].patient_id;
  select.innerHTML = state.patients.map((patient) => `<option value="${esc(patient.patient_id)}">${esc(patient.patient_id)}${patient.is_synthetic ? " · synthetic" : ""}</option>`).join("");
  select.value = state.selectedId;
  $("#predict-button").disabled = !state.summary?.model.trained;
  $("#add-reading-button").disabled = false;
}
function clearPatientView() {
  state.readings = [];
  state.latestPrediction = null;
  $("#profile-fields").innerHTML = '<div class="panel-empty">Create or select a profile to inspect available context.</div>';
  $("#profile-badge").textContent = "No profile";
  $("#reading-table").innerHTML = '<tr><td colspan="6" class="table-empty">No patient profile is selected.</td></tr>';
  $("#freshness-badge").textContent = "No readings";
  $("#reading-range").textContent = "Choose a profile to inspect stored observations.";
  $("#score-value").textContent = "—";
  $("#score-ring-value").textContent = "—";
  $("#input-time").textContent = "—";
  $("#explanation-content").innerHTML = "<p>Run a prediction to view the latest observed signals and data-quality notes.</p>";
  $("#feature-ranking").innerHTML = "<p>Available after training and a prediction.</p>";
  if (state.chart) { state.chart.destroy(); state.chart = null; }
  $("#glucose-chart").hidden = true;
  $("#chart-empty").hidden = false;
}
async function loadPatient(patientId) {
  if (!patientId) return clearPatientView();
  state.selectedId = patientId;
  state.latestPrediction = null;
  $("#score-value").textContent = "—";
  $("#score-ring-value").textContent = "—";
  $("#score-label").textContent = "Run a prediction to see the model output.";
  $("#prediction-warnings").hidden = true;
  try {
    const [twin, readingsResult, historyResult] = await Promise.all([
      api(`/api/patients/${encodeURIComponent(patientId)}`),
      api(`/api/patients/${encodeURIComponent(patientId)}/readings?limit=500`),
      api(`/api/patients/${encodeURIComponent(patientId)}/predictions?limit=1`),
    ]);
    state.readings = readingsResult.readings;
    renderProfile(twin);
    renderReadings(state.readings);
    if (historyResult.predictions.length) renderPrediction(historyResult.predictions[0]);
  } catch (error) { showNotice(error.message, true); }
}
function renderProfile(twin) {
  const patient = twin.patient;
  $("#profile-badge").textContent = patient.is_synthetic || twin.contains_synthetic_data ? "Synthetic data" : "Anonymous profile";
  $("#profile-fields").innerHTML = [
    ["AGE", patient.age == null ? "Not provided" : `${patient.age} years`],
    ["BMI", patient.bmi == null ? "Not provided" : patient.bmi],
    ["DIABETES DURATION", patient.diabetes_duration_years == null ? "Not provided" : `${patient.diabetes_duration_years} years`],
    ["HBA1C", patient.hba1c == null ? "Not provided" : `${patient.hba1c}%`],
  ].map(([label, value]) => `<div class="field-value"><span>${esc(label)}</span><b>${esc(value)}</b></div>`).join("");
  $("#profile-foot").textContent = `${twin.reading_count} stored observation(s) · Sources: ${twin.data_sources.length ? twin.data_sources.map(esc).join(", ") : "none"} · Latest: ${formatTime(twin.latest_reading_at)}`;
}
function renderReadings(readings) {
  const hasRows = readings.length > 0;
  $("#synthetic-tag").hidden = !readings.some((item) => item.is_synthetic);
  const range = hasRows ? `${formatTime(readings[0].timestamp)} — ${formatTime(readings.at(-1).timestamp)} · Showing ${Math.min(readings.length, 96)} most recent` : "No stored observations for this profile.";
  $("#reading-range").textContent = range;
  const latest = hasRows ? readings.at(-1) : null;
  const ageHours = latest ? (Date.now() - new Date(latest.timestamp).getTime()) / 3600000 : null;
  const freshness = $("#freshness-badge");
  freshness.classList.toggle("stale", ageHours !== null && ageHours > 2);
  freshness.textContent = !latest ? "No readings" : ageHours > 2 ? `Stale · ${ageHours.toFixed(1)}h ago` : ageHours < -0.1 ? "Future timestamp" : `Fresh · ${formatTime(latest.timestamp)}`;
  const displayRows = readings.slice(-12).reverse();
  $("#reading-table").innerHTML = displayRows.length ? displayRows.map((item) => `<tr><td>${esc(formatTime(item.timestamp))}</td><td>${esc(item.glucose_mg_dl)} mg/dL</td><td>${item.heart_rate_bpm == null ? "—" : `${esc(item.heart_rate_bpm)} bpm`}</td><td>${item.sleep_hours == null ? "—" : `${esc(item.sleep_hours)} h`}</td><td>${item.steps == null ? "—" : esc(item.steps)}</td><td>${esc(item.is_synthetic ? "Synthetic" : item.source)}</td></tr>`).join("") : '<tr><td colspan="6" class="table-empty">No readings stored. Add an observation or initialize demo data from the command line.</td></tr>';
  renderChart(readings.slice(-96));
}
function renderChart(readings) {
  if (state.chart) { state.chart.destroy(); state.chart = null; }
  const canvas = $("#glucose-chart");
  const empty = $("#chart-empty");
  if (!readings.length || !window.Chart) {
    canvas.hidden = true;
    empty.textContent = readings.length ? "Chart library unavailable; readings remain available in the timeline." : "No glucose readings are stored for this profile yet.";
    empty.hidden = false;
    return;
  }
  canvas.hidden = false;
  empty.hidden = true;
  const context = canvas.getContext("2d");
  state.chart = new Chart(context, {
    type: "line",
    data: { labels: readings.map((item) => item.timestamp),
      datasets: [{ label: "Measured glucose", data: readings.map((item) => item.glucose_mg_dl), borderColor: "#2877c7", backgroundColor: "rgba(40,119,199,.08)", pointRadius: readings.length > 48 ? 0 : 2, pointHoverRadius: 4, borderWidth: 2, fill: true, tension: .25 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: "index" },
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: (item) => ` ${item.parsed.y} mg/dL (measured)` } } },
      scales: {
        x: {
          ticks: {
            callback: (value) => {
              const date = new Date(readings[Number(value)]?.timestamp);
              if (Number.isNaN(date.getTime())) return "";
              return window.innerWidth < 520
                ? date.toLocaleTimeString([], { hour: "numeric" })
                : date.toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
            },
            color: "#95a3af", maxTicksLimit: 6, maxRotation: 0, font: { size: 8 },
          },
          grid: { display: false }, border: { display: false },
        },
        y: {
          ticks: { color: "#95a3af", font: { size: 8 } }, grid: { color: "#eff3f6" },
          border: { display: false },
          title: { display: true, text: "mg/dL", color: "#95a3af", font: { size: 8 } },
        },
      },
    }
  });
}
function renderPrediction(prediction) {
  state.latestPrediction = prediction;
  const score = prediction.raw_model_score;
  const percent = score * 100;
  const displayScore = `${percent.toFixed(1)}%`;
  $("#score-value").textContent = displayScore;
  $("#score-ring-value").textContent = displayScore;
  $("#score-ring").style.background = `conic-gradient(${percent > 65 ? "#d28b42" : "#16a58c"} ${percent * 3.6}deg, #e5edf2 0deg)`;
  $("#score-label").textContent = prediction.score_interpretation;
  $("#forecast-horizon").textContent = `${prediction.forecast_horizon_minutes} minutes`;
  $("#input-time").textContent = formatTime(prediction.latest_input_timestamp);
  $("#score-disclaimer").textContent = `${prediction.uncertainty_note} ${prediction.disclaimer}`;
  $("#explanation-content").innerHTML = `<p>${esc(prediction.explanation)}</p>${prediction.key_observed_signals.map((item) => `<p>• ${esc(item)}</p>`).join("")}`;
  const features = prediction.global_model_features || [];
  $("#feature-ranking").innerHTML = features.length ? `<div class="feature-list">${features.map((item) => `<span class="feature-chip">${esc(item.feature.replaceAll("_", " "))} · ${Number(item.importance).toFixed(3)}</span>`).join("")}</div>` : "<p>Not available for this model.</p>";
  const warnings = prediction.data_quality_warnings || [];
  const warningBox = $("#prediction-warnings");
  warningBox.innerHTML = warnings.length ? `<ul>${warnings.map((warning) => `<li>${esc(warning)}</li>`).join("")}</ul>` : "";
  warningBox.hidden = !warnings.length;
}
async function refresh() {
  $("#error-state").hidden = true;
  try {
    const [health, summary, patients] = await Promise.all([api("/health"), api("/api/dashboard/summary"), api("/api/patients")]);
    setApiStatus(health.status === "ok");
    renderSummary(summary);
    state.patients = patients;
    renderPatients();
    if (state.selectedId) await loadPatient(state.selectedId);
  } catch (error) {
    setApiStatus(false);
    $("#error-state").textContent = `The backend could not be reached: ${error.message} Use the startup instructions in the project README, then refresh.`;
    $("#error-state").hidden = false;
  }
}
$("#patient-select").addEventListener("change", (event) => loadPatient(event.target.value));
$("#refresh-button").addEventListener("click", refresh);
$("#new-patient-button").addEventListener("click", () => $("#patient-dialog").showModal());
$("#close-dialog").addEventListener("click", () => $("#patient-dialog").close());
$("#cancel-dialog").addEventListener("click", () => $("#patient-dialog").close());
$("#patient-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = {};
  for (const key of ["age", "bmi", "diabetes_duration_years", "hba1c"]) {
    const value = form.get(key);
    payload[key] = value === "" ? null : Number(value);
  }
  payload.is_synthetic = form.has("is_synthetic");
  try {
    const created = await api("/api/patients", { method: "POST", body: JSON.stringify(payload) });
    $("#patient-dialog").close();
    event.currentTarget.reset();
    state.selectedId = created.patient_id;
    showNotice(`Anonymous profile ${created.patient_id} created.`);
    await refresh();
  } catch (error) { showNotice(error.message, true); }
});
$("#reading-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.selectedId) return;
  const timestamp = $("#reading-time").value;
  const payload = {
    timestamp: new Date(timestamp).toISOString(),
    glucose_mg_dl: Number($("#reading-glucose").value),
    heart_rate_bpm: $("#reading-heart").value ? Number($("#reading-heart").value) : null,
    sleep_hours: $("#reading-sleep").value ? Number($("#reading-sleep").value) : null,
    steps: $("#reading-steps").value ? Number($("#reading-steps").value) : null,
    source: "manual",
    is_synthetic: $("#reading-synthetic").checked,
  };
  try {
    await api(`/api/patients/${encodeURIComponent(state.selectedId)}/readings`, { method: "POST", body: JSON.stringify(payload) });
    event.currentTarget.reset();
    setDefaultReadingTime();
    await refresh();
    showNotice("Observation stored successfully.");
  } catch (error) { showNotice(error.message, true); }
});
$("#predict-button").addEventListener("click", async (event) => {
  if (!state.selectedId) return;
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Running prediction…";
  try {
    const prediction = await api(`/api/patients/${encodeURIComponent(state.selectedId)}/predict`, { method: "POST", body: "{}" });
    renderPrediction(prediction);
    await refreshSummaryOnly();
    showNotice("Experimental model output recorded. Do not use it for care decisions.");
  } catch (error) { showNotice(error.message, true); }
  finally { event.currentTarget.innerHTML = 'Run experimental prediction <span>→</span>'; event.currentTarget.disabled = !state.summary?.model.trained; }
});
async function refreshSummaryOnly() {
  const summary = await api("/api/dashboard/summary");
  renderSummary(summary);
}
function setDefaultReadingTime() {
  const now = new Date();
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
  $("#reading-time").value = now.toISOString().slice(0, 16);
}
setDefaultReadingTime();
refresh();

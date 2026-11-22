import re

path = "frontend/cat_dashboard.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("\r\n", "\n")

# 1. Add profiles to globalData
old_global = """        let globalData = {
            sprintInfo: {
                week: "", dates: "", name: "", sprintNum: ""
            },
            sprints: [],
            metrics: [], // array of objects { engagement, spoc, ...cols }
            details: [],
            ragConfig: {}
        };"""

new_global = """        let globalData = {
            sprintInfo: {
                week: "", dates: "", name: "", sprintNum: ""
            },
            sprints: [],
            metrics: [], // array of objects { engagement, spoc, ...cols }
            details: [],
            ragConfig: {},
            profiles: []
        };"""

if old_global in content:
    content = content.replace(old_global, new_global, 1)

# 2. Update fetchDataFromAPI to fetch /profiles
old_fetch_cache = """                    globalData.metrics = parsed.metrics;
                    globalData.details = parsed.details;
                    globalData.ragConfig = parsed.ragConfig;
                    globalData.sprints = parsed.sprints || [];"""

new_fetch_cache = """                    globalData.metrics = parsed.metrics;
                    globalData.details = parsed.details;
                    globalData.ragConfig = parsed.ragConfig;
                    globalData.sprints = parsed.sprints || [];
                    globalData.profiles = parsed.profiles || [];"""

if old_fetch_cache in content:
    content = content.replace(old_fetch_cache, new_fetch_cache, 1)

old_fetch_call = """                const [metricsRes, detailsRes, configsRes, sprintsRes] = await Promise.all([
                    fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/sprints', { headers: { 'Authorization': 'Bearer ' + token } })
                ]);"""

new_fetch_call = """                const [metricsRes, detailsRes, configsRes, sprintsRes, profilesRes] = await Promise.all([
                    fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/sprints', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/profiles', { headers: { 'Authorization': 'Bearer ' + token } })
                ]);"""

if old_fetch_call in content:
    content = content.replace(old_fetch_call, new_fetch_call, 1)

old_fetch_parse = """                if (metricsRes.ok && detailsRes.ok && configsRes.ok && sprintsRes.ok) {
                    const metrics = await metricsRes.json();
                    const details = await detailsRes.json();
                    const configs = await configsRes.json();
                    const sprints = await sprintsRes.json();

                    globalData.metrics = metrics;
                    globalData.details = details;
                    globalData.ragConfig = configs;
                    globalData.sprints = sprints;

                    calculateProcessCompliance();

                    sessionStorage.setItem('dashboardData', JSON.stringify({
                        metrics: metrics,
                        details: details,
                        ragConfig: configs,
                        sprints: sprints
                    }));"""

new_fetch_parse = """                if (metricsRes.ok && detailsRes.ok && configsRes.ok && sprintsRes.ok) {
                    const metrics = await metricsRes.json();
                    const details = await detailsRes.json();
                    const configs = await configsRes.json();
                    const sprints = await sprintsRes.json();
                    const profiles = profilesRes && profilesRes.ok ? await profilesRes.json() : [];

                    globalData.metrics = metrics;
                    globalData.details = details;
                    globalData.ragConfig = configs;
                    globalData.sprints = sprints;
                    globalData.profiles = profiles;

                    calculateProcessCompliance();

                    sessionStorage.setItem('dashboardData', JSON.stringify({
                        metrics: metrics,
                        details: details,
                        ragConfig: configs,
                        sprints: sprints,
                        profiles: profiles
                    }));"""

if old_fetch_parse in content:
    content = content.replace(old_fetch_parse, new_fetch_parse, 1)

# 3. Update banner elements in renderAll
old_banner_code = """            const bannerCatManager = document.getElementById('bannerCatManager');
            const bannerEngagementCode = document.getElementById('bannerEngagementCode');
            if (bannerCatManager) {
                bannerCatManager.textContent = curD.catManager || "--";
            }
            if (bannerEngagementCode) {
                bannerEngagementCode.textContent = curD.engagementCode || "--";
            }

            document.getElementById('currentSpoc').textContent = curM.spoc || "--";"""

new_banner_code = """            const curP = (globalData.profiles && globalData.profiles.find(x => x.engagement === currentEngagement)) || {};
            const bannerCatManager = document.getElementById('bannerCatManager');
            const bannerEngagementCode = document.getElementById('bannerEngagementCode');
            if (bannerCatManager) {
                bannerCatManager.textContent = curP.catManager || curD.catManager || "--";
            }
            if (bannerEngagementCode) {
                bannerEngagementCode.textContent = curP.engagementCode || curD.engagementCode || "--";
            }

            document.getElementById('currentSpoc').textContent = curP.spoc || curM.spoc || "--";"""

if old_banner_code in content:
    content = content.replace(old_banner_code, new_banner_code, 1)

# 4. Update renderHealth to read from team profile
old_render_health = """        function renderHealth() {
            const sprintSel = document.getElementById('mainSprintSelect');
            const sprintId = sprintSel ? sprintSel.value : null;
            const m = globalData.metrics.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const d = globalData.details.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};

            document.getElementById('healthMetricsGrid').innerHTML = `
                ${createCard("Defect Leakage", m.defectLeakage, 'defectLeakage', "%")}
                ${createCard("Production Incidents", m.prodIncidents, 'prodIncidents')}
                ${createCard("Open Risks & Issues", m.openRisks, 'openRisks')}
                ${createCard("Escalations", m.escalations, 'escalations')}
                ${createCard("SOW Milestones", m.sowMilestones, RAG.NONE)}
            `;

            document.getElementById('healthDetailsGrid').innerHTML = `
                ${createListPanel("Defect Leakages", d.defectPts)}
                ${createListPanel("Production Incidents", d.incidentPts)}
                ${createListPanel("Open Risks & Issues", d.riskPts)}
                ${createListPanel("SOW Milestones", d.sowPts)}
                ${createListPanel("Escalations RCA", d.escalationPts)}
            `;
        }"""

new_render_health = """        function renderHealth() {
            const sprintSel = document.getElementById('mainSprintSelect');
            const sprintId = sprintSel ? sprintSel.value : null;
            const m = globalData.metrics.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const d = globalData.details.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const p = (globalData.profiles && globalData.profiles.find(x => x.engagement === currentEngagement)) || {};

            const defectLeakage = p.defectLeakage !== null && p.defectLeakage !== undefined ? p.defectLeakage : m.defectLeakage;
            const prodIncidents = p.prodIncidents !== null && p.prodIncidents !== undefined ? p.prodIncidents : m.prodIncidents;
            const openRisks = p.openRisks !== null && p.openRisks !== undefined ? p.openRisks : m.openRisks;
            const escalations = p.escalations !== null && p.escalations !== undefined ? p.escalations : m.escalations;
            const sowMilestones = p.sowMilestones !== null && p.sowMilestones !== undefined ? p.sowMilestones : m.sowMilestones;

            const defectPts = p.defectPts || d.defectPts;
            const incidentPts = p.incidentPts || d.incidentPts;
            const riskPts = p.riskPts || d.riskPts;
            const sowPts = p.sowPts || d.sowPts;
            const escalationPts = p.escalationPts || d.escalationPts;

            document.getElementById('healthMetricsGrid').innerHTML = `
                ${createCard("Defect Leakage", defectLeakage, 'defectLeakage', "%")}
                ${createCard("Production Incidents", prodIncidents, 'prodIncidents')}
                ${createCard("Open Risks & Issues", openRisks, 'openRisks')}
                ${createCard("Escalations", escalations, 'escalations')}
                ${createCard("SOW Milestones", sowMilestones, RAG.NONE)}
            `;

            document.getElementById('healthDetailsGrid').innerHTML = `
                ${createListPanel("Defect Leakages", defectPts)}
                ${createListPanel("Production Incidents", incidentPts)}
                ${createListPanel("Open Risks & Issues", riskPts)}
                ${createListPanel("SOW Milestones", sowPts)}
                ${createListPanel("Escalations RCA", escalationPts)}
            `;
        }"""

if old_render_health in content:
    content = content.replace(old_render_health, new_render_health, 1)

# 5. Update renderCapability to read from team profile
old_render_cap = """        function renderCapability() {
            const sprintSel = document.getElementById('mainSprintSelect');
            const sprintId = sprintSel ? sprintSel.value : null;
            const m = globalData.metrics.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const d = globalData.details.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};

            document.getElementById('capabilityMetricsGrid').innerHTML = `
                ${createCard("Automation Tools Competency", m.autoToolsReq, 'autoToolsReq')}
                ${createCard("Build Tools Competency", m.buildToolsReq, 'buildToolsReq')}
            `;

            document.getElementById('capabilityDetailsGrid').innerHTML = `
                <div class="space-y-4">
                    ${createListPanel("Automation Tools Required", d.autoToolPts)}
                    ${createListPanel("Build Tools Required", d.buildToolPts)}
                </div>
                <div class="space-y-4">
                    ${createYesNoBadge("Cloud & DevOps Proficiencies (Azure/AWS)", d.cloudProf, getYesNoRag(d.cloudProf))}
                    ${createYesNoBadge("CI/CD Pipeline Setup Proficiency", d.cicdSetup, getYesNoRag(d.cicdSetup))}
                    ${createYesNoBadge("KT Videos/Documents Prepared", d.ktPrep)}
                </div>
            `;
        }"""

new_render_cap = """        function renderCapability() {
            const sprintSel = document.getElementById('mainSprintSelect');
            const sprintId = sprintSel ? sprintSel.value : null;
            const m = globalData.metrics.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const d = globalData.details.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const p = (globalData.profiles && globalData.profiles.find(x => x.engagement === currentEngagement)) || {};

            const autoToolsReq = p.autoToolsReq !== null && p.autoToolsReq !== undefined ? p.autoToolsReq : m.autoToolsReq;
            const buildToolsReq = p.buildToolsReq !== null && p.buildToolsReq !== undefined ? p.buildToolsReq : m.buildToolsReq;
            const autoToolPts = p.autoToolPts || d.autoToolPts;
            const buildToolPts = p.buildToolPts || d.buildToolPts;
            const cloudProf = p.cloudProf || d.cloudProf;
            const cicdSetup = p.cicdSetup || d.cicdSetup;
            const ktPrep = p.ktPrep || d.ktPrep;

            document.getElementById('capabilityMetricsGrid').innerHTML = `
                ${createCard("Automation Tools Competency", autoToolsReq, 'autoToolsReq')}
                ${createCard("Build Tools Competency", buildToolsReq, 'buildToolsReq')}
            `;

            document.getElementById('capabilityDetailsGrid').innerHTML = `
                <div class="space-y-4">
                    ${createListPanel("Automation Tools Required", autoToolPts)}
                    ${createListPanel("Build Tools Required", buildToolPts)}
                </div>
                <div class="space-y-4">
                    ${createYesNoBadge("Cloud & DevOps Proficiencies (Azure/AWS)", cloudProf, getYesNoRag(cloudProf))}
                    ${createYesNoBadge("CI/CD Pipeline Setup Proficiency", cicdSetup, getYesNoRag(cicdSetup))}
                    ${createYesNoBadge("KT Videos/Documents Prepared", ktPrep)}
                </div>
            `;
        }"""

if old_render_cap in content:
    content = content.replace(old_render_cap, new_render_cap, 1)

# 6. Update renderAutomation to read from team profile
old_render_auto = """        function renderAutomation() {
            const sprintSel = document.getElementById('mainSprintSelect');
            const sprintId = sprintSel ? sprintSel.value : null;
            const m = globalData.metrics.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const d = globalData.details.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};

            document.getElementById('automationMetricsGrid').innerHTML = `
                ${createCard("Automation Coverage", m.autoCoverage, 'autoCoverage', "%")}
                ${createCard("Automation Stability", m.autoStability, 'autoStability', "%")}
                ${createCard("Reusable Assets Created", m.assets, RAG.NONE, "", "📊 Informational")}
                ${createCard("Regression Run Time (hrs)", m.regRunTime, RAG.NONE, " hrs", "📈 Track Trend")}
                ${createCard("Manual Test Execution time (hrs)", m.regExecTimeNoAuto, RAG.NONE, " hrs", "📈 Track Trend")}
                ${createCard("Automation Bugs Reported", m.autoBugs, RAG.NONE)}
            `;

            document.getElementById('automationDetailsGrid').innerHTML = `
                <div class="space-y-4">
                    ${createListPanel("Automation Bugs Reported", d.autoBugsPts)}
                    ${createListPanel("Assets Reused", d.assetPts)}
                </div>
                <div>
                    ${createYesNoBadge("CI/CD Maturity", d.cicdMat, getYesNoRag(d.cicdMat))}
                </div>
            `;
        }"""

new_render_auto = """        function renderAutomation() {
            const sprintSel = document.getElementById('mainSprintSelect');
            const sprintId = sprintSel ? sprintSel.value : null;
            const m = globalData.metrics.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const d = globalData.details.find(x => x.engagement === currentEngagement && x.sprint_id == sprintId) || {};
            const p = (globalData.profiles && globalData.profiles.find(x => x.engagement === currentEngagement)) || {};

            const autoCoverage = p.autoCoverage !== null && p.autoCoverage !== undefined ? p.autoCoverage : m.autoCoverage;
            const autoStability = p.autoStability !== null && p.autoStability !== undefined ? p.autoStability : m.autoStability;
            const assets = p.assets !== null && p.assets !== undefined ? p.assets : m.assets;
            const regRunTime = p.regRunTime !== null && p.regRunTime !== undefined ? p.regRunTime : m.regRunTime;
            const regExecTimeNoAuto = p.regExecTimeNoAuto !== null && p.regExecTimeNoAuto !== undefined ? p.regExecTimeNoAuto : m.regExecTimeNoAuto;
            const autoBugs = p.autoBugs !== null && p.autoBugs !== undefined ? p.autoBugs : m.autoBugs;
            const autoBugsPts = p.autoBugsPts || d.autoBugsPts;
            const assetPts = p.assetPts || d.assetPts;
            const cicdMat = p.cicdMat || d.cicdMat;

            document.getElementById('automationMetricsGrid').innerHTML = `
                ${createCard("Automation Coverage", autoCoverage, 'autoCoverage', "%")}
                ${createCard("Automation Stability", autoStability, 'autoStability', "%")}
                ${createCard("Reusable Assets Created", assets, RAG.NONE, "", "📊 Informational")}
                ${createCard("Regression Run Time (hrs)", regRunTime, RAG.NONE, " hrs", "📈 Track Trend")}
                ${createCard("Manual Test Execution time (hrs)", regExecTimeNoAuto, RAG.NONE, " hrs", "📈 Track Trend")}
                ${createCard("Automation Bugs Reported", autoBugs, RAG.NONE)}
            `;

            document.getElementById('automationDetailsGrid').innerHTML = `
                <div class="space-y-4">
                    ${createListPanel("Automation Bugs Reported", autoBugsPts)}
                    ${createListPanel("Assets Reused", assetPts)}
                </div>
                <div>
                    ${createYesNoBadge("CI/CD Maturity", cicdMat, getYesNoRag(cicdMat))}
                </div>
            `;
        }"""

if old_render_auto in content:
    content = content.replace(old_render_auto, new_render_auto, 1)

# 7. Update renderSummaryCards for static capability and health
old_summary_loop = """            sprintMetrics.forEach(m => {
                const d = globalData.details.find(x => x.engagement === m.engagement && x.sprint_id == sprintId) || {};
                const eng = m.engagement;"""

new_summary_loop = """            sprintMetrics.forEach(m => {
                const d = globalData.details.find(x => x.engagement === m.engagement && x.sprint_id == sprintId) || {};
                const p = (globalData.profiles && globalData.profiles.find(x => x.engagement === m.engagement)) || {};
                const eng = m.engagement;

                const defLeak = p.defectLeakage !== null && p.defectLeakage !== undefined ? p.defectLeakage : m.defectLeakage;
                const pInc = p.prodIncidents !== null && p.prodIncidents !== undefined ? p.prodIncidents : m.prodIncidents;
                const oRisk = p.openRisks !== null && p.openRisks !== undefined ? p.openRisks : m.openRisks;
                const esc = p.escalations !== null && p.escalations !== undefined ? p.escalations : m.escalations;
                const aCov = p.autoCoverage !== null && p.autoCoverage !== undefined ? p.autoCoverage : m.autoCoverage;
                const aStab = p.autoStability !== null && p.autoStability !== undefined ? p.autoStability : m.autoStability;
                const aTools = p.autoToolsReq !== null && p.autoToolsReq !== undefined ? p.autoToolsReq : m.autoToolsReq;
                const bTools = p.buildToolsReq !== null && p.buildToolsReq !== undefined ? p.buildToolsReq : m.buildToolsReq;
                const cMat = p.cicdMat || d.cicdMat;
                const cProf = p.cloudProf || d.cloudProf;
                const cSetup = p.cicdSetup || d.cicdSetup;"""

if old_summary_loop in content:
    content = content.replace(old_summary_loop, new_summary_loop, 1)

# Replace variables in renderSummaryCards
content = content.replace("getRagDef('defectLeakage', m.defectLeakage, eng),", "getRagDef('defectLeakage', defLeak, eng),")
content = content.replace("getRagDef('prodIncidents', m.prodIncidents, eng),", "getRagDef('prodIncidents', pInc, eng),")
content = content.replace("getRagDef('openRisks', m.openRisks, eng),", "getRagDef('openRisks', oRisk, eng),")
content = content.replace("getRagDef('escalations', m.escalations, eng)", "getRagDef('escalations', esc, eng)")
content = content.replace("getRagDef('autoCoverage', m.autoCoverage, eng),", "getRagDef('autoCoverage', aCov, eng),")
content = content.replace("getRagDef('autoStability', m.autoStability, eng),", "getRagDef('autoStability', aStab, eng),")
content = content.replace("getYesNoRag(d.cicdMat)", "getYesNoRag(cMat)")
content = content.replace("getRagDef('autoToolsReq', m.autoToolsReq, eng),", "getRagDef('autoToolsReq', aTools, eng),")
content = content.replace("getRagDef('buildToolsReq', m.buildToolsReq, eng),", "getRagDef('buildToolsReq', bTools, eng),")
content = content.replace("getYesNoRag(d.cloudProf)", "getYesNoRag(cProf)")
content = content.replace("getYesNoRag(d.cicdSetup)", "getYesNoRag(cSetup)")

# 8. Update Update Modal Tabs in HTML
old_modal_tabs = """                <div class="flex gap-4 border-b border-tremor-border mb-4 items-center">
                    <button id="tabMetrics"
                        class="px-4 py-2 text-sm font-medium text-tremor-brand-DEFAULT border-b-2 border-tremor-brand-DEFAULT">Metrics</button>
                    <button id="tabDetails"
                        class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong">Details</button>
                    <button id="tabAdo"
                        class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong">ADO
                        Setup</button>
                    <button id="tabConfigs"
                        class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong hidden">Configurations</button>
                    <button id="syncAdoBtn"
                        class="ml-auto px-4 py-1.5 bg-blue-100 text-blue-700 text-sm font-medium rounded-md hover:bg-blue-200 border border-blue-300 shadow-sm flex items-center gap-2 hidden">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                            </path>
                        </svg>
                        Auto-Sync from ADO
                    </button>
                </div>"""

new_modal_tabs = """                <div class="flex gap-4 border-b border-tremor-border mb-4 items-center flex-wrap">
                    <button id="tabSprint"
                        class="px-4 py-2 text-sm font-medium text-tremor-brand-DEFAULT border-b-2 border-tremor-brand-DEFAULT">Sprint Delivery</button>
                    <button id="tabProfile"
                        class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong">Team Profile (Static)</button>
                    <button id="tabAdo"
                        class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong">ADO Setup</button>
                    <button id="tabConfigs"
                        class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong hidden">Configurations</button>
                    <button id="syncAdoBtn"
                        class="ml-auto px-4 py-1.5 bg-blue-100 text-blue-700 text-sm font-medium rounded-md hover:bg-blue-200 border border-blue-300 shadow-sm flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                            </path>
                        </svg>
                        Auto-Sync from ADO
                    </button>
                </div>"""

assert old_modal_tabs in content, "old_modal_tabs not found"
content = content.replace(old_modal_tabs, new_modal_tabs, 1)

# 9. Update currentUpdateTab initialization and tab listeners
old_tab_setup = """        let userRole = null;
        let userTeamId = null;
        let teamsList = [];
        let currentUpdateTab = 'metrics';"""

new_tab_setup = """        let userRole = null;
        let userTeamId = null;
        let teamsList = [];
        let currentUpdateTab = 'sprint';"""

if old_tab_setup in content:
    content = content.replace(old_tab_setup, new_tab_setup, 1)

old_tab_listeners = """        ['tabMetrics', 'tabDetails', 'tabConfigs', 'tabAdo'].forEach(tab => {
            document.getElementById(tab).addEventListener('click', (e) => {
                ['tabMetrics', 'tabDetails', 'tabConfigs', 'tabAdo'].forEach(t => {
                    document.getElementById(t).classList.remove('border-b-2', 'border-tremor-brand-DEFAULT', 'text-tremor-brand-DEFAULT');
                    document.getElementById(t).classList.add('text-tremor-content');
                });
                e.target.classList.remove('text-tremor-content');
                e.target.classList.add('border-b-2', 'border-tremor-brand-DEFAULT', 'text-tremor-brand-DEFAULT');
                currentUpdateTab = tab.replace('tab', '').toLowerCase();
                if (currentUpdateTab === 'metrics') {
                    document.getElementById('syncAdoBtn').classList.remove('hidden');
                } else {
                    document.getElementById('syncAdoBtn').classList.add('hidden');
                }
                renderUpdateForm();
            });
        });"""

new_tab_listeners = """        ['tabSprint', 'tabProfile', 'tabConfigs', 'tabAdo'].forEach(tab => {
            const btnEl = document.getElementById(tab);
            if (!btnEl) return;
            btnEl.addEventListener('click', (e) => {
                ['tabSprint', 'tabProfile', 'tabConfigs', 'tabAdo'].forEach(t => {
                    const el = document.getElementById(t);
                    if (el) {
                        el.classList.remove('border-b-2', 'border-tremor-brand-DEFAULT', 'text-tremor-brand-DEFAULT');
                        el.classList.add('text-tremor-content');
                    }
                });
                e.target.classList.remove('text-tremor-content');
                e.target.classList.add('border-b-2', 'border-tremor-brand-DEFAULT', 'text-tremor-brand-DEFAULT');
                currentUpdateTab = tab.replace('tab', '').toLowerCase();
                const syncBtn = document.getElementById('syncAdoBtn');
                const sprintDropdown = document.getElementById('updateSprintSelect');
                const addSprintBtn = document.getElementById('addSprintBtn');

                if (currentUpdateTab === 'sprint') {
                    if (syncBtn) syncBtn.classList.remove('hidden');
                    if (sprintDropdown) sprintDropdown.classList.remove('hidden');
                    if (addSprintBtn) addSprintBtn.classList.remove('hidden');
                } else if (currentUpdateTab === 'profile') {
                    if (syncBtn) syncBtn.classList.add('hidden');
                    if (sprintDropdown) sprintDropdown.classList.add('hidden');
                    if (addSprintBtn) addSprintBtn.classList.add('hidden');
                } else {
                    if (syncBtn) syncBtn.classList.add('hidden');
                }
                renderUpdateForm();
            });
        });"""

if old_tab_listeners in content:
    content = content.replace(old_tab_listeners, new_tab_listeners, 1)

# 10. Update renderUpdateForm sections and data mapping
old_render_form_head = """            const METRIC_SECTIONS = {
                'Delivery': ['spAssigned', 'spCompleted', 'usPushed', 'usAssigned', 'usCompleted'],
                'Program Health': ['defectLeakage', 'prodIncidents', 'openRisks', 'escalations', 'sowMilestones'],
                'Capability & Gaps': ['autoToolsReq', 'buildToolsReq'],
                'Automation': ['autoCoverage', 'autoStability', 'regRunTime', 'regExecTimeNoAuto', 'autoBugs', 'assets']
            };

            const DETAIL_SECTIONS = {
                'General Information': ['catManager', 'engagementCode', 'lobLead'],
                'Delivery Details': ['usAssignedPts'],
                'Program Health Details': ['defectPts', 'incidentPts', 'riskPts', 'escalationPts', 'sowPts'],
                'Capability Details': ['autoToolPts', 'buildToolPts', 'cloudProf', 'cicdSetup'],
                'Automation Details': ['autoBugsPts', 'assetPts', 'ktPrep', 'cicdMat'],
                'Compliance Details': ['deloitteTime', 'tenroxTime']
            };

            const ADO_SECTIONS = {
                'Azure DevOps Configuration': ['ado_org', 'ado_project', 'ado_team', 'ado_pat', 'ado_iteration']
            };

            const CONFIG_SECTIONS = {
                'Delivery Rules': ['spAssigned', 'spCompleted', 'usPushed'],
                'Quality & Health Rules': ['defectLeakage', 'prodIncidents', 'openRisks', 'escalations'],
                'Automation Rules': ['autoCoverage', 'autoStability'],
                'Capability Rules': ['autoToolsReq', 'buildToolsReq']
            };

            let sections = {};
            let sourceData = {};

            if (currentUpdateTab === 'metrics') {
                sections = METRIC_SECTIONS;
                sourceData = { ...metric };
            } else if (currentUpdateTab === 'details') {
                sections = DETAIL_SECTIONS;
                sourceData = { ...detail };
            } else if (currentUpdateTab === 'ado') {
                sections = ADO_SECTIONS;
                const teamData = teamsList.find(t => t.id == teamId) || {};
                sourceData = {
                    ado_org: teamData.ado_org || '',
                    ado_project: teamData.ado_project || '',
                    ado_team: teamData.ado_team || '',
                    ado_iteration: teamData.ado_iteration || '',
                    ado_pat: teamData.ado_org ? '********' : '' // placeholder if exists
                };
            } else if (currentUpdateTab === 'configs') {"""

new_render_form_head = """            const SPRINT_SECTIONS = {
                'Sprint Delivery Metrics': ['spAssigned', 'spCompleted', 'usPushed', 'usAssigned', 'usCompleted'],
                'Sprint Work Items': ['usAssignedPts'],
                'Sprint Timesheet Compliance': ['deloitteTime', 'tenroxTime']
            };

            const PROFILE_SECTIONS = {
                'General Information': ['catManager', 'engagementCode', 'lobLead'],
                'Capabilities & Gaps': ['cloudProf', 'cicdSetup', 'cicdMat', 'autoToolsReq', 'buildToolsReq', 'autoToolPts', 'buildToolPts'],
                'Automation Suite': ['autoCoverage', 'autoStability', 'regRunTime', 'regExecTimeNoAuto', 'ktPrep', 'assets', 'assetPts', 'autoBugs', 'autoBugsPts'],
                'Program Health (Persistent)': ['defectLeakage', 'prodIncidents', 'openRisks', 'escalations', 'sowMilestones', 'defectPts', 'incidentPts', 'riskPts', 'escalationPts', 'sowPts']
            };

            const ADO_SECTIONS = {
                'Azure DevOps Configuration': ['ado_org', 'ado_project', 'ado_team', 'ado_pat', 'ado_iteration']
            };

            const CONFIG_SECTIONS = {
                'Delivery Rules': ['spAssigned', 'spCompleted', 'usPushed'],
                'Quality & Health Rules': ['defectLeakage', 'prodIncidents', 'openRisks', 'escalations'],
                'Automation Rules': ['autoCoverage', 'autoStability'],
                'Capability Rules': ['autoToolsReq', 'buildToolsReq']
            };

            let sections = {};
            let sourceData = {};

            const profile = (globalData.profiles && globalData.profiles.find(p => p.team_id == teamId)) || {};

            if (currentUpdateTab === 'sprint' || currentUpdateTab === 'metrics') {
                sections = SPRINT_SECTIONS;
                sourceData = { ...metric, ...detail };
            } else if (currentUpdateTab === 'profile' || currentUpdateTab === 'details') {
                sections = PROFILE_SECTIONS;
                sourceData = { ...profile };
            } else if (currentUpdateTab === 'ado') {
                sections = ADO_SECTIONS;
                const teamData = teamsList.find(t => t.id == teamId) || {};
                sourceData = {
                    ado_org: teamData.ado_org || '',
                    ado_project: teamData.ado_project || '',
                    ado_team: teamData.ado_team || '',
                    ado_iteration: teamData.ado_iteration || '',
                    ado_pat: teamData.ado_org ? '********' : '' // placeholder if exists
                };
            } else if (currentUpdateTab === 'configs') {"""

if old_render_form_head in content:
    content = content.replace(old_render_form_head, new_render_form_head, 1)

# 11. In saveUpdateBtn, add support for profile saving
old_save_handler = """                if (currentUpdateTab === 'metrics' || currentUpdateTab === 'details') {
                    const metric = globalData.metrics.find(m => m.team_id == teamId);
                    if (metric) {
                        payload['engagement'] = metric.engagement;
                        payload['spoc'] = metric.spoc;
                    }
                    const sprintSel = document.getElementById('updateSprintSelect');
                    if (sprintSel && sprintSel.value) {
                        payload['sprint_id'] = parseInt(sprintSel.value);
                        const spObj = globalData.sprints.find(s => s.id == sprintSel.value);
                        if(spObj) payload['sprint'] = spObj.name;
                    }
                }

                const token = localStorage.getItem('token');
                const url = "http://localhost:8000/" + (currentUpdateTab === 'configs' ? 'teams/' + teamId + '/configs' : currentUpdateTab + '/' + teamId);

                try {
                    const res = await fetchWithDbWakeup(url, {
                        method: 'PUT',
                        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    const msgEl = document.getElementById('updateMsg');
                    msgEl.classList.remove('hidden');
                    if (res.ok) {
                        msgEl.textContent = 'Saved successfully!';
                        msgEl.className = 'text-sm mt-2 text-green-600 font-medium';
                        const [mRes, dRes, cRes, sRes] = await Promise.all([
                            fetchWithDbWakeup('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                            fetchWithDbWakeup('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                            fetchWithDbWakeup('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } }),
                            fetchWithDbWakeup('http://localhost:8000/sprints', { headers: { 'Authorization': 'Bearer ' + token } })
                        ]);
                        globalData.metrics = await mRes.json();
                        globalData.details = await dRes.json();
                        globalData.ragConfig = await cRes.json();
                        globalData.sprints = await sRes.json();"""

new_save_handler = """                const token = localStorage.getItem('token');

                if (currentUpdateTab === 'profile' || currentUpdateTab === 'details') {
                    const msgEl = document.getElementById('updateMsg');
                    try {
                        const res = await fetchWithDbWakeup('http://localhost:8000/teams/' + teamId + '/profile', {
                            method: 'PUT',
                            headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        msgEl.classList.remove('hidden');
                        if (res.ok) {
                            msgEl.textContent = 'Team Profile saved successfully!';
                            msgEl.className = 'text-sm mt-2 text-green-600 font-medium';
                            const pRes = await fetchWithDbWakeup('http://localhost:8000/profiles', { headers: { 'Authorization': 'Bearer ' + token } });
                            if (pRes.ok) globalData.profiles = await pRes.json();
                            renderAll();
                            renderUpdateForm();
                        } else {
                            msgEl.textContent = 'Error saving profile.';
                            msgEl.className = 'text-sm mt-2 text-red-600 font-medium';
                        }
                    } catch(e) {
                        console.error(e);
                    }
                    setTimeout(() => { msgEl.classList.add('hidden'); }, 3000);
                    return;
                }

                if (currentUpdateTab === 'sprint' || currentUpdateTab === 'metrics') {
                    const metric = globalData.metrics.find(m => m.team_id == teamId);
                    if (metric) {
                        payload['engagement'] = metric.engagement;
                        payload['spoc'] = metric.spoc;
                    }
                    const sprintSel = document.getElementById('updateSprintSelect');
                    if (sprintSel && sprintSel.value) {
                        payload['sprint_id'] = parseInt(sprintSel.value);
                        const spObj = globalData.sprints.find(s => s.id == sprintSel.value);
                        if(spObj) payload['sprint'] = spObj.name;
                    }

                    // Save both metric and detail in sprint delivery tab
                    try {
                        const [mSave, dSave] = await Promise.all([
                            fetchWithDbWakeup('http://localhost:8000/metrics/' + teamId, {
                                method: 'PUT',
                                headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                                body: JSON.stringify(payload)
                            }),
                            fetchWithDbWakeup('http://localhost:8000/details/' + teamId, {
                                method: 'PUT',
                                headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                                body: JSON.stringify(payload)
                            })
                        ]);
                        const msgEl = document.getElementById('updateMsg');
                        msgEl.classList.remove('hidden');
                        if (mSave.ok && dSave.ok) {
                            msgEl.textContent = 'Sprint Data saved successfully!';
                            msgEl.className = 'text-sm mt-2 text-green-600 font-medium';
                            const [mRes, dRes, cRes, sRes, pRes] = await Promise.all([
                                fetchWithDbWakeup('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                                fetchWithDbWakeup('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                                fetchWithDbWakeup('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } }),
                                fetchWithDbWakeup('http://localhost:8000/sprints', { headers: { 'Authorization': 'Bearer ' + token } }),
                                fetchWithDbWakeup('http://localhost:8000/profiles', { headers: { 'Authorization': 'Bearer ' + token } })
                            ]);
                            globalData.metrics = await mRes.json();
                            globalData.details = await dRes.json();
                            globalData.ragConfig = await cRes.json();
                            globalData.sprints = await sRes.json();
                            if (pRes.ok) globalData.profiles = await pRes.json();"""

if old_save_handler in content:
    content = content.replace(old_save_handler, new_save_handler, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully patched cat_dashboard.html for static/sprint separation!")

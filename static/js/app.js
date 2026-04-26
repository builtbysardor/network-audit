/**
 * CyberGlass Pro Dashboard - Application Logic
 */

// ============ Elements ============
const $ = document.querySelector.bind(document);

const targetInput = $('#targetInput');
const scanTypeSelect = $('#scanTypeSelect');
const startScanBtn = $('#startScanBtn');

// Progress Elements
const scanProgressContainer = $('#scanProgressContainer');
const ringFill = $('#ringFill');
const ringPercentText = $('#ringPercentText');
const scanStatusTitle = $('#scanStatusTitle');
const scanStatusSub = $('#scanStatusSub');

// Stats Elements
const statDevices = $('#statDevices');
const statPorts = $('#statPorts');
const statThreatScore = $('#statThreatScore');
const statServices = $('#statServices');
const lastScanTime = $('#lastScanTime');
const localIpValue = $('#localIpValue');

// Risk Elements
const riskBars = {
    high: { bar: $('#riskHighBar'), label: $('#riskHighLabel') },
    med: { bar: $('#riskMedBar'), label: $('#riskMedLabel') },
    low: { bar: $('#riskLowBar'), label: $('#riskLowLabel') },
    info: { bar: $('#riskInfoBar'), label: $('#riskInfoLabel') }
};

const devicesTableBody = $('#devicesTableBody');
const systemLogs = $('#systemLogs');

let scanPollingInterval = null;

// ============ Initialization ============
document.addEventListener('DOMContentLoaded', () => {
    loadNetworkInfo();
    setupEventListeners();
    addLog('UI Initialized. CyberGlass Engine Ready.', 'info');
    
    // Auto-update CPU usage mock (just for visual pro effect)
    setInterval(() => {
        const usage = Math.floor(Math.random() * 20) + 5;
        $('#cpuUsage').textContent = `${usage}%`;
        $('#cpuUsage').style.color = usage > 15 ? 'var(--warning)' : 'var(--accent-green)';
    }, 3000);
});

async function loadNetworkInfo() {
    try {
        const res = await fetch('/api/network-info');
        const data = await res.json();
        localIpValue.textContent = data.local_ip || '127.0.0.1';
        targetInput.value = data.subnet || '';
        addLog(`Network interface bound: ${data.local_ip}`, 'info');
    } catch {
        addLog('Failed to fetch network bindings.', 'error');
    }
}

function setupEventListeners() {
    startScanBtn.addEventListener('click', startScan);
    targetInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') startScan();
    });
}

// ============ Core Scan Logic ============
async function startScan() {
    const target = targetInput.value.trim();
    const type = scanTypeSelect.value;
    
    if (!target) {
        addLog('Error: Target input cannot be empty', 'error');
        return;
    }

    try {
        await fetch('/api/scan/reset', { method: 'POST' });

        const res = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target, scan_type: type })
        });

        const data = await res.json();
        if (!res.ok) {
            addLog(`Error: ${data.error}`, 'error');
            return;
        }

        addLog(`Scan sequence initiated on ${target} (${type} mode)`);
        showProgressUI();
        startPolling();

    } catch (err) {
        addLog('Critial Error: API Connection refused.', 'error');
    }
}

// ============ UI Updaters ============
function showProgressUI() {
    scanProgressContainer.style.display = 'block';
    startScanBtn.disabled = true;
    startScanBtn.style.opacity = '0.5';
    startScanBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg> SCAN IN PROGRESS';
    
    setRingProgress(0);
    scanStatusTitle.textContent = 'SCAN ACTIVE';
    scanStatusSub.textContent = 'Discovering topology...';
}

function setRingProgress(percent) {
    const dashoffset = 408 - (408 * percent) / 100;
    ringFill.style.strokeDashoffset = dashoffset;
    ringPercentText.textContent = `${percent}%`;
}

// ============ Polling ============
function startPolling() {
    if (scanPollingInterval) clearInterval(scanPollingInterval);
    scanPollingInterval = setInterval(pollScanStatus, 1500);
}

async function pollScanStatus() {
    try {
        const res = await fetch('/api/scan/status');
        const data = await res.json();
        const p = data.progress || 0;
        
        setRingProgress(p);

        if (p < 30) scanStatusSub.textContent = 'Mapping subnets & hosts';
        else if (p < 70) scanStatusSub.textContent = 'Port knocking & service fingerprinting';
        else if (p < 100) scanStatusSub.textContent = 'Compiling risk matrix';

        if (data.status === 'completed') {
            clearInterval(scanPollingInterval);
            scanStatusTitle.textContent = 'SCAN COMPLETE';
            scanStatusSub.textContent = 'Parsing output metrics...';
            setRingProgress(100);
            
            setTimeout(() => {
                fetchResults();
                resetScanButton();
                addLog('Scan sequence complete. Results injected into DOM.');
            }, 1000);
            
        } else if (data.status === 'error') {
            clearInterval(scanPollingInterval);
            scanStatusTitle.textContent = 'SCAN FAILED';
            scanStatusSub.textContent = data.error || 'Unknown Error';
            addLog(`Scan Exception: ${data.error}`, 'error');
            resetScanButton();
        }

    } catch (e) {
        // silent fail on poll errs to prevent log spam
    }
}

function resetScanButton() {
    scanProgressContainer.style.display = 'none';
    startScanBtn.disabled = false;
    startScanBtn.style.opacity = '1';
    startScanBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Start Deep Scan';
}

// ============ Result Rendering ============
async function fetchResults() {
    try {
        const res = await fetch('/api/scan/results');
        const json = await res.json();
        
        if (json.status === 'completed' && json.data) {
            renderDashboard(json.data);
            const d = new Date();
            lastScanTime.textContent = d.toLocaleTimeString();
        }
    } catch {
        addLog('Result compilation failed.', 'error');
    }
}

function renderDashboard(data) {
    const summary = data.summary || {};
    const hosts = data.hosts || [];
    const risks = summary.risk_summary || {};

    // Update Top Stats
    animateVal(statDevices, summary.total_hosts || 0);
    animateVal(statPorts, summary.total_open_ports || 0);
    animateVal(statServices, summary.unique_services || 0);
    
    // Threat score: High=10, Med=5, Low=2
    const totalScore = (risks.high || 0)*10 + (risks.medium || 0)*5 + (risks.low || 0)*2;
    animateVal(statThreatScore, totalScore);
    statThreatScore.style.color = totalScore > 20 ? 'var(--danger)' : (totalScore > 5 ? 'var(--warning)' : 'var(--text-primary)');

    // Update Risk Bars (calc percentage relative to total risks)
    const totalRisks = (risks.high || 0) + (risks.medium || 0) + (risks.low || 0) + (risks.info || 0) || 1;
    
    updateRiskBar(riskBars.high, risks.high || 0, totalRisks);
    updateRiskBar(riskBars.med, risks.medium || 0, totalRisks);
    updateRiskBar(riskBars.low, risks.low || 0, totalRisks);
    updateRiskBar(riskBars.info, risks.info || 0, totalRisks);

    // Update Live Devices Table
    devicesTableBody.innerHTML = '';
    
    if (hosts.length === 0) {
        devicesTableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No devices mapped on subnets.</td></tr>';
        return;
    }

    hosts.forEach(host => {
        const tr = document.createElement('tr');
        
        const stateClass = host.state === 'up' ? 'badge-status' : 'badge-status badge-offline';
        const stateText = host.state === 'up' ? 'ONLINE' : 'OFFLINE';
        
        const osString = host.os && host.os !== 'Unknown' ? `${host.os_icon} ${host.os}` : `${host.os_icon} Unknown OS`;
        
        const portsStr = host.ports && host.ports.length > 0 ? 
            host.ports.map(p => `<span style="color:var(--accent-blue)">${p.port}</span>`).join(', ') : 
            '<span style="color:var(--text-muted)">None detected</span>';

        tr.innerHTML = `
            <td class="td-ip">${host.ip}</td>
            <td>${host.hostname || '<span style="color:var(--text-muted)">---</span>'}</td>
            <td class="td-os">${osString}</td>
            <td class="td-ports" style="font-size: 0.8rem">${portsStr}</td>
            <td><span class="${stateClass}">${stateText}</span></td>
        `;
        devicesTableBody.appendChild(tr);
    });
}

function updateRiskBar(barObj, val, total) {
    barObj.label.textContent = val;
    // Cap visual bar at 100%
    const perc = Math.min((val / total) * 100, 100);
    // Smooth width transition via CSS
    barObj.bar.style.width = `${perc}%`;
}

// ============ Utilities ============
function addLog(msg, type = 'normal') {
    const d = new Date();
    const timeStr = d.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' });
    
    const div = document.createElement('div');
    div.className = 'log-item';
    if (type === 'error') div.style.borderLeftColor = 'var(--danger)';
    if (type === 'info') div.style.borderLeftColor = 'var(--accent-green)';
    
    div.innerHTML = `<span class="log-time">${timeStr}</span><span>${msg}</span>`;
    
    systemLogs.prepend(div);
    if(systemLogs.children.length > 30) {
        systemLogs.removeChild(systemLogs.lastChild);
    }
}

function animateVal(obj, target) {
    const start = parseInt(obj.textContent) || 0;
    const dur = 800; // ms
    const startTime = performance.now();
    
    function update(cTime) {
        const elapsed = cTime - startTime;
        const progress = Math.min(elapsed / dur, 1);
        // ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (target - start) * eased);
        obj.textContent = current;
        if (progress < 1) requestAnimationFrame(update);
        else obj.textContent = target; // Ensure exact finish point
    }
    requestAnimationFrame(update);
}

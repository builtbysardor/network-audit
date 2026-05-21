<div align="center">

# 🛡️ NetShield — Home Network Security Audit Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Nmap-Powered-orange?style=for-the-badge&logo=gnu-bash&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/builtbysardor/Home-Network-Security-Audit-Tool?style=flat-square" />
  <img src="https://img.shields.io/github/forks/builtbysardor/Home-Network-Security-Audit-Tool?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/builtbysardor/Home-Network-Security-Audit-Tool?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Glassmorphism-blueviolet?style=flat-square" />
</p>

<br/>

> **Scan your home network** for devices, open ports, services & vulnerabilities —  
> all from a stunning cyberpunk web dashboard. Powered by Python + Flask + Nmap.

<br/>

**[🚀 Quick Start](#-installation) • [🖥 Usage](#️-usage) • [📊 Features](#-features) • [⚠️ Security](#️-security-notes)**

</div>

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Site-00C7B7?style=for-the-badge)](https://network-audit.vercel.app)

---

## 🎥 Demo

<div align="center">

![NetShield Audit Demo](demo.webp)
*Full network scan with real-time radar animation and risk assessment*

</div>

---

## 📸 Interface Preview

<div align="center">

![CyberGlass Dashboard](preview.png)
*Dark glassmorphism dashboard with neon accents*

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚡ **Quick Scan** | Fast host discovery across your local subnet |
| 🔌 **Port Scan** | Top 100 TCP ports with service detection |
| 🔬 **Full Scan** | Service/version detection + OS fingerprinting |
| 🛡️ **Vuln Scan** | NSE vulnerability scripts for deeper analysis |
| 📊 **Risk Assessment** | Automatic scoring: High / Medium / Low / Info |
| 💾 **JSON Export** | Download structured scan results |
| 🎨 **Cyber UI** | Dark glassmorphism dashboard with neon accents |
| 🎯 **Auto-detect** | One-click subnet auto-fill from your current IP |

---

## 🛠️ Tech Stack

```
Backend:   Python 3.10+ · Flask · python-nmap
Scanner:   Nmap (system binary)
Frontend:  HTML5 · Vanilla CSS · Vanilla JavaScript
Design:    Glassmorphism · CSS animations · Responsive layout
```

---

## 📦 Installation

### Step 1: Install Nmap

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install nmap

# Fedora / RHEL
sudo dnf install nmap

# macOS
brew install nmap
```

### Step 2: Setup Python App

```bash
# Clone the repository
git clone https://github.com/builtbysardor/Home-Network-Security-Audit-Tool.git
cd Home-Network-Security-Audit-Tool

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python3 app.py
```

Open **http://localhost:5000** in your browser 🌐

---

## 🖥️ Usage

1. **Auto-fill** your local subnet with the 🔗 button, or enter IP/range manually (e.g. `192.168.1.0/24`)
2. **Select scan type** — Quick, Port, Full, or Vulnerability
3. Click **Start Scan** and watch the radar animation
4. View discovered **devices**, **open ports**, **services**, and **risk levels**
5. **Export** results as JSON for documentation or further analysis

### Scan Type Comparison

| Type | Speed | Detail | Use Case |
|------|-------|--------|----------|
| ⚡ Quick | Fast | Host discovery only | Find all devices |
| 🔌 Port | Medium | Top 100 ports | Check open ports |
| 🔬 Full | Slow | OS + service versions | Deep audit |
| 🛡️ Vuln | Slowest | CVE vulnerability check | Security audit |

---

## 📁 Project Structure

```
Home-Network-Security-Audit-Tool/
├── app.py              # Flask server & API endpoints
├── scanner.py          # Nmap scanner wrapper
├── utils.py            # Validation & helper utilities
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Dashboard UI
├── static/
│   ├── css/
│   │   └── style.css   # Cyberpunk dark theme
│   └── js/
│       └── app.js      # Frontend scan logic
├── demo.webp           # Live demo recording
├── preview.png         # Dashboard screenshot
└── README.md
```

---

## ⚠️ Security Notes

> **For authorized use only.** Only scan networks you own or have explicit permission to scan.

- Some scan types require **root/sudo** privileges for OS detection
- **Never** expose port 5000 publicly on the internet
- Keep this tool on your **local network only**
- Legal disclaimer: unauthorized scanning is illegal in most jurisdictions

---

## 🔮 Roadmap

- [ ] 📧 **Email reports** — automated weekly network audit emails
- [ ] 🔔 **New device alerts** — notify when unknown devices join the network
- [ ] 🗄️ **Scan history** — SQLite database for tracking changes over time
- [ ] 🐳 **Docker support** — containerized one-command deployment
- [ ] 📱 **Mobile UI** — responsive dashboard for phone monitoring
- [ ] 🔐 **Auth layer** — password-protect the dashboard
- [ ] 📊 **Risk trends** — visualize how network security changes over time

---

## 📄 License

MIT License — free for personal and educational use.

---

<div align="center">

**Built with ❤️ by [Sardor Buriyev](https://github.com/builtbysardor)**

⭐ **Star this repo if NetShield helped secure your network!**

</div>

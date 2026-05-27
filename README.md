# NetShield

> Home network security auditor — port scanning, vulnerability detection, and device discovery.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=flat-square)](https://flask.palletsprojects.com)
[![Nmap](https://img.shields.io/badge/Nmap-required-red?style=flat-square)](https://nmap.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

## Preview

![NetShield Demo](demo.webp)

![Dashboard Preview](preview.png)

## Features

- **Port Scanning** — Identify open ports on all devices using Nmap
- **Vulnerability Detection** — Flag known vulnerable services by version fingerprint
- **Device Discovery** — Map all active hosts on the local subnet
- **Security Reports** — Generate human-readable audit reports
- **Web Dashboard** — Flask UI to run scans and review results

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Flask |
| Scanner | Nmap (python-nmap) |
| Frontend | HTML · CSS · JavaScript |

## Prerequisites

```bash
sudo apt install nmap   # Debian/Ubuntu
brew install nmap       # macOS
```

## Quick Start

```bash
git clone https://github.com/builtbysardor/network-audit.git
cd network-audit
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Usage

1. Enter your network range (e.g. `192.168.1.0/24`)
2. Click **Scan**
3. Review open ports and flagged vulnerabilities
4. Export the security report

> **Legal notice:** Only scan networks you own or have explicit permission to test.

## License

MIT © 2024 Sardor Buriyev

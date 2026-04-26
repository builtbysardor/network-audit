"""
Network Scanner module — wraps python-nmap for structured scanning.
Provides Quick, Full, and Vulnerability scan modes.
"""

import nmap
import threading
from datetime import datetime
from utils import get_service_risk_level, get_os_icon


class NetworkScanner:
    """Main scanner class wrapping python-nmap."""

    def __init__(self):
        self.scanner = nmap.PortScanner()
        self.scan_result = None
        self.scan_status = "idle"  # idle, scanning, completed, error
        self.scan_progress = 0
        self.scan_start_time = None
        self.scan_end_time = None
        self.error_message = None
        self._lock = threading.Lock()

    def get_status(self) -> dict:
        """Get current scan status."""
        with self._lock:
            elapsed = None
            if self.scan_start_time:
                end = self.scan_end_time or datetime.now()
                elapsed = (end - self.scan_start_time).total_seconds()

            return {
                "status": self.scan_status,
                "progress": self.scan_progress,
                "elapsed_seconds": round(elapsed, 1) if elapsed else 0,
                "error": self.error_message,
            }

    def start_scan(self, target: str, scan_type: str = "quick") -> None:
        """Start a scan in a background thread."""
        with self._lock:
            if self.scan_status == "scanning":
                return
            self.scan_status = "scanning"
            self.scan_progress = 0
            self.scan_start_time = datetime.now()
            self.scan_end_time = None
            self.scan_result = None
            self.error_message = None

        thread = threading.Thread(
            target=self._run_scan, args=(target, scan_type), daemon=True
        )
        thread.start()

    def _run_scan(self, target: str, scan_type: str) -> None:
        """Execute the nmap scan (runs in background thread)."""
        try:
            scan_args = self._get_scan_arguments(scan_type)

            with self._lock:
                self.scan_progress = 10

            self.scanner.scan(hosts=target, arguments=scan_args)

            with self._lock:
                self.scan_progress = 80

            result = self._parse_results()

            with self._lock:
                self.scan_result = result
                self.scan_progress = 100
                self.scan_status = "completed"
                self.scan_end_time = datetime.now()

        except nmap.PortScannerError as e:
            with self._lock:
                self.scan_status = "error"
                self.error_message = f"Nmap error: {str(e)}"
                self.scan_end_time = datetime.now()
        except Exception as e:
            with self._lock:
                self.scan_status = "error"
                self.error_message = f"Scan error: {str(e)}"
                self.scan_end_time = datetime.now()

    def _get_scan_arguments(self, scan_type: str) -> str:
        """Get nmap arguments based on scan type."""
        scan_configs = {
            "quick": "-sn -T4",                          # Ping scan — fast host discovery
            "port": "-sT -T4 --top-ports 100",           # Top 100 TCP ports
            "full": "-sV -sC -O -T4 --top-ports 1000",   # Service/OS detection
            "vuln": "-sV --script=vuln -T3",             # Vulnerability scripts
        }
        return scan_configs.get(scan_type, scan_configs["quick"])

    def _parse_results(self) -> dict:
        """Parse nmap scan results into structured data."""
        hosts = []
        total_open_ports = 0
        total_services = set()
        risk_summary = {"high": 0, "medium": 0, "low": 0, "info": 0}

        for host in self.scanner.all_hosts():
            host_data = {
                "ip": host,
                "hostname": self._get_hostname(host),
                "state": self.scanner[host].state(),
                "os": self._detect_os(host),
                "os_icon": "",
                "ports": [],
                "services": [],
                "mac": "",
                "vendor": "",
            }

            # MAC address and vendor
            if "addresses" in self.scanner[host]:
                addrs = self.scanner[host]["addresses"]
                host_data["mac"] = addrs.get("mac", "")

            if "vendor" in self.scanner[host]:
                vendors = self.scanner[host]["vendor"]
                if vendors:
                    host_data["vendor"] = list(vendors.values())[0]

            host_data["os_icon"] = get_os_icon(host_data["os"])

            # Ports and services
            for proto in self.scanner[host].all_protocols():
                ports = self.scanner[host][proto].keys()
                for port in sorted(ports):
                    port_info = self.scanner[host][proto][port]
                    service_name = port_info.get("name", "unknown")
                    service_version = port_info.get("version", "")

                    risk = get_service_risk_level(port, service_name)
                    risk_summary[risk["level"]] += 1

                    port_entry = {
                        "port": port,
                        "protocol": proto,
                        "state": port_info.get("state", "unknown"),
                        "service": service_name,
                        "version": service_version,
                        "product": port_info.get("product", ""),
                        "risk": risk,
                    }
                    host_data["ports"].append(port_entry)

                    if port_info.get("state") == "open":
                        total_open_ports += 1
                        total_services.add(service_name)
                        if service_name not in host_data["services"]:
                            host_data["services"].append(service_name)

            hosts.append(host_data)

        return {
            "hosts": hosts,
            "summary": {
                "total_hosts": len(hosts),
                "hosts_up": sum(1 for h in hosts if h["state"] == "up"),
                "total_open_ports": total_open_ports,
                "unique_services": len(total_services),
                "risk_summary": risk_summary,
                "scan_time": str(self.scan_end_time or datetime.now()),
            },
        }

    def _get_hostname(self, host: str) -> str:
        """Get hostname for a host."""
        try:
            hostnames = self.scanner[host].hostname()
            return hostnames if hostnames else ""
        except Exception:
            return ""

    def _detect_os(self, host: str) -> str:
        """Detect OS from scan results."""
        try:
            if "osmatch" in self.scanner[host]:
                os_matches = self.scanner[host]["osmatch"]
                if os_matches:
                    return os_matches[0].get("name", "Unknown")
            if "osclass" in self.scanner[host]:
                os_classes = self.scanner[host]["osclass"]
                if os_classes:
                    return os_classes[0].get("osfamily", "Unknown")
        except Exception:
            pass
        return "Unknown"

    def get_results(self) -> dict:
        """Get the latest scan results."""
        with self._lock:
            return self.scan_result

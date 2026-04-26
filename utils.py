"""
Utility functions for the Home Network Security Audit Tool.
IP validation, network detection, and formatting helpers.
"""

import re
import socket
import subprocess
from datetime import datetime


def validate_target(target: str) -> bool:
    """Validate an IP address, CIDR range, or hostname."""
    # Single IP
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    # CIDR notation
    cidr_pattern = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    # IP range (e.g., 192.168.1.1-50)
    range_pattern = r'^(\d{1,3}\.){3}\d{1,3}-\d{1,3}$'
    # Hostname
    hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'

    if re.match(ip_pattern, target):
        octets = target.split('.')
        return all(0 <= int(o) <= 255 for o in octets)
    elif re.match(cidr_pattern, target):
        ip_part, prefix = target.rsplit('/', 1)
        octets = ip_part.split('.')
        return all(0 <= int(o) <= 255 for o in octets) and 0 <= int(prefix) <= 32
    elif re.match(range_pattern, target):
        return True
    elif re.match(hostname_pattern, target):
        return True

    return False


def get_local_ip() -> str:
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_default_gateway() -> str:
    """Get the default gateway IP address."""
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout:
            parts = result.stdout.strip().split()
            if "via" in parts:
                return parts[parts.index("via") + 1]
    except Exception:
        pass
    return "Unknown"


def get_subnet() -> str:
    """Get the local subnet in CIDR notation."""
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return "127.0.0.0/8"
    # Assume /24 for typical home networks
    parts = local_ip.split('.')
    return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"


def format_timestamp(ts=None) -> str:
    """Format a timestamp for display."""
    if ts is None:
        ts = datetime.now()
    return ts.strftime("%Y-%m-%d %H:%M:%S")


def get_service_risk_level(port: int, service: str) -> dict:
    """Assess the security risk level of a discovered service."""
    high_risk_ports = {
        21: "FTP — unencrypted file transfer",
        23: "Telnet — unencrypted remote access",
        25: "SMTP — can be used for spam relay",
        135: "MSRPC — Windows RPC exploitation target",
        139: "NetBIOS — information disclosure",
        445: "SMB — ransomware attack vector",
        1433: "MSSQL — database exposure",
        3306: "MySQL — database exposure",
        3389: "RDP — remote desktop brute force",
        5432: "PostgreSQL — database exposure",
        5900: "VNC — unencrypted remote desktop",
        6379: "Redis — often unsecured",
        27017: "MongoDB — often unsecured",
    }

    medium_risk_ports = {
        22: "SSH — ensure key-based auth",
        53: "DNS — potential DNS amplification",
        80: "HTTP — unencrypted web traffic",
        110: "POP3 — unencrypted email",
        143: "IMAP — unencrypted email",
        161: "SNMP — information disclosure",
        8080: "HTTP Proxy — alternate web server",
        8443: "HTTPS Alt — alternate secure web",
    }

    low_risk_ports = {
        443: "HTTPS — encrypted web traffic",
        993: "IMAPS — encrypted email",
        995: "POP3S — encrypted email",
    }

    if port in high_risk_ports:
        return {"level": "high", "description": high_risk_ports[port]}
    elif port in medium_risk_ports:
        return {"level": "medium", "description": medium_risk_ports[port]}
    elif port in low_risk_ports:
        return {"level": "low", "description": low_risk_ports[port]}
    else:
        return {"level": "info", "description": f"Port {port} — {service or 'unknown service'}"}


def get_os_icon(os_name: str) -> str:
    """Return an emoji/icon for the detected OS."""
    os_lower = os_name.lower() if os_name else ""
    if "windows" in os_lower:
        return "🪟"
    elif "linux" in os_lower or "ubuntu" in os_lower or "debian" in os_lower:
        return "🐧"
    elif "mac" in os_lower or "apple" in os_lower or "darwin" in os_lower:
        return "🍎"
    elif "android" in os_lower:
        return "🤖"
    elif "ios" in os_lower or "iphone" in os_lower:
        return "📱"
    elif "router" in os_lower or "cisco" in os_lower:
        return "📡"
    elif "printer" in os_lower:
        return "🖨️"
    else:
        return "💻"

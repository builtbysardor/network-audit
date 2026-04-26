"""
Home Network Security Audit Tool — Flask Application
Main server with REST API endpoints for network scanning.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from scanner import NetworkScanner
from utils import validate_target, get_local_ip, get_default_gateway, get_subnet, format_timestamp

app = Flask(__name__)
CORS(app)

# Global scanner instance
scanner = NetworkScanner()


@app.route("/")
def index():
    """Serve the main dashboard."""
    return render_template("index.html")


@app.route("/api/network-info")
def network_info():
    """Return local network information."""
    return jsonify({
        "local_ip": get_local_ip(),
        "gateway": get_default_gateway(),
        "subnet": get_subnet(),
        "timestamp": format_timestamp(),
    })


@app.route("/api/scan", methods=["POST"])
def start_scan():
    """Start a network scan."""
    data = request.get_json() or {}
    target = data.get("target", "").strip()
    scan_type = data.get("scan_type", "quick")

    if not target:
        return jsonify({"error": "Target IP/range is required"}), 400

    if not validate_target(target):
        return jsonify({"error": "Invalid target format. Use IP, CIDR, or hostname."}), 400

    valid_types = ["quick", "port", "full", "vuln"]
    if scan_type not in valid_types:
        return jsonify({"error": f"Invalid scan type. Use one of: {valid_types}"}), 400

    # Check if already scanning
    status = scanner.get_status()
    if status["status"] == "scanning":
        return jsonify({"error": "A scan is already in progress"}), 409

    scanner.start_scan(target, scan_type)
    return jsonify({
        "message": f"Scan started for {target}",
        "scan_type": scan_type,
    })


@app.route("/api/scan/status")
def scan_status():
    """Return the current scan status."""
    return jsonify(scanner.get_status())


@app.route("/api/scan/results")
def scan_results():
    """Return scan results."""
    results = scanner.get_results()
    if results is None:
        status = scanner.get_status()
        if status["status"] == "scanning":
            return jsonify({"message": "Scan still in progress", "status": "scanning"}), 202
        return jsonify({"message": "No scan results available", "status": "idle"}), 404

    return jsonify({
        "status": "completed",
        "data": results,
    })


@app.route("/api/scan/reset", methods=["POST"])
def reset_scan():
    """Reset the scanner for a new scan."""
    global scanner
    status = scanner.get_status()
    if status["status"] == "scanning":
        return jsonify({"error": "Cannot reset while scanning"}), 409
    scanner = NetworkScanner()
    return jsonify({"message": "Scanner reset"})


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🛡️  Home Network Security Audit Tool")
    print("  🌐  http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)

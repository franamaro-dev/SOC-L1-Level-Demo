import http.server
import socketserver
import logging
from datetime import datetime
import re

# Configuración de Logs tipo Syslog
logging.basicConfig(
    filename='data/soc_alerts.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [SOC-L1-SENSOR] %(message)s',
    datefmt='%b %d %H:%M:%S'
)

PORT = 8080

class HoneypotHandler(http.server.SimpleHTTPRequestHandler):
    # Diccionario de firmas de ataque simples
    ATTACK_SIGNATURES = {
        "SQL_INJECTION": r"(union\s+select|' OR 1=1|--|drop\s+table)",
        "PATH_TRAVERSAL": r"(\.\./\.\./|/etc/passwd|/windows/system32)",
        "XSS": r"(<script>|alert\(|onerror=)",
        "COMMAND_INJECTION": r"(;|\s)&&\s(cat|ls|whoami|net\suser)"
    }

    def do_GET(self):
        client_ip = self.client_address[0]
        path = self.path
        self.analyze_request(client_ip, path)
        
        # Respuesta Genérica (Honeypot)
        self.send_response(200)
        self.send_header("Header-Security-Info", "System-Protected-By-SOC-L1")
        self.end_headers()
        self.wfile.write(b"Unauthorized Access - Connection Logged")

    def analyze_request(self, ip, path):
        # 1. Detección de Patrones de Ataque (Signatures)
        for attack_name, pattern in self.ATTACK_SIGNATURES.items():
            if re.search(pattern, path, re.I):
                self.log_alert(ip, "HIGH", f"Detected {attack_name}", path)
                return

        # 2. Log de tráfico normal para análisis de anomalías
        logging.info(f"NORMAL_TRAFFIC from {ip} - Path: {path}")

    def log_alert(self, ip, severity, attack_type, detail):
        alert_msg = f"SourceIP={ip} Severity={severity} Type='{attack_type}' Payload='{detail}'"
        logging.error(alert_msg)
        print(f"[!!!] {severity} ALERT: {attack_type} from {ip}")

if __name__ == "__main__":
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    print(f"[*] SOC Honeypot escuchando en puerto {PORT}...")
    with socketserver.TCPServer(("", PORT), HoneypotHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Apagando sensor SOC...")
            httpd.server_close()

# [SOC-L1] Triage Guide: Honeypot Alerts

Este documento es una guía rápida para un Analista L1 sobre cómo procesar las alertas generadas por el sensor `SOC-L1-Level-Demo`.

## 1. Clasificación de Alertas

| Ataque | Riesgo | Descripción | Acción Inmediata |
|--------|--------|-------------|------------------|
| **SQL_INJECTION** | CRITICAL | Intento de exfiltración de base de datos. | Bloqueo de IP + Escalar a L2. |
| **COMMAND_INJECTION** | CRITICAL | Intento de ejecución remota (RCE). | Bloqueo de IP + Verificación de procesos en host. |
| **PATH_TRAVERSAL** | HIGH | Intento de lectura de archivos sensibles. | Bloqueo de IP + Auditoría de permisos de archivos. |
| **RECONNAISSANCE** | MEDIUM | Escaneo de archivos de config (.env, .git). | Monitorización de IP + Verificar si el archivo existe. |
| **LOG4SHELL** | HIGH | Intento de explotación de vulnerabilidad Java. | Verificar stack tecnológico del backend. |

## 2. Pasos de Investigación (Verification)

1. **Revisión de Payload**: ¿El payload está codificado? Usa CyberChef para decodificar Base64/URL.
2. **Reputación de IP**: Consulta la IP en **AbuseIPDB** o **VirusTotal**.
3. **Frecuencia**: ¿Es un evento aislado o un barrido masivo? (Brute Force vs Targeted).

## 3. Remediación Sugerida

- **False Positive**: Si la IP es de un sensor de uptime (ej: StatusCake), añadir a WhiteList en el código.
- **True Positive**:
    1. Bloquear en el Gateway (CheckPoint/Asa/Mikrotik).
    2. Notificar al equipo de infraestructura para parcheado.
    3. Documentar IOC (IP, User-Agent, Timestamp) en el reporte de incidente.

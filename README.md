# Industrial Monitoring Pipeline

> **Status: work in progress (draft README).** Sections marked TODO are filled in as the project advances. Only describe features that actually work.

A small Industry 4.0 style pipeline: a simulated machine speaks **Modbus TCP**, **Node-RED** converts the data to **MQTT**, the data is stored in **InfluxDB** and shown in **Grafana** with an alert, all started with Docker Compose.

## Architecture

```mermaid
flowchart LR
  SIM["modbus-sim<br/>Python / pymodbus"] -- "Modbus TCP" --> NR1["Node-RED<br/>read + publish"]
  NR1 -- "MQTT" --> MQ["Mosquitto"]
  MQ -- "MQTT" --> NR2["Node-RED<br/>store"]
  NR2 --> DB[("InfluxDB")]
  DB --> G["Grafana"]
```

## Current status
| Component | Status |
|---|---|
| Mosquitto (MQTT broker) | TODO |
| Modbus simulator | TODO |
| Node-RED read and publish flow | TODO |
| InfluxDB storage | TODO |
| Grafana dashboard and alert | TODO |

## Requirements
- Windows, macOS or Linux
- Docker Desktop (with Docker Compose v2)
- Git
- About 8 GB RAM

## Quick start
TODO (completed in Phase 8 after the full stack works).

## Services and ports
| Service | Port (on your PC only) |
|---|---|
| Mosquitto | 1883 |
| Modbus simulator | 5020 |
| Node-RED | 1880 (TODO) |
| InfluxDB | 8086 (TODO) |
| Grafana | 3000 (TODO) |

## Results
TODO: measured values stored per minute and pipeline latency (real numbers only).

## Known limitations
- The Modbus device is simulated, not a real PLC.
- MQTT is anonymous; ports are bound to `127.0.0.1` for local lab use only.

## Documentation
See the `docs/` folder: `PROJECT_MASTER_GUIDE.md`, `PROGRESS.md`, `DECISIONS.md`, `TROUBLESHOOTING.md`, `GIT_GUIDE.md`.

## Author
Amenallah Ben Hamida, IoT engineering student, EPI Digital School, Sousse.

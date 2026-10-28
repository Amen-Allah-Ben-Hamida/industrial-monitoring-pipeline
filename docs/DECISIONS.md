# DECISIONS

Record every important technical decision: what, why, alternatives. Add new entries at the bottom with the next ID. Do not delete old ones; mark them SUPERSEDED instead.

| ID | Decision | Why | Alternatives considered | Status |
|---|---|---|---|---|
| D-001 | Run everything in Docker Compose | One-command, reproducible, standard in industry | Installing each tool on Windows | Accepted |
| D-002 | Simulate the Modbus device with Python `pymodbus==3.6.9` in a container | No PLC available; no Python needed on the PC. The pymodbus API changed between versions, so the version is pinned | Free GUI simulators (Windows-only, not reproducible) | Accepted |
| D-003 | Simulator listens on port 5020 | Port 502 (standard) needs admin rights inside Linux containers | 502 | Accepted |
| D-004 | Use Node-RED for both Modbus to MQTT and MQTT to InfluxDB | User already knows it; visible flows are good for demos | Telegraf for the storage step (kept as optional O4) | Accepted |
| D-005 | InfluxDB 2.x with Flux queries | Current mainstream line, Grafana supports it | InfluxDB 3, TimescaleDB, Prometheus | Accepted |
| D-006 | Anonymous MQTT, port bound to 127.0.0.1 only | Local lab; the port is not reachable from the network. MQTT auth is optional enhancement O2 | Password file from day one | Accepted (document as limitation in README) |
| D-007 | Force LF line endings with `.gitattributes` | Linux containers can fail on CRLF files | Default Windows behavior | Accepted |
| D-008 | Branch strategy: `main` always works; one `feature/<name>` branch per feature, merged by Pull Request | Teaches the professional workflow | Committing directly on `main` | Accepted |
| D-009 | Fault threshold 75 °C is used in both the simulator and the Grafana alert | One consistent value | Different values | Accepted |
| D-010 | Pin container image versions after first successful run (to be recorded here in Part 2) | Reproducibility | `latest` forever | PENDING (record versions: Node-RED ___, InfluxDB ___, Grafana ___) |

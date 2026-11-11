# PROGRESS

**Last updated:** 2026-10-27 (guide Part 1 delivered, no work started yet)
**Update this file at every Git checkpoint. Do not mark a step COMPLETED before its completion criteria are verified.**

## Resume here
- **Current phase:** Phase 0
- **Current step:** P00-S01 — Create GitHub account (NOT STARTED)
- **Next action:** go to https://github.com/signup and follow P00-S01 in `PROJECT_MASTER_GUIDE.md`.

## Handoff context for any AI
- **Project:** Industrial monitoring pipeline: simulated Modbus TCP device → Node-RED → MQTT (Mosquitto) → Node-RED → InfluxDB 2.x → Grafana (dashboard + alert), all in Docker Compose. Full requirements: `PROJECT_MASTER_GUIDE.md` section A.
- **Purpose:** personal portfolio project for an IoT engineering student targeting Industry 4.0 / robotics internships.
- **User level:** learner. Knows MQTT and Node-RED already. **Never used Git or GitHub.** Docker not installed at start.
- **OS:** Windows. All commands are PowerShell. Editor: VS Code (assumed).
- **Assumptions made (not confirmed by the user):** full version with InfluxDB and Grafana, about 5 hours per week, README in English, no deadline.
- **Guide status:** Part 1 written (Phases 0–3). **Part 2 (Phases 4–8) not written.** Ask for it, giving the AI the files in `docs/`.
- **Rules:** permanent step IDs; no secrets in Git; do not invent facts; label unfinished work honestly.

## Step status
| Step | Status |
|---|---|
| P00-S01 GitHub account | COMPLETED |
| P00-S02 Install/configure Git | COMPLETED |
| P00-S03 VS Code and settings | COMPLETED |
| P00-S04 WSL 2 + Docker Desktop | COMPLETED |
| P00-S05 Verify Docker | COMPLETED |
| P01-S01 Folder + git init | COMPLETED |
| P01-S02 .gitignore / .gitattributes / .env.example | COMPLETED |
| P01-S03 First commit | COMPLETED |
| P01-S04 GitHub repo + push | COMPLETED |
| P02-S01 Branch feature/mosquitto | COMPLETED |
| P02-S02 Broker config + compose | COMPLETED |
| P02-S03 Test pub/sub | COMPLETED |
| P02-S04 Commit, PR, merge | COMPLETED |
| P03-S01 Branch feature/modbus-simulator | COMPLETED |
| P03-S02 Simulator files | COMPLETED |
| P03-S03 Compose + build | COMPLETED |
| P03-S04 Verify, commit, PR, merge | COMPLETED |
| Phases 4–8 | NOT STARTED (steps not yet written) |
P04-S01	Branch feature/nodered-flows	COMPLETED
P04-S02	Add Node-RED to compose and start it	COMPLETED
P04-S03	Install the Modbus palette	COMPLETED
P04-S04	Build the Modbus read flow	COMPLETED
P04-S05	Convert to JSON and publish to MQTT	COMPLETED
P04-S06	Verify messages in MQTT	COMPLETED
P04-S07	Commit, PR, merge	NOT STARTED
P05-S01	Branch feature/influxdb-storage	NOT STARTED
P05-S02	Create the real .env file	NOT STARTED
P05-S03	Add InfluxDB to compose and start it	NOT STARTED
P05-S04	Install the InfluxDB palette	NOT STARTED
P05-S05	Build the store flow (MQTT to InfluxDB)	NOT STARTED
P05-S06	Verify data in InfluxDB	NOT STARTED
P05-S07	Commit, PR, merge	NOT STARTED
P06-S01	Branch feature/grafana-dashboard	NOT STARTED
P06-S02	Grafana service and data source provisioning	NOT STARTED
P06-S03	Log in and test the data source	NOT STARTED
P06-S04	Build the dashboard	NOT STARTED
P06-S05	Create the alert rule (temperature above 75 °C)	NOT STARTED
P06-S06	Export dashboard backup and take screenshots	NOT STARTED
P06-S07	Commit, PR, merge	NOT STARTED

## Actual project state
- Repository: not created yet
- Git branch: n/a
- Last commit: n/a
- Docker containers running: none
- Installed versions (fill in as you go): Git ___ · Docker ___ · Compose ___ · VS Code ___

## Open issues / blockers
None.

## Deviations from the plan
None.

## Measured results (fill in during Phase 7; use only real numbers on the CV)
- Values stored per minute: ___
- Pipeline latency (Node-RED read → MQTT → Node-RED subscriber): ___ ms
11 Nov 22:53:46 - [info] Node-RED version: v5.0.9
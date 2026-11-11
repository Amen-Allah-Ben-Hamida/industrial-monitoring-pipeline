# PROJECT MASTER GUIDE — PART 2 (Phases 4–6)

**Put this file in `docs/` next to `PROJECT_MASTER_GUIDE.md`.** Part 1 holds sections A–C (overview, architecture, register map) and Phases 0–3.
**Guide status:** Part 1 written · **Part 2 written (this file: Phases 4, 5, 6)** · **Part 3 NOT written yet: Phase 7 (tests, failure scenarios, measurements), Phase 8 (README, screenshots, delivery), Phase 9 (replace the simulator with an ESP32 Modbus TCP server).**
Same rules as Part 1: permanent step IDs, shell is PowerShell, statuses NOT STARTED / IN PROGRESS / BLOCKED / COMPLETED.

**Before starting Part 2, these must be true:** P03-S04 COMPLETED, you are on updated `main`, `docker compose ps` shows `mosquitto` and `modbus-sim` running, Docker Desktop is running.

## Part 2 roadmap
| Step ID | Title | Status |
|---|---|---|
| P04-S01 | Branch `feature/nodered-flows` | NOT STARTED |
| P04-S02 | Add Node-RED to compose and start it | NOT STARTED |
| P04-S03 | Install the Modbus palette | NOT STARTED |
| P04-S04 | Build the Modbus read flow | NOT STARTED |
| P04-S05 | Convert to JSON and publish to MQTT | NOT STARTED |
| P04-S06 | Verify messages in MQTT | NOT STARTED |
| P04-S07 | Commit, PR, merge | NOT STARTED |
| P05-S01 | Branch `feature/influxdb-storage` | NOT STARTED |
| P05-S02 | Create the real `.env` file | NOT STARTED |
| P05-S03 | Add InfluxDB to compose and start it | NOT STARTED |
| P05-S04 | Install the InfluxDB palette | NOT STARTED |
| P05-S05 | Build the store flow (MQTT to InfluxDB) | NOT STARTED |
| P05-S06 | Verify data in InfluxDB | NOT STARTED |
| P05-S07 | Commit, PR, merge | NOT STARTED |
| P06-S01 | Branch `feature/grafana-dashboard` | NOT STARTED |
| P06-S02 | Grafana service and data source provisioning | NOT STARTED |
| P06-S03 | Log in and test the data source | NOT STARTED |
| P06-S04 | Build the dashboard | NOT STARTED |
| P06-S05 | Create the alert rule (temperature above 75 °C) | NOT STARTED |
| P06-S06 | Export dashboard backup and take screenshots | NOT STARTED |
| P06-S07 | Commit, PR, merge | NOT STARTED |

## Key concept for this part: containers talk by service name
Inside Docker Compose, containers reach each other by **service name**, not `localhost`. From Node-RED, the simulator is `modbus-sim`, the broker is `mosquitto`, the database is `influxdb`. `localhost` inside a container means that container itself. From your **browser**, you use `localhost` plus the published port (for example `http://localhost:1880`).

---

# PHASE 4 — Node-RED: Modbus to MQTT

## P04-S01 — Branch `feature/nodered-flows`
- **Commands:**
  ```powershell
  git switch main
  git pull
  git switch -c feature/nodered-flows
  git branch
  ```
- **Verification:** `* feature/nodered-flows` in the list.
- **Completion criteria:** on the new branch. **Next:** P04-S02.

## P04-S02 — Add Node-RED to compose and start it
- **Objective:** a running Node-RED whose flows are saved in your project folder.
- **Why this matters:** `./nodered` is mounted into the container as `/data`, so `flows.json` appears in your repo and can be committed.
- **Prerequisites:** P04-S01.
- **Concepts:** a *bind mount* links a folder on your PC to a folder in the container. `depends_on` only controls start order.
- **Exact actions:**
  1. Create an empty folder `nodered` in the project root.
  2. In `docker-compose.yml`, add this block under `services:` (after `modbus-sim`, same indentation as the other services):
  ```yaml
    nodered:
      image: nodered/node-red:latest
      container_name: nodered
      ports:
        - "127.0.0.1:1880:1880"
      volumes:
        - ./nodered:/data
      environment:
        - TZ=Africa/Tunis
      depends_on:
        - mosquitto
        - modbus-sim
      restart: unless-stopped
  ```
- **Commands:**
  ```powershell
  docker compose config
  docker compose up -d
  docker compose ps
  docker compose logs nodered --tail 30
  ```
- **Expected result:** `nodered` is running; logs contain `Welcome to Node-RED` with a version number (**write it down** for pinning in Part 3) and `Started flows`. Open http://localhost:1880: the Node-RED editor loads.
- **Verification:** the editor opens; `Get-ChildItem nodered -Force` now lists files such as `settings.js` and `package.json`.
- **Common problems:** editor not loading right after start → wait 20 seconds; `port is already allocated` → another Node-RED runs on your PC (stop it, or change the left port); container restarting → read the logs (permission errors on `nodered` are rare on Docker Desktop, tell me the message).
- **Completion criteria:** editor opens at `localhost:1880` and `nodered/settings.js` exists.
- **Git checkpoint:** wait for P04-S07. **Next:** P04-S03.

## P04-S03 — Install the Modbus palette
- **Objective:** add Modbus nodes to Node-RED.
- **Why:** Node-RED has no Modbus support by default.
- **Prerequisites:** P04-S02.
- **Exact actions:**
  1. In the editor, top-right menu (☰) → **Manage palette** → **Install** tab.
  2. Search `node-red-contrib-modbus` and click **install** (confirm the popup). Wait until it says installed.
  3. Close the palette window. In the left node list, a **modbus** category now exists.
- **Expected result:** nodes named *modbus-read*, *modbus-getter*, *modbus-flex-getter* and others.
- **Verification:** `Get-Content nodered\package.json` contains `node-red-contrib-modbus`.
- **Common problems:** install fails with a network error → check your internet, retry; the palette search is empty → wait a few seconds.
- **Completion criteria:** the modbus nodes are visible.
- **Git checkpoint:** later. **Next:** P04-S04.

## P04-S04 — Build the Modbus read flow
- **Objective:** read the 3 registers every second and see them in the debug panel.
- **Why:** this is the Modbus client part of the gateway.
- **Prerequisites:** P04-S03, `modbus-sim` running.
- **Concepts:** the *modbus-read* node polls a device cyclically. Its output `msg.payload` is an array of register values, for example `[653, 1506, 0]` = temperature×10, rpm, fault (see the register map in Part 1, Section C).
- **Exact actions:**
  1. Drag a **modbus-read** node onto the canvas and double-click it.
  2. Click the pencil next to **Server** to create a new Modbus client: **Type** TCP, **Host** `modbus-sim` (the service name, not `localhost`), **Port** `5020`, **Unit-Id** `1`. Click **Add**.
  3. In the read node: **FC** = *FC 3: Read Holding Registers*, **Address** `0`, **Quantity** `3`, **Poll Rate** `1` second. Name it `Read machine1`. Click **Done**.
  4. Drag a **debug** node, connect modbus-read to it, click **Deploy** (top right red button).
  5. Open the debug panel (bug icon in the right sidebar).
- **Expected result:** every second the debug panel shows an array like `[653,1506,0]`. Under the modbus-read node, a status label shows it is active.
- **Verification:** values change over time; the third value becomes `1` when the first exceeds `750`.
- **Common problems:** status "connection refused"/red → the host is wrong (it must be `modbus-sim`) or the simulator isn't running (`docker compose ps`); nothing appears → the poll rate is empty, or you forgot to Deploy; payload empty → Quantity is not 3.
- **Completion criteria:** a stream of 3-number arrays in the debug panel.
- **Git checkpoint:** later. **Next:** P04-S05.

## P04-S05 — Convert to JSON and publish to MQTT
- **Objective:** turn the array into a readable JSON message and publish it.
- **Why:** a message such as `{"temperature":65.3,...}` is self-explanatory for any subscriber, unlike raw registers.
- **Prerequisites:** P04-S04.
- **Concepts:** a *function node* runs a few lines of JavaScript on each message. `msg.topic` can carry the MQTT topic.
- **Exact actions:**
  1. Drag a **function** node between modbus-read and the debug node. Name it `To JSON`. Paste this in the **On Message** tab:
  ```javascript
  const [temp10, rpm, fault] = msg.payload;
  msg.payload = {
      machine: "machine1",
      temperature: temp10 / 10,
      rpm: rpm,
      fault: fault,
      ts_read: Date.now()
  };
  msg.topic = "factory/line1/machine1/telemetry";
  return msg;
  ```
  2. Drag an **mqtt out** node (in the *network* category), connect `To JSON` to it. Double-click it: next to **Server** click the pencil, set **Server** `mosquitto` (the service name), **Port** `1883`, leave the rest default, **Add**. Leave **Topic** empty (it comes from `msg.topic`), **QoS** 0, **Retain** false. Click **Done**.
  3. Keep the debug node connected to `To JSON` so you can see the JSON. Click **Deploy**.
- **Code explanation:** `const [a, b, c] = msg.payload` unpacks the array. `temp10 / 10` converts back to °C. `Date.now()` is the read time in milliseconds, used in Phase 5 to measure latency. A JS object as payload is converted to JSON text by the mqtt node.
- **Expected result:** debug shows `{machine:"machine1", temperature:65.3, rpm:1506, fault:0, ts_read:...}` every second; the mqtt out node shows "connected".
- **Verification:** next step.
- **Common problems:** mqtt node says "disconnected" → the server host is `localhost` instead of `mosquitto`; function error in the debug panel → a typo (check the quotes and braces).
- **Completion criteria:** mqtt out is connected and JSON appears in debug.
- **Git checkpoint:** later. **Next:** P04-S06.

## P04-S06 — Verify messages in MQTT
- **Objective:** prove messages reach the broker from outside Node-RED.
- **Commands (PowerShell, project folder):**
  ```powershell
  docker compose exec mosquitto mosquitto_sub -t "factory/#" -v
  ```
  (This keeps running. Stop it with Ctrl+C.)
- **Expected result:** one line per second:
  `factory/line1/machine1/telemetry {"machine":"machine1","temperature":65.3,"rpm":1506,"fault":0,"ts_read":1793...}`
- **Verification:** values change; `fault` becomes 1 when `temperature` exceeds 75.
- **Common problems:** nothing prints → check the mqtt out status in Node-RED and that you clicked Deploy.
- **Completion criteria:** at least 10 consecutive messages seen.
- **Git checkpoint:** next step. **Next:** P04-S07.

## P04-S07 — Commit, PR, merge
- **Exact actions:** update `docs/PROGRESS.md`. Then:
  ```powershell
  git status
  ```
  `git status` should list `docker-compose.yml`, `docs/...` and `nodered/` files such as `flows.json`, `package.json`, `settings.js`. It must **not** list `node_modules`, `flows_cred.json` or `.config.*.json` (they are ignored). If it does, stop and tell me.
  ```powershell
  git add .
  git commit -m "feat: add Node-RED flow reading Modbus and publishing to MQTT"
  git push -u origin feature/nodered-flows
  ```
  On GitHub: pull request → merge → delete branch. Then:
  ```powershell
  git switch main
  git pull
  git branch -d feature/nodered-flows
  ```
- **Completion criteria:** merged, on updated `main`. **Next:** P05-S01.

---

# PHASE 5 — InfluxDB storage

## P05-S01 — Branch `feature/influxdb-storage`
- **Commands:**
  ```powershell
  git switch main
  git pull
  git switch -c feature/influxdb-storage
  ```
- **Completion criteria:** on the new branch. **Next:** P05-S02.

## P05-S02 — Create the real `.env` file
- **Objective:** store the database passwords and token locally, never in Git.
- **Why:** `.env.example` is the public template; `.env` holds your real secrets and is ignored by Git. Docker Compose reads `.env` automatically.
- **Exact actions:**
  1. Copy the template:
     ```powershell
     copy .env.example .env
     ```
  2. Generate a random token (40 characters):
     ```powershell
     -join ((48..57)+(97..122) | Get-Random -Count 40 | ForEach-Object {[char]$_})
     ```
  3. Open `.env` in VS Code and edit. Use a password of at least 8 characters, and paste the token you generated:
     ```
     INFLUXDB_USERNAME=admin
     INFLUXDB_PASSWORD=<your password, 8+ chars>
     INFLUXDB_ORG=lab
     INFLUXDB_BUCKET=factory
     INFLUXDB_TOKEN=<the 40-char token>
     GRAFANA_ADMIN_PASSWORD=<another password, 8+ chars>
     ```
  4. Also add the line `GRAFANA_ADMIN_PASSWORD=change-me-too-123` to `.env.example` (placeholder only, never real values there).
- **Expected result:** a `.env` file in the project root.
- **Verification:** `git status` shows `.env.example` as modified but **no** `.env` (ignored). Keep the token somewhere safe (you need it in P05-S05).
- **Common problems:** if `.env` shows up in `git status`, the `.gitignore` entry is wrong; do NOT commit, tell me.
- **Completion criteria:** `.env` exists, is ignored, and contains all 6 values.
- **Git checkpoint:** later (only `.env.example` gets committed). **Next:** P05-S03.

## P05-S03 — Add InfluxDB to compose and start it
- **Concepts:** InfluxDB stores time-stamped data. *Org* and *bucket* are its top-level containers (like a workspace and a database). A *named volume* is storage managed by Docker that survives container removal. The `DOCKER_INFLUXDB_INIT_*` variables create the org, bucket, user and token on the **first start only**.
- **Exact actions:** in `docker-compose.yml`, add under `services:` (same indentation as the others):
  ```yaml
    influxdb:
      image: influxdb:2.7
      container_name: influxdb
      ports:
        - "127.0.0.1:8086:8086"
      volumes:
        - influxdb-data:/var/lib/influxdb2
      environment:
        - DOCKER_INFLUXDB_INIT_MODE=setup
        - DOCKER_INFLUXDB_INIT_USERNAME=${INFLUXDB_USERNAME}
        - DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUXDB_PASSWORD}
        - DOCKER_INFLUXDB_INIT_ORG=${INFLUXDB_ORG}
        - DOCKER_INFLUXDB_INIT_BUCKET=${INFLUXDB_BUCKET}
        - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=${INFLUXDB_TOKEN}
      restart: unless-stopped
  ```
  And at the **very bottom** of the file, with no indentation, add:
  ```yaml
  volumes:
    influxdb-data:
  ```
- **Commands:**
  ```powershell
  docker compose config
  docker compose up -d
  docker compose ps
  docker compose logs influxdb --tail 20
  ```
- **Expected result:** `influxdb` is running. Open http://localhost:8086 and log in with `INFLUXDB_USERNAME` and `INFLUXDB_PASSWORD`.
- **Verification:** you reach the InfluxDB home page; under **Load Data → Buckets** a bucket named `factory` exists.
- **Common problems:** `docker compose config` warns that a variable is not set → `.env` is missing a value or has a typo in a name; login fails → **the init variables only apply to an empty volume.** If you must change credentials after the first start, you have to delete the volume with `docker compose down -v`, which erases stored data. Tell me before doing that.
- **Completion criteria:** login works and the `factory` bucket exists.
- **Git checkpoint:** later. **Next:** P05-S04.

## P05-S04 — Install the InfluxDB palette
- **Exact actions:** in Node-RED (http://localhost:1880): ☰ → Manage palette → Install → search `node-red-contrib-influxdb` → install.
- **Verification:** the *influxdb out* node appears in the *storage* category; `nodered\package.json` mentions it.
- **Completion criteria:** node visible. **Next:** P05-S05.

## P05-S05 — Build the store flow (MQTT to InfluxDB)
- **Objective:** a second flow that subscribes to MQTT and writes each message to InfluxDB.
- **Why:** it decouples storage from reading: the second flow only needs MQTT.
- **Prerequisites:** P05-S03, P05-S04, the token from `.env`.
- **Exact actions (on a new tab/flow in Node-RED, or below the first flow):**
  1. **mqtt in** node: Server = the existing `mosquitto:1883`, Topic `factory/line1/+/telemetry` (`+` matches any machine name), QoS 0, **Output: a parsed JSON object**.
  2. **function** node `Compute latency and format`:
  ```javascript
  const d = msg.payload;
  const latency = Date.now() - d.ts_read;
  msg.payload = [
      {
          temperature: d.temperature,
          rpm: d.rpm,
          fault: d.fault,
          latency_ms: latency
      },
      { machine: d.machine }
  ];
  return msg;
  ```
  3. **influxdb out** node: pencil next to **Server** → **Version** 2.0, **URL** `http://influxdb:8086`, **Token** = the token from your `.env`, click **Add**. Then **Organization** `lab`, **Bucket** `factory`, **Measurement** `machine_telemetry`.
  4. Connect them in order: mqtt in → function → influxdb out. Add a debug node on the function output. **Deploy**.
- **Code explanation:** InfluxDB points have *fields* (the measured values) and *tags* (labels you filter by, here the machine name). The influxdb node accepts `[fields, tags]`. `latency_ms` is the delay between reading the registers in flow 1 and processing the message in flow 2, so it covers Modbus read → MQTT → subscriber.
- **Expected result:** debug shows arrays with `latency_ms` values of a few milliseconds; the influxdb out node shows no error.
- **Verification:** next step.
- **Common problems:** influx node shows an auth error → the token is wrong (copy it again from `.env`, no spaces); `ECONNREFUSED` → the URL uses `localhost` instead of `influxdb`; "bucket not found" → check the name `factory`.
- **Completion criteria:** no red error on the influxdb node after a minute.
- **Git checkpoint:** later. **Next:** P05-S06.

## P05-S06 — Verify data in InfluxDB
- **Exact actions:** open http://localhost:8086 → **Data Explorer** (chart icon) → **From**: bucket `factory` → filter `_measurement` = `machine_telemetry` → choose the field `temperature` → **Submit**.
- **Expected result:** a line chart of temperature over time. Switching the time range to *Past 5m* shows about 300 points.
- **Verification:** the chart updates when you press Submit again; fields `rpm`, `fault`, `latency_ms` exist.
- **Common problems:** empty chart → flow 2 isn't deployed or the Node-RED influx node has an error; wrong time range → pick *Past 5m*.
- **Completion criteria:** you see temperature points arriving.
- **Git checkpoint:** next step. **Next:** P05-S07.

## P05-S07 — Commit, PR, merge
- **Exact actions:** update `docs/PROGRESS.md`. Then `git status`. It must show `.env.example` (modified), `docker-compose.yml`, `nodered/flows.json`, `nodered/package.json`, `docs/...` and **not** `.env` or `flows_cred.json`.
  ```powershell
  git add .
  git commit -m "feat: store MQTT telemetry in InfluxDB"
  git push -u origin feature/influxdb-storage
  ```
  PR, merge, delete branch on GitHub. Then:
  ```powershell
  git switch main
  git pull
  git branch -d feature/influxdb-storage
  ```
- **Security check before pushing:** run `git ls-files` and confirm no `.env` and no `flows_cred.json` in the list.
- **Completion criteria:** merged, on updated `main`. **Next:** P06-S01.

---

# PHASE 6 — Grafana dashboard and alert

## P06-S01 — Branch `feature/grafana-dashboard`
- **Commands:**
  ```powershell
  git switch main
  git pull
  git switch -c feature/grafana-dashboard
  ```
- **Next:** P06-S02.

## P06-S02 — Grafana service and data source provisioning
- **Objective:** start Grafana already connected to InfluxDB.
- **Why:** *provisioning* means configuration from files, so anyone who clones the repo gets the same setup without clicking.
- **Exact actions:**
  1. Create the folders `grafana/provisioning/datasources` (all three nested).
  2. Create the file `grafana/provisioning/datasources/influxdb.yml`:
  ```yaml
  apiVersion: 1

  datasources:
    - name: InfluxDB
      type: influxdb
      access: proxy
      url: http://influxdb:8086
      isDefault: true
      jsonData:
        version: Flux
        organization: ${INFLUXDB_ORG}
        defaultBucket: ${INFLUXDB_BUCKET}
      secureJsonData:
        token: ${INFLUXDB_TOKEN}
  ```
  3. In `docker-compose.yml` add this service under `services:` and the `grafana-data` line under the existing `volumes:` section at the bottom:
  ```yaml
    grafana:
      image: grafana/grafana-oss:latest
      container_name: grafana
      ports:
        - "127.0.0.1:3000:3000"
      volumes:
        - grafana-data:/var/lib/grafana
        - ./grafana/provisioning:/etc/grafana/provisioning:ro
      environment:
        - GF_SECURITY_ADMIN_USER=admin
        - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
        - INFLUXDB_ORG=${INFLUXDB_ORG}
        - INFLUXDB_BUCKET=${INFLUXDB_BUCKET}
        - INFLUXDB_TOKEN=${INFLUXDB_TOKEN}
      depends_on:
        - influxdb
      restart: unless-stopped
  ```
  ```yaml
  volumes:
    influxdb-data:
    grafana-data:
  ```
  (the bottom `volumes:` section now lists both).
- **Code explanation:** Grafana replaces `${...}` in provisioning files with environment variables, so the token never appears in the repo. `version: Flux` selects the query language that InfluxDB 2.x uses.
- **Commands:**
  ```powershell
  docker compose config
  docker compose up -d
  docker compose logs grafana --tail 30
  ```
- **Expected result:** `grafana` running; logs mention the data source being provisioned; **write down the version** shown on the Grafana login page or logs.
- **Common problems:** an empty variable warning → missing value in `.env`; YAML error → indentation of the provisioning file (2 spaces).
- **Completion criteria:** container running without restarts for 1 minute.
- **Git checkpoint:** later. **Next:** P06-S03.

## P06-S03 — Log in and test the data source
- **Exact actions:** open http://localhost:3000, log in with `admin` and your `GRAFANA_ADMIN_PASSWORD` (skip any "change password" prompt if offered). Menu → **Connections** → **Data sources** → click **InfluxDB** → scroll down → **Save & test**.
- **Expected result:** a green message such as "datasource is working. 1 bucket found".
- **Common problems:** an error about authorization → the token in `.env` doesn't match the one InfluxDB was created with (see the volume warning in P05-S03); connection refused → the URL must be `http://influxdb:8086`.
- **Completion criteria:** green test result.
- **Git checkpoint:** later. **Next:** P06-S04.

## P06-S04 — Build the dashboard
- **Objective:** live panels for temperature, speed and fault state.
- **Exact actions:**
  1. **Dashboards → New → New dashboard → Add visualization → InfluxDB**.
  2. Switch the query editor to the Flux text query and paste (panel 1, **Time series**, title `Temperature (°C)`):
  ```
  from(bucket: "factory")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
    |> filter(fn: (r) => r._measurement == "machine_telemetry" and r._field == "temperature")
  ```
  3. In panel options → **Thresholds**, set a red threshold at `75`.
  4. Add panel 2 (**Time series**, title `Motor speed (rpm)`): same query with `r._field == "rpm"`.
  5. Add panel 3 (**State timeline** or **Stat**, title `Fault`): same query with `r._field == "fault"`.
  6. Top right: time range **Last 15 minutes**, auto-refresh **5s**. **Save dashboard** as `Machine 1`.
- **Expected result:** three live panels updating every few seconds; the temperature line touches the red zone periodically.
- **Common problems:** "No data" → time range too short (use 15 min) or Node-RED isn't running; if you changed the bucket name in `.env`, change it in the queries too; if a menu label differs from this text (Grafana UI changes between versions), send me a screenshot.
- **Completion criteria:** all three panels show live data.
- **Git checkpoint:** later. **Next:** P06-S05.

## P06-S05 — Create the alert rule (temperature above 75 °C)
- **Objective:** an alert that fires when temperature exceeds the fault threshold.
- **Concepts:** Grafana evaluates a query on a schedule, reduces it to a number, and compares it to a threshold. States: Normal, Pending, Firing.
- **Exact actions:** **Alerting → Alert rules → New alert rule**:
  1. Name `High temperature machine1`.
  2. Query A: data source InfluxDB, same Flux query as the temperature panel.
  3. Expressions: **Reduce** (input A, function *Last*), then **Threshold** (input = the Reduce, **IS ABOVE 75**) set as the alert condition.
  4. Folder: create `Machine alerts`. Evaluation group: new, interval `10s`. Pending period: `0s`.
  5. Contact point: leave the default (no email is configured; the firing state is still visible in the UI).
  6. **Save rule and exit**.
- **Expected result:** the rule shows **Normal**. When the simulated temperature passes 75 °C (up to about 3 minutes), it switches to **Firing**, and goes back to Normal when it drops.
- **Verification:** reload the **Alert rules** page now and then; take a screenshot when it says Firing.
- **Common problems:** `Error` state on the rule → open it and read the message (often the query returned no data in the default window; check the range or the bucket name); never fires → the temperature may not have peaked yet, wait a few minutes.
- **Completion criteria:** you have seen the rule in **Firing** and then back in **Normal**.
- **Git checkpoint:** later. **Next:** P06-S06.

## P06-S06 — Export a dashboard backup and take screenshots
- **Exact actions:**
  1. Dashboard → **Export** (or Share → Export) → **Save to file**. Create the folder `grafana/dashboards/` and save it as `machine1.json`. This is a backup (it isn't auto-loaded).
  2. Create the folder `docs/screenshots/`. Save screenshots with the Windows Snipping Tool (Win+Shift+S): `dashboard.png` (all three panels with data), `alert-firing.png` (the alert rule in Firing state), `nodered-flows.png` (both flows visible).
- **Verification:** the files exist; open the screenshots and check no password or token is visible.
- **Completion criteria:** 1 JSON file, 3 screenshots, no secrets visible.
- **Git checkpoint:** next step. **Next:** P06-S07.

## P06-S07 — Commit, PR, merge
- **Exact actions:** update `docs/PROGRESS.md`. `git status` must show `grafana/`, `docs/screenshots/`, `docker-compose.yml`, and **not** `.env`.
  ```powershell
  git add .
  git commit -m "feat: add Grafana dashboard and temperature alert"
  git push -u origin feature/grafana-dashboard
  ```
  PR, merge, delete branch on GitHub. Then:
  ```powershell
  git switch main
  git pull
  git branch -d feature/grafana-dashboard
  ```
- **Final check for Part 2:** on a spare moment run `docker compose down` then `docker compose up -d`. Everything should come back by itself with your data kept (the flows are in `nodered/`, the data in named volumes). Do **not** add `-v` to `down`, which deletes stored data.
- **Completion criteria:** merged, the stack restarts cleanly, the dashboard shows live data again.
- **Next:** Part 3 (Phases 7, 8, 9).

---

# Add these to your other docs (copy-paste)

**`docs/PROGRESS.md`:** add the rows P04-S01 … P06-S07 from the table above, set the guide status to "Part 1 and Part 2 written; Part 3 not written", and record the versions you observed: Mosquitto 2.1.2 · Node-RED ___ · InfluxDB 2.7.__ · Grafana ___.

**`docs/DECISIONS.md`:** add these rows.
| ID | Decision | Why | Status |
|---|---|---|---|
| D-011 | Node-RED data folder is bind-mounted (`./nodered:/data`) so `flows.json` is versioned in Git; `flows_cred.json` is git-ignored | Flows are part of the project; credentials are not | Accepted |
| D-012 | InfluxDB and Grafana use Docker named volumes | Data should survive container removal and is not part of Git | Accepted |
| D-013 | Secrets live in `.env` (ignored); `.env.example` is committed with placeholders; Grafana reads the token through environment variables | No secrets in Git | Accepted |
| D-014 | Latency metric = time between the Modbus read in flow 1 and processing in flow 2 (`latency_ms`), not end-to-end to the dashboard | Simple, honest, measurable inside the pipeline | Accepted |
| D-015 | Mosquitto pinned at 2.1.2 observed; Node-RED, InfluxDB 2.7 and Grafana versions to be pinned after the first successful run | Reproducibility | PENDING |

**`docs/TROUBLESHOOTING.md`:** (POSSIBLE issues for Part 2) Node-RED "connection refused" to Modbus/MQTT/InfluxDB usually means `localhost` was used instead of the service name; InfluxDB login fails after credentials were edited because the init variables apply only to an empty volume; Grafana "No data" is usually the time range or bucket name; Grafana data source auth errors usually mean a token mismatch.

---

# Remaining sections (Part 3, not written yet)
- Phase 7: tests (end-to-end), failure scenarios (stop the simulator, stop the broker, restart the stack), measurements (values per minute, latency).
- Phase 8: complete README (quick start, screenshots, results, limitations), repository cleanup, version pinning, final checklist against requirements M1–M8, CV update.
- Phase 9: replace the simulator with an ESP32 acting as a real Modbus TCP server.
- Section G expansion with real issues you hit in Parts 1 and 2.

# TROUBLESHOOTING

**Status labels:** CONFIRMED = it happened and the fix was verified. POSSIBLE = likely cause, not yet confirmed on this project. Add real incidents under "Confirmed issues" with the date.

## Debugging method (use this every time)
1. **Read the exact error message.** Copy it fully; do not paraphrase.
2. **Find where it happens:** which step, which command, which container.
3. **Check the logs:** `docker compose ps` then `docker compose logs <service>` (add `--tail 50` to limit).
4. **Change one thing at a time**, then retest. Note what you changed.
5. **Confirm the cause** before calling it fixed: the symptom must disappear after the fix and come back if you undo it.
6. **Write it down** in "Confirmed issues" below.

## Safe diagnostic commands
```powershell
docker compose ps                      # which containers run
docker compose logs <service> --tail 50
docker compose config                  # validates docker-compose.yml
docker compose down                    # stop and remove containers (data in named volumes is kept)
git status                             # what changed
git diff                               # exactly what changed
```
Do not use `docker compose down -v` (it deletes stored data) or `docker system prune -a` unless you understand what they delete.

## Possible issues (Phases 0–3)

### Docker Desktop will not start / "Virtualization must be enabled"
- **Possible cause:** CPU virtualization disabled in BIOS.
- **Investigate:** Task Manager → Performance → CPU → Virtualization.
- **Fix:** enable Intel VT-x / AMD SVM in BIOS, restart. **Verify:** `docker run hello-world`.

### "WSL 2 installation is incomplete" or Docker stuck on "starting"
- **Possible cause:** outdated WSL kernel.
- **Fix:** `wsl --update`, then `wsl --shutdown`, start Docker Desktop again. **Verify:** `wsl --status`.

### `cannot connect to the Docker daemon`
- **Possible cause:** Docker Desktop not running. **Fix:** start it and wait for "Engine running".

### `port is already allocated`
- **Possible cause:** another program uses the port (1883, 5020, 1880, 8086, 3000).
- **Investigate:** `netstat -ano | findstr :1883`
- **Fix:** stop that program, or change the LEFT number of the port mapping in compose (for example `"127.0.0.1:1884:1883"`) and record the change in `DECISIONS.md`.

### `git` is not recognized
- **Possible cause:** terminal opened before installing Git. **Fix:** close and reopen PowerShell. **Verify:** `git --version`.

### `Author identity unknown` on commit
- **Fix:** run `git config --global user.name "..."` and `git config --global user.email "..."`.

### GitHub asks for a password and rejects it
- **Possible cause:** GitHub no longer accepts account passwords for Git over HTTPS; the browser sign-in via Git Credential Manager is needed.
- **Fix:** Windows "Credential Manager" → Windows Credentials → remove `git:https://github.com` entries, then run `git push` again and sign in via the browser.

### Simulator container keeps restarting
- **Investigate:** `docker compose logs modbus-sim`.
- **Possible causes:** `ImportError` from a pymodbus version different from the pinned `3.6.9`; a typo in `simulator.py`.
- **Fix:** correct the file, then `docker compose up -d --build`.

### Config file seems ignored or garbled inside a container
- **Possible cause:** Windows CRLF line endings or a file saved in UTF-16.
- **Fix:** create/edit files in VS Code (UTF-8, LF); confirm `.gitattributes` exists.

## Confirmed issues
_None yet. Add entries here: date, symptom/error message, confirmed cause, fix, how it was verified, how to prevent it._

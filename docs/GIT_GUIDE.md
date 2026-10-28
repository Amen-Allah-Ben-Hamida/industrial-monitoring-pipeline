# GIT GUIDE (project-specific)

## Vocabulary
| Term | Meaning |
|---|---|
| Repository | Your project folder plus its full history (hidden `.git` folder) |
| Working directory | The files as you see and edit them |
| Staging area | The waiting room for changes that will go into the next commit (`git add`) |
| Commit | A saved snapshot with a message |
| Branch | An independent line of commits |
| Remote / origin | The copy of the repo on GitHub |
| Pull Request (PR) | A GitHub request to merge one branch into another |
| Git vs GitHub | Git = the tool on your PC. GitHub = a website that hosts repos |

## Workflow used in this project
1. `main` always contains working, verified code.
2. For each feature: `git switch main` → `git pull` → `git switch -c feature/<name>`.
3. Work in small steps. After each verified milestone: inspect, stage, commit.
4. Push the branch, open a PR on GitHub, read "Files changed", merge, delete the branch.
5. Back locally: `git switch main` → `git pull` → `git branch -d feature/<name>`.

Planned branches: `feature/mosquitto` (P02), `feature/modbus-simulator` (P03), `feature/nodered-flows` (P04), `feature/influxdb-storage` (P05), `feature/grafana-dashboard` (P06), `docs/final-readme` (P08).

## Everyday commands
| Command | What it does | When |
|---|---|---|
| `git status` | Shows changed/untracked files and the current branch | Constantly |
| `git diff` | Shows unstaged changes line by line | Before staging |
| `git diff --staged` | Shows what will go into the next commit | Before committing |
| `git add <file>` / `git add .` | Stages changes | After checking the diff |
| `git commit -m "type: message"` | Saves a snapshot | After a verified milestone |
| `git log --oneline` | Compact history | To see what happened |
| `git switch <branch>` / `git switch -c <new>` | Change / create branch | Feature work |
| `git push -u origin <branch>` | Uploads a branch (first time) | End of a feature |
| `git push` | Uploads new commits | Later pushes |
| `git pull` | Downloads and merges remote changes | Before starting work |
| `git branch -d <branch>` | Deletes a merged local branch | After the PR is merged |

## Commit message convention
`type: short description in present tense` with type one of `feat`, `fix`, `docs`, `chore`, `test`, `refactor`.
Examples: `feat: add Node-RED read flow`, `fix: correct MQTT topic name`, `docs: add architecture diagram`.

## Never commit
`.env`, passwords, tokens, Node-RED `flows_cred.json`, database files, `node_modules`. Check with `git status` before every `git add .`. If a secret was committed by mistake, **change the secret immediately** (removing it from history is a separate, harder job).

## Resolving a merge conflict (when it happens)
1. `git pull` or a merge reports `CONFLICT` in some file.
2. Open the file: conflicting parts are marked `<<<<<<<`, `=======`, `>>>>>>>`.
3. Keep the correct content, delete the markers, save.
4. `git add <file>` then `git commit` (Git proposes a message).
5. Run the project again to verify it still works.
To cancel a merge that went wrong: `git merge --abort`.

## Recovery guide
| Situation | Safe action | Warning |
|---|---|---|
| Edited a file and want the last committed version | `git restore <file>` | **Destroys your uncommitted edits in that file.** Check `git diff <file>` first. |
| Staged a file by mistake | `git restore --staged <file>` | Safe; keeps your edits |
| Wrong commit message on the last commit (not pushed) | `git commit --amend -m "new message"` | Rewrites that commit; don't do it after pushing |
| Committed on the wrong branch (not pushed) | Ask for help before using `git reset`; copy your work elsewhere first | `git reset --hard` destroys work |
| "I lost a commit" | `git reflog` shows where HEAD has been; `git switch -c rescue <hash>` makes a branch at that commit | Safe: it only creates a branch |
| Push rejected ("non-fast-forward") | `git pull`, resolve conflicts, push again | Do NOT use `git push --force` |
| Unsure about anything | `git status`, `git log --oneline`, then ask | Never run commands you don't understand |

Commands that can destroy work: `git reset --hard`, `git clean -fd`, `git push --force`, `git branch -D`, `git restore` on edited files. Never use them as a routine fix.

## Cloning the finished repo on another machine
```powershell
git clone https://github.com/<username>/industrial-monitoring-pipeline.git
cd industrial-monitoring-pipeline
copy .env.example .env      # then edit .env (Phase 5)
docker compose up -d
```

## Current Git state (keep updated in PROGRESS.md)
Repository not created yet.

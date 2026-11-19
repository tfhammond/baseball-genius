# Baseball Genius setup for teammates

**CECS 491A · Setup and Initial Programming Assignment**

Before you start, clone the public repository and get the shared PostgreSQL hostname, database name (`nonballknower`), and private connection URL from Thomas. You do not need a GitHub invite to clone the public repo. You’ll use your own VS Code and Python environment with the team’s central database.

## 1. Pick your operating system and install the tools

| Your setup | Terminal to use | VS Code Python interpreter after step 2 |
| --- | --- | --- |
| Windows 10 or 11 (native x64) | PowerShell | `.venv\Scripts\python.exe` |
| macOS 13 or later (Apple Silicon or Intel) | Terminal, typically zsh | `.venv/bin/python` |
| Windows with WSL2 Ubuntu | Ubuntu terminal | `.venv/bin/python` in a WSL window |

### Windows · PowerShell

1. Install [Git for Windows](https://git-scm.com/install/windows) and [VS Code](https://code.visualstudio.com/download).
2. Open PowerShell and install uv.

```powershell
winget install --id=astral-sh.uv -e
```

If WinGet is unavailable, use uv’s standalone PowerShell installer.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Reopen PowerShell and VS Code so both can see the updated PATH. Use a **PowerShell** integrated terminal for the remaining steps. Run Python through `uv run --locked` so you can use the environment without activating `.venv` in PowerShell.

### macOS · Terminal

1. Install [VS Code](https://code.visualstudio.com/download) for your Mac's processor. Check **About This Mac** if you need to identify Apple Silicon or Intel.
2. Run `git --version`. If macOS prompts for Apple’s command-line tools, install them and rerun the check. You can also start that installation with `xcode-select --install`.
3. Install uv in Terminal, then reopen Terminal and VS Code.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open the repo in VS Code through **File → Open Folder** after cloning.

### Windows · WSL2 Ubuntu (optional)

Use this path if you already develop inside Ubuntu. Run `wsl -l -v` from PowerShell to verify Ubuntu is using version 2. Install the **WSL** extension in Windows VS Code. In Ubuntu, install the tools.

```bash
sudo apt update
sudo apt install -y git curl ca-certificates
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reopen Ubuntu. Clone under your Linux home directory, for example `~/projects`, and open the checkout with `code .` from Ubuntu. Install the VS Code Python extension in the **WSL: Ubuntu** environment. Use a separate clone and virtual environment if you also develop from native Windows.

### Verify the tools

Run these commands in the terminal for the path you chose. Install the Microsoft **Python** extension in VS Code.

```text
git --version
uv --version
```

Steps 2–4 use the same commands in PowerShell, macOS Terminal, and WSL, with a separate command for creating `.env` on each shell type. All teammates connect to the hosted PostgreSQL instance, and uv installs Python and the locked dependencies locally.

## 2. Clone and install the locked Python environment

```bash
git clone --branch main https://github.com/tfhammond/baseball-genius.git
cd baseball-genius
git log -1 --oneline
```

If you already have a clone, use these commands from a clean working tree to update `main`.

```bash
git fetch origin
git switch main
git merge --ff-only origin/main
```

```bash
uv python install 3.12
uv sync --locked
uv run --locked python -c "import platform, sys; print(sys.version.split()[0], platform.machine(), sys.executable)"
uv run --locked python -m django --version
uv run --locked python -c "import psycopg; print(psycopg.__version__)"
uv run --locked python -c "import duckdb; print(duckdb.sql('select 42').fetchone())"
```

Expect Python 3.12.x from the checkout’s `.venv`, Django 5.2.x, Psycopg 3.x, and `(42,)` from DuckDB. The committed `uv.lock` pins the Python packages. Record the Python patch and uv version you used if you need to report a setup issue.

Open the repository folder in VS Code. In **Python: Select Interpreter**, select `.venv/bin/python` on macOS, Linux, or WSL, or `.venv\Scripts\python.exe` on native Windows. If VS Code does not list the interpreter, choose **Enter interpreter path** and browse to the executable in the table above. Run the remaining commands in VS Code’s integrated terminal so your IDE is visible in the demo.

## 3. Connect Django to the team database

From the repository root, use the command for your shell to create `.env` if it is missing.

**Windows PowerShell**

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

**macOS Terminal or WSL**

```bash
if [ ! -f .env ]; then cp .env.example .env; fi
```

Generate a local Django secret and paste the output after `DJANGO_SECRET_KEY=` in `.env`. Leave `DJANGO_DEBUG=True` for local use. Paste the private direct PostgreSQL URL Thomas sent you after `DATABASE_URL=`. It should use the shared branch, the `nonballknower` database, and the development role, with connection pooling turned off. Keep the URL private.

```bash
uv run --locked python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Check the application and database connection. If migrations are pending, tell the migration owner so they can apply them to the shared database.

```bash
git check-ignore .env
uv run --locked python manage.py check
uv run --locked python manage.py migrate --check
```

## 4. Run your individual class demo

Each person runs the following in VS Code. Replace the sample suffix with your own name in lowercase with hyphens. For a fresh insert during the live demo, append a new suffix such as `-class`. Reusing the same name safely reads the existing record.

```bash
uv run --locked python -m scripts.db_smoke setup-demo-your-first-last
```

For the live demo and screenshot, use a name that produces `Inserted`. Confirm the output shows the shared PostgreSQL host, `nonballknower`, and `Read back` with the same row ID. If you see `Already stored`, choose a new suffix and rerun the command. For an optional cross-platform check, one teammate writes on Windows and the Mac teammate reads the same row with `--read-only`. Then swap roles. Use the original writer's exact row name. The reader should see the same database and row ID from a different computer.

```bash
uv run --locked python -m scripts.db_smoke setup-demo-your-first-last --read-only
```

Collect these screenshots for your own setup PDF. Use your full name and check Canvas for the due date.

| Assignment check | What to show |
| --- | --- |
| GitHub access | The team repo open while you are signed in, with the setup on `main` visible |
| Central database and host | Use the owner's redacted host screenshot and your own terminal output showing the shared host and database |
| IDE setup | VS Code open to the cloned repo, with the project interpreter visible |
| Write and read from code | `scripts/db_smoke.py` open in VS Code and the integrated terminal showing the insert and read-back on the shared host |

Submit your own setup PDF and be ready to run the demo live for the instructor. If you cannot demo on a class day, arrange a time with the instructor before the due date. Missing either the PDF or the live demo results in a zero.

## Optional project tools

- **Frontend.** The Developer Guide lists Node.js. If you are working on the frontend, install [Node.js 24 LTS](https://nodejs.org/en/download) in your development environment and check `node --version` and `npm --version`. JavaScript served by Django runs in the browser. If the team adds npm tooling, record the exact Node version, commit `package-lock.json`, then use `npm ci` in the directory that contains the lockfile.
- **Historical baseball data.** DuckDB is ready after step 2. Follow the data-owner steps below if you are building the dataset. Everyone else can use the published snapshot.
- **Team tools.** Request access to the team’s [Figma prototype](https://www.figma.com/design/IvUn9M3p2M0rtFNjcRLKo8/prototyp?node-id=9-3), [Jira board](https://baseballanalysis.atlassian.net/jira/software/projects/SCRUM/boards/1?filter=&groupBy=none), and [Discord](https://discord.com/channels/1547730407544590497/1547730408224071833) using the Developer Guide.

### Data-owner setup for the historical dataset

The team's data flow is `pybaseballstats → database → statistical query tools`. The repository pins the ingestion dependency in `pyproject.toml` and `uv.lock`. From the repository root, install the locked ingestion group and check the import.

```bash
uv sync --locked --group ingest
uv run --locked --group ingest python -c "from pybaseballstats.statcast import pitch_by_pitch_data; print(callable(pitch_by_pitch_data))"
```

Expect `True`. If your chosen source function requires Playwright, run `uv run --locked --group ingest playwright install chromium`. On Ubuntu, use `uv run --locked --group ingest playwright install --with-deps chromium` if system libraries are missing.

Once the team implements the importer, document its exact command, source/date range, and output filename. Publish a small DuckDB seed snapshot with its SHA-256 checksum. Teammates put the snapshot under `data/local/`, verify the checksum, and run this command after substituting the published filename.

```bash
uv run --locked python -c "import duckdb; db = duckdb.connect('data/local/baseball.duckdb', read_only=True); print(db.sql('SHOW TABLES').fetchall())"
```

Compare the table list with the data owner's documented schema. The app's statistical tools query the prepared data. Use PostgreSQL migrations for the app tables and publish a new DuckDB snapshot when the historical dataset changes.

## Common setup failures

| Symptom | Check |
| --- | --- |
| `uv` or `code` is missing | Reopen the terminal after installation. In WSL, install the VS Code WSL extension on Windows and run `code .` from Ubuntu. |
| `uv sync --locked` says the lock is stale | Check the commit and fetch the matching `pyproject.toml` and `uv.lock`. The teammate changing dependencies updates and commits both. |
| Django says `DATABASE_URL` or `DJANGO_SECRET_KEY` is missing | Check that `.env` is next to `manage.py`. On Windows, verify the filename did not become `.env.txt`. Existing shell variables can override dotenv values. |
| Connection fails | Recopy the direct URL, verify host, branch, database, role and TLS parameters, then retry. If it only fails on a campus network, test that network’s access to PostgreSQL port 5432 before demo day. |
| `auth_group` is missing or migrations are pending | Compare your database and endpoint with the team’s. Ask the migration owner to run `manage.py migrate` on that database. |
| Peer cannot read your row | Compare the exact row name, host, and database in both environments. Use the exact same branch endpoint. |

## References

- Project sources supplied by the team. *Setup and Initial Programming Assignment*, Submission 1. *Baseball Analysis Developer Guide*, Setting Up Project Tools. *Requirements Specification*, Compatibility. *Baseball Analysis Prototype*, application stack and technical flow.
- Installation and configuration references. [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [VS Code Python](https://code.visualstudio.com/docs/languages/python), [uv installation](https://docs.astral.sh/uv/getting-started/installation/), [uv platform support](https://docs.astral.sh/uv/reference/policies/platforms/), [uv lock and sync](https://docs.astral.sh/uv/concepts/projects/sync/), [Django PostgreSQL support](https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes), [django-environ](https://django-environ.readthedocs.io/en/latest/quickstart.html), [Neon with Django](https://neon.com/docs/guides/django), [DuckDB concurrency](https://duckdb.org/docs/current/connect/concurrency), [pybaseballstats README](https://github.com/nico671/pybaseballstats/blob/4ae8b00d90a50ac933fb0b6f74b9938e1503e77d/README.md), and [Node.js releases](https://nodejs.org/en/about/previous-releases).

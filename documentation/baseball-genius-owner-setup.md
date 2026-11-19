# Small Ball setup for Thomas

**CECS 491A · Setup and Initial Programming Assignment**

The Django setup is already on the public GitHub repository’s `main` branch. As owner, verify the shared Neon database, send the team the setup details, and prepare your own individual demo and PDF.

## 1. Set up your Windows 10 and WSL2 tools

In Windows PowerShell, run `wsl -l -v` and verify Ubuntu shows version 2. Install [VS Code](https://code.visualstudio.com/download) on Windows with the **WSL** extension. Run the following in your existing Ubuntu terminal.

```bash
sudo apt update
sudo apt install -y git curl ca-certificates
git --version
```

If `uv --version` is unavailable, install uv in Ubuntu and reopen the terminal.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
uv --version
uv python install 3.12
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/tfhammond/baseball-genius.git small-ball
cd small-ball
git log -1 --oneline
code .
```

The commands use the existing GitHub repository URL and create a local folder named `small-ball`. If you rename the repository on GitHub, give teammates the new clone URL at handoff.

If you already have a clone, open a terminal in it. With a clean working tree, switch to `main` and fast-forward it from GitHub.

```bash
git fetch origin
git switch main
git merge --ff-only origin/main
code .
```

Install the Microsoft **Python** extension in the **WSL: Ubuntu** environment in VS Code. Use the Ubuntu integrated terminal for the commands below.

## 2. Confirm team access to GitHub

Ask each teammate to open the [public repository](https://github.com/tfhammond/baseball-genius) while signed in and show the setup on `main`. They can clone it and demonstrate access without an invite. Use **Settings → Collaborators → Add people** to give teammates write access for project work if needed.

## 3. Confirm the central PostgreSQL database

1. Open the existing project in the [Neon Console](https://console.neon.tech/) and select the branch that hosts `nonballknower`. Record the endpoint hostname and database name.
2. In **Connect**, select that branch, `nonballknower`, and the development role. Turn connection pooling off and copy the direct URL with its TLS parameters.
3. Capture a redacted screenshot showing the database name and host. Take separate screenshots if Neon displays them in separate views. Hide credentials and the full URL.
4. Coordinate shared migrations yourself or designate one teammate to apply them.

## 4. Install the existing project

From the repo root, install the locked dependencies and select `.venv/bin/python` in VS Code using **Python: Select Interpreter**.

```bash
uv sync --locked
uv run --locked python -m django --version
```

## 5. Configure Django and test the shared database

From the repository root, create `.env` if this is your first setup.

```bash
if [ ! -f .env ]; then cp .env.example .env; fi
```

Use the same direct URL you intend to give the team. Generate a local Django secret and paste the output after `DJANGO_SECRET_KEY=` in `.env`. Leave `DJANGO_DEBUG=True` for local use. Paste the private direct PostgreSQL URL after `DATABASE_URL=`.

```bash
uv run --locked python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Run these checks from VS Code’s integrated terminal. If `migrate --check` reports pending migrations, confirm the endpoint and database, apply the team’s migrations with `uv run --locked python manage.py migrate`, and rerun the check.

```bash
git check-ignore .env
uv run --locked python manage.py check
uv run --locked python manage.py migrate --check
uv run --locked python -m scripts.db_smoke setup-demo-thomas-hammond
```

Confirm that the script prints the expected remote hostname and `nonballknower`. For the live demo and screenshot, use a fresh name and show `Inserted` and `Read back` with the same row ID.

Open **SQL Editor** in the Neon Console. Select `nonballknower` and the Neon branch whose endpoint hostname matches the host printed by `db_smoke`. Run this query to see the saved demo records.

```sql
SELECT id, name
FROM public.auth_group
WHERE name LIKE 'setup-demo-%'
ORDER BY id;
```

Find your demo name in the results and confirm that its ID matches the one printed in VS Code.

## 6. Hand off to the team and finish your own demo

- Send the [teammate setup guide](baseball-genius-environment-setup.md), the GitHub clone URL, the expected hostname and database name, and the redacted Neon screenshot. Tell teammates to use `main`. Share the connection URL privately.
- Ask one teammate to set up from a fresh clone and run `uv run --locked python -m scripts.db_smoke setup-demo-thomas-hammond --read-only`. Compare their output to your saved row ID. Then have them write their own row and read it from your computer using the same command with their row name.
- For your own submission, capture GitHub access, the shared PostgreSQL host and database, the VS Code interpreter, and the database script with its insert and read-back output. Use your full name on the PDF, check Canvas for the deadline, and demo live. Use a fresh row name such as `setup-demo-thomas-hammond-class` for the live insert.
- When the team adds dependencies, merge the updated `pyproject.toml` and `uv.lock` together. Merge Django migrations with their models and coordinate when to apply them to the shared database.

Each teammate must submit their own PDF and demonstrate GitHub access, the shared database and host, their IDE, and a database write and read from their own computer. If anyone cannot demo on a class day, they must arrange a time with the instructor before the due date. Missing either the PDF or the live demo results in a zero.

## Stats ingestion and AI conversations

| Workflow | What runs |
| --- | --- |
| Dataset build or refresh | Run the importer as a separate command. It uses `pybaseballstats` to collect stats and writes them to the historical stats database. |
| User asks a baseball question | The AI calls a stats query tool. The tool reads the prepared database and returns results the AI can explain in the conversation. |

Keep the importer out of web app startup and conversation handlers. Once the importer exists, document its command, covered dates, and output location. Use the DuckDB seed snapshot described in the teammate guide for local query development. If a question falls outside the loaded coverage, report the missing data in the conversation and handle any dataset refresh through the importer.

## Later integrations

When the team chooses providers for live scores and the LLM, document the endpoints, environment variable names, and a smoke-test request for each. Add empty placeholders to `.env.example` and provide real keys through server-side environment settings. When choosing a web host, use the same locked dependencies, set `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS`, and follow the host’s deployment instructions. These integrations can follow the setup demo.

## References

- Project sources supplied by the team. *Setup and Initial Programming Assignment*, Submission 1. *Baseball Analysis Developer Guide*, Setting Up Project Tools. *Requirements Specification*, Compatibility. *Baseball Analysis Prototype*, application stack and technical flow.
- Installation and configuration references. [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [VS Code Python](https://code.visualstudio.com/docs/languages/python), [uv installation](https://docs.astral.sh/uv/getting-started/installation/), [uv lock and sync](https://docs.astral.sh/uv/concepts/projects/sync/), [Django PostgreSQL support](https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes), [django-environ](https://django-environ.readthedocs.io/en/latest/quickstart.html), [Neon with Django](https://neon.com/docs/guides/django), [DuckDB concurrency](https://duckdb.org/docs/current/connect/concurrency), [pybaseballstats README](https://github.com/nico671/pybaseballstats/blob/4ae8b00d90a50ac933fb0b6f74b9938e1503e77d/README.md), and [Node.js releases](https://nodejs.org/en/about/previous-releases).

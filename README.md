# GRACE

**Development of an AI-Enabled Governance, Risk, and Compliance Management System with Intelligent Monitoring and Decision Support for Limay Polytechnic College**

GRACE is a centralized institutional GRC application for governance accountability, deterministic risk and compliance monitoring, evidence workflows, traceable AI-assisted interpretation, and human decision-making. AI output is advisory and never declares compliance, approves decisions, closes risks, or overrides accountable personnel.

## Architecture and stack

- `backend/` — Python 3.12+, Django, Django REST Framework, Simple JWT, django-filter, drf-spectacular, PostgreSQL, pytest.
- `frontend/` — React, TypeScript, Vite, Material UI, TanStack Query, React Router, Axios.
- `docs/ARCHITECTURE.md` — system, module, and AI/human-validation diagrams.

## Main features

- Governance objectives, deterministic KPI state, and decision accountability.
- A 5×5 risk register, mitigation tracking, KRIs, and dynamic heat map.
- Compliance obligations, evidence review, findings, and corrective actions.
- Deduplicated deterministic monitoring rules and in-app alerts.
- Mock or OpenAI advisory analyses with immutable inputs and human review.
- Aggregate executive dashboard, CSV reports, activity history, and audit trail.
- Custom user model, JWT authentication, role-based authorization, pagination, search, filtering, and ordering.

## Development setup

PostgreSQL is the primary database. Create a `grace` database/user, then copy the environment template and supply local values.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

In a second terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open `http://localhost:5173`. API documentation is available at `http://localhost:8000/api/docs/`.

## Demo data

`python manage.py seed_demo` creates clearly labeled **DEMO / SAMPLE DATA**, not actual LPC records. Development-only accounts are `sysadmin`, `grcadmin`, `executive`, `compliance`, `riskowner`, and `auditor`, using the password printed by the command. Change or remove them outside a local demonstration environment.

## AI configuration

The default `AI_PROVIDER=mock` requires no external service. To use OpenAI, set `AI_PROVIDER=openai`, `AI_MODEL`, and `OPENAI_API_KEY` in the backend environment. Keys and record content are never logged. Controlled prompts treat stored text as untrusted data and send only the structured record snapshot needed for an analysis.

## Tests

```bash
cd backend
../.venv/bin/pytest
```

Tests use an isolated SQLite database for portability; deployed and local application settings remain PostgreSQL-first.

## Security and privacy notes

Use unique production secrets, HTTPS, a strict host/CORS allowlist, secure cookies, managed PostgreSQL backups, malware scanning for uploaded files, and a deployment-level Content Security Policy. GRACE minimizes personal data and does not claim that software use itself establishes compliance with the Philippine Data Privacy Act. The institution remains responsible for privacy governance, retention, access reviews, incident response, and legal interpretation.


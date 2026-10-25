# GRACE Backend

The backend is a versioned REST API at `/api/v1/` with OpenAPI at `/api/schema/` and Swagger UI at `/api/docs/`.

## Commands

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py run_monitoring
python manage.py runserver
pytest
```

Use `config.settings.development` locally and `config.settings.production` in deployment. Environment variables are documented in `.env.example`. PostgreSQL is required for normal operation; the test settings use SQLite only to isolate automated domain tests.

The monitoring command can be invoked by cron or Windows Task Scheduler. Celery and Redis are intentionally not required for this MVP.

## API areas

- Authentication: login, refresh, logout, and current user.
- Organization and user administration.
- Governance objectives, KPIs, and decisions.
- Risks, categories, mitigations, indicators, and heat map.
- Compliance obligations, evidence, findings, and corrective actions.
- Monitoring alerts and authorized execution.
- Advisory AI analysis generation and human review.
- Dashboard, reports, audit, activity history, attachments, notifications, and system settings.


# Little Lemon APIs — Django

A restaurant REST API learning project using Django REST Framework, TDD, and GitHub issues and pull requests.

## Current progress

The planning documents are merged. Step 0 is in progress in [issue #2](https://github.com/MohamadAlhajAli/LittleLemon-APIs-django/issues/2): Django scaffolding, dependency setup, environment configuration, and the test harness. 
The GitHub Actions workflow is prepared; its first remote run is pending. API features are not implemented yet.

The course rubric was not found locally. The planning documents define the working baseline until the rubric can be checked.

## Local setup

Commands below use Git Bash on Windows, starting at the repository root. Python 3.14.4 and Pipenv 2026.7.1 were used for initial setup. The project locks its application dependencies in `LittleLemon/Pipfile.lock`; Django is restricted to the 5.2 LTS series.

```bash
python -m pip install --user pipenv
cd LittleLemon
python -m pipenv sync --dev
```

Generate a local `.env` from the example with a fresh secret key. This command refuses to overwrite an existing `.env`:

```bash
python -c "from pathlib import Path; import secrets; template = Path('.env.example').read_text(); content = template.replace('DJANGO_SECRET_KEY=', 'DJANGO_SECRET_KEY=' + secrets.token_urlsafe(64), 1); Path('.env').open('x', encoding='utf-8').write(content)"
```

Pipenv loads `.env` when running commands. Django reads the resulting environment variables. Keep `.env` local; only `.env.example` belongs in Git. See [Pipenv environment loading](https://pipenv.pypa.io/en/latest/shell.html#automatic-loading-of-env-files).

| Variable | Purpose | Default when unset |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django signing key | Required; startup fails if missing or empty |
| `DJANGO_DEBUG` | Development error pages; use `true` locally | `false` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hostnames | `localhost,127.0.0.1` |

The project timezone is `Africa/Cairo` with timezone support enabled. SQLite is used for local development. This is a development scaffold, not a production deployment configuration.

```bash
python -m pipenv run python manage.py migrate
python -m pipenv run python manage.py check
python -m pipenv run python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Stop the server with **Ctrl+C**. Do not start a second server while one is already using the port.

Pipenv may place the virtual environment under your user profile. Run `python -m pipenv --venv` to locate it. There is no need to activate it when using `pipenv run`.

## Verification

Run from `LittleLemon/`:

```bash
python -m pipenv run python -m pip check
python -m pipenv run python manage.py check
python -m pipenv run python manage.py makemigrations --check --dry-run
python -m pipenv run python manage.py test
```

The empty `LittleLemonAPI/tests/` package establishes test discovery. Zero tests is expected at this scaffold stage and does not establish API coverage. Step 1 introduces model behavior through observed Red → Green → Refactor cycles.

## Project layout

- Repository root: README, ignore rules, and planning documents.
- `LittleLemon/`: Pipfile, lockfile, manage.py, and local environment configuration.
- `LittleLemon/LittleLemon/`: Django settings and root URLs.
- `LittleLemon/LittleLemonAPI/`: the single API app and its tests.

## Planning and development workflow

- [Requirements](01%20SRS%20-%20Software%20Requirements%20Specification.md)
- [Design](02%20Design%20Document.md)
- [Build plan](03%20Build%20Plan.md)

Track a small change in an issue, work on a branch, follow TDD for application behavior, and submit a pull request with verification evidence. Review the changes before merging and synchronize local `main` afterwards. Never commit virtual environments, local databases, passwords or tokens.

Future roles are Customer, Manager, and Delivery crew. Registration and token login arrive in Step 2; role setup arrives in Step 3. Endpoint contracts are in the requirements document.

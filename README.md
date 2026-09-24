# Little Lemon APIs — Django

A restaurant REST API learning project using Django REST Framework, TDD, and GitHub issues and pull requests.

## Current progress

- **Step 0 complete:** Django scaffolding, locked dependencies, environment configuration, and GitHub Actions CI ([issue #2](https://github.com/MohamadAlhajAli/LittleLemon-APIs-django/issues/2)).
- **Step 1 complete:** Category, MenuItem, Cart, Order, and OrderItem models, migrations, database constraints, deletion rules, and admin configuration ([issue #4](https://github.com/MohamadAlhajAli/LittleLemon-APIs-django/issues/4)).
- **Next: Step 2:** registration, token authentication, and a login page. API endpoints are not implemented yet.

Django admin supports managing categories and menu items. Carts, orders, and order items are view-only, including for superusers, so direct admin writes cannot bypass the planned application services.

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
python -m pipenv run python manage.py createsuperuser
python -m pipenv run python manage.py runserver
```

Create a superuser once per local database; skip that command if you already have an account. Open [Django admin](http://127.0.0.1:8000/admin/) and sign in. No homepage is configured at `/` yet. Stop the server with **Ctrl+C**.

For a sample catalog, use admin to create two categories (for example, Main Courses and Desserts) and six menu items. These records belong to your local SQLite database and are not included in Git; a fresh setup starts without sample data.

Pipenv may place the virtual environment under your user profile. Run `python -m pipenv --venv` to locate it. There is no need to activate it when using `pipenv run`.

Alternatively, run `python -m pipenv shell` **from the `LittleLemon/` directory containing the Pipfile**, then use commands such as `python manage.py test`. Run `exit` to leave the shell. Changing directories does not switch an already active virtual environment.

## Verification

Run from `LittleLemon/`:

```bash
python -m pipenv run python -m pip check
python -m pipenv run python manage.py check
python -m pipenv run python manage.py makemigrations --check --dry-run
python -m pipenv run python manage.py test
```

The current suite contains 35 tests: 29 model tests in `test_models.py` and six admin tests in `test_admin.py`. They cover persistence, constraints, deletion rules, saved order-item prices, and admin access restrictions. API authentication and endpoint tests will be added in subsequent steps.

For detailed output, use `python -m pipenv run python manage.py test --verbosity 2`. GitHub Actions runs dependency checks, Django system checks, migration drift checks, migration application, and tests on pull requests targeting `main` and pushes to `main`.

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

Keep related commits in one pull request. After merging, start the next branch from updated `main` instead of reusing a branch that was squash-merged. Delete completed branches after confirming their changes are merged. Keep committed migrations so other checkouts can reproduce the database schema.

Future roles are Customer, Manager, and Delivery crew. Registration and token login arrive in Step 2; role setup arrives in Step 3. Endpoint contracts are in the requirements document.

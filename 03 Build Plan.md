# Little Lemon API — Step-by-Step Build Plan

**Companions:** `01 SRS - Software Requirements Specification.md` and `02 Design Document.md`
**Version:** 1.2
**Reviewed:** 2026-09-23
**Status:** Step 0 in progress; feature implementation not started

**How we will work:** explain one small behavior, write and run a failing test, implement the minimum to pass, then refactor with tests passing. Work through one step at a time and pause for your next instruction. Each feature also practices the GitHub issue → branch → commit → pull request → review → merge workflow. Step 12 is a final audit; tests lead development from Step 1 onward.

The SRS defines behavior. If a course requirement changes a decision, update all three documents before implementing the affected feature. The tracker and recorded evidence identify completed work; the remaining snippets describe work still to do.

---

## Progress Tracker

| Step | Title | Depends on | Status | Evidence |
|---|---|---|---|---|
| 0 | Environment and scaffold | — | Completed | Python 3.14.4, Django 5.2.17; system check and initial migrations pass; no migration drift; runner discovers 0 tests as expected |
| 1 | Models, migrations, admin | 0 | Completed | — |
| 2 | Djoser registration, tokens, login page | 1 | In Progress | — |
| 3 | Roles and permissions | 1, 2 | ☐ Not started | — |
| 4 | Menu endpoints | 1, 3 | ☐ Not started | — |
| 5 | Group management | 3 | ☐ Not started | — |
| 6 | Cart endpoints | 1, 3, 4 | ☐ Not started | — |
| 7 | Order placement | 6 | ☐ Not started | — |
| 8 | Order visibility, assignment, delivery | 5, 7 | ☐ Not started | — |
| 9 | Filters, search, ordering, pagination | 4, 5, 8 | ☐ Not started | — |
| 10 | Throttling | 2, 4–9 | ☐ Not started | — |
| 11 | Error and status-code audit | 0–10 | ☐ Not started | — |
| 12 | Performance and final verification | 0–11 | ☐ Not started | — |

Use Evidence for the command/result and relevant test module. Mark a step complete only after its acceptance checks pass.

## TDD: Our Development Loop

For each acceptance criterion, repeat this cycle rather than implementing all tasks and testing at the end:

1. **Red:** write one focused test for expected behavior. Run it and verify it fails for the expected reason. Fix unrelated environment errors first. If a missing symbol requires a minimal stub, add only the stub and rerun to reach the intended behavioral failure.
2. **Green:** implement the smallest change that satisfies the test. Rerun the focused test and relevant existing tests.
3. **Refactor:** improve names, structure or duplication without changing behavior. Keep tests passing.
4. **Record:** note the failing test and reason, passing command/result, and any refactoring in the step evidence or PR. Do not invent or claim a Red run that was not observed.
5. **Commit:** commit a coherent passing change. Several TDD cycles may fit into one commit; separate failing commits are optional, not required. Before a PR is ready, run the full checks.

Example for Step 6: first test that adding a new cart item returns 201 and server-calculated prices. Make it pass. Then test that a repeated POST returns 200, replaces quantity and preserves unit price. Make that pass. Then test another user's cart is unaffected.

Use Django TestCase/APITestCase and plain unittest assertions initially. Avoid adding another test framework solely for TDD. Prefer behavior and boundary cases over testing Django internals. Documentation, environment setup and generated scaffold files need appropriate validation, not contrived failing tests.

## GitHub Practice Before Step 0

**Repository setup progress:** this folder is connected to [LittleLemon-APIs-django](https://github.com/MohamadAlhajAli/LittleLemon-APIs-django), with `main` tracking `origin/main`. [PR #1](https://github.com/MohamadAlhajAli/LittleLemon-APIs-django/pull/1) was merged with merge commit `38d4207`, preserving the existing README history. [Issue #2](https://github.com/MohamadAlhajAli/LittleLemon-APIs-django/issues/2) tracks Step 0 on `chore/2-project-scaffold`. Root ignore rules, the Django scaffold, local environment configuration and test package are prepared; the browser startup check, issue/PR templates, CI and scaffold PR remain. Git is installed; the `gh` CLI was not found on PATH. We use Git Bash and the GitHub website.

**Guided practice:** explain each command, what it changes and what output to inspect. Give the user small command batches to execute and help interpret the output. Keep GitHub exercises visible instead of silently completing the entire collaboration workflow. The user can ask the assistant to execute a batch when preferred.

Repository setup is a preliminary checkpoint, not an extra application implementation step:

1. Inspect the supplied repository URL, visibility, default branch and existing files/history. Check local Git name/email without changing global configuration. Use the user's selected commit identity, including a GitHub no-reply address if preferred; never infer their email.
2. Connect this folder while preserving both the three documents and any remote commits. If the remote is empty, initialize a local repository and add its remote. If it already contains commits, first inspect/fetch its history and choose a safe integration route; do not overwrite the remote or combine histories blindly. Exact commands depend on that inspection.
3. Prepare the initial baseline: the three planning documents, root README, `.gitignore`, an issue template and a PR template. Inspect `git status` and `git diff`; stage named files so the first push contains only reviewed content.
4. Commit and push the baseline. A truly empty repository may need an initial default-branch commit before the first PR can exist; after that, use feature branches. If the remote already has a default-branch commit, the documentation can be its own first PR.
5. Create the first issue for Step 0, with a goal and acceptance checklist. Use labels such as documentation, feature, bug or testing only where helpful. Start a small backlog; do not create every task or a complex project board at once.

**Repository setup acceptance:** local root and remote match the intended project; history is preserved; the user understands staging versus committing versus pushing; the initial reviewed files are on GitHub; the first implementation issue exists. No application feature is required for this checkpoint.

## GitHub Workflow for Each Feature

Use [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow): a short-lived branch, focused changes, a pull request, review, and merge. Treat each build step as an issue initially; split it into smaller issues/PRs when needed for review.

| Stage | What we practice |
|---|---|
| Issue | State the problem, link SRS requirement IDs, list acceptance criteria and test cases |
| Branch | Start from the up-to-date default branch; use a descriptive name such as `feat/cart-replacement` |
| TDD | Run Red → Green → Refactor for one acceptance criterion at a time |
| Commit | Review `git diff`, stage named files, inspect `git diff --staged`, write a meaningful message |
| Push | Push the feature branch and understand its upstream tracking branch |
| Pull request | Explain the behavior change, link the issue, include Red/Green evidence and limitations |
| Review | Read the Files changed tab, examine automated check results, address feedback with follow-up commits |
| Merge | With checks passing and review complete, practice squash merge and understand the resulting history |
| Sync | Return to the default branch, pull with `--ff-only`, and remove the completed feature branch after checking it is no longer needed |

Use `Closes #<actual-issue-number>` only for an issue the PR fully resolves; merging into the default branch can then close it automatically. For partial work, use a normal issue reference. [GitHub issue-linking rules](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

Start with concise commit messages such as `docs: define TDD workflow`, `chore: scaffold Django project`, `feat: replace cart quantities` and `fix: preserve cart price snapshots`. These prefixes are a project convention, not a Git requirement. Passing tests and their implementation normally belong together in a coherent commit.

PR checklist: acceptance criteria satisfied; Red failure observed; focused/full tests pass; migrations included where required; no secrets or unintended files; documentation updated. Open a draft PR for early feedback if useful. Self-review is a learning exercise, not an independent reviewer approval.

After Step 0, GitHub Actions must run system checks, migration drift checks and tests. Add required checks where supported after their first successful run. Do not require an unavailable second reviewer in this solo project. Preserve the repository's existing settings unless intentionally changing them.

Practice merge conflicts, revert and releases when real changes make those lessons useful. After the complete acceptance suite passes, prepare a first release such as `v0.1.0`; do not tag unfinished work as complete. Never use force pushes or destructive resets as routine synchronization steps.

## Shared Working Rules

- Commands assume Git Bash on Windows. Run setup from the project folder, then use `LittleLemon/` as the working directory for `manage.py` commands.
- Prefer `pipenv run ...` so commands always use the intended environment; an interactive `pipenv shell` is optional.
- Maintain one `REST_FRAMEWORK` settings dictionary; add settings without replacing previous ones.
- Business URLs and registration have no trailing slash. Login and current-user routes use the exact trailing slashes specified in the SRS.
- All successful business DELETE operations return 200 with `{"detail": "Deleted successfully."}`.
- Write and run tests before implementing each behavior. The Tasks lists below describe the scope to work through with the TDD loop, not permission to implement an entire step before testing. Keep non-throttle tests independent of throttle cache state.
- Commit source, migrations and lockfile when version control is available. Never commit tokens, passwords, `.env`, virtual environments or the local SQLite database.

---

## Step 0 — Environment and Project Scaffold

**Goal:** a reproducible project with one app, a test harness and a verified dependency baseline, delivered through the first implementation PR.

**Tasks**

1. Inspect available Python and Pipenv, the current directory and any existing Git repository. Record Python version and verify package compatibility before installing.
2. Check the actual course rubric if available. Confirm the unusual current-user path, any mandated framework/model versions and response codes. If the rubric is unavailable, record that limitation and proceed with the current SRS; do not invent course requirements.
3. Prefer Django 5.2 LTS with compatible dependencies. If a course environment requires another version, record the reason and adjust the lockfile intentionally.
4. Create the application directory and scaffold. These example commands assume the version decision above is confirmed:

   ```bash
   mkdir LittleLemon
   cd LittleLemon
   pipenv install 'Django>=5.2,<5.3' djangorestframework djoser django-filter
   pipenv run django-admin startproject LittleLemon .
   pipenv run python manage.py startapp LittleLemonAPI
   ```

5. Add `rest_framework`, `rest_framework.authtoken`, `djoser`, `django_filters` and `LittleLemonAPI` to `INSTALLED_APPS`.
6. Set and document the project timezone (`Africa/Cairo` for this local project unless the course specifies otherwise), keep timezone support enabled, and update the repository-root `.gitignore` and README with setup commands. Keep secrets outside committed configuration; document any required environment variables.
7. Run migrations and the checks below. Add optional Debug Toolbar only when needed later.
8. Replace generated `tests.py` with `tests/__init__.py`, verify test discovery and establish CI as in Design §9.1. Zero feature tests is an honest scaffold state, not proof of application coverage; Step 1 must add the first behavioral tests.
9. Push the scaffold branch, open a PR linked to the Step 0 issue, inspect its diff and CI results, then complete the review/merge/sync exercise.

**Acceptance checks**

- ☐ Python and dependency versions are recorded; `Pipfile.lock` exists
- ☐ `pipenv run python manage.py check` reports no issues
- ☐ Initial migrations succeed and the development server starts
- ☐ The Django welcome page loads locally
- ☐ The README records rubric availability and any documented deviations
- ☐ The test harness runs; GitHub Actions uses locked dependencies and passes the scaffold checks
- ☐ The first implementation PR has review/test evidence and is merged after checks pass

**Verify**

```bash
pipenv run python manage.py migrate
pipenv run python manage.py check
pipenv run python manage.py runserver
```

**Checkpoint:** what belongs to the Django project, and what belongs to its single app?

---

## Step 1 — Models, Migrations and Admin

**Goal:** the five models satisfy Design §2 without losing order history.

**Tasks**

1. Create Category, MenuItem, Cart, Order and OrderItem in dependency order.
2. Use `settings.AUTH_USER_MODEL` for user FKs; give Order's two user relationships distinct reverse names: `orders` and `assigned_orders`. Use `items` for OrderItem's reverse relation.
3. Implement Design §2.2: named uniqueness constraints, quantity checks, nonnegative amounts, unit-price limits, wider line/total decimals, and callable `timezone.localdate` for the date default.
4. Apply the specified deletion behavior: protect categories with menu items, menu items with order items and order owners; SET_NULL for delivery users; cascade Order → OrderItem.
5. Add useful string representations and admin registrations. Keep derived financial data read-only and disable direct cart/order/order-item mutations that bypass services.
6. Create migrations; inspect and apply them. Create a superuser interactively, then two categories and roughly six menu items in admin.
7. Use the tests package established in Step 0. Write each isolated model test before its corresponding model/constraint behavior; do not experiment destructively on seeded data.

**Acceptance checks**

- ☐ Migrations apply and all five models are visible in admin
- ☐ Duplicate cart/order-item pairs and invalid quantities fail their database constraints
- ☐ Protected deletions preserve referenced records
- ☐ Deleting a delivery user leaves its order intact with null assignment
- ☐ Valid large line totals fit the selected decimal fields

**Verify**

```bash
pipenv run python manage.py makemigrations LittleLemonAPI
pipenv run python manage.py migrate
pipenv run python manage.py check
pipenv run python manage.py test LittleLemonAPI.tests.test_models
```

**Checkpoint:** why does Order need distinct reverse names for its two User foreign keys?

---

## Step 2 — Authentication, Tokens and Login Page

**Goal:** register, log in and retrieve the current user using the exact contract paths.

**Tasks**

1. Set global `TokenAuthentication` and `IsAuthenticated`. Keep API session authentication disabled; admin retains its own session login.
2. Implement the explicit Djoser action mapping in Design §5.1. Do not nest `djoser.urls.authtoken` below `/token/login/`, which repeats the prefix.
3. Require email in the registration serializer, preserve Django password validation, and reject unexpected/privileged fields.
4. Add the empty app URLconf and route names. Verify route resolution and restricted HTTP methods.
5. Implement `/login/` and its form from Design §5.3. A successful submit uses the returned token to retrieve the current user and display their username.
6. Add authentication tests using real tokens and verify no unintended Djoser user-list/delete endpoints are exposed.

**Acceptance checks**

- ☐ `POST /api/users` with valid username/email/password → 201
- ☐ Missing/invalid email, weak password, duplicate username or privilege fields → 400
- ☐ `POST /token/login/` with correct credentials → 200 and `auth_token`; wrong credentials → 400
- ☐ `GET /api/users/users/me/` with token → 200; missing/invalid token → 401
- ☐ Registration creates a normal user without role groups
- ☐ The HTML page handles success and failure; it does not persist or log tokens
- ☐ Requests hit the exact URLs without relying on redirects

**Manual sequence**

```text
POST /api/users             {"username":"ana","email":"ana@example.com","password":"<valid test password>"}
POST /token/login/          {"username":"ana","password":"<same password>"}
GET  /api/users/users/me/    Authorization: Token <returned token>
```

Use a manual `Authorization: Token ...` header in Postman/Insomnia. A Bearer header is a different authentication scheme.

**Checkpoint:** why can a user log into Django admin without that session authenticating token-only API requests?

---

## Step 3 — Roles and Permission Layer

**Goal:** one consistent role resolver and reusable endpoint permissions.

**Tasks**

1. Create `Manager` and `Delivery crew` groups in admin, with exact spelling.
2. Implement the resolver and `IsManager`, `IsDeliveryCrew`, `IsManagerOrReadOnly` using Design §3.1.
3. Seed manual users: `ana` and `ben` (Customers), `maria` (Manager), `sam` and `lee` (Delivery crew). Tests create their own independent fixtures, plus a superuser and a staff-only user.
4. Verify permissions with focused tests, avoiding a permanent test-only endpoint.

**Acceptance checks**

- ☐ Superuser and Manager resolve to Manager; Delivery member resolves to Delivery
- ☐ Staff-only and unrelated-group users resolve to Customer
- ☐ Accidental dual membership resolves to Manager consistently
- ☐ Anonymous protected access → 401; authenticated wrong role → 403

**Checkpoint:** what is the difference between authenticating a caller, authorizing a method and limiting visible rows?

---

## Step 4 — Menu Endpoints

**Goal:** FR-3, with role restrictions and clear validation.

**Tasks**

1. Create CategorySerializer and MenuItemSerializer: nested category on read, category_id on write.
2. Add MenuItemsView and SingleMenuItemView with `IsManagerOrReadOnly` and `select_related('category')`.
3. Define exact list/detail routes and validate price, title, category, unknown fields and full PUT versus partial PATCH.
4. Override deletion to 200; map protected order-history deletion to 400.
5. Test every SRS §4.2 role/method cell, including superuser behavior. Tests can create referenced orders directly as fixtures before checkout exists.

**Acceptance checks**

- ☐ All authenticated roles read menu list/detail → 200; anonymous → 401
- ☐ Manager creates → 201, updates/deletes → 200; Customer/Delivery writes → 403
- ☐ Invalid title/price/category and unknown fields → 400
- ☐ Unknown menu ID → 404
- ☐ Deleting an item referenced by an order → 400 with history intact
- ☐ Deleting an item referenced only by cart rows removes those rows

**Checkpoint:** why should a nested category be read-only while category_id is writable?

---

## Step 5 — Group Management

**Goal:** FR-2 and the single-role rule.

**Tasks**

1. Create the four group routes and a limited user serializer (`id`, `username`, `email`).
2. Guard each view with IsManager; validate the username input explicitly.
3. Implement transactional group changes per Design §3.3. Reject cross-role assignment rather than silently removing the previous role.
4. Block removal of Delivery membership when pending assigned orders exist; test with order fixtures.
5. Add role, duplicate, conflict, unknown-user and removal tests. Pagination is added in Step 9.

**Acceptance checks**

- ☐ Manager GET lists members → 200
- ☐ New membership → 201; repeated addition → 200 without duplication
- ☐ Existing membership in the other role group → 400, original role preserved
- ☐ Missing/blank username → 400; unknown username → 404
- ☐ Remove an existing member → 200; unknown user/nonmember → 404
- ☐ Delivery member with pending assignments cannot be removed → 400
- ☐ Customer/Delivery calls → 403; anonymous → 401

**Checkpoint:** why does removing a superuser from Manager not remove their API manager privileges?

---

## Step 6 — Cart Endpoints

**Goal:** FR-4, including predictable repeated additions and price snapshots.

**Tasks**

1. Use a dedicated input serializer accepting only menuitem and quantity; require integer quantity 1–100.
2. Pass request.user explicitly to the cart service. Expose ownership and prices read-only in output.
3. Implement transactional create-or-replace behavior: new row snapshots current menu price; existing row replaces quantity and retains its unit price.
4. Enforce at most 100 distinct rows. Set `pagination_class = None` and scope every query/delete to the caller.
5. Test owner/price spoofing, invalid quantities, duplicate replacement, menu price changes and two-user isolation.

**Acceptance checks**

- ☐ New item → 201 with correct server-calculated prices
- ☐ Repeated item with quantity 3 → 200 and exactly quantity 3, regardless of previous quantity
- ☐ Menu price changes do not change an existing row's unit price, including on repeated POST
- ☐ Unknown/server-owned fields, invalid menu ID or quantity → 400
- ☐ A 101st distinct item → 400; updating one of 100 existing items remains allowed
- ☐ All roles can access only their own cart; GET returns an array
- ☐ DELETE → 200; following GET → `[]`; another user's cart is unchanged

**Checkpoint:** why does `read_only=True` with CurrentUserDefault not replace passing an owner explicitly at save time?

---

## Step 7 — Order Placement

**Goal:** FR-5.2, FR-5.3 and BR-5: an atomic cart-to-order transfer.

**Tasks**

1. Build read-only OrderItemSerializer and OrderSerializer with the `items` relation.
2. Add OrderView; require Customer for POST from the outset. Reject a nonempty creation payload.
3. Implement Design §6.2 in a transaction: materialize cart, validate, compute Decimal total, create order/items, delete captured rows.
4. Provide Customer-scoped order GET initially; complete other role reads in Step 8 before considering order endpoints finished.
5. Test rollback by injecting failures during item creation and cart deletion, using isolated test data.

**Acceptance checks**

- ☐ Populated cart → 201 with correct owner, items, total, date and pending status
- ☐ Cart becomes empty; another user's cart is unchanged
- ☐ Empty cart → 400 with no Order created
- ☐ Client-supplied owner/items/total/status → 400
- ☐ Manager/Delivery POST → 403
- ☐ Each injected write failure leaves the original cart intact and no partial order
- ☐ Price changes after cart creation do not change checkout amounts
- ☐ A second sequential checkout of the now-empty cart → 400

**Scope note:** these checks prove sequential behavior and atomic rollback. SQLite does not prove concurrent checkout safety; see Design §6.3. Do not describe this as preventing duplicate payments—payments are outside scope.

**Checkpoint:** what does a transaction roll back, and why is that different from serializing concurrent requests?

---

## Step 8 — Order Visibility, Assignment and Delivery

**Goal:** complete the SRS §4.5 matrix and order update contract.

**Tasks**

1. Reuse role-scoped querysets for list and detail: Manager all; Delivery assigned; Customer owned.
2. Add SingleOrderView with method permissions and separate Manager/Delivery update validation.
3. Validate delivery targets as active users resolving to Delivery crew, or null.
4. Manager PUT requires delivery_crew and status; PATCH requires at least one. Delivery PATCH accepts only status. Reject empty updates.
5. Override Manager DELETE to 200 and cascade order items. Add every remaining order role/method test.

**Acceptance checks**

- ☐ Customer reads only owned orders; another owner's detail → 404
- ☐ Delivery reads/patches assigned orders only; unassigned target → 404
- ☐ Manager and superuser can view all orders
- ☐ Valid assignment/unassignment → 200; Customer, Manager, inactive or unknown assignee → 400
- ☐ Manager amount/owner/item/date changes → 400
- ☐ Delivery status PATCH → 200; another field → 403; PUT/DELETE → 403
- ☐ Customer PUT/PATCH/DELETE → 403; Manager DELETE → 200
- ☐ Boolean or integer 0/1 status accepted; other encodings rejected
- ☐ Group removal checks from Step 5 work with orders created through the API

**Checkpoint:** why should a role-scoped queryset be reused for update operations as well as reads?

---

## Step 9 — Filtering, Search, Ordering and Pagination

**Goal:** FR-6 with exact query names and consistent response shapes.

**Tasks**

1. Add explicit MenuItemFilter and OrderFilter per Design §7.1; do not substitute different query names for the SRS aliases.
2. Add menu SearchFilter and strict ordering validation. Append a unique tie-breaker to requested ordering.
3. Implement StandardPagination: page/perpage, default 5, cap 100, explicit invalid-value behavior from SRS §10.
4. Apply pagination to menu/order lists and explicitly invoke it in group function views. Keep cart unpaginated.
5. Update earlier list tests for the final pagination envelope and test role isolation with filters applied.

**Acceptance checks**

- ☐ `category=<slug>`, `from_price=5`, `to_price=40` filter menu correctly
- ☐ Menu search matches title or category title case-insensitively
- ☐ `ordering=price,-title` works; invalid field → 400
- ☐ Orders filter by status 0/1 and ISO date without exposing another user's rows
- ☐ Invalid filter values/reversed bounds → 400
- ☐ Paginated output contains count/next/previous/results
- ☐ perpage above 100 caps at 100; malformed/nonpositive perpage → 400
- ☐ Invalid/nonpositive/out-of-range page → 404; empty page 1 is valid
- ☐ Equal sort values have stable ordering; cart GET still returns an array

**Checkpoint:** why is an explicit primary-key tie-breaker useful when many items have the same price?

---

## Step 10 — Throttling

**Goal:** FR-7 with testable anonymous and authenticated quotas.

**Tasks**

1. Extend the existing settings with AnonRateThrottle, UserRateThrottle and both rates at 5/minute.
2. Confirm registration and token login use the intended anonymous throttle policy in the installed Djoser version.
3. Add isolated throttle tests with a fresh cache; disable throttling in unrelated suites to avoid false failures.
4. Check quotas shared across protected endpoints for one user, and independent between different users.

**Acceptance checks**

- ☐ Five anonymous invalid-credential login attempts → 400; sixth → 429
- ☐ Registration is also covered by anonymous throttling
- ☐ Five permitted requests by an authenticated user → success; sixth → 429
- ☐ The 429 response includes Retry-After
- ☐ Missing token on a protected endpoint remains 401, not an anonymous throttle demonstration
- ☐ Changing rates requires settings changes only
- ☐ Tests do not leak throttle cache state into each other

**Checkpoint:** why do repeated anonymous calls to a protected menu endpoint fail to exercise the normal throttle check?

---

## Step 11 — Error Handling and Status-Code Audit

**Goal:** every documented error is intentional and useful.

**Tasks**

1. Run the complete SRS endpoint/role/method matrix with valid payloads and available quota.
2. Add boundary cases: malformed JSON, non-integer path ID, nonexistent FK, quantity 0/negative/101, excess precision, huge numbers, privilege fields, invalid date/status/order/page values.
3. Verify unsupported methods with an authenticated permitted role, so authentication/permissions do not mask 405.
4. Catch expected validation/protection errors narrowly; let unexpected defects fail tests.

| Scenario | Expected |
|---|---|
| GET, valid update, successful delete, login, existing cart/group POST | 200 |
| Registration, new menu/cart/group/order | 201 |
| Invalid payload/query, empty cart, protected menu deletion | 400 |
| Missing/invalid token on protected route | 401 |
| Valid token, forbidden role/method/Delivery field | 403 |
| Unknown or hidden resource, invalid page | 404 |
| Unsupported method after prerequisite checks pass | 405 |
| Unsupported response format / input media type | 406 / 415 |
| Quota exceeded | 429 with Retry-After |

**Acceptance checks**

- ☐ Every matrix cell and status scenario has test evidence
- ☐ Known invalid inputs produce useful field/detail errors and no unexpected 5xx
- ☐ Successful DELETE uses 200 consistently; no accidental 204 defaults remain
- ☐ No broad exception handler hides programming or infrastructure failures

**Checkpoint:** why is a blanket `except Exception: return 400` misleading?

---

## Step 12 — Performance and Final Verification

**Goal:** NFR-2/NFR-7 and all seven SRS §9 acceptance criteria.

**Tasks**

1. Measure menu/order/group query counts using CaptureQueriesContext or assertNumQueries.
2. Confirm menu category loading and order `items__menuitem__category` prefetching. Compare small and larger datasets within the same page-size cap.
3. Run the full test suite, Django system checks and migration drift check. Fix only issues justified by failures or review.
4. Complete README setup instructions, required environment variables, versions, timezone, group setup, endpoint/payload examples and SQLite concurrency limitation.
5. Record a manual walkthrough: register → login → cart → order → Manager assignment → Delivery status update → Customer reads delivered status.

**Acceptance checks**

- ☐ Query count does not grow per serialized row/item within the tested page
- ☐ Full automated suite passes and each completed step has evidence
- ☐ System check passes; no missing migrations
- ☐ Lockfile and migrations are tracked; no credentials/local database included
- ☐ A fresh setup can follow the README and run the walkthrough
- ☐ Feature issues/PRs provide traceable TDD evidence and the final GitHub Actions run passes

**Verify**

```bash
pipenv run python manage.py check
pipenv run python manage.py makemigrations --check --dry-run
pipenv run python manage.py test
```

Debug Toolbar is an optional aid for suitable HTML responses; automated query measurements are the acceptance evidence.

---

## Requirements Traceability

| Requirement | Primary implementation steps | Verification |
|---|---|---|
| FR-1 authentication | 2 | Real-token auth and route tests; login page walkthrough |
| FR-2 groups | 3, 5 | Group matrix, role conflicts, repeat/remove cases |
| FR-3 menu | 4 | Menu matrix and validation/deletion tests |
| FR-4 cart | 6 | Ownership, replacement, snapshots and boundaries |
| FR-5 orders | 7, 8 | Checkout rollback, visibility and update matrix |
| FR-6 collections | 9 | Filters, ordering, pagination and isolation |
| FR-7 throttling | 10 | Fresh-cache quota and Retry-After tests |
| FR-8 HTTP contract | 11 | Complete matrix/status audit |
| BR-1–BR-11 | 1, 3, 5–8 | Database constraints and business-operation tests |
| NFR-1–NFR-7 | 0–12 | Security cases, reproducible setup, query checks and test evidence |

## Definition of Done

- ☐ All 13 steps complete with recorded checks
- ☐ Every SRS §4 matrix cell verified
- ☐ All seven SRS §9 acceptance criteria satisfied
- ☐ All eleven business rules and SRS §10 clarifications covered
- ☐ Source, migrations and dependency lockfile ready for version control
- ☐ README explains setup, roles, endpoints, token usage and limitations
- ☐ All three planning documents reflect the implemented behavior
- ☐ Application behaviors were developed through observed Red → Green → Refactor cycles
- ☐ GitHub issues, branches, reviewed PRs and passing CI record the development history

**Next action:** verify the development server in the browser, then add issue/PR templates and CI before submitting the scaffold PR for issue #2. Do not mark Step 0 complete until its remaining acceptance checks pass.

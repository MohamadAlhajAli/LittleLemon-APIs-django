# Little Lemon API — Software Requirements Specification (SRS)

**Project:** Little Lemon Restaurant API
**Django app:** `LittleLemonAPI`
**Version:** 1.2
**Status:** Reviewed implementation baseline; implementation not started
**Reviewed:** 2026-09-23

**Document order:** this SRS defines behavior; `02 Design Document.md` explains implementation; `03 Build Plan.md` defines the learning sequence. Changes to behavior must be reflected in all three.

---

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements for a REST API serving the Little Lemon restaurant. The API is consumed by third-party client developers building web and mobile applications. It must support browsing and managing a menu, cart management, order placement, and the delivery workflow — with different capabilities for each user role.

### 1.2 Scope

The system provides:

- User registration and token-based authentication
- Role assignment (Manager, Delivery crew) by managers
- Menu item CRUD, restricted by role
- A per-user shopping cart
- Order placement, browsing, assignment and delivery tracking
- Filtering, searching, ordering and pagination on collection endpoints
- Rate limiting for authenticated and anonymous users

**Out of scope:** payment processing, email/SMS notification, a production frontend, real-time updates, inventory tracking, delivery routing.

### 1.3 Definitions

| Term | Meaning |
|---|---|
| **Token** | A DRF `authtoken` string sent as `Authorization: Token <key>` |
| **Customer** | An authenticated non-superuser in neither application role group |
| **Manager** | An authenticated superuser or member of the `Manager` group |
| **Delivery crew** | An authenticated member of `Delivery crew` who does not resolve to Manager |
| **Anonymous** | An unauthenticated request (no valid token) |
| **Cart** | Temporary per-user storage of menu items before an order is placed |
| **Order** | A placed order; header record with a total and status |
| **Order item** | A line within an order, copied from the cart at placement time |

### 1.4 References

- Course scope reading: *Little Lemon API project requirements*
- Course models video: *Creating the models*
- APIs cheat sheet §1–19 (`Meta Backend/APIs/APIs Cheat Sheet.md`)

The course reading and model video are references, not locally verified source material. The local cheat sheet was reviewed. Preserve the existing endpoint paths until checked against the actual grading rubric in Step 0. Clarifications in §10 are project decisions, not claims about course requirements.

---

## 2. Actors and Roles

| Actor | How identified | Capabilities |
|---|---|---|
| **Anonymous** | No token | Register, obtain a token, open the development login page |
| **Customer** | Valid token, neither application role group, not superuser | Browse menu, manage own cart, place orders, view own orders |
| **Delivery crew** | Valid token, in `Delivery crew` | Browse menu, view **assigned** orders, mark them delivered |
| **Manager** | Valid token, in `Manager` | Menu CRUD, group management, all orders, assign delivery crew, delete orders; cannot place orders |
| **Superuser** | `is_superuser` | Django admin access; treated as a manager by the API |

> **Rule:** resolve roles in this order: superuser → Manager; `Manager` group → Manager; `Delivery crew` group → Delivery crew; otherwise Customer. Unrelated Django groups and `is_staff` do not grant an API role. API assignments reject membership in the other role group with **400**. If admin edits create dual membership, Manager takes precedence; correct the membership in admin.

---

## 3. Functional Requirements

### FR-1 — Authentication and Registration

| ID | Requirement |
|---|---|
| FR-1.1 | An anonymous user **shall** register via `POST /api/users` with `username`, `email`, `password`. Returns **201**. |
| FR-1.2 | A registered user **shall** obtain a token via `POST /token/login/` with `username` and `password`. Returns **200** with `{"auth_token": "..."}`. |
| FR-1.3 | An authenticated user **shall** retrieve their own details via `GET /api/users/users/me/`. Returns **200**. |
| FR-1.4 | All protected endpoints **shall** require the header `Authorization: Token <key>`. |
| FR-1.5 | A request with a missing or invalid token to a protected endpoint **shall** return **401**. |
| FR-1.6 | The system **shall** provide a simple HTML login page (username, password, submit) for manual testing. |

### FR-2 — User Group Management

| ID | Requirement |
|---|---|
| FR-2.1 | A manager **shall** list members of the `Manager` group via `GET /api/groups/manager/users`. Returns **200**. Superusers appear only if members of that group. |
| FR-2.2 | A manager **shall** assign a user to the `Manager` group via `POST /api/groups/manager/users` with `{"username": "..."}`. Returns **201** for new membership, **200** for existing membership. |
| FR-2.3 | A manager **shall** remove a user from the `Manager` group via `DELETE /api/groups/manager/users/{userId}`. Returns **200**, or **404** if the user does not exist. |
| FR-2.4 | FR-2.1 to FR-2.3 **shall** apply identically to `/api/groups/delivery-crew/users` for the `Delivery crew` group. |
| FR-2.5 | Any authenticated non-manager accessing these endpoints **shall** receive **403**; anonymous requests receive **401**. |
| FR-2.6 | A `POST` with a missing or unknown `username` **shall** return **400** or **404** respectively. |
| FR-2.7 | Adding an existing member **shall** return **200** without duplication; adding a member of the other role group **shall** return **400** without changing membership. |
| FR-2.8 | Removing an existing user who is not in the specified group **shall** return **404**. A delivery member with pending assigned orders cannot be removed until those orders are reassigned or unassigned; returns **400**. |

### FR-3 — Menu Items

| ID | Requirement |
|---|---|
| FR-3.1 | Any authenticated user **shall** list menu items via `GET /api/menu-items`. Returns **200**. |
| FR-3.2 | Any authenticated user **shall** retrieve one menu item via `GET /api/menu-items/{id}`. Returns **200**, or **404** if absent. |
| FR-3.3 | A manager **shall** create a menu item via `POST /api/menu-items`. Returns **201**. |
| FR-3.4 | A manager **shall** update a menu item via `PUT` or `PATCH /api/menu-items/{id}`. Returns **200**. |
| FR-3.5 | A manager **shall** delete a menu item via `DELETE /api/menu-items/{id}`. Returns **200**, or **400** if an order item references it, preserving order history. Cart-only references are removed with the menu item. |
| FR-3.6 | A customer or delivery crew member attempting `POST`, `PUT`, `PATCH` or `DELETE` **shall** receive **403**. |
| FR-3.7 | Invalid payloads on write operations **shall** return **400** with field-level error messages. |

### FR-4 — Cart Management

| ID | Requirement |
|---|---|
| FR-4.1 | A customer **shall** view their cart via `GET /api/cart/menu-items`. Returns **200**. |
| FR-4.2 | A customer **shall** add an item via `POST /api/cart/menu-items` with `menuitem` and `quantity`. Returns **201** for a new row or **200** when replacing quantity on an existing row. |
| FR-4.3 | The system **shall** set the cart owner from the **authenticated token**, never from the request body. |
| FR-4.4 | An authenticated user **shall** empty their own cart via `DELETE /api/cart/menu-items`. Returns **200**, including when already empty. |
| FR-4.5 | A user **shall** see and modify **only their own** cart. |
| FR-4.6 | `unit_price` **shall** be copied from the menu item when a cart row is first created; `price` **shall** equal `unit_price × quantity`. |
| FR-4.7 | Adding an existing menu item **shall** replace its quantity, retain its original `unit_price`, recalculate `price`, and return **200**. A new row returns **201**. |
| FR-4.8 | Cart operations **shall** be available to all authenticated roles, always restricted to the caller; only Customers may place orders. |

### FR-5 — Order Management

| ID | Requirement |
|---|---|
| FR-5.1 | A customer **shall** list **their own** orders via `GET /api/orders`. Returns **200**. |
| FR-5.2 | A customer **shall** place an order via `POST /api/orders`. The system moves all cart items into order items, computes the total, then **empties the cart**. Returns **201**. |
| FR-5.3 | `POST /api/orders` with an **empty cart shall** return **400**. |
| FR-5.4 | A customer **shall** retrieve one of their orders with its items via `GET /api/orders/{id}`. Returns **200**. |
| FR-5.5 | A customer requesting another user's order, or delivery crew requesting an order not assigned to them, **shall** receive **404**. |
| FR-5.6 | A manager **shall** list **all** orders via `GET /api/orders`. Returns **200**. |
| FR-5.7 | A manager **shall** assign a delivery crew member and/or set `status` via `PUT`/`PATCH /api/orders/{id}`. Returns **200**. |
| FR-5.8 | A manager **shall** delete an order via `DELETE /api/orders/{id}`. Returns **200**. |
| FR-5.9 | A delivery crew member **shall** list **only orders assigned to them** via `GET /api/orders`. Returns **200**. |
| FR-5.10 | A delivery crew member **shall** update **only** `status` via `PATCH /api/orders/{id}`. Any attempt to change another field **shall** return **403**. |
| FR-5.11 | A delivery crew member **shall not** use `PUT` or `DELETE` on orders — returns **403**. |
| FR-5.12 | Order responses **shall** include the order status and total price. |
| FR-5.13 | Assignment **shall** accept only an active, non-superuser Delivery crew user, or `null` to unassign. Invalid assignments return **400**. |
| FR-5.14 | Order ownership, items, date and amounts **shall** be immutable through order updates. Manager writes to fields other than `delivery_crew` and `status` return **400**; delivery writes to fields other than `status` return **403**. |

### FR-6 — Filtering, Searching, Ordering, Pagination

| ID | Requirement |
|---|---|
| FR-6.1 | `/api/menu-items` **shall** support filtering by `category` and by price range (`to_price` / `from_price`). |
| FR-6.2 | `/api/menu-items` **shall** support searching by `title` (case-insensitive, partial) and category title. |
| FR-6.3 | `/api/menu-items` **shall** support ordering by `price` and `title`, ascending and descending, on multiple fields. |
| FR-6.4 | `/api/orders` **shall** support filtering by `status` (e.g. `?status=1`) and by `date`. |
| FR-6.5 | Menu, order and group lists **shall** use `page` and `perpage` (default 5, maximum 100), with `count`, `next`, `previous`, `results`. The cart is an unpaginated array, capped at 100 distinct items. |
| FR-6.6 | An invalid ordering field **shall** return **400**, never a 500. |

### FR-7 — Throttling

| ID | Requirement |
|---|---|
| FR-7.1 | Anonymous users **shall** be limited to a configured rate (default **5/minute**). |
| FR-7.2 | Authenticated users **shall** be limited to **5/minute**, shared across protected endpoints per user. This is the project baseline, pending rubric verification. |
| FR-7.3 | Exceeding a limit **shall** return **429** with a `Retry-After` header. |
| FR-7.4 | Rates **shall** be configurable in `settings.py`, not hard-coded in views. |

### FR-8 — HTTP Methods and Status Codes

| ID | Requirement |
|---|---|
| FR-8.1 | Each endpoint **shall** accept its specified methods, plus framework `HEAD` for GET routes and `OPTIONS`. Unsupported methods return **405** after authentication, permission and throttle checks pass. |
| FR-8.2 | The system **shall** return the correct status code for every outcome, per §5. |
| FR-8.3 | Expected invalid input and business-rule failures **shall** produce documented 4xx responses. Unexpected defects or infrastructure failures must remain visible as server errors, never be disguised as successful requests or generic 400 responses. |

---

## 4. Complete Endpoint Matrix

Legend: **✓** allowed · **403** forbidden · **—** not applicable

All business endpoints require a valid token; anonymous requests return **401**, including tables without an Anonymous column. Success cells assume valid payloads, business rules satisfied and available throttle quota. Detailed FR rules define validation exceptions.

### 4.1 Authentication (Djoser)

| Endpoint | Method | Anonymous | Customer | Delivery | Manager |
|---|---|---|---|---|---|
| `/api/users` | POST | ✓ 201 | ✓ | ✓ | ✓ |
| `/api/users/users/me/` | GET | 401 | ✓ 200 | ✓ 200 | ✓ 200 |
| `/token/login/` | POST | ✓ 200 | ✓ | ✓ | ✓ |

### 4.2 Menu items

| Endpoint | Method | Anonymous | Customer | Delivery | Manager |
|---|---|---|---|---|---|
| `/api/menu-items` | GET | 401 | ✓ 200 | ✓ 200 | ✓ 200 |
| `/api/menu-items` | POST | 401 | **403** | **403** | ✓ 201 |
| `/api/menu-items/{id}` | GET | 401 | ✓ 200 | ✓ 200 | ✓ 200 |
| `/api/menu-items/{id}` | PUT / PATCH | 401 | **403** | **403** | ✓ 200 |
| `/api/menu-items/{id}` | DELETE | 401 | **403** | **403** | ✓ 200 |

### 4.3 Group management

| Endpoint | Method | Customer | Delivery | Manager |
|---|---|---|---|---|
| `/api/groups/manager/users` | GET | **403** | **403** | ✓ 200 |
| `/api/groups/manager/users` | POST | **403** | **403** | ✓ 201 new / 200 existing |
| `/api/groups/manager/users/{userId}` | DELETE | **403** | **403** | ✓ 200 / 404 |
| `/api/groups/delivery-crew/users` | GET | **403** | **403** | ✓ 200 |
| `/api/groups/delivery-crew/users` | POST | **403** | **403** | ✓ 201 new / 200 existing |
| `/api/groups/delivery-crew/users/{userId}` | DELETE | **403** | **403** | ✓ 200 / 404 |

### 4.4 Cart

| Endpoint | Method | Customer | Delivery | Manager |
|---|---|---|---|---|
| `/api/cart/menu-items` | GET | ✓ 200 (own) | ✓ (own) | ✓ (own) |
| `/api/cart/menu-items` | POST | ✓ 201 new / 200 existing | ✓ same | ✓ same |
| `/api/cart/menu-items` | DELETE | ✓ 200 (own) | ✓ | ✓ |

> The cart endpoint is scoped by token, so every role technically has a cart; only customers are expected to use it.

### 4.5 Orders

| Endpoint | Method | Customer | Delivery | Manager |
|---|---|---|---|---|
| `/api/orders` | GET | ✓ own orders | ✓ assigned orders | ✓ all orders |
| `/api/orders` | POST | ✓ 201 (from cart) | **403** | **403** |
| `/api/orders/{id}` | GET | ✓ own, else 404 | ✓ assigned, else 404 | ✓ any |
| `/api/orders/{id}` | PUT | **403** | **403** | ✓ 200 |
| `/api/orders/{id}` | PATCH | **403** | ✓ **status only** | ✓ 200 |
| `/api/orders/{id}` | DELETE | **403** | **403** | ✓ 200 |

---

## 5. Status Code Contract

| Code | When |
|---|---|
| **200 OK** | Successful GET, PUT, PATCH, DELETE, login, existing cart/group POST |
| **201 Created** | Successful POST that creates a resource |
| **400 Bad Request** | Validation failure on POST/PUT/PATCH; empty cart on order placement; invalid ordering field |
| **401 Unauthorized** | **Authentication** failed — missing, malformed or invalid token |
| **403 Forbidden** | **Authorization** failed — valid token, insufficient role |
| **404 Not Found** | Resource does not exist or is outside the caller's visible queryset; invalid/out-of-range page |
| **405 Method Not Allowed** | Method not supported by the endpoint |
| **429 Too Many Requests** | Throttle limit exceeded |

Use standard HTTP meanings: authentication → **401**, authorization → **403**. Invalid login credentials return **400** from Djoser. Malformed JSON returns **400**; unsupported media types may return **415**, and unacceptable response formats may return **406**. Success on DELETE uses **200** with `{"detail": "Deleted successfully."}`; generic DRF deletion must be overridden to meet this contract.

---

## 6. Business Rules

| ID | Rule |
|---|---|
| BR-1 | API role assignments enforce **at most one** application role group; role resolution and the superuser exception follow §2. |
| BR-2 | A user has **at most one cart** at a time (enforced as a set of cart rows owned by that user). |
| BR-3 | A cart has at most 100 distinct items and **one row per menu item**; repeated POST replaces quantity, never increments it. |
| BR-4 | An order **may contain multiple** menu items, but **only one order-item row per menu item**. |
| BR-5 | Placing an order **atomically** copies cart → order items, computes the total, and **clears the cart**. Partial completion is not permitted. |
| BR-6 | `unit_price` is **snapshotted** at cart-add time; later menu price changes do not alter existing carts or orders. |
| BR-7 | `status = 0` means pending / out for delivery; `status = 1` means delivered. Default is `0`. |
| BR-8 | Only a **manager** may assign a delivery crew member to an order. |
| BR-9 | A delivery crew member may change **only** `status`, and only on orders assigned to them. |
| BR-10 | A category **cannot be deleted** while menu items reference it. |
| BR-11 | The cart/order **owner** is always taken from the token. Manager group targets and delivery assignments are separate, explicitly validated user references. |

---

## 7. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | **Security** — passwords hashed by Django; tokens never logged; user input sanitized; no raw SQL built by string interpolation. |
| NFR-2 | **Performance** — list endpoints avoid N+1 queries; verify with automated query-count checks. Debug Toolbar is an optional development aid. |
| NFR-3 | **Scalability** — menu, order and group lists are paginated; cart size is bounded as in FR-6.5. |
| NFR-4 | **Maintainability** — one app (`LittleLemonAPI`); permissions in a dedicated module; throttle rates in settings. |
| NFR-5 | **Portability** — dependencies managed by `pipenv`; `Pipfile.lock` committed. GitHub Actions installs locked dependencies and runs system checks, migration checks and tests on pull requests once the scaffold exists. |
| NFR-6 | **Usability** — DRF browsable API enabled in development for manual testing. |
| NFR-7 | **Testability** — develop application behavior using TDD: observe a failing test, implement the minimum behavior, then refactor with tests passing. Every endpoint × role × method combination in §4 is covered by automated tests; manual checks complement them for the login page and learning exercises. |

---

## 8. Assumptions and Constraints

- Database is **SQLite** for sequential local coursework. Atomic rollback is required; concurrent checkout guarantees require a database supporting row locks and separate concurrency tests (Design §6.3).
- A single Django app named **`LittleLemonAPI`** holds all API code (project constraint).
- Groups `Manager` and `Delivery crew` are created manually via the Django admin.
- Token authentication only; JWT is explicitly **not** used.
- The HTML login page is a development aid, not a production frontend.
- Categories are managed through Django admin; category API endpoints are outside this baseline.
- Prefer a supported Django LTS compatible with DRF, Djoser and the available Python runtime; confirm any course version requirement in Step 0.

---

## 9. Acceptance Criteria

The project is complete when:

1. Every cell in the §4 matrix behaves exactly as specified, verified by test.
2. Every status code in §5 is produced by at least one real request.
3. All eleven business rules in §6 hold under test, including the atomic cart→order transfer.
4. Menu lists support filtering, search, ordering and pagination; order lists support filtering, ordering and pagination; group lists support pagination.
5. Throttling returns **429** with `Retry-After` once the configured rate is exceeded.
6. Documented invalid-input and authorization cases return the expected 4xx codes, with no unexpected 5xx in the acceptance suite.
7. No list endpoint exhibits an N+1 query pattern.

---

## 10. Clarified Contracts for Implementation

These decisions resolve gaps in version 1.0. Keep them synchronized with the design and tests.

| Area | Contract |
|---|---|
| Paths | Preserve the exact paths in §4, including `/api/users/users/me/`. Business endpoints and registration have no trailing slash; login and current-user paths have one. Do not depend on redirects for POST. |
| Registration | Require username, valid email and password; use Django password validators. New users receive no role group. Never accept privilege fields such as `is_staff`, `is_superuser` or `groups`. |
| Cart payload | Accept only `menuitem` (existing ID) and integer `quantity` from 1 to 100. Unknown/server-owned fields return **400**. New rows snapshot the current menu price; repeat POST retains the original snapshot. |
| Money | Nonnegative amounts; menu and unit prices at most `9999.99`, with two decimal places. Use Decimal arithmetic and decimal strings in JSON. Line prices and order totals have wider storage than unit prices. Currency conversion, tax and delivery fees are outside scope. |
| Menu payload | `title` (nonblank, max 255), `price`, `category_id` (existing ID), `featured` (default false). PUT requires all four; PATCH changes supplied fields. Nested `category` is response-only. |
| Order creation | Empty body or `{}` only; the server supplies owner, date, status, items and total. Reject supplied order fields with **400**. |
| Order updates | Manager PUT requires both `delivery_crew` and `status`; PATCH requires at least one. Delivery PATCH requires `status`. Empty update payloads return **400**. |
| Status | Accept JSON booleans or integers 0/1, emit booleans. Both roles authorized to update status may set either value; repeated updates are allowed. No terminal-state restriction is assumed. Manager may mark an unassigned order delivered. |
| Filters | Menu: `category=<slug>`, `from_price`, `to_price`; order: `status=0/1`, `date=YYYY-MM-DD`. Invalid values or reversed price bounds return **400**. Unknown category slug gives an empty list. |
| Ordering | Menu allows `price,title`; orders allow `date,total`, with optional `-` and comma-separated fields. Reject unknown fields with **400**. Append an internal primary-key tie-breaker for stable pagination. |
| Pagination | Default ordering: menu/group `id`, orders `-date,-id`. Positive `perpage` values over 100 are capped; malformed/nonpositive `perpage` returns **400**. Invalid/nonpositive/out-of-range `page` returns **404**. Empty page 1 is valid. |
| Error bodies | Field validation uses field-name keys and message lists; general errors use `detail` or `non_field_errors`. Error prose need not be byte-identical except where a response is explicitly specified. |

**Learning workflow:** implementation proceeds one step at a time, using the Red → Green → Refactor cycle. Each small feature is linked to a GitHub issue, developed on a short-lived branch, and reviewed through a pull request with passing checks before merge. Explain Git commands and their effects so the user can practice them. Record test evidence and pause before the next step. Repository setup precedes Step 0; all implementation steps remain unstarted after this document review. Details are in the Build Plan's TDD and GitHub workflow sections.

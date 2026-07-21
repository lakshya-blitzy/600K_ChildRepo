# 600K_ChildRepo

A minimal **Flask** web application that serves, over HTTP, the exact same
output the original console program printed to stdout. This is the child
submodule of the `600K_ParentRepo` project; it runs standalone and is fully
self-contained.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup / Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Code Overview (Inline Explanations)](#code-overview-inline-explanations)
- [Deployment Guide](#deployment-guide)
- [Project Structure](#project-structure)
- [Notes](#notes)

---

## Overview

This repository was migrated from a standard-library console program into a
Flask WSGI web application. The migration changed **only the I/O channel** —
results that were previously written to stdout with `print()` are now returned
as the body of an HTTP response. The input, the computation, and the output
ordering are preserved verbatim, so the observable result is identical to the
original program.

The computation is fully deterministic: it operates on the fixed, hard-coded
input `[10, 20, 30, 40]` and takes no configuration, environment variables, or
request parameters.

## Requirements

- **Python 3.9+** (this project targets Python 3.12; it is verified to run on
  the CPython 3.13 host as well).
- **Flask 3.1.3** — the only direct dependency, pinned in `requirements.txt`.
  Installing Flask automatically pulls its transitive dependencies (Werkzeug,
  Jinja2, MarkupSafe, ItsDangerous, Click, and Blinker).

## Setup / Installation

Create and activate an isolated virtual environment, then install the pinned
dependency from the manifest:

```bash
# 1. Create a virtual environment in the repository directory
python -m venv .venv

# 2. Activate it
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows (PowerShell/cmd)

# 3. Install the dependency
pip install -r requirements.txt
```

> **Clean-environment note.** On some hosts `python -m venv .venv` fails while
> bootstrapping pip (an `ensurepip` / "No module named pip" error). If that
> happens, create the environment *without* pip, bootstrap the tooling
> explicitly, and then install the dependency:
>
> ```bash
> python -m venv .venv --without-pip
> python -m pip --python .venv/bin/python install --upgrade pip setuptools wheel
> .venv/bin/python -m pip install -r requirements.txt
> ```

Verify the installation:

```bash
pip show flask        # should report Version: 3.1.3
pip check             # should report: No broken requirements found.
```

## Running the Application

Start the built-in Flask development server in either of the two supported
ways:

```bash
python app.py
# or
flask run
```

Both commands launch Werkzeug's development server, which listens on
`http://127.0.0.1:5000/` by default. Because `app.py` exposes a module-level
`app` object, the `flask` CLI auto-detects it; you can also be explicit:

```bash
flask --app app run
```

To use a different port (useful when running several apps side by side):

```bash
flask --app app run --port 5001
```

Stop the server with `Ctrl+C`.

## API Documentation

The application exposes exactly one endpoint.

### `GET /`

| Property        | Value                                                        |
|-----------------|--------------------------------------------------------------|
| Method          | `GET`                                                        |
| Path            | `/`                                                          |
| Query params    | None                                                         |
| Request body    | None                                                         |
| Success status  | `200 OK`                                                     |
| Content-Type    | `text/plain; charset=utf-8`                                  |
| Response body   | The six lines shown below, in this exact order              |

**Response body**

```text
Total: 100
10
20
30
40
Application completed
```

- Line 1 — `Total: <sum>`: the running sum of the fixed input `[10, 20, 30, 40]`,
  which is `100`.
- Lines 2–5 — each input number on its own line, in order.
- Line 6 — the `Application completed` completion marker.

**Example request**

```bash
curl -s http://127.0.0.1:5000/
```

**Example response**

```text
Total: 100
10
20
30
40
Application completed
```

Any path other than `/` returns Flask's standard `404 Not Found`, and any
method other than `GET`/`HEAD` on `/` returns `405 Method Not Allowed` — both
are the framework defaults; no custom error handlers are defined.

## Code Overview (Inline Explanations)

The application is intentionally tiny: two modules that sit side by side at the
repository root.

### `app.py` — the Flask server

```python
from flask import Flask
from service import calculate_total          # pure business logic (no HTTP)


def create_app():                            # application-factory pattern
    app = Flask(__name__, static_folder=None)  # no static route (single endpoint)

    @app.route("/")                          # register the one GET route
    def index():
        numbers = [10, 20, 30, 40]           # fixed, deterministic input
        total = calculate_total(numbers)     # delegate the sum to the service layer
        lines = [f"Total: {total}"]          # line 1: the summary
        lines += [str(number) for number in numbers]  # lines 2-5: each number
        lines.append("Application completed")          # line 6: completion marker
        body = "\n".join(lines)              # join with newlines -> plain text
        return body, 200, {"Content-Type": "text/plain; charset=utf-8"}

    return app                               # hand back the configured app


app = create_app()                           # module-level WSGI app for `flask run`


if __name__ == "__main__":
    app.run()                                # direct-run affordance: `python app.py`
```

Key points:

- **Application factory (`create_app`)** — building the app inside a function
  avoids import-time global side effects and makes the app easy to instantiate
  in tests, e.g. `create_app().test_client()`.
- **`static_folder=None`** — disables Flask's default `/static/<path>` route so
  the URL map contains only the single intended endpoint.
- **`index` view** — reproduces the original `main()` workflow exactly and
  returns the result as `text/plain` so `curl`/browsers show the raw lines with
  no HTML wrapper.
- **Module-level `app`** — lets the `flask` CLI and external WSGI servers
  discover the application, while the `__main__` guard keeps `python app.py`
  working.

### `service.py` — the business logic (framework-agnostic)

```python
def calculate_total(numbers):
    total = 0
    for number in numbers:
        total += number          # accumulate a running sum
    return total

def calculate_average(numbers):
    if not numbers:
        return 0                 # falsey input -> integer 0
    return calculate_total(numbers) / len(numbers)   # otherwise a float average
```

`service.py` has no knowledge of Flask or HTTP — it is a pure computation
module. `calculate_average` is retained for parity with the original project
even though the web layer does not call it.

## Deployment Guide

### Development

For local development and evaluation, the built-in server is sufficient:

```bash
python app.py           # or: flask --app app run
```

> **Do not use the development server in production.** Werkzeug's built-in
> server is single-worker and intended for development only.

### Production (WSGI server)

For production, serve the module-level `app` (or the `create_app` factory) with
a dedicated WSGI server. These servers are **not** listed in `requirements.txt`
(the manifest pins only Flask); install whichever you prefer separately.

**Gunicorn** (Linux/macOS):

```bash
pip install gunicorn
# "app:app" = module `app.py`, object `app`
gunicorn --bind 0.0.0.0:8000 --workers 4 "app:app"
# or call the factory directly:
gunicorn --bind 0.0.0.0:8000 --workers 4 "app:create_app()"
```

**Waitress** (cross-platform, incl. Windows):

```bash
pip install waitress
waitress-serve --host 0.0.0.0 --port 8000 --call app:create_app
```

### Notes for deployment

- The application is **stateless** and reads no configuration, environment
  variables, or secrets, so it scales horizontally without coordination.
- Choose the worker count based on the host's CPU cores; a common starting
  point is `(2 x cores) + 1`.
- Place a reverse proxy (e.g. Nginx) in front of the WSGI server if you need
  TLS termination, compression, or static asset handling (this app serves no
  static assets).

## Project Structure

```text
600K_ChildRepo/
├── app.py             # Flask application: create_app() factory + GET "/" route
├── service.py         # Business logic: calculate_total / calculate_average
├── requirements.txt   # Dependency manifest: Flask==3.1.3
├── README.md          # This document
├── .gitmodules        # Submodule wiring (NestedChild)
├── .blitzyignore      # Ignore rules
└── NestedChild/       # Nested submodule (its own standalone Flask app)
```

## Notes

- The response body is the single source of truth for behavior parity: it
  equals the original console program's stdout output, line for line.
- The input is hard-coded and the computation is deterministic — the endpoint
  returns the same six lines on every request.
- This repository contains a nested submodule, `NestedChild`, which is itself a
  standalone Flask application with its own `README.md` and `requirements.txt`.

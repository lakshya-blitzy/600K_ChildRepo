# 600K_ChildRepo

A minimal Flask web application that serves, over HTTP, the same output the
original console program printed.

## Requirements

- Python 3.9+ (this project targets Python 3.12)
- Flask 3.1.3 (installed via the manifest)

## Installation

Create and activate a virtual environment, then install the dependency:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If `python -m venv .venv` fails while bootstrapping pip (an `ensurepip`/pip
error on some hosts), create it without pip and bootstrap the tooling first:

```bash
python -m venv .venv --without-pip
python -m pip --python .venv/bin/python install pip setuptools wheel
.venv/bin/python -m pip install -r requirements.txt
```

## Running

Start the development server in either of the following ways:

```bash
python app.py
# or
flask run
```

The development server listens on `http://127.0.0.1:5000/` by default.

## Usage

The application exposes a single endpoint:

- `GET /` — returns a `text/plain` body reproducing the original program output.

The response body is exactly:

```text
Total: 100
10
20
30
40
Application completed
```

For example:

```bash
curl http://127.0.0.1:5000/
```

This returns the plain-text block shown above.

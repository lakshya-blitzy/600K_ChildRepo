"""Flask web application entry point for the ``600K_ChildRepo`` child submodule.

This module is the *server* for the child repository. It was migrated from a
standard-library console program (which wrote its results to stdout via
``print``) into a Flask WSGI web application that serves the **identical**
content over HTTP. Only the I/O channel changed (stdout -> HTTP response body);
the fixed input, the computation, and the output ordering are preserved
verbatim, so behavior parity with the original program is exact.

Architecture
------------
* **Application Factory** (:func:`create_app`) constructs and returns a fully
  configured :class:`flask.Flask` instance. Building the app inside a function
  (rather than at import time) avoids global import-time side effects and makes
  the application easy to instantiate repeatedly in tests
  (for example, ``create_app().test_client()``).
* **Service layer** (``service.py``, imported below) owns the pure business
  logic and has no awareness of Flask or HTTP. The web layer calls into it.
* **Route / view handler** (the nested ``index`` view) performs exactly what the
  original ``main()`` routine did and returns the result as the HTTP response
  body.

Run this module directly (``python app.py``) to start Flask's built-in
development server, or point a WSGI server / the ``flask`` CLI at the
module-level :data:`app` object (``flask --app app run``).
"""

# Third-party framework import: Flask provides the WSGI application object,
# URL routing, and the development server used to serve the single endpoint.
from flask import Flask

# Local service-layer import, preserved verbatim from the original program.
# ``service.py`` sits beside this module at the repository root, so this is a
# top-level, non-package import that resolves from the script's own directory.
from service import calculate_total


def create_app():
    """Build, configure, and return the Flask application instance.

    This is the Flask *application factory*. It creates the application object
    and registers every route, then hands back the ready-to-serve instance. No
    web server is started here -- starting the server is the caller's
    responsibility (see the ``__main__`` guard at the bottom of this file, or an
    external WSGI server such as gunicorn/waitress in production).

    Returns:
        flask.Flask: A configured application exposing a single ``GET /`` route.
    """
    # ``static_folder=None`` disables Flask's default
    # ``/static/<path:filename>`` route. This application serves no static
    # assets and exposes exactly one endpoint, so removing the extra route
    # keeps the URL map limited to the single intended route (AAP 0.2.2 /
    # 0.3.3 -- no scope creep).
    app = Flask(__name__, static_folder=None)

    @app.route("/")
    def index():
        """Handle ``GET /`` and reproduce the original ``main()`` output.

        The response body is assembled line-for-line so that it equals the
        former stdout output exactly, then returned as ``text/plain`` so that a
        browser or ``curl`` renders the raw lines without any HTML wrapper.

        Returns:
            tuple: A ``(body, status_code, headers)`` triple where ``body`` is
            the newline-joined text, ``status_code`` is ``200`` (HTTP OK), and
            ``headers`` forces a UTF-8 plain-text content type.
        """
        # Fixed, deterministic input -- unchanged from the original console
        # program (AAP 0.7.1 preserves determinism; no request parameters,
        # environment variables, or configuration influence the result).
        numbers = [10, 20, 30, 40]

        # Delegate the running-sum computation to the service layer. For the
        # fixed input above this evaluates to 100.
        total = calculate_total(numbers)

        # Assemble the response body in the EXACT order the console printed it:
        #   1) the "Total: {total}" summary line,
        #   2) each input number on its own line, in order,
        #   3) the "Application completed" completion line.
        lines = [f"Total: {total}"]
        lines += [str(number) for number in numbers]
        lines.append("Application completed")
        body = "\n".join(lines)

        # Return an explicit (body, status, headers) tuple. Plain text
        # guarantees the numbers and text lines appear verbatim, matching the
        # original stdout content line-for-line.
        return body, 200, {"Content-Type": "text/plain; charset=utf-8"}

    return app


# Module-level WSGI application instance. Exposing ``app`` at module scope lets
# the ``flask`` CLI (``flask --app app run``) and external WSGI servers discover
# it, while the ``__main__`` guard below still supports ``python app.py``.
app = create_app()


if __name__ == "__main__":
    # Direct-run affordance (preserved from the original program): launch
    # Flask's built-in development server. It listens on http://127.0.0.1:5000/
    # by default. This call replaces the original ``main()`` invocation.
    app.run()

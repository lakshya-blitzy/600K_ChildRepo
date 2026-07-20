from flask import Flask
from service import calculate_total


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        numbers = [10, 20, 30, 40]
        total = calculate_total(numbers)
        lines = [f"Total: {total}"]
        lines += [str(number) for number in numbers]
        lines.append("Application completed")
        body = "\n".join(lines)
        return body, 200, {"Content-Type": "text/plain; charset=utf-8"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

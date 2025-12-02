from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        result = None

        if request.method == "POST":
            email_text = request.form.get("email_text", "").strip()

            if email_text:
                result = {
                    "email_text": email_text,
                    "label": "phishing (demo only)",
                    "probability": 0.5,
                }

        return render_template("index.html", result=result)

    return app

from flask import Flask, render_template, request
import pandas as pd
from analysis import run_analysis

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    results = None
    error = None

    if request.method == "POST":
        try:
            file = request.files["file"]

            if not file or not file.filename.endswith(".csv"):
                raise ValueError("PLEASE UPLOAD A VALID CSV FILE")

            data = pd.read_csv(file)
            results = run_analysis(data)

        except Exception as e:
            error = str(e)

    return render_template(
        "dashboard.html",
        results=results,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)


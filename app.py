from flask import Flask, render_template
from analysis import analyze_sales

app = Flask(__name__)

@app.route("/")
def dashboard():
    results = analyze_sales()
    return render_template("dashboard.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)


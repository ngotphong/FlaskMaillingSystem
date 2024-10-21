from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from controlSending import customHTMLEmail

load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a strong key


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        doc_url = request.form["doc_url"]
        sheet_url = request.form["sheet_url"]
        sheet_title = request.form["sheet_title"]
        subject = request.form["subject"]

        try:
            customHTMLEmail(
                docURL=doc_url,
                sheetURL=sheet_url,
                sheetTitle=sheet_title,
                subject=subject,
            )
            flash("Emails sent successfully!", "success")
            return redirect(url_for("success"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)

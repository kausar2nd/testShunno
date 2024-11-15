from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def signup():
    return render_template("all_login.html")


@app.route("/user_login")
def user_login():
    return render_template("user_login.html")


@app.route("/user_signup")
def user_signup():
    return render_template("user_signup.html")


@app.route("/company_login")
def company_login():
    return render_template("company_login.html")


@app.route("/company_signup")
def company_signup():
    return render_template("company_signup.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")

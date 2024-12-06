from flask import Flask, render_template, session, request, url_for, redirect, flash
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

app.secret_key = "your secret key"


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="alteruse_users"
    )
    return connection


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def all_login():
    return render_template("all_login.html")


@app.route("/user_signup", methods=["POST", "GET"])
def user_signup():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            account = cursor.fetchone()

            if account:
                flash("Account already exists!")
            else:
                cursor.execute(
                    "INSERT INTO users (name, email, password, location) VALUES (%s, %s, %s, %s)",
                    (name, email, password, location),
                )
                print("Account created successfully!")
                conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

        return redirect(url_for("user_login"))

    return render_template("user_signup.html")


@app.route("/user_login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            account = cursor.fetchone()

            if account[3] == password:
                print("Password matched!")
                session["loggedin"] = True
                session["id"] = account[0]
                session["username"] = account[1]
                print("Logged in successfully!")
                return redirect(url_for("user_dashboard"))
            else:
                print("Incorrect username/password!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return render_template("user_login.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "loggedin" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for("user_login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/user_dashboard")
@login_required
def user_dashboard():
    username = session.get("username", "User")
    return render_template("user_dashboard.html", username=username)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    print("You have been logged out.")
    return redirect(url_for("user_login"))


@app.route("/company_signup", methods=["POST", "GET"])
def company_signup():
    if request.method == "POST":
        company_name = request.form["company_name"]
        location = request.form["location"]
        email = request.form["email"]
        password = request.form["password"]

        print(company_name, location, email, password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies WHERE email = %s", (email,))
            account = cursor.fetchone()

            if account:
                flash("Company account already exists!")
            else:
                cursor.execute(
                    "INSERT INTO companies (company_name, location, email, password) VALUES (%s, %s, %s, %s)",
                    (company_name, location, email, password),
                )
                print("Company account created successfully!")
                conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

        return redirect(url_for("company_login"))

    return render_template("company_signup.html")


@app.route("/company_login", methods=["POST", "GET"])
def company_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies WHERE email = %s", (email,))
            account = cursor.fetchone()

            if account[4] == password:
                print("Password matched!")
                session["loggedin"] = True
                session["company_id"] = account[0]
                session["company_name"] = account[1]
                print("Company logged in successfully!")
                return redirect(url_for("company_dashboard"))
            else:
                print("Incorrect email/password!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return render_template("company_login.html")


@app.route("/find_bins")
def find_bins():
    return render_template("find_bins.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")

from flask import Flask, render_template, session, request, url_for, redirect, flash
import mysql.connector
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
                session["email"] = account[2]
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
    username = session.get("username", "John Doe")
    email = session.get("email", "john@example.com")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user information
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        joined = cursor.fetchone()

        # Fetch user submission history
        cursor.execute(
            "SELECT sub_date, sub_description, sub_branch FROM user_submission_history WHERE user_email = %s ORDER BY sub_date DESC LIMIT 5",
            (email,),
        )
        submissions = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        joined = None
        submissions = []
    finally:
        conn.close()

    return render_template(
        "user_dashboard.html",
        username=username,
        email=email,
        joined=joined,
        submissions=submissions,
    )


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
                session["company_email"] = email
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


@app.route("/user_submit", methods=["POST", "GET"])
@login_required
def user_submit():
    if request.method == "POST":
        branch = request.form["branch"]
        plastic_quantity = request.form.get("plastic-quantity", 0, type=int)
        cardboard_quantity = request.form.get("cardboard-quantity", 0, type=int)
        glass_quantity = request.form.get("glass-quantity", 0, type=int)
        user_email = session.get("email")

        if not user_email:
            flash("Please log in to submit an order.")
            return redirect(url_for("user_login"))

        sub_description = (
            f"Plastic Bottles: {plastic_quantity}, "
            f"Cardboard: {cardboard_quantity}, "
            f"Glass: {glass_quantity}"
        )

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO user_submission_history (user_email, sub_description, sub_branch) VALUES (%s, %s, %s)",
                (user_email, sub_description, branch),
            )

            cursor.execute(
                """
                UPDATE storage
                SET
                    plastic = plastic + %s,
                    cardboard = cardboard + %s,
                    glass = glass + %s
                """,
                (plastic_quantity, cardboard_quantity, glass_quantity),
            )

            conn.commit()
            flash("Submission successful!")
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred during submission.")
        finally:
            conn.close()

        return redirect(url_for("user_dashboard"))

    return render_template("user_dashboard.html")


@app.route("/company_dashboard")
@login_required
def company_dashboard():
    """Dashboard for the logged-in company user."""
    company_name = session.get("company_name", "Company")
    company_email = session.get("company_email", "Email")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch current stock information from the storage table
        cursor.execute("SELECT Plastic, Cardboard, Glass FROM storage LIMIT 1")
        stock_data = cursor.fetchone()
        stock = {
            "Plastic": stock_data[0],
            "Cardboard": stock_data[1],
            "Glass": stock_data[2],
        }

        # Fetch company's order history from the company_order_history table
        cursor.execute(
            """
            SELECT order_date, order_description
            FROM company_order_history
            WHERE company_email = %s
            ORDER BY order_date DESC LIMIT 5
            """,
            (company_email,),
        )
        history_data = cursor.fetchall()
        history_data = [
            {"order_date": row[0], "order_description": row[1]} for row in history_data
        ]

    except Exception as e:
        print(f"Error: {e}")
        stock = {"Plastic": 0, "Cardboard": 0, "Glass": 0}
        history_data = []
    finally:
        conn.close()

    return render_template(
        "company_dashboard.html",
        company_name=company_name,
        stock_data=stock,
        history_data=history_data,
    )


@app.route("/company_submit", methods=["POST"])
@login_required
def company_submit():
    """Handles the company's order submission."""
    if request.method == "POST":
        plastic_quantity = request.form.get("plasticBottles", 0, type=int)
        cardboard_quantity = request.form.get("cardboard", 0, type=int)
        glass_quantity = request.form.get("glass", 0, type=int)
        company_email = session.get("company_email")  # Fetch logged-in company's email

        if not company_email:
            flash("Please log in to submit an order.")
            return redirect(url_for("company_login"))

        # Create order description
        order_description = (
            f"Plastic Bottles: {plastic_quantity}, "
            f"Cardboard: {cardboard_quantity}, "
            f"Glass: {glass_quantity}"
        )
        print(order_description)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert the order into the company_order_history table
            cursor.execute(
                """
                INSERT INTO company_order_history (company_email, order_description)
                VALUES (%s, %s)
                """,
                (company_email, order_description),
            )

            # Update the storage table to reduce stock quantities
            cursor.execute(
                """
                UPDATE storage
                SET
                    plastic = plastic - %s,
                    cardboard = cardboard - %s,
                    glass = glass - %s
                """,
                (plastic_quantity, cardboard_quantity, glass_quantity),
            )

            conn.commit()
            flash("Order placed successfully!")
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while placing the order.")
        finally:
            conn.close()

        return redirect(url_for("company_dashboard"))

    return render_template("company_dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")

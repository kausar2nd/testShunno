from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.db_utils import get_db_connection
from app.utils.auth_utils import login_required

company_bp = Blueprint("company", __name__)


@company_bp.route("/company_submit", methods=["POST"])
@login_required
def company_submit():
    if request.method == "POST":
        plastic_quantity = request.form.get("plasticBottles", 0, type=int)
        cardboard_quantity = request.form.get("cardboard", 0, type=int)
        glass_quantity = request.form.get("glass", 0, type=int)
        company_email = session.get("company_email")

        if not company_email:
            flash("Please log in to submit an order.")
            return redirect(url_for("company_login"))

        company_history_description = (
            f"Plastic Bottles: {plastic_quantity}, "
            f"Cardboard: {cardboard_quantity}, "
            f"Glass: {glass_quantity}"
        )
        print(company_history_description)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO company_history (company_email, company_history_description) VALUES (%s, %s)",
                (company_email, company_history_description),
            )

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

        except Exception as e:
            print(f"Error: {e}")

        finally:
            conn.close()

        return redirect(url_for("company.company_dashboard"))

    return render_template("company_dashboard.html")


@company_bp.route("/company_signup", methods=["POST", "GET"])
def company_signup():
    if request.method == "POST":
        company_name = request.form["company_name"]
        company_location = request.form["company_location"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies WHERE email = %s", (email,))
            account = cursor.fetchone()

            if account:
                flash("Company account already exists!")
            else:
                cursor.execute(
                    "INSERT INTO companies (company_name, company_location, email, password) VALUES (%s, %s, %s, %s)",
                    (company_name, company_location, email, password),
                )
                print("Company account created successfully!")
                conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
        return redirect(url_for("company.company_login"))
    return render_template("company_signup.html")


@company_bp.route("/company_login", methods=["POST", "GET"])
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
                return redirect(url_for("company.company_dashboard"))
            else:
                print("Incorrect email/password!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return render_template("company_login.html")


@company_bp.route("/company_dashboard")
@login_required
def company_dashboard():
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

        cursor.execute(
            """
            SELECT order_date, company_history_description
            FROM company_history
            WHERE company_email = %s
            ORDER BY order_date DESC LIMIT 5
            """,
            (company_email,),
        )
        history_data = cursor.fetchall()
        history_data = [
            {"order_date": row[0], "company_history_description": row[1]}
            for row in history_data
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

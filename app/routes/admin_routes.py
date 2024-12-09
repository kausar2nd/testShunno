from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.db_utils import get_db_connection
from app.utils.auth_utils import login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/superuser", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT email FROM admin WHERE email = %s AND password = %s",
                (email, password),
            )

            admin = cursor.fetchone()

            if admin:
                session["email"] = email
                return redirect(url_for("admin.admin_dashboard"))
            else:
                flash("Invalid email or password.")

        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred during login.")

        finally:
            conn.close()

    return render_template("admin_login.html")


@admin_bp.route("/admin_dashboard", methods=["POST", "GET"])
# @login_required
def admin_dashboard():
    email = session.get("email", "admin@example.com")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, location, joining_date FROM users")
        users = cursor.fetchall()
        cursor.execute(
            "SELECT company_name, email, location, joining_date FROM companies"
        )
        companies = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        users = []
        companies = []

    finally:
        conn.close()

    return render_template(
        "admin_dashboard.html",
        email=email,
        users=users,
        companies=companies,
    )

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.db_utils import get_db_connection
from app.utils.auth_utils import login_required

user_bp = Blueprint("user", __name__)


@user_bp.route("/user_submit", methods=["POST", "GET"])
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

        return redirect(url_for("user.user_dashboard"))

    return render_template("user_dashboard.html")


@user_bp.route("/user_signup", methods=["POST", "GET"])
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

        return redirect(url_for("user.user_login"))

    return render_template("user_signup.html")


@user_bp.route("/user_login", methods=["POST", "GET"])
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
                return redirect(url_for("user.user_dashboard"))
            else:
                print("Incorrect username/password!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return render_template("user_login.html")


@user_bp.route("/user_dashboard")
@login_required
def user_dashboard():
    username = session.get("username", "John Doe")
    email = session.get("email", "john@example.com")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        joined = cursor.fetchone()

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

from flask import Blueprint, render_template, request, redirect, url_for, session
from app.utils.db_utils import get_db_connection
from app.utils.auth_utils import login_required

user_bp = Blueprint("user", __name__)


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
            cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
            account = cursor.fetchone()

            if account:
                print("Account already exists!")
            else:
                cursor.execute(
                    "INSERT INTO user (user_name, user_email, user_password, user_location) VALUES (%s, %s, %s, %s)",
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
            cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
            account = cursor.fetchone()

            if account[3] == password:
                session["loggedin"] = True
                session["id"] = account[0]
                session["username"] = account[1]
                session["email"] = account[2]
                session["points"] = account[5]
                session["date"] = account[6]
                print("Login successful!")
                return redirect(url_for("user.user_dashboard"))
            else:
                print("Incorrect username/password!")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return render_template("user_login.html")


@user_bp.route("/user_submit", methods=["POST", "GET"])
@login_required
def user_submit():
    if request.method == "POST":
        branch = request.form["branch"]
        plastic_quantity = request.form.get("plastic-quantity", 0, type=int)
        cardboard_quantity = request.form.get("cardboard-quantity", 0, type=int)
        glass_quantity = request.form.get("glass-quantity", 0, type=int)
        user_id = session.get("id")
        email = session.get("email")

        if not user_id:
            print("Please log in to submit an order.")
            return redirect(url_for("user_login"))

        user_history_description = (
            f"Plastic Bottles: {plastic_quantity}, "
            f"Cardboard: {cardboard_quantity}, "
            f"Glass: {glass_quantity}"
        )

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO user_history (user_id, user_history_description, user_history_branch) VALUES (%s, %s, %s)",
                (user_id, user_history_description, branch),
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
            print("Submission successful!")

        except Exception as e:
            print(f"Error: {e}")
            print("An error occurred during submission.")

        finally:
            conn.close()

        return redirect(url_for("user.user_dashboard"))

    return render_template("user_dashboard.html")


@user_bp.route("/user_dashboard")
@login_required
def user_dashboard():
    username = session.get("username")
    user_id = session.get("id")
    points = session.get("points")
    email = session.get("email")
    date = session.get("date")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_history_date, user_history_description, user_history_branch FROM user_history WHERE user_id = %s ORDER BY user_history_date DESC",
            (user_id,),
        )
        submissions = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        submissions = []

    finally:
        conn.close()

    return render_template(
        "user_dashboard.html",
        username=username,
        email=email,
        date=date,
        points=points,
        submissions=submissions,
    )

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)
from app.utils.db_utils import get_db_connection
from app.utils.auth_utils import login_required
from datetime import datetime

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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
            account = cursor.fetchone()

            if account and account["user_password"] == password:
                session.update(
                    {
                        "loggedin": True,
                        "id": account["user_id"],
                        "username": account["user_name"],
                        "email": account["user_email"],
                        "points": account["user_points"],
                        "date": account["user_joining_date"],
                    }
                )
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
    date = session.get("date")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Get user location
        cursor.execute("SELECT user_location FROM user WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        location = user_data.get("user_location", "")

        cursor.execute(
            "SELECT user_history_date, user_history_description, user_history_branch FROM user_history WHERE user_id = %s ORDER BY user_history_date DESC",
            (user_id,),
        )
        submissions = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        submissions = []
        location = ""

    finally:
        conn.close()

    date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")

    # Format the date as YYYY-MM-DD
    formatted_date = date_obj.strftime("%B %d, %Y")

    return render_template(
        "user_dashboard.html",
        username=username,
        email=session.get("email"),
        date=formatted_date,
        points=points,
        location=location,
        submissions=submissions,
    )


@user_bp.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")
    user_id = session.get("id")

    if not name or not location:
        return jsonify({"success": False, "message": "Name and location are required"})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user SET user_name = %s, user_location = %s WHERE user_id = %s",
            (name, location, user_id),
        )
        conn.commit()

        # Update session data
        session["username"] = name

        return jsonify({"success": True})

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({"success": False, "message": "Database error occurred"})
    finally:
        conn.close()


@user_bp.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    data = request.get_json()
    withdrawal_amount = data.get("amount", 0)
    user_id = session.get("id")
    points = session.get("points", 0)

    if withdrawal_amount <= 0:
        return jsonify({"success": False, "message": "Invalid withdrawal amount."})

    if withdrawal_amount > points:
        return jsonify({"success": False, "message": "Insufficient points available."})

    points -= withdrawal_amount
    session["points"] = points

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user SET user_points = %s WHERE user_id = %s",
            (points, user_id),
        )
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(
            {"success": False, "message": "An error occurred during withdrawal."}
        )
    finally:
        conn.close()

    return jsonify({"success": True, "new_balance": points})
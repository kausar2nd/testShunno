from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
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


@admin_bp.route("/admin_edit/<email>", methods=["GET", "POST"])
def admin_edit(email):
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT sub_id, user_email, sub_description, sub_branch, sub_date 
                FROM user_submission_history 
                WHERE user_email = %s 
                ORDER BY sub_date DESC
                """,
                (email,),
            )
            submissions = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            submissions = []
        finally:
            conn.close()

        return jsonify({"submissions": submissions})


@admin_bp.route("/admin_post/<int:submission_id>", methods=["POST", "GET"])
def admin_post(submission_id):
    if request.method == "POST":
        print("Received submission_id:", submission_id)
        action = request.form["action"]
        plastic = int(request.form.get("plastic", 0))
        cardboard = int(request.form.get("cardboard", 0))
        glass = int(request.form.get("glass", 0))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if action == "delete":
                # Delete the submission
                cursor.execute(
                    "DELETE FROM user_submission_history WHERE sub_id = %s",
                    (submission_id,),
                )

                # Update the storage table
                cursor.execute(
                    """
                    UPDATE storage
                    SET plastic = plastic - %s,
                        cardboard = cardboard - %s,
                        glass = glass - %s
                    """,
                    (plastic, cardboard, glass),
                )

            elif action == "edit":
                # Update the submission
                updated_description = f"Plastic Bottles: {plastic}, Cardboard: {cardboard}, Glass: {glass}"
                cursor.execute(
                    """
                    UPDATE user_submission_history
                    SET sub_description = %s
                    WHERE sub_id = %s
                    """,
                    (updated_description, submission_id),
                )

                # Update the storage table
                cursor.execute(
                    """
                    UPDATE storage
                    SET plastic = plastic + %s,
                        cardboard = cardboard + %s,
                        glass = glass + %s
                    """,
                    (plastic, cardboard, glass),
                )

            conn.commit()
            flash(
                "Submission updated successfully!"
                if action == "edit"
                else "Submission deleted successfully!"
            )

        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while updating the submission.")

        finally:
            conn.close()

        return redirect(url_for("admin.admin_dashboard"))

    else:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Fetch the submission details
            cursor.execute(
                "SELECT sub_description FROM user_submission_history WHERE sub_id = %s",
                (submission_id,),
            )
            submission = cursor.fetchone()

            # Parse the sub_description to extract material quantities
            description = submission["sub_description"]
            parts = description.split(", ")
            plastic = int(parts[0].split(": ")[1])
            cardboard = int(parts[1].split(": ")[1])
            glass = int(parts[2].split(": ")[1])

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred."
        finally:
            conn.close()

        return render_template(
            "admin_post.html",
            submission_id=submission_id,
            plastic=plastic,
            cardboard=cardboard,
            glass=glass,
        )

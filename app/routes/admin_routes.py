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
                print("Invalid email or password.")

        except Exception as e:
            print(f"Error: {e}")

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
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        users = []
        companies = []
    # finally:

    return render_template(
        "admin_dashboard.html",
        email=email,
        users=users,
        companies=companies,
    )


@admin_bp.route("/usub_admin/<email>", methods=["GET", "POST"])
def usub_admin(email):
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
            user_submissions = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            user_submissions = []
        finally:
            conn.close()

        return jsonify({"user_submissions": user_submissions})


@admin_bp.route("/csub_admin/<email>", methods=["GET", "POST"])
def csub_admin(email):
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT order_id, company_email, order_description, order_date
                FROM company_order_history 
                WHERE company_email = %s 
                ORDER BY order_date DESC
                """,
                (email,),
            )
            company_submissions = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            company_submissions = []
        finally:
            conn.close()

        return jsonify({"company_submissions": company_submissions})


@admin_bp.route("/usub_edit/<int:submission_id>", methods=["POST", "GET"])
def uedit_admin(submission_id):
    try:
        new_plastic = int(request.form.get("plastic"))
        new_cardboard = int(request.form.get("cardboard"))
        new_glass = int(request.form.get("glass"))

        if new_plastic < 0 or new_cardboard < 0 or new_glass < 0:
            return {
                "message": "Quantities cannot be negative. Please enter valid values."
            }, 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sub_description FROM user_submission_history WHERE sub_id = %s",
            (submission_id,),
        )
        current_submission = cursor.fetchone()
        if not current_submission:
            return {"message": "Submission not found."}, 404

        current_description = current_submission["sub_description"]

        # Parse current values
        parts = current_description.split(", ")
        current_plastic = int(parts[0].split(": ")[1])
        current_cardboard = int(parts[1].split(": ")[1])
        current_glass = int(parts[2].split(": ")[1])

        # Calculate the differences
        diff_plastic = new_plastic - current_plastic
        diff_cardboard = new_cardboard - current_cardboard
        diff_glass = new_glass - current_glass

        # Constraints: Automatically delete if all materials are zero
        if new_plastic == 0 and new_cardboard == 0 and new_glass == 0:
            # Delete the submission
            cursor.execute(
                "DELETE FROM user_submission_history WHERE sub_id = %s",
                (submission_id,),
            )

            # Reduce storage by the current values
            cursor.execute(
                """
                UPDATE storage
                SET plastic = plastic - %s,
                    cardboard = cardboard - %s,
                    glass = glass - %s
                """,
                (current_plastic, current_cardboard, current_glass),
            )
            conn.commit()
            return {
                "message": "Submission deleted as all materials were set to zero."
            }, 200

        # Update submission and storage
        updated_description = f"Plastic Bottles: {new_plastic}, Cardboard: {new_cardboard}, Glass: {new_glass}"
        cursor.execute(
            """
            UPDATE user_submission_history
            SET sub_description = %s
            WHERE sub_id = %s
            """,
            (updated_description, submission_id),
        )

        cursor.execute(
            """
            UPDATE storage
            SET plastic = plastic + %s,
                cardboard = cardboard + %s,
                glass = glass + %s
            """,
            (diff_plastic, diff_cardboard, diff_glass),
        )
        conn.commit()
        conn.close()

        return {"message": "Submission updated successfully!"}, 200

    except Exception as e:
        print(f"Error: {e}")
        # conn.close()
        return {"message": "An error occurred while updating the submission."}, 500

    # finally:
    #     conn.close()


@admin_bp.route("/usub_delete/<int:submission_id>", methods=["POST"])
def udelete_admin(submission_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sub_description FROM user_submission_history WHERE sub_id = %s",
            (submission_id,),
        )
        current_submission = cursor.fetchone()
        if not current_submission:
            return {"message": "Submission not found."}, 404

        current_description = current_submission["sub_description"]

        # Parse current values
        parts = current_description.split(", ")
        current_plastic = int(parts[0].split(": ")[1])
        current_cardboard = int(parts[1].split(": ")[1])
        current_glass = int(parts[2].split(": ")[1])

        # Delete the submission
        cursor.execute(
            "DELETE FROM user_submission_history WHERE sub_id = %s",
            (submission_id,),
        )

        # Reduce storage by the current values
        cursor.execute(
            """
            UPDATE storage
            SET plastic = plastic - %s,
                cardboard = cardboard - %s,
                glass = glass - %s
            """,
            (current_plastic, current_cardboard, current_glass),
        )
        conn.commit()

        return {"message": "Submission deleted successfully."}, 200

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred while deleting the submission."}, 500

    finally:
        conn.close()


@admin_bp.route("/cedit_admin/<int:order_id>", methods=["POST", "GET"])
def cedit_admin(order_id):
    pass


@admin_bp.route("/fetch_usub_d/<int:submission_id>", methods=["GET", "POST"])
def admin_post(submission_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sub_description FROM user_submission_history WHERE sub_id = %s",
            (submission_id,),
        )
        submission = cursor.fetchone()

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

    return jsonify({"plastic": plastic, "cardboard": cardboard, "glass": glass})

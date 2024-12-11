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


@admin_bp.route("/uedit_admin/<int:submission_id>", methods=["POST", "GET"])
def admin_post(submission_id):
    if request.method == "POST":
        print("Received submission_id:", submission_id)
        #     action = request.form["action"]
        #     plastic = int(request.form.get("plastic", 0))
        #     cardboard = int(request.form.get("cardboard", 0))
        #     glass = int(request.form.get("glass", 0))

        #     try:
        #         conn = get_db_connection()
        #         cursor = conn.cursor()

        #         if action == "delete":
        #             cursor.execute(
        #                 "DELETE FROM user_submission_history WHERE sub_id = %s",
        #                 (submission_id,),
        #             )
        #             cursor.execute(
        #                 """
        #                 UPDATE storage
        #                 SET plastic = plastic - %s,
        #                     cardboard = cardboard - %s,
        #                     glass = glass - %s
        #                 """,
        #                 (plastic, cardboard, glass),
        #             )

        #         elif action == "edit":
        #             updated_description = f"Plastic Bottles: {plastic}, Cardboard: {cardboard}, Glass: {glass}"
        #             cursor.execute(
        #                 """
        #                 UPDATE user_submission_history
        #                 SET sub_description = %s
        #                 WHERE sub_id = %s
        #                 """,
        #                 (updated_description, submission_id),
        #             )
        #             cursor.execute(
        #                 """
        #                 UPDATE storage
        #                 SET plastic = plastic + %s,
        #                     cardboard = cardboard + %s,
        #                     glass = glass + %s
        #                 """,
        #                 (plastic, cardboard, glass),
        #             )

        #         conn.commit()
        #     except Exception as e:
        #         print(f"Error: {e}")
        #     finally:
        #         conn.close()

        #     return redirect(url_for("admin.admin_dashboard"))

        # else:
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

        # return render_template(
        #     "admin_post.html",
        #     submission_id=submission_id,
        #     plastic=plastic,
        #     cardboard=cardboard,
        #     glass=glass,
        # )

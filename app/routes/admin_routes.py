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
def superuser():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
            account = cursor.fetchone()

            if account and account[2] == password:
                session["admin_loggedin"] = True
                session["admin_id"] = account[0]
                session["admin_email"] = account[1]
                print("Logged in successfully!")
                return redirect(url_for("admin.admin_dashboard"))
            else:
                print("Invalid email or password.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return render_template("admin_login.html")


@admin_bp.route("/admin_dashboard", methods=["POST", "GET"])
@login_required
def admin_dashboard():
    email = session.get("admin_email", "admin@example.com")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_name, user_email, user_location, user_joining_date FROM user"
        )
        users = cursor.fetchall()
        cursor.execute(
            "SELECT company_name, company_email, company_location, company_joining_date FROM company"
        )
        companies = cursor.fetchall()
        conn.close()

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
                SELECT user_history_id, user_history_email, user_history_description, user_history_branch, user_history_date 
                FROM user_history 
                WHERE user_email = %s 
                ORDER BY user_history_date DESC
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


@admin_bp.route("/fetch_usub_d/<int:id>", methods=["GET", "POST"])
def admin_post(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_history_description FROM user_history WHERE user_history_id = %s",
            (id,),
        )
        submission = cursor.fetchone()

        description = submission["user_history_description"]
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


@admin_bp.route("/usub_edit/<int:history_id>", methods=["POST", "GET"])
def uedit_admin(history_id):
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
            "SELECT user_history_description FROM user_history WHERE user_history_id = %s",
            (history_id,),
        )
        current_submission = cursor.fetchone()
        if not current_submission:
            return {"message": "Submission not found."}, 404

        current_description = current_submission["user_history_description"]
        parts = current_description.split(", ")
        current_plastic = int(parts[0].split(": ")[1])
        current_cardboard = int(parts[1].split(": ")[1])
        current_glass = int(parts[2].split(": ")[1])

        diff_plastic = new_plastic - current_plastic
        diff_cardboard = new_cardboard - current_cardboard
        diff_glass = new_glass - current_glass

        if new_plastic == 0 and new_cardboard == 0 and new_glass == 0:
            cursor.execute(
                "DELETE FROM user_history WHERE user_history_id = %s",
                (history_id,),
            )

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

        updated_description = f"Plastic Bottles: {new_plastic}, Cardboard: {new_cardboard}, Glass: {new_glass}"
        cursor.execute(
            """
            UPDATE user_history
            SET user_history_description = %s
            WHERE user_history_id = %s
            """,
            (updated_description, history_id),
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

        return {"message": "Submission updated successfully!"}, 200

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred while updating the submission."}, 500

    finally:
        conn.close()


@admin_bp.route("/usub_delete/<int:id>", methods=["POST"])
def udelete_admin(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_history_description FROM user_history WHERE user_history_id = %s",
            (id,),
        )
        current_submission = cursor.fetchone()
        if not current_submission:
            return {"message": "Submission not found."}, 404

        current_description = current_submission["user_history_description"]
        parts = current_description.split(", ")
        current_plastic = int(parts[0].split(": ")[1])
        current_cardboard = int(parts[1].split(": ")[1])
        current_glass = int(parts[2].split(": ")[1])

        cursor.execute(
            "DELETE FROM user_history WHERE user_history_id = %s",
            (id,),
        )

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


@admin_bp.route("/csub_admin/<email>", methods=["GET", "POST"])
def csub_admin(email):
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT company_history_id, company_history_email, company_history_description, company_history_date
                FROM company_history 
                WHERE company_history_email = %s 
                ORDER BY company_history_date DESC
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


@admin_bp.route("/fetch_csub_d/<int:company_history_id>", methods=["GET", "POST"])
def cadmin_post(company_history_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT company_history_description FROM company_history WHERE company_history_id = %s",
            (company_history_id,),
        )
        order = cursor.fetchone()

        description = order["company_history_description"]
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


@admin_bp.route("/csub_edit/<int:company_history_id>", methods=["POST", "GET"])
def cedit_admin(company_history_id):
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
            "SELECT company_history_description FROM company_history WHERE company_history_id = %s",
            (company_history_id,),
        )
        current_order = cursor.fetchone()
        if not current_order:
            return {"message": "Order not found."}, 404

        current_description = current_order["company_history_description"]

        parts = current_description.split(", ")
        current_plastic = int(parts[0].split(": ")[1])
        current_cardboard = int(parts[1].split(": ")[1])
        current_glass = int(parts[2].split(": ")[1])

        diff_plastic = new_plastic - current_plastic
        diff_cardboard = new_cardboard - current_cardboard
        diff_glass = new_glass - current_glass

        if new_plastic == 0 and new_cardboard == 0 and new_glass == 0:
            cursor.execute(
                "DELETE FROM company_history WHERE company_history_id = %s",
                (company_history_id,),
            )

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
            return {"message": "Order deleted as all materials were set to zero."}, 200

        updated_description = f"Plastic Bottles: {new_plastic}, Cardboard: {new_cardboard}, Glass: {new_glass}"
        cursor.execute(
            """
            UPDATE company_history
            SET company_history_description = %s
            WHERE company_history_id = %s
            """,
            (updated_description, company_history_id),
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

        return {"message": "Order updated successfully!"}, 200

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred while updating the order."}, 500

    finally:
        conn.close()


@admin_bp.route("/csub_delete/<int:company_history_id>", methods=["POST"])
def cdelete_admin(company_history_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT company_history_description FROM company_history WHERE company_history_id = %s",
            (company_history_id,),
        )
        current_order = cursor.fetchone()
        if not current_order:
            return {"message": "Order not found."}, 404

        current_description = current_order["company_history_description"]
        parts = current_description.split(", ")
        current_plastic = int(parts[0].split(": ")[1])
        current_cardboard = int(parts[1].split(": ")[1])
        current_glass = int(parts[2].split(": ")[1])

        cursor.execute(
            "DELETE FROM company_history WHERE company_history_id = %s",
            (company_history_id,),
        )

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

        return {"message": "Order deleted successfully."}, 200

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred while deleting the order."}, 500

    finally:
        conn.close()

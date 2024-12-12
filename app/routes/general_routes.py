from flask import Blueprint, render_template, redirect, url_for, session
from app.utils.auth_utils import login_required

general_bp = Blueprint("general", __name__)


@general_bp.route("/")
def index():
    return render_template("index.html")


@general_bp.route("/login")
def login_general():
    return render_template("login_general.html")


@general_bp.route("/find_bins")
def find_bins():
    return render_template("find_bin.html")


@general_bp.route("/logout")
@login_required
def logout():
    session.clear()
    print("You have been logged out.")
    return redirect(url_for("general.login_general"))

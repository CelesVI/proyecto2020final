from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User

from app.validators import authValidator


def login():
    return render_template("auth/login.html")


def authenticate():

    params = request.form

    user = User.find_by_email_and_pass(params["email"], params["password"])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    if not user.active:
        flash("No se puede iniciar sesión, el usuario está deshabilitado")
        return redirect(url_for("auth_login"))

    session["user"] = user.get_email()
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))

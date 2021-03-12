from flask import redirect, render_template, request, url_for, session, abort, flash

from app.helpers.permiso import check as check_permission
from app.helpers.permiso import checkeos_session_permisos
from app.models.configuracion import Configuracion
from app.models.user import User

from sqlalchemy import or_, and_
from app.db import db

def index():

    checkeos_session_permisos('configuracion_index')

    config = Configuracion.all()

    return render_template("configuracion/index.html", config=config)

def update():

    checkeos_session_permisos('configuracion_update')

    conf = Configuracion.get_config_by_id(request.form["id"])

    conf.update(request.form)

    return redirect(url_for("home"))

    

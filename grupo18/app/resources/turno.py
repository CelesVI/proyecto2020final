from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.rol import Rol
from app.models.configuracion import Configuracion
from app.models.turno import Turno
from app.models.centro_social import Centro_social

from app.helpers.auth import authenticated
from app.helpers.handler import load_errors
from app.helpers.permiso import check as check_permission
from app.helpers.permiso import checkeos_session_permisos

from sqlalchemy import or_, and_
from app.db import db

from app.validators import apiValidator

from datetime import datetime, date, time, timedelta

def index(page_num=1):
    checkeos_session_permisos("turno_index")
    fechaMin = date.today()
    fechaMax = fechaMin + timedelta(days=2)
    cantTurnos = Configuracion.get_cantidad_elementos_lista()
    turnos = Turno.query.filter(and_(Turno.fecha >= fechaMin, Turno.fecha <= fechaMax)).order_by(Turno.fecha.asc(), Turno.hora_inicio.asc()).paginate(per_page=int(cantTurnos), page=page_num, error_out=True)
    return render_template("turnos/index.html", turnos=turnos)

def index_by_centro(centro_id, page_num=1):
    checkeos_session_permisos("index_by_centro")
    fecha_min = date.today()
    fecha_max = fecha_min + timedelta(days=2)
    cant_turnos = Configuracion.get_cantidad_elementos_lista()
    turnos = Turno.find_by_id_centro(centro_id).filter(and_(Turno.fecha >= fecha_min, Turno.fecha <= fecha_max)).order_by(Turno.fecha.asc(),Turno.hora_inicio.asc()).paginate(per_page=int(cant_turnos), page=page_num, error_out=True)
    return render_template("turnos/index_by_centro.html", centro_id=centro_id, page_num=page_num, turnos=turnos)

def new():
    checkeos_session_permisos('turno_new')
    centros = Centro_social.all()
    return render_template("turnos/new.html", centros=centros)

def new_by_centro(centro_id):
    checkeos_session_permisos("turno_new")
    return render_template("turnos/new_by_centro.html", centro_id=centro_id)

def create():
    checkeos_session_permisos('turno_new')
    is_valid, errors = apiValidator.create_turno(request.form)
    
    centros = Centro_social.query.all()

    if is_valid:
        
        if Turno.existe(request.form["hora_inicio"], request.form["fecha"], request.form["centro_social"]):
            flash("Ya existe un turno con ese día y horario!")
            return render_template("turnos/new.html", centros=centros)

        if not Turno.horario_is_valid(request.form["hora_inicio"], request.form["hora_fin"]):
            flash("Ingreso de hora inválida: los turnos son de 9 a 16 en bloques de 30 minutos")
            return render_template("turnos/new.html", centros=centros)
        
        Turno.create(request.form)
    else:
        load_errors(errors)
        return render_template("turnos/new.html", centros=centros)
    return redirect(url_for("turno_index", page_num=1))

def create_by_centro(centro_id):
    checkeos_session_permisos('turno_new')
    is_valid, errors = apiValidator.create_turno(request.form)
    
    if is_valid:
        if Turno.existe(request.form["hora_inicio"], request.form["fecha"], centro_id):
            flash("Ya existe un turno con ese día y horario!")
            return render_template("turnos/new_by_centro.html", centro_id=centro_id)

        if not Turno.horario_is_valid(request.form["hora_inicio"], request.form["hora_fin"]):
            flash("Ingreso de hora inválida: los turnos son de 9 a 16 en bloques de 30 minutos")
            return render_template("turnos/new_by_centro.html", centro_id=centro_id)
        
        Turno.create_by_centro(request.form,centro_id)
    else:
        load_errors(errors)
        return render_template("turnos/new_by_centro.html", centro_id=centro_id)
    return redirect(url_for("index_by_centro", centro_id=centro_id, page_num=1))

def existe(hora_inicio, fecha, centro_id):
    turno = Turno.query.filter(and_(Turno.hora_inicio == hora_inicio, Turno.fecha == fecha, Turno.centro_id == centro_id))
    return   turno.count() > 0

def horario_is_valid(hora_inicio, hora_fin):
    hora_apertura = datetime.strptime("9:00", '%H:%M')
    hora_inicio = datetime.strptime(hora_inicio, '%H:%M')
    hora_fin = datetime.strptime(hora_fin, '%H:%M')
    return (hora_inicio >= hora_apertura) and (hora_inicio <= datetime.strptime("15:30", '%H:%M')) and (hora_fin > hora_inicio)    


def confirmar(id):
    checkeos_session_permisos('turno_destroy')
    return render_template("turnos/delete.html",id=id)

def confirmar_by_centro(centro_id, turno_id):
    checkeos_session_permisos('turno_destroy')
    return render_template("turnos/delete_by_centro.html", centro_id=centro_id,turno_id=turno_id)

def delete(id):
    checkeos_session_permisos('turno_destroy')
    Turno.delete(id)
    return redirect(url_for("turno_index", page_num=1))

def delete_by_centro(centro_id, turno_id):
    checkeos_session_permisos('turno_destroy')
    Turno.delete(turno_id)
    return redirect(url_for("index_by_centro", centro_id=centro_id, page_num=1))#faltan args

def edit(id):
    checkeos_session_permisos("turno_update")
    turno = Turno.get_turno_by_id(id)
    centros = Centro_social.all()
    return render_template("turnos/edit.html", turno = turno, centros=centros)

def edit_by_centro(centro_id, turno_id):
    checkeos_session_permisos("turno_update")
    turno = Turno.get_turno_by_id(turno_id)
    centro = Centro_social.get_centro_by_id(centro_id)
    return render_template("turnos/edit_by_centro.html", centro=centro, turno_id=turno_id, turno = turno)


def update(id):
    checkeos_session_permisos("turno_update")
    centros=Centro_social.query.all()
    turno = Turno.get_turno_by_id(id)
    centros = Centro_social.all()
    is_valid, errors = apiValidator.create_turno(request.form)

    if is_valid:
        if Turno.existe_otro(request.form["hora_inicio"], request.form["fecha"], request.form["centro_social"], id):
            flash("Ya existe un turno con ese día y horario!")
            return render_template("turnos/edit.html", turno=turno, centros=centros)
        
        turno.update(request.form)
    else:
        load_errors(errors)
        return render_template("turnos/edit.html", turno=turno, centros=centros)
    return redirect(url_for("turno_index", page_num=1))

def update_by_centro(centro_id, turno_id):
    checkeos_session_permisos("turno_update")
    turno = Turno.get_turno_by_id(turno_id)
    centro = Centro_social.get_centro_by_id(centro_id)

    is_valid, errors = apiValidator.create_turno(request.form)
    
    if is_valid:
        if Turno.existe_otro(request.form["hora_inicio"], request.form["fecha"], centro_id, turno_id):
            flash("Ya existe un turno con ese día y horario!")
            return render_template("turnos/edit_by_centro.html", centro=centro, turno_id=turno_id, turno=turno)
        
        turno.update(request.form)
    else:
        load_errors(errors)
        return render_template("turnos/edit_by_centro.html", centro=centro, turno_id=turno_id, turno=turno)
    return redirect(url_for("index_by_centro", centro_id=centro_id, page_num=1))
    
def buscar(page_num):
    if not authenticated(session):
        abort(401)
    cant_turnos = Configuracion.get_cantidad_elementos_lista()
    search = "%{}%".format(request.form["filtro"])
    if request.form["opcion"] == 'Email':
        turnos = Turno.query.filter(Turno.email.ilike(search)).paginate(per_page=int(cant_turnos), page=page_num, error_out=True)
    else:
        if request.form["opcion"] == 'Centro':
            centros = Centro_social.query.filter(Centro_social.nombre.ilike(search)).all()
            lista_id_centros = []
            for centro in centros:
                lista_id_centros.append(centro.id)
            turnos = Turno.query.filter(Turno.centro_id.in_(lista_id_centros)).paginate(per_page=int(cant_turnos), page=page_num, error_out=True)
        else:
            return redirect(url_for("turno_index", page_num=1))
    return render_template("turnos/index.html", turnos=turnos)


def buscar_by_email(centro_id, page_num):
    if not authenticated(session):
        abort(401)
    cant_turnos = Configuracion.get_cantidad_elementos_lista()
    email = "%{}%".format(request.form["email"])
    turnos = Turno.query.filter(and_(Turno.email.ilike(email), Turno.centro_id==centro_id)).paginate(per_page=int(cant_turnos), page=page_num, error_out=True)
    return render_template("turnos/index_by_centro.html", centro_id=centro_id, page_num=page_num, turnos=turnos)


def checkeos_session_permisos(perm):
    user = authenticated(session)
    if not user:
        abort(401)
    usuario = User.get_user_by_email(user)
    if not check_permission(usuario.id, perm):
        abort(401)
    return True

from flask import redirect, render_template, request, url_for, session, abort, flash, send_from_directory, current_app
from app.test import Test
from app.models.centro_social import Centro_social as Centro
from app.models.tipo_centro import Tipo_centro as TC
from app.models.configuracion import Configuracion
from app.models.user import User

from werkzeug.utils import secure_filename

from app.helpers.handler import load_errors
from app.helpers.permiso import checkeos_session_permisos
from app.helpers.municipio_api import get_municipio_by_id, get_municipios

from sqlalchemy import or_, and_
from app.db import db

import os
import requests

from app.validators import apiValidator, protocoloValidator



# Protected resources
def index(page_num=1):

    checkeos_session_permisos("centro_index")

    cantCentros = Configuracion.get_cantidad_elementos_lista()

    centros = Centro.query.paginate(per_page=int(cantCentros), page=page_num, error_out=True)

    municipios = get_municipios()

    return render_template("centros/index.html", centros=centros, municipios=municipios, busqueda=False)


def new():

    checkeos_session_permisos('centro_new')
    tipos_centros = TC.all()
    municipios = get_municipios()

    return render_template("centros/new.html", lista_tipos=tipos_centros, municipios=municipios)


def create():

    dir_uploads = current_app.config['PROTOCOLO_UPLOADS']

    checkeos_session_permisos('centro_new')

    is_valid, errors = apiValidator.create_centro(request.form)
    
    if  not is_valid:
        load_errors(errors)
        return redirect(url_for("centro_new"))

    if Centro.existe(0, request.form["nombre"], request.form["direccion"], request.form["telefono"]):
        flash("Ya existe un centro con este nombre, dirección o teléfono!")
        return redirect(url_for("centro_new"))
    
    if request.files:

        protocolo = request.files["protocolo"]
        filename = secure_filename(request.form["nombre"]+"-"+protocolo.filename) 
        if not (protocolo.filename == ''):
            is_valid, erros = protocoloValidator.create_protocolo(filename)
            if is_valid:
                protocolo.save(os.path.join(dir_uploads, filename))
            else:
                load_errors(errors)
                return redirect(url_for("centro_new"))
        else:
            filename = ''

    Centro.create(request.form, filename)

    return redirect(url_for("centro_index", page_num=1))

def details(id):
    checkeos_session_permisos('centro_show')

    centro = Centro.get_centro_by_id(id)

    aprobacion = "Pendiente"
    if centro.aprobacion_id == 2:
        aprobacion = "Aceptada"
    else:
        if centro.aprobacion_id == 3:
            aprobacion = "Rechazada"

    tipo = TC.get_tipo_by_id(centro.tipo_centro_id)

    municipio = get_municipio_by_id(centro.municipio_id)
    nombreMunicipio = municipio[str(centro.municipio_id)]["name"]

    return render_template("centros/details.html", centro=centro, aprobacion=aprobacion, tipo=tipo, municipio=nombreMunicipio)

def act_aprobacion_centro(id, num):
    checkeos_session_permisos('centro_aprobacion')

    centro = Centro.get_centro_by_id(id)
    centro.aprobacion_id = num
    centro.update_by_object(centro)

    return redirect(url_for("centro_index", page_num=1))

def delete(name):

    checkeos_session_permisos('centro_destroy')

    Centro.delete(name)

    return redirect(url_for("centro_index", page_num=1))

def confirmar(name):

    checkeos_session_permisos('centro_destroy')
    
    return render_template("centros/delete.html", name=name)


def edit(id):

    checkeos_session_permisos('centro_update')

    centro = Centro.get_centro_by_id(id)
    aprobacion = "Pendiente"
    if centro.aprobacion_id == 2:
        aprobacion = "Aceptada"
    else:
        if centro.aprobacion_id == 3:
            aprobacion = "Rechazada"

    tipos_centros = TC.all()
    municipios = get_municipios()

    return render_template("centros/edit.html", centro=centro, aprobacion=aprobacion, lista_tipos=tipos_centros, municipios=municipios)

def update(id):

    dir_uploads = current_app.config['PROTOCOLO_UPLOADS']
    
    checkeos_session_permisos('centro_update')

    centro = Centro.get_centro_by_id(id)

    is_valid, errors = apiValidator.create_centro(request.form)
    
    if Centro.existe(centro.id, request.form["nombre"], request.form["direccion"], request.form["telefono"]):
        flash("Ya existe un centro con este nombre, dirección o teléfono!")
        return redirect(url_for("centro_edit", id=id))

    if not is_valid:
        load_errors(errors)
        return redirect(url_for("centro_edit"))
    else:
        if request.files:
            protocolo = request.files["protocolo"]
            filename = protocolo.filename
            if not (protocolo.filename == ''):
                is_valid, erros = protocoloValidator.create_protocolo(filename)
                if is_valid:
                    if (centro.protocolo != ''):
                        os.remove(dir_uploads+centro.protocolo)
                    protocolo.save(os.path.join(dir_uploads,filename))
                else:
                    load_errors(errors)
                    return redirect(url_for("centro_edit"))
            else:
                filename = centro.protocolo
        else:    
            filename = centro.protocolo

    if request.form["latitud"] != '':
        centro.latitud = request.form["latitud"]
        centro.longitud = request.form["longitud"]        

    centro.complete_update(request.form, filename, centro.latitud, centro.longitud)

    return redirect(url_for("centro_index", page_num=1))

def descargar(name):
    
    # dir_uploads = current_app.config['PROTOCOLO_UPLOADS']

    dir_uploads = "{}/app/static/uploads/".format(os.getcwd())


    try:
        return send_from_directory(dir_uploads, filename=name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


def buscar(page_num):
    
    checkeos_session_permisos('centro_index')

    cantCentros = Configuracion.get_cantidad_elementos_lista()

    search = "%{}%".format(request.form["name"])

    opcion = request.form["active"]

    if opcion == 'Todos':
        centros = Centro.query.filter(Centro.nombre.ilike(search)).paginate(per_page=int(cantCentros), page=page_num, error_out=True)
    else:
        num = 1
        if opcion == 'Aceptado':
            num = 2
        else:
            if opcion == 'Rechazado':
                num = 3
        centros = Centro.query.filter(and_(Centro.nombre.ilike(search), Centro.aprobacion_id == num )).paginate(per_page=int(cantCentros), page=page_num, error_out=True)

    municipios = get_municipios()
    return render_template("centros/index.html", centros=centros, municipios=municipios, busqueda=True, nombre=search, opcion=opcion)

def cbuscar(page_num, name, opcion):
    
    checkeos_session_permisos("centro_index")

    cantCentros = Configuracion.get_cantidad_elementos_lista()

    if opcion == 'Todos':
        centros = Centro.query.filter(Centro.nombre.ilike(name)).paginate(per_page=int(cantCentros), page=page_num, error_out=True)
    else:
        num = 1
        if opcion == 'Aceptado':
            num = 2
        else:
            if opcion == 'Rechazado':
                num = 3
        centros = Centro.query.filter(and_(Centro.nombre.ilike(name), Centro.aprobacion_id == num )).paginate(per_page=int(cantCentros), page=page_num, error_out=True)

    municipios = get_municipios()
    return render_template("centros/index.html", centros=centros, municipios=municipios, busqueda=True, nombre=name, opcion=opcion)

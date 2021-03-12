from flask import jsonify, json, request, abort
from app.models.centro_social import Centro_social as Centro
from app.models.tipo_centro import Tipo_centro as Tipo
from app.models.configuracion import Configuracion
from app.helpers.municipio_api import get_municipio_by_id, get_municipios
from app.validators.apiValidator import create_centro
from app.db import db

import requests

def index():
    if len(request.args) == 0:
        page_num = 1
    else:
        page_num = int(request.args["page"])

    try:
        cant_centros = Configuracion.get_cantidad_elementos_lista()
        municipios = get_municipios()
        centros = Centro.query.paginate(per_page=int(
            cant_centros), page=page_num, error_out=False)
    except:
        return abort(500)

    data = []

    for centro in centros.items:
        try:
            tipo_centro = Tipo.get_tipo_by_id(centro.tipo_centro_id)
            data.append(
                {
                    "nombre":
                    centro.nombre,
                    "direccion":
                    centro.direccion,
                    "telefono":
                    centro.telefono,
                    "hora_apertura":
                    str(centro.hora_de_apertura),
                    "hora_cierre":
                    str(centro.hora_de_cierre),
                    "tipo":
                    tipo_centro.nombre,
                    "web":
                    centro.web,
                    "email":
                    centro.email,
                    "municipalidad":
                    municipios[str(centro.municipio_id)]['name']
                }
            )
        except:
            abort(500)

    return jsonify(centros=data, total=centros.total, pagina=page_num), 200


def create():

    data = request.get_json(True)

    if not create_centro(data):
        abort(400)

    try:
        municipio = get_municipio_by_id(data["municipio_id"])
    except:
        abort(400)

    try:
        centro = Centro(data["nombre"], data["direccion"], data["telefono"], data["hora_de_apertura"],
                        data["hora_de_cierre"], data["municipio_id"], data["tipo_centro_id"],
                        data["web"], data["email"], "", data["latitud"], data["longitud"])
        db.session.add(centro)
        db.session.commit()

        tipo_centro = Tipo.get_tipo_by_id(centro.tipo_centro_id)
    except:
        abort(500)

    data = {
        "nombre":
        centro.nombre,
        "direccion":
        centro.direccion,
        "telefono":
        centro.telefono,
        "hora_apertura":
        str(centro.hora_de_apertura),
        "hora_cierre":
        str(centro.hora_de_cierre),
        "tipo":
        tipo_centro.nombre,
        "web":
        centro.web,
        "email":
        centro.email,
        "municipalidad":
        municipio[str(centro.municipio_id)]['name']
    }

    return jsonify(Atributos=data), 201


def details(id):

    try:
        centro = Centro.get_centro_by_id(id)
    except:
        abort(500)

    data = {}

    if not centro:
        return abort(404)

    tipo_centro = Tipo.get_tipo_by_id(centro.tipo_centro_id)

    try:
        municipio = get_municipio_by_id(centro.municipio_id)
    except:
        abort(500)

    data = {
        "nombre":
        centro.nombre,
        "direccion":
        centro.direccion,
        "telefono":
        centro.telefono,
        "hora_apertura":
        str(centro.hora_de_apertura),
        "hora_cierre":
        str(centro.hora_de_cierre),
        "tipo":
        tipo_centro.nombre,
        "web":
        centro.web,
        "email":
        centro.email,
        "municipalidad":
        municipio[str(centro.municipio_id)]['name']
    }

    return jsonify(Atributos=data), 200

def all_centros():
    try:
        municipios = get_municipios()
        centros = Centro.all()
    except:
        return abort(500)

    data = []

    for centro in centros:
        try:
            tipo_centro = Tipo.get_tipo_by_id(centro.tipo_centro_id)
            data.append(
                {
                    "id":
                    centro.id,
                    "nombre":
                    centro.nombre,
                    "direccion":
                    centro.direccion,
                    "telefono":
                    centro.telefono,
                    "hora_apertura":
                    str(centro.hora_de_apertura),
                    "hora_cierre":
                    str(centro.hora_de_cierre),
                    "tipo":
                    tipo_centro.nombre,
                    "web":
                    centro.web,
                    "email":
                    centro.email,
                    "municipalidad":
                    municipios[str(centro.municipio_id)]['name'],
                    "latitud":
                    centro.latitud,
                    "longitud":
                    centro.longitud
                }
            )
        except:
            abort(500)

    return jsonify(centros=data), 200
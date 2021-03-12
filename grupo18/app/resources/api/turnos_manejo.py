from flask import jsonify, json, request, abort
from app.models.turno import Turno
from app.db import db
from datetime import datetime, timedelta
from app.validators.apiValidator import validar_treinta_minutos, validar_centro_id, validar_data_format, validar_email


def create(centro_id):

    data = request.get_json()

    try:
        turnos = Turno.get_turno_by_centro_id(centro_id)
        turno_libre = True
        valido = False
        if validar_treinta_minutos(data["hora_fin"], data["hora_inicio"]) == '0:30:00':
            if validar_data_format(data["fecha"]):
                if validar_email(data["email_donante"]):
                    if validar_centro_id(centro_id):
                        valido = True
                    else:
                        return jsonify({"message": "Centro ID innexistente"}), 400
                else:
                    return jsonify({"message": "Email inválido"}), 400
            else:
                return jsonify({"message": "Formato de fecha inválido"}), 400
        else:
            return jsonify({"message": "Bloque distinto a 30 minutos"}), 400
        if valido:
            for turno_in in turnos:
                inicio = turno_in.hora_inicio.strftime("%H:%M:%S")
                fecha = turno_in.fecha.strftime("%Y-%m-%d")
                if (data["hora_inicio"] == inicio) and (data["fecha"] == fecha) and (centro_id == turno_in.centro_id):
                    turno_libre = False
                    break
            if turno_libre and valido:
                dato = {
                    "centro_id":
                    centro_id,
                    "email_donante":
                    data["email_donante"],
                    "telefono_donante":
                    data["telefono_donante"],
                    "hora_inicio":
                    str(data["hora_inicio"]),
                    "hora_fin":
                    str(data["hora_fin"]),
                    "fecha":
                    str(data["fecha"]),
                    "nombre":
                    data["nombre"],
                    "apellido":
                    data["apellido"]
                }
                try:
                    turno = Turno(data["email_donante"], data["telefono_donante"], data["hora_inicio"],
                                  data["hora_fin"], data["fecha"], centro_id, data["nombre"], data["apellido"])
                    db.session.add(turno)
                    db.session.commit()

                    return jsonify(Atributos=dato), 201
                except:
                    abort(400)
        else:
            return jsonify({"message": "Turno ocupado"}), 400
    except:
        return jsonify({"message": "500 Internal Server Error"}), 500


def turnos_disponibles(centro_id):
    horarios = ['09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00',
                '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00']
    if len(request.args) > 0:
        fecha = request.args["fecha"]
    else:
        fecha = datetime.today().strftime("%Y-%m-%d")
    try:
        turnos_centro_fecha = Turno.get_turno_by_centro_id_and_date(
            centro_id, fecha)
    except:
        return jsonify({"message": "500 Internal Server Error"}), 500
    turnos = []
    for turno in turnos_centro_fecha:
        horarios.remove(turno.hora_inicio.strftime('%H:%M:%S'))
    for horario in horarios:
        hora = datetime.strptime(horario, '%H:%M:%S')
        hora_fin = hora + timedelta(minutes=30)
        turnos.append(
            {
                "centro_id":
                centro_id,
                "hora_inicio":
                horario,
                "hora_fin":
                hora_fin.strftime('%H:%M:%S'),
                "fecha":
                str(fecha)
            }
        )
    return jsonify(turnos=turnos), 200


def turnos_ocupados():
    turnos = []
    turnos = Turno.all()
    data = []
    for turno in turnos:
        data.append({
            "nombre":
            turno.nombre,
            "apellido":
            turno.apellido,
            "email":
            turno.email,
            "telefono":
            turno.telefono,
            "hora_inicio":
            str(turno.hora_inicio),
            "fecha":
            str(turno.fecha),
            "mes":
            turno.fecha.month,
            "centro_id":
            turno.centro_id
        })
    return jsonify(turnos=data), 200


def turnos_ocupados_centro(centro_id):
    turnos = []
    turnos = Turno.find_by_id_centro(centro_id)
    data = []
    for turno in turnos:
        data.append({
            "nombre":
            turno.nombre,
            "apellido":
            turno.apellido,
            "email":
            turno.email,
            "telefono":
            turno.telefono,
            "hora_inicio":
            str(turno.hora_inicio),
            "fecha":
            str(turno.fecha),
            "mes":
            turno.fecha.month,
            "centro_id":
            turno.centro_id
        })
    return jsonify(turnos=data), 200

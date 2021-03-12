import re
from datetime import datetime, timedelta
from app.models.centro_social import Centro_social


def create_centro(params):
    required_params = ["nombre", "direccion", "telefono",
                       "hora_de_apertura", "hora_de_cierre", "municipio_id"]

    errors = []

    for attribute in required_params:
        if attribute not in params:
            errors.append(f"El atributo '{attribute}' es requerido!")

        if not params.get(attribute):
            errors.append(f"El atributo '{attribute}' no puede estar vacío!")

    result = len(errors) == 0

    return result, errors


def create_turno(params):
    required_params = ["email", "telefono", "hora_inicio",
                       "hora_fin", "fecha", "nombre", "apellido"]

    errors = []

    for attribute in required_params:
        if attribute not in params:
            errors.append(f"El atributo '{attribute}' es requerido!")

        if not params.get(attribute):
            errors.append(f"El atributo '{attribute}' no puede estar vacío!")

    result = len(errors) == 0

    return result, errors


def validar_centro(params):

    return validar_email(params["email"]) and validar_hora_apertura_cierre(params["hora_de_apertura"], params["hora_de_cierre"])


def validar_email(email):
    # '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' Otra opcion pero no acepta mayusculas
    regex_email = '^[a-zA-Z0-9._-]+@[a-zA-Z-]+\.[a-zA-Z]{2,3}$'
    return not re.search(regex_email, email) == None


def validar_hora_apertura_cierre(h_apertura, h_cierre):
    return datetime.strptime(h_apertura, '%H:%M').time() < datetime.strptime(h_cierre, '%H:%M').time()


def validar_centro_id(centro_id):
    centro = Centro_social.get_centro_by_id(centro_id)
    if centro:
        return True
    else:
        return False


def validar_data_format(fecha):
    date_format = '%Y-%m-%d'
    try:
        datetime.strptime(fecha, date_format)
        return True
    except:
        return False


def validar_treinta_minutos(hora_fin, hora_inicio):
    # if dif == '0:30:00'
    return str(datetime.strptime(hora_fin, '%H:%M:%S') - datetime.strptime(hora_inicio, '%H:%M:%S'))

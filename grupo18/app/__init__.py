from os import path, environ
from flask import Flask, render_template, g
from flask_session import Session
from flask_cors import CORS
from config import config
from app.db import db
from app.resources import issue
from app.resources import configuracion
from app.resources import user
from app.resources import auth
from app.resources import turno
from app.resources import centro_social as centro
from app.resources.api import centro_social as api_centro
from app.resources.api import turnos_manejo as api_turno
from app.resources.api import issue as api_issue
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import permiso as helper_permiso
from flask_cors import CORS


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    
    CORS(app)
    cors = CORS(app, resources={
        r"/*" : {
            "origins": "*"
        }
    })

    # Carga del CORS
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    cors = CORS(app, resources={
        r"/*": {
            "origins": "*"
        }
    })

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Configuración de subida de archivos
    PROTOCOLO_UPLOADS = "app/static/uploads/"
    ALLOWED_FILES_EXTENSIONS = {'PDF'}

    app.config["PROTOCOLO_UPLOADS"] = PROTOCOLO_UPLOADS
    app.config["ALLOWED_FILES_EXTENSIONS"] = ALLOWED_FILES_EXTENSIONS

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db con SQLALCHEMY (acordarse de instalar antes pip3 install -r requirements.txt para tener flask-sqlalchemy)
    conf = app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + \
        conf["DB_USER"]+":"+conf["DB_PASS"]+"@" + \
        conf["DB_HOST"]+"/"+conf["DB_NAME"]
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(tiene_permiso=helper_permiso.check)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Consultas
    # app.add_url_rule("/consultas", "issue_index", issue.index)
    # app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    # app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/confirmar/<string:username>",
                     "user_confirmar", user.confirmar)
    app.add_url_rule("/usuarios/delete/<string:username>",
                     "user_delete", user.delete)
    app.add_url_rule("/usuarios/edit/<string:username>",
                     "user_edit", user.edit)
    app.add_url_rule("/usuarios/update/<int:id>",
                     "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/busqueda/<int:page_num>",
                     "user_buscar", user.buscar, methods=["POST"])

    app.add_url_rule("/usuarios/asignarRoles/<string:username>",
                     "user_asignarRoles", user.asignar_roles)
    app.add_url_rule("/usuarios/updateRoles/<int:id>",
                     "user_updateRoles", user.update_roles, methods=["POST"])
    app.add_url_rule("/usuarios/quitarRoles/<string:username>",
                     "user_quitarRoles", user.quitar_roles, methods=["POST"])

    app.add_url_rule("/usuarios/perfil", "user_perfil", user.perfil)

    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "configuracion_index",
                     configuracion.index)
    app.add_url_rule("/configuracion", "configuracion_update",
                     configuracion.update, methods=["POST"])

    # Rutas de Turno
    app.add_url_rule("/turnos/<int:page_num>", "turno_index", turno.index)
    app.add_url_rule("/turnos", "turno_create", turno.create, methods=["POST"])
    app.add_url_rule("/turnos/nuevo", "turno_new", turno.new)
    app.add_url_rule("/turnos/confirmar/<int:id>",
                     "turno_confirmar", turno.confirmar)
    app.add_url_rule("/turnos/delete/<int:id>", "turno_delete", turno.delete)
    app.add_url_rule("/turnos/edit/<int:id>", "turno_edit", turno.edit)
    app.add_url_rule("/turnos/update/<int:id>", "turno_update",
                     turno.update, methods=["POST"])
    app.add_url_rule("/turnos/busqueda/<int:page_num>",
                     "turno_buscar", turno.buscar, methods=["POST"])

    # Rutas de Centro
    app.add_url_rule("/centros/<int:page_num>", "centro_index", centro.index)
    app.add_url_rule("/centros", "centro_create",
                     centro.create, methods=["POST"])
    app.add_url_rule("/centros/nuevo", "centro_new", centro.new)
    app.add_url_rule("/centros/aprobacion/<int:id>/<int:num>",
                     "centro_aprobacion", centro.act_aprobacion_centro)
    app.add_url_rule("/centros/busqueda/<int:page_num>",
                     "centro_buscar", centro.buscar, methods=["POST"])
    app.add_url_rule("/centros/details/<int:id>",
                     "centro_details", centro.details)
    app.add_url_rule("/centros/confirmar/<string:name>",
                     "centro_confirmar", centro.confirmar)
    app.add_url_rule("/centros/delete/<string:name>",
                     "centro_delete", centro.delete)
    app.add_url_rule("/centros/edit/<int:id>", "centro_edit", centro.edit)
    app.add_url_rule("/centros/update/<int:id>",
                     "centro_update", centro.update, methods=["POST"])
    app.add_url_rule("/centros/descargar-protocolo/<string:name>",
                     "centro_descargar", centro.descargar)

    # Rutas de turno para un único centro
    app.add_url_rule("/centros/<int:centro_id>/turnos/<int:page_num>",
                     "index_by_centro", turno.index_by_centro)
    app.add_url_rule("/centros/<int:centro_id>/turnos",
                     "create_by_centro", turno.create_by_centro, methods=["POST"])
    app.add_url_rule("/centros/<int:centro_id>/turnos/nuevo",
                     "new_by_centro", turno.new_by_centro)
    app.add_url_rule("/centros/<int:centro_id>/turnos/confirmar/<int:turno_id>",
                     "confirmar_by_centro", turno.confirmar_by_centro)
    app.add_url_rule("/centros/<int:centro_id>/turnos/delete/<int:turno_id>",
                     "delete_by_centro", turno.delete_by_centro)
    app.add_url_rule("/centros/<int:centro_id>/turnos/busqueda/<int:page_num>",
                     "turno_by_email", turno.buscar_by_email, methods=["POST"])
    app.add_url_rule("/centros/<int:centro_id>/turnos/edit/<int:turno_id>",
                     "edit_by_centro", turno.edit_by_centro)
    app.add_url_rule("/centros/<int:centro_id>/turnos/update/<int:turno_id>",
                     "update_by_centro", turno.update_by_centro, methods=["POST"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-rest
    app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    app.add_url_rule("/api/centros", "api_centro_index", api_centro.index)
    app.add_url_rule("/api/centros", "api_centro_create",
                     api_centro.create, methods=["POST"])
    app.add_url_rule("/api/centros/<int:id>",
                     "api_centro_details", api_centro.details)
    app.add_url_rule("/api/centros/<int:centro_id>/reserva",
                     "api_turno_create", api_turno.create, methods=["POST"])
    app.add_url_rule("/api/centros/<int:centro_id>/turnos_disponibles",
                     "api_turno_disponibles", api_turno.turnos_disponibles)

    # Agregado para consumir desde VUEJS
    app.add_url_rule("/api/centros/all", "api_centro_all",
                     api_centro.all_centros)
    app.add_url_rule("/api/turnos_ocupados", "api_turnos_ocupados", api_turno.turnos_ocupados)
    app.add_url_rule("/api/<int:centro_id>/turnos_ocupados", "api_turnos_ocupados_centro", api_turno.turnos_ocupados_centro)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(405, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada
    return app

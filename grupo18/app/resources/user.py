from flask import redirect, render_template, request, url_for, session, abort, flash

from app.models.user import User
from app.models.rol import Rol
from app.models.configuracion import Configuracion

from app.helpers.auth import authenticated
from app.helpers.handler import load_errors
from app.helpers.permiso import check as check_permission

from sqlalchemy import or_, and_
from app.db import db

from app.validators import userValidator 

# Protected resources
def index():

    if len(request.args) == 0:
        page_num = 1
    else:
        page_num = int(request.args["page_num"])

    checkeos_session_permisos("usuario_index")

    cant_users = Configuracion.get_cantidad_elementos_lista() 

    users = User.query.paginate(per_page=int(cant_users), page=page_num, error_out=True)


    return render_template("user/index.html", users=users)


def new():

    checkeos_session_permisos('usuario_new')

    return render_template("user/new.html")


def create():

    checkeos_session_permisos('usuario_new')

    is_valid, errors = userValidator.create_user(request.form)
    
    if existe(request.form["username"], request.form["email"]):
        flash("Ya existe un usuario con este nombre de usuario o email!")
        return render_template("user/new.html")

    if is_valid:
        User.create(request.form)
    else:
        load_errors(errors)
        return render_template("user/new.html")

    return redirect(url_for("user_index", page_num=1))


def existe(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email))
    return   user.count() > 0


def delete(username):

    checkeos_session_permisos('usuario_destroy')

    User.delete(username)

    return redirect(url_for("user_index", page_num=1))


def confirmar(username):

    checkeos_session_permisos('usuario_destroy')
    
    return render_template("user/delete.html", username=username)


def edit(username):

    checkeos_session_permisos('usuario_update')

    usuario = User.get_user_by_username(username)

    rol_admin = Rol.getRolByName('administrador')

    is_admin = rol_admin in usuario.roles

    return render_template("user/edit.html", user=usuario, is_admin=is_admin)


def update(id):
    
    checkeos_session_permisos('usuario_update')

    usuario = User.get_user_by_id(id)

    is_valid, errors = userValidator.create_user(request.form)
    
    if User.existe(id, request.form["username"], request.form["email"]):
        flash("Ya existe un usuario con este nombre de usuario o email!")
        return render_template("user/edit.html", user=usuario)

    if is_valid:
        usuario.update(request.form)
    else:
        load_errors(errors)
        return render_template("user/edit.html", user=usuario)

    return redirect(url_for("user_index", page_num=1))
    

def perfil():
    checkeos_session_permisos('usuario_show')

    useremail = authenticated(session)

    usuario = User.get_user_by_email(useremail)

    return render_template("user/details.html", user=usuario)

def asignar_roles(username):

   checkeos_session_permisos('usuario_update')
   
   roles = Rol.all()
   
   user = User.get_user_by_username(username)
   return render_template("user/asignarRoles.html", user=user, roles=roles)


def quitar_roles(username):

    checkeos_session_permisos('usuario_update')

    rol = Rol.getRolByName(request.form["nombre"])
    user = User.get_user_by_username(username)

    user.delete_rol(rol)

    return redirect(url_for("user_asignarRoles", username=username))


def update_roles(id):
    
    checkeos_session_permisos('usuario_update')

    user = User.get_user_by_id(id)

    rolesId = request.form.getlist("id")

    for rol in rolesId:
        user.roles.append(Rol.query.filter_by(id=rol).first())
        
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('user_index', page_num=1))


def buscar(page_num):
    if not authenticated(session):
        abort(401)

    cantUsers = Configuracion.get_cantidad_elementos_lista()

    search = "%{}%".format(request.form["username"])

    if request.form["active"] == 'Todos':
        users = User.query.filter(User.username.ilike(search)).paginate(per_page=int(cantUsers), page=page_num, error_out=True)
    else:
        act = request.form["active"] == 'True'
        users = User.query.filter(and_(User.username.ilike(search), User.active == act )).paginate(per_page=int(cantUsers), page=page_num, error_out=True)


    return render_template("user/index.html", users=users)



def checkeos_session_permisos(perm):
    user = authenticated(session)
    if not user:
        abort(401)

    usuario = User.get_user_by_email(user)

    if not check_permission(usuario.id, perm):
        abort(401)

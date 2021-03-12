from flask import abort, session
from app.helpers.auth import authenticated
from app.models.user import User
from app.models.permiso import Permiso

def check(user_id, permission_name):
    permission = Permiso.get_permission_by_name(permission_name)

    return User.tiene_permiso(user_id, permission)


def checkeos_session_permisos(perm):
    user = authenticated(session)
    if not user:
        abort(401)

    usuario = User.get_user_by_email(user)

    if not check(usuario.id, perm):
        abort(401)

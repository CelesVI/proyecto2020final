from flask import session
from app.models.user import User
from app.models.permission import Permiso
from app.models.rol import Rol


def check(permiso):
   user = User.query.filter_by(email=session.get('user')).first()
   per = Permiso.query.filter_by(nombre=permiso).first()

   for rol in user.roles:
       if per in rol.permisos:
           return True

   return False
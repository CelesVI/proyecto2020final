from app.db import db
from app.models import rol
from app.models.rol import Rol
# from werkzeug.security import generate_password_hash as genph
# from werkzeug.security import check_password_hash as checkph

from sqlalchemy import or_, and_


usuarios_tienen_roles = db.Table('usuarios_tienen_roles', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)    
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100))
    roles = db.relationship('Rol', secondary=usuarios_tienen_roles, lazy='subquery', backref=db.backref('users', lazy=True))

    def __init__(self, email, username, password, active, first_name, last_name):
        self.email = email
        self.username = username
        #self.encriptar(password)
        self.password = password
        self.active = active == 'True'
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User {0} {1} {2} {3}>'.format(self.email, self.username, self.password, self.active, self.first_name, self.last_name)


    @classmethod
    def tiene_permiso(cls, user_id, permission):
        user = User.get_user_by_id(user_id)

        for rol in user.roles:
            if permission in rol.permisos:
                return True

        return False
        
    @classmethod
    def all(cls):
        return User.query.all()
    
    @classmethod
    def create(cls, data):
        newUser = User(data["email"], data["username"], data["password"], data["active"], data["first_name"], data["last_name"])
        db.session.add(newUser)
        db.session.commit()
        return True

    @classmethod
    def find_by_email_and_pass(cls, em, pas ):
        return User.query.filter_by(email=em, password=pas).first()

        # if usuario.verificar(pas):
        #     return usuario
        # else:
        #     return None

    @classmethod
    def delete(cls, username):
        usuario = User.query.filter_by(username=username).first()
        db.session.delete(usuario)
        db.session.commit()
        return True        
          
    @classmethod
    def existe(cls, id , uname, mail):
        user = User.query.filter(and_(or_(User.username == uname, User.email == mail), (User.id != id)))
        return   user.count() > 0

    
    @classmethod
    def get_user_by_id(cls, id):
        return User.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def buscar(self, username, activado):
        search = "%{}%".format(username)

        if activado == 'Todos':
            return User.query.filter(User.username.ilike(search)).all()
        else:
            act = activado == 'True'
            return User.query.filter(and_(User.username.ilike(search), User.active == act )).all()


    def update(self, data):

        # self.encriptar(data["password"])
        self.password = data["password"]
        self.email = data["email"]
        self.username = data["username"]
        self.active = data["active"] == 'True'
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]

        db.session.commit()

        return True

    def delete_rol(self, rol):
        self.roles.remove(rol)

        db.session.commit()

        return True

    #Encriptar/Verificar password

    # def encriptar(self, clave):
    #     self.password = genph(clave)

    # def verificar(self, clave):
    #     return checkph(self.password, clave)

    def get_email(self):
        return self.email

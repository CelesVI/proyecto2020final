from app.db import db
from app.models import permiso

roles_tienen_permisos = db.Table('roles_tienen_permisos',
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id'), primary_key=True)
)

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    permisos = db.relationship('Permiso', secondary=roles_tienen_permisos, lazy='subquery', backref=db.backref('roles', lazy=True))

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return '<Rol {0}>'.format(self.nombre)

    @classmethod
    def all(cls):
        return Rol.query.all()

    @classmethod
    def getRolByName(cls, nombre):
        return Rol.query.filter_by(nombre=nombre).first()

  
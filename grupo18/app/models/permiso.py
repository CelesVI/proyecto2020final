from app.db import db

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__():
        return '<Permiso {0}>'.format(self.nombre)

    @classmethod
    def get_permission_by_name(cls, name):
        return Permiso.query.filter_by(nombre=name).first()
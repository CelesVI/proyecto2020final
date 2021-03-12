from app.db import db
from app.models.centro_social import Centro_social

class Tipo_centro(db.Model):
    __tablename__ = 'tipos_centros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    centros = db.relationship('Centro_social', backref='tipos_centros', lazy=True)

    def __init__ (self, nombre):
        self.nombre = nombre

    @classmethod
    def all(cls):
        return Tipo_centro.query.all()

    @classmethod
    def get_tipo_by_id(cls, id):
        return Tipo_centro.query.filter_by(id=id).first()
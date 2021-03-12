from app.db import db

class Configuracion(db.Model):
    __tablename__ = 'configuraciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __repr__(self):
        return '<Configuracion {0} {1}>'.format(self.nombre, self.valor)

    @classmethod
    def all(cls):
        return Configuracion.query.all()

    @classmethod
    def get_config_by_id(cls, id):
        return Configuracion.query.filter_by(id=id).first()

    @classmethod
    def get_cantidad_elementos_lista(cls):
        cant = Configuracion.query.filter_by(nombre='cantidad_elementos').first()
        return cant.valor

    def update(self, data):
        self.valor = data["valor"]

        db.session.commit()
        return True


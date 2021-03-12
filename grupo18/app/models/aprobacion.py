from app.db import db

class Aprobacion(db.Model):
    __tablename__ = 'aprobacion'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo

    @classmethod
    def all(cls):
            return Aprobacion.query.all()

    @classmethod
    def create(cls, data):
        nuevaAprobacion = Aprobacion(data["tipo"])
        db.session.add(nuevaAprobacion)
        db.session.commit()
        return True

    @classmethod
    def name_by_id(cls, id)
        name = Centro_social.query.filter_by(id=id).first()
        return name.tipo 


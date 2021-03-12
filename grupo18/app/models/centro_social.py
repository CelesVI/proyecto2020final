from app.db import db
#from app.models.aprobacion import Aprobacion
#from app.models.tipo_centro import Tipo_centro
import datetime
from sqlalchemy import or_, and_

class Centro_social(db.Model):
    __tablename__ = 'centros_sociales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    direccion = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    municipio_id = db.Column(db.Integer, nullable=False)
    web = db.Column(db.String(100), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    hora_de_apertura = db.Column(db.Time, nullable=False)
    hora_de_cierre = db.Column(db.Time, nullable=False)
    tipo_centro_id = db.Column(db.Integer, db.ForeignKey('tipos_centros.id'), nullable=False)
    aprobacion_id = db.Column(db.Integer, nullable=False)
    protocolo = db.Column(db.String(100), nullable=True)
    latitud = db.Column(db.String(50), unique=True, nullable=False)
    longitud = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, nombre, direccion, telefono, hora_de_apertura, 
                 hora_de_cierre, municipio_id, tipo_centro_id, web='No posee',
                 email='No posee', protocolo='No posee', latitud='No posee', 
                 longitud='No posee'):

        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.hora_de_apertura = hora_de_apertura
        self.hora_de_cierre = hora_de_cierre
        self.municipio_id = municipio_id
        self.web = web
        self.email = email
        self.aprobacion_id = 1 
        self.latitud = latitud
        self.longitud = longitud
        self.protocolo = protocolo
        self.tipo_centro_id = tipo_centro_id


    @classmethod
    def all(cls):
        return Centro_social.query.all()

    @classmethod
    def create(cls, data, filename):
        nuevoCentro = Centro_social(data["nombre"], data["direccion"], data["telefono"], 
                                    data["hora_de_apertura"], data["hora_de_cierre"], 
                                    data["municipio_id"], data["tipo_centro_id"] , data["web"], 
                                    data["email"], filename, data["latitud"], data["longitud"])
        db.session.add(nuevoCentro)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, name):
        centro = Centro_social.query.filter_by(nombre=name).first()
        db.session.delete(centro)
        db.session.commit()
        return True  

    @classmethod
    def get_centro_by_id(cls, id):
        return Centro_social.query.filter_by(id=id).first()

    @classmethod
    def existe(cls, id , name, direccion, telefono):
        centro = Centro_social.query.filter(and_(or_(or_(
                                                        Centro_social.nombre == name, Centro_social.direccion == direccion), 
                                                (Centro_social.telefono == telefono)),
                                            (Centro_social.id != id)))
        return   centro.count() > 0

    @classmethod
    def get_centro_by_name(cls, name):
        return Centro_social.query.filter_by(nombre=name).first()

    @classmethod
    def get_centro_by_email(cls, email):
        return Centro_social.query.filter_by(email=email).first()

    @classmethod
    def buscar(self, name, activado):
        search = "%{}%".format(name)

        if activado == 'Todos':
            return Centro_social.query.filter(Centro_social.nombre.ilike(search)).all()
        else:
            act = activado == 'True'
            #Revisar Devolución con tipo distinto
            return Centro_social.query.filter(and_(Centro_social.nombre.ilike(search),
                                                   Centro_social.active == act )).all()

    def update(self, data, filename):
        self.nombre = data["nombre"]
        self.direccion = data["direccion"]
        self.telefono = data["telefono"]
        self.hora_de_apertura = data["hora_de_apertura"]
        self.hora_de_cierre = data["hora_de_cierre"]
        self.web = data["web"]
        self.email = data["email"]
        self.aprobacion_id = data["aprobacion_id"]
        self.municipio_id = data["municipio_id"]   
        self.protocolo = filename
        self.latitud = data["latitud"]
        self.longitud = data["longitud"]

        db.session.commit()
        return True

    def complete_update(self, data, filename, latitud, longitud):
        self.nombre = data["nombre"]
        self.direccion = data["direccion"]
        self.telefono = data["telefono"]
        self.hora_de_apertura = data["hora_de_apertura"]
        self.hora_de_cierre = data["hora_de_cierre"]
        self.web = data["web"]
        self.email = data["email"]
        self.municipio_id = data["municipio_id"]
        self.aprobacion_id = data["aprobacion_id"]   
        self.protocolo = filename
        self.latitud = latitud
        self.longitud = longitud

        db.session.commit()
        return True

    def update_by_object(self, centro):
        self.nombre = centro.nombre
        self.direccion = centro.direccion
        self.telefono = centro.telefono
        self.hora_de_apertura = centro.hora_de_apertura
        self.hora_de_cierre = centro.hora_de_cierre
        self.web = centro.web
        self.email = centro.email
        self.municipio_id = centro.municipio_id
        self.protocolo = centro.protocolo
        self.latitud = centro.latitud
        self.longitud = centro.longitud
        self.aprobacion_id = centro.aprobacion_id

        db.session.commit()
        return True
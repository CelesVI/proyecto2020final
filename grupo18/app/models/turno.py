from sqlalchemy import and_
from app.db import db
from datetime import datetime, date, time, timedelta

from sqlalchemy import and_, or_
class Turno(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    telefono = db.Column(db.String(100), unique = True, nullable = False)
    hora_inicio = db.Column(db.Time, nullable = False)
    hora_fin = db.Column(db.Time, nullable = False)
    fecha = db.Column(db.Date)
    centro_id = db.Column(db.Integer, unique = True, nullable = True)
    nombre = db.Column(db.String(100), nullable = False)
    apellido = db.Column(db.String(100), nullable = False)

    def __init__(self, email, telefono, hora_inicio, hora_fin, fecha, centro_id,nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.fecha = fecha
        self.centro_id = centro_id
        # self.nombre = nombre
        self.apellido = apellido

    @classmethod
    def all(cls):
        return Turno.query.all()

    @classmethod
    def create(cls, data):
        new_turno = Turno(data["email"], data["telefono"], data["hora_inicio"], data["hora_fin"], data["fecha"], data["centro_social"], data["nombre"], data["apellido"])
        db.session.add(new_turno)
        db.session.commit()
        return True

    @classmethod
    def create_by_centro(cls, data, centro_id):
        new_turno = Turno(data["nombre"], data["apellido"], data["email"], data["telefono"], data["hora_inicio"], data["hora_fin"], data["fecha"], centro_id)
        db.session.add(new_turno)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, id):
        turno = Turno.query.filter_by(id=id).first()
        db.session.delete(turno)
        db.session.commit()
        return True
    
    def update(self, data):
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.telefono = data["telefono"]
        self.hora_inicio = data["hora_inicio"]
        self.hora_fin = data["hora_fin"]
        self.fecha = data["fecha"]
        self.centro_id = data["centro_social"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        db.session.commit()
        return True

    @classmethod
    def find_by_email(cls, email):
        turnos = Turno.query.filter_by(email=email)
        return turnos
    
    @classmethod
    def find_by_id_centro(cls,id):
        turnos = Turno.query.filter_by(centro_id=id)
        return turnos

    @classmethod
    def get_turno_by_id(cls, id):
        return Turno.query.filter_by(id=id).first()

    @classmethod
    def existe(cls, hora_inicio, fecha, centro_id):
        turno = Turno.query.filter(and_(and_(Turno.hora_inicio == hora_inicio, Turno.fecha == fecha), Turno.centro_id == centro_id))
        return   turno.count() > 0

    @classmethod
    def existe_otro(cls, hora_inicio, fecha, centro_id, turno_id):
        turno = Turno.query.filter(and_(and_(and_(Turno.hora_inicio == hora_inicio, Turno.fecha == fecha), Turno.centro_id == centro_id)), Turno.id != turno_id)
        return   turno.count() > 0

    @classmethod
    def horario_is_valid(cls, hora_inicio, hora_fin):
        hora_apertura = datetime.strptime("9:00", '%H:%M')
        hora_cierre = datetime.strptime("15:00", '%H:%M')
        hora_inicio = datetime.strptime(hora_inicio, '%H:%M')
        hora_fin = datetime.strptime(hora_fin, '%H:%M')
        media_hora = hora_inicio + timedelta(minutes=30) 
        return ((hora_inicio >= hora_apertura) and (hora_inicio <= hora_cierre) and (hora_fin > hora_inicio) and (media_hora == hora_fin))
    
    @classmethod
    def get_turno_by_centro_id(cls, centro_id):
        return Turno.query.filter_by(centro_id=centro_id).all()
        
    @classmethod
    def get_turno_by_centro_id_and_date(cls, centro_id, fecha):
        return Turno.query.filter(and_(Turno.centro_id==centro_id, Turno.fecha==fecha)).all()

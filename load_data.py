import csv
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import (create_engine, Column, String, Integer, Boolean,
                        Date, Float, ForeignKey)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError



DATABASE_URL = "postgresql://postgres:1234@localhost:5432/sigma"

engine = create_engine(DATABASE_URL) # crea la conexión con PostgreeSQL
Session = sessionmaker(bind=engine) # abre sesión para añadir datos
Base = declarative_base()



# Modelos SQLALCHEMY

class Alumnado(Base):
    __tablename__ = "alumnado"
    email = Column(String(20), primary_key=True)
    nombre = Column(String(100), nullable=False)
    movil = Column(String(10), unique=True, nullable=False)
    grado = Column(String(10), nullable=False)
    curso = Column(String(10), nullable=False)


class Proyecto(Base):
    __tablename__ = "proyecto"
    codigo = Column(String(10), primary_key=True)
    nombre = Column(String(120), unique=True, nullable=False)
    descripcion = Column(String(300), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)


class Evento(Base):
    __tablename__ = "evento"
    codigo = Column(String(10), primary_key=True)
    nombre = Column(String(100), nullable=False)
    aforo_max = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    lugar = Column(String(30), nullable=False)
    descripcion = Column(String(300))
    sold_out = Column(Boolean, nullable=False)


class Organizacion(Base):
    __tablename__ = "organizacion"
    codigo = Column(String(10), primary_key=True)
    nombre = Column(String(120), nullable=False)
    tipo = Column(String(30))


class Ponente(Base):
    __tablename__ = "ponente"
    codigo = Column(String(10), primary_key=True)
    nombre = Column(String(120), nullable=False)
    cargo = Column(String(80))
    contacto = Column(String(120))


class PublicacionRRSS(Base):
    __tablename__ = "publicacionrrss"
    id_pub = Column(String(10), primary_key=True)
    plataforma = Column(String(20), nullable=False)
    fecha_hora = Column(Date, nullable=False)
    tipo_contenido = Column(String(100))
    url = Column(String(200))


class RegistroHoras(Base):
    __tablename__ = "registrohoras"
    codigo = Column(String(10), primary_key=True)
    email_alumno = Column(String(20), ForeignKey("alumnado.email", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    fecha = Column(Date, nullable=False)
    horas = Column(Float, nullable=False)
    concepto = Column(String(100))
    tipo = Column(String(20))


class AsignacionCredito(Base):
    __tablename__ = "asignacioncredito"
    codigo_asignacion = Column(String(10), primary_key=True)
    email_alumno = Column(String(20), ForeignKey("alumnado.email", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    creditos = Column(String(10), nullable=False)
    fecha_asignacion = Column(Date, nullable=False)
    motivo = Column(String(50))


class ParticipacionProyecto(Base):
    __tablename__ = "participacionproyecto"
    email = Column(String(20), ForeignKey("alumnado.email", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    codigo_proyecto = Column(String(10), ForeignKey("proyecto.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    rol = Column(String(30))
    nivel_participacion = Column(String(20))
    horas_dedicadas = Column(Integer)


class Inscripcion(Base):
    __tablename__ = "inscripcion"
    email = Column(String(20), ForeignKey("alumnado.email", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    codigo_evento = Column(String(10), ForeignKey("evento.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    fecha_inscripcion = Column(Date, nullable=False)
    canal = Column(String(30))
    asiste = Column(Boolean, nullable=False)


class Participa(Base):
    __tablename__ = "participa"
    codigo_evento = Column(String(10), ForeignKey("evento.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    codigo_organizacion = Column(String(10), ForeignKey("organizacion.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class Imparte(Base):
    __tablename__ = "imparte"
    codigo_evento = Column(String(10), ForeignKey("evento.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    codigo_ponente = Column(String(10), ForeignKey("ponente.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class Promociona(Base):
    __tablename__ = "promociona"
    id_pub = Column(String(10), ForeignKey("publicacionrrss.id_pub", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    codigo_evento = Column(String(10), ForeignKey("evento.codigo", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class MetricaPublicacion(Base):
    __tablename__ = "metricapublicacion"
    codigo = Column(String(10), primary_key=True)
    fecha_medicion = Column(Date, primary_key=True)
    likes = Column(Integer)
    reposts = Column(Integer)
    comentarios = Column(Integer)
    visualizaciones = Column(Integer)
    id_pub = Column(String(10), ForeignKey("publicacionrrss.id_pub", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)



# Función de carga

def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_csv(session, model, path):
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile) # lee cada fila como un diccionario
        for row in reader:
            for key, value in row.items():
                if isinstance(key, str) and "fecha" in key and value:
                    row[key] = parse_date(value)
                if value == "true":
                    row[key] = True
                if value == "false":
                    row[key] = False

            try:
                obj = model(**row)
                session.add(obj)
            except IntegrityError:
                session.rollback()
                print(f"IntegrityError en {model.__tablename__}: {row}")
            except Exception as e:
                print(f"Error en {model.__tablename__}: {e}")

        session.commit()
        print(f"{model.__tablename__} cargado")




if __name__ == "__main__":

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine) # crea en PostgreeSQL las tablas 
    session = Session()

    try:
        
        load_csv(session, Alumnado, "data/alumnado.csv")
        load_csv(session, Proyecto, "data/proyecto.csv")
        load_csv(session, Evento, "data/evento.csv")
        load_csv(session, Organizacion, "data/organizacion.csv")
        load_csv(session, Ponente, "data/ponente.csv")
        load_csv(session, PublicacionRRSS, "data/publicacionrrss.csv")

        load_csv(session, RegistroHoras, "data/registrohoras.csv")
        load_csv(session, AsignacionCredito, "data/asignacioncredito.csv")
        load_csv(session, ParticipacionProyecto, "data/participacionproyecto.csv")
        load_csv(session, Inscripcion, "data/inscripcion.csv")
        load_csv(session, Participa, "data/participa.csv")
        load_csv(session, Imparte, "data/imparte.csv")
        load_csv(session, Promociona, "data/promociona.csv")
        load_csv(session, MetricaPublicacion, "data/metricapublicacion.csv")

        print("CARGA COMPLETADA")

    finally:
        session.close()
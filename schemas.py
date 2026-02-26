from __future__ import annotations  # Permite usar tipos sin problemas de orden
from datetime import date, datetime  # Tipos para fecha y fecha+hora
from typing import Optional  # Permite que un campo pueda ser None
from pydantic import BaseModel, EmailStr, HttpUrl  # Herramientas para validar datos

# ------TABLA ALUMNADO ----------
class Alumnado(BaseModel):
    email: EmailStr  # tira(20) pero validando formato email
    nombre: str  
    movil: str  
    grado: str  
    curso: str  

# ------TABLA EVENTO ----------
class Evento(BaseModel):
    codigo: str  
    nombre: str  
    aforo_max: int  # entero
    fecha: date  # fecha
    lugar: str 
    descripcion: Optional[str] = None  # tira(300) {0..1}
    sold_out: bool  # booleano

# ------TABLA REGISTRO HORAS ----------
class RegistroHoras(BaseModel):
    codigo: str
    email_alumno: EmailStr  
    fecha: date
    horas: float  #real
    concepto: Optional[str] = None
    tipo: Optional[str] = None

# ------TABLA ASIGNACIÓN CRÉDITO ----------
class AsignacionCredito(BaseModel):
    codigo_asignacion: str
    email_alumno: EmailStr  
    creditos: str
    fecha_asignacion: date
    motivo: Optional[str] = None

# ------TABLA PROYECTO ----------
class Proyecto(BaseModel):
    codigo: str
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None

# ------TABLA PARTICIPACION PROYECTO (ASOCIATIVA) ----------
class ParticipacionProyecto(BaseModel):
    codigo_proyecto: str  #lo hereda de Proyecto por ser una tabla asociativa
    email: EmailStr  #lo hereda de Proyecto por ser una tabla asociativa
    rol: Optional[str] = None
    nivel_participacion: Optional[str] = None
    horas_dedicadas: Optional[int] = None

# ------TABLA INSCRIPCION (ASOCIATIVA) ----------
class Inscripcion(BaseModel):
    email: EmailStr  #lo hereda de Proyecto por ser una tabla asociativa
    codigo_evento: str  #lo hereda de Evento por ser una tabla asociativa
    fecha_inscripcion: date
    canal: Optional[str] = None
    asiste:bool

# ------TABLA PONENTE ----------
class Ponente(BaseModel):
    codigo: str
    nombre: str
    cargo: Optional[str] = None
    contacto: Optional[str] = None

# ------TABLA ORGANIZACION ----------
class Organizacion(BaseModel):
    codigo: str
    nombre: str
    tipo: Optional[str] = None

# ------TABLA PUBLICACION RRSS ----------
class PublicacionRRSS(BaseModel):
    id_pub: str
    plataforma: str
    fecha_hora: date
    tipo_contenido: Optional[str] = None
    url: Optional[HttpUrl] = None    #url

# ------TABLA METRICA PUBLICACION ----------
class MetricaPublicacion(BaseModel):
    codigo: str
    fecha_medicion: date
    likes: Optional[int] = None
    reposts: Optional[int] = None
    comentarios: Optional[int] = None
    visualizaciones: Optional[int] = None
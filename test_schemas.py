from pydantic import ValidationError
from schemas import Alumnado, PublicacionRRSS, Evento

def test_ok_alumnado():
    data = {"email": "emma@gmail.com",
        "nombre": "Emma",
        "movil": "612345678",
        "grado": "GII",
        "curso": "3",}
    alumno = Alumnado(**data)  #convierte el diccionario en un objeto de la clase Alumnado
    print("OK Alumnado")

def test_fail_alumnado_email():
    data = {"email": "esto_no_es_email",  #email inválido porque no tiene @,
        "nombre": "Emma",
        "movil": "612345678",
        "grado": "GII",
        "curso": "3",}
    try:
        Alumnado(**data)
    except ValidationError as e:
        print("FAIL email (como debe ser) ->")
        print(e)  #imprime el error y cómo corregirlo

def test_ok_publicacion_url():
    data = {"id_pub": "PUB001",
        "plataforma": "Instagram",
        "fecha_hora": "2026-02-13",  # string -> se convierte a date
        "tipo_contenido": "foto",
        "url": "https://example.com/post/1",}
    pub = PublicacionRRSS(**data)
    print("OK PublicacionRRSS")

def test_fail_publicacion_url():
    data = {"id_pub": "PUB001",
        "plataforma": "Instagram",
        "fecha_hora": "2026-02-13",
        "url": "no_es_una_url",}
    try:
        PublicacionRRSS(**data)
    except ValidationError as e:
        print("FAIL url (como debe ser) ->")
        print(e)

def test_ok_evento():
    data = {"codigo": "E001",
        "nombre": "Charla IA",
        "aforo_max": 100,
        "fecha": "2026-03-01",  # string -> date
        "lugar": "Valencia",
        "sold_out": False,}
    evento = Evento(**data)
    print("OK Evento")

if __name__ == "__main__":
    test_ok_alumnado()
    test_fail_alumnado_email()
    test_ok_publicacion_url()
    test_fail_publicacion_url()
    test_ok_evento()

from fastapi import FastAPI, HTTPException
from typing import List
from db import get_conn
from schemas import Alumnado, Evento  # Importamos el modelo Pydantic de las tablas Alumnado y Evento creado en schemas.py

app = FastAPI(title="Sigma Internal Database API", version="0.1")  # Creación de FastAPI

@app.get("/health")     # Para probar que FastAPI arranca, incluso antes de conectar a la BD
def health():
    return {"status": "ok"}


# ------CRUD: ALUMNADO ----------

@app.get("/alumnado", response_model=List[Alumnado])   # Método GET /alumnado (devuelve una lista en JSON de todo el alumnado)
def list_alumnado():
    with get_conn() as conn:   # Abre una conexión a PostgreSQL (temporal) y se cerrará al salir del bloque
        with conn.cursor() as cur:   #Ejecuta un SQL (SELECT en este caso)
            cur.execute("""
                SELECT email, nombre, movil, grado, curso
                FROM alumnado
                ORDER BY email;
            """)
            return cur.fetchall()  # Devuelve todas las filas (lista de dicts) -> FastAPI lo convierte a JSON


@app.get("/alumnado/{email}", response_model=Alumnado)   # Método GET /alumnado/{email} (busca y muestra el alumno por ID)
def get_alumno(email: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT email, nombre, movil, grado, curso
                FROM alumnado
                WHERE email = %s;   
            """, (email,))   # %s porque es el mecanismo seguro de psycopg2 para pasar parámetros
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Alumno no encontrado")
            return row


@app.post("/alumnado", response_model=Alumnado, status_code=201)   # Método POST /alumnado (crear un alumno)
def create_alumno(payload: Alumnado):
    with get_conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO alumnado (email, nombre, movil, grado, curso)
                    VALUES (%s, %s, %s, %s, %s);
                """, (payload.email, payload.nombre, payload.movil, payload.grado, payload.curso))
                conn.commit()       # Guarda definitivamente el INSERT
            except Exception as e:    # Si hay error (duplicado de PK..)
                raise HTTPException(status_code=409, detail=f"No se pudo crear: {str(e)}")
    return payload


@app.put("/alumnado/{email}", response_model=Alumnado) # Método PUT /alumnado/{email} (actualiza un alumno)
def update_alumno(email: str, payload: Alumnado):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT email
                FROM alumnado
                WHERE email = %s;
            """, (email,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Alumno no encontrado")

            try:
                cur.execute("""
                    UPDATE alumnado
                    SET nombre = %s, movil = %s, grado = %s, curso = %s
                    WHERE email = %s;
                """, (payload.nombre, payload.movil, payload.grado, payload.curso, email))
                conn.commit()
            except Exception as e:
                raise HTTPException(status_code=409, detail=f"No se pudo actualizar: {str(e)}")

    return payload


@app.delete("/alumnado/{email}", status_code=204)   # Método DELETE /alumnado/{email} (elimina un alumno)
def delete_alumno(email: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM alumnado
                WHERE email = %s;
            """, (email,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Alumno no encontrado")
            conn.commit()


# ------CRUD: EVENTO ----------

@app.get("/evento", response_model=List[Evento])   # Método GET /evento (lista todos los eventos)
def list_eventos():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT codigo, nombre, aforo_max, fecha, lugar, descripcion, sold_out
                FROM evento
                ORDER BY fecha DESC;
            """)
            return cur.fetchall()


@app.get("/evento/{codigo}", response_model=Evento)   # Método GET /evento/{codigo} (busca y muestra el evento por ID)
def get_evento(codigo: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT codigo, nombre, aforo_max, fecha, lugar, descripcion, sold_out
                FROM evento
                WHERE codigo = %s;
            """, (codigo,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Evento no encontrado")
            return row


@app.post("/evento", response_model=Evento, status_code=201)    # Método POST /evento (crear un evento)
def create_evento(payload: Evento):
    with get_conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO evento (codigo, nombre, aforo_max, fecha, lugar, descripcion, sold_out)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    payload.codigo,
                    payload.nombre,
                    payload.aforo_max,
                    payload.fecha,
                    payload.lugar,
                    payload.descripcion,
                    payload.sold_out
                ))
                conn.commit()
            except Exception as e:
                raise HTTPException(status_code=409, detail=f"No se pudo crear: {str(e)}")
    return payload

@app.put("/evento/{codigo}", response_model=Evento)   # Método PUT /evento/{codigo} (actualiza un evento)
def update_evento(codigo: str, payload: Evento):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT codigo
                FROM evento
                WHERE codigo = %s;
            """, (codigo,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Evento no encontrado")

            try:
                cur.execute("""
                    UPDATE evento
                    SET nombre = %s, aforo_max = %s, fecha = %s,
                        lugar = %s, descripcion = %s, sold_out = %s
                    WHERE codigo = %s;
                """, (
                    payload.nombre,
                    payload.aforo_max,
                    payload.fecha,
                    payload.lugar,
                    payload.descripcion,
                    payload.sold_out,
                    codigo
                ))
                conn.commit()
            except Exception as e:
                raise HTTPException(status_code=409, detail=f"No se pudo actualizar: {str(e)}")

    return payload

@app.delete("/evento/{codigo}", status_code=204)   # Método DELETE /evento/{codigo} (elimina un evento)
def delete_evento(codigo: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM evento
                WHERE codigo = %s;
            """, (codigo,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Evento no encontrado")
            conn.commit()
BEGIN;

CREATE TABLE alumnado (
  email          VARCHAR(20)  PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  movil         VARCHAR(10)  NOT NULL UNIQUE,
  grado         VARCHAR(50)  NOT NULL,
  curso         VARCHAR(10)  NOT NULL
);

CREATE TABLE proyecto (
  codigo        VARCHAR(10)  PRIMARY KEY,
  nombre        VARCHAR(120) NOT NULL UNIQUE,
  descripcion   VARCHAR(300) NOT NULL,
  fecha_inicio  DATE         NOT NULL,
  fecha_fin     DATE
);

CREATE TABLE evento (
  codigo        VARCHAR(10)  PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  aforo_max     INTEGER      NOT NULL,
  fecha         DATE         NOT NULL,
  lugar         VARCHAR(30)  NOT NULL,
  descripcion   VARCHAR(300),
  sold_out      BOOLEAN      NOT NULL
);

CREATE TABLE organizacion (
  codigo        VARCHAR(10)  PRIMARY KEY,
  nombre        VARCHAR(120) NOT NULL,
  tipo          VARCHAR(30)
);

CREATE TABLE ponente (
  codigo        VARCHAR(10)  PRIMARY KEY,
  nombre        VARCHAR(120) NOT NULL,
  cargo         VARCHAR(80),
  contacto      VARCHAR(120)
);

CREATE TABLE publicacion_rrss (
  id_pub        VARCHAR(10)  PRIMARY KEY,
  plataforma    VARCHAR(20)  NOT NULL,
  fecha_hora    DATE         NOT NULL,
  tipo_contenido VARCHAR(100),
  url           VARCHAR(200)
);

CREATE TABLE registro_horas (
  codigo        VARCHAR(10) PRIMARY KEY,
  email_alumno  VARCHAR(20)  NOT NULL,
  fecha         DATE         NOT NULL,
  horas         REAL         NOT NULL,
  concepto      VARCHAR(100),
  tipo          VARCHAR(20),
  CONSTRAINT fk_registrohoras_alumno
    FOREIGN KEY (email_alumno)
    REFERENCES alumnado(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE asignacion_credito (
  codigo_asignacion VARCHAR(10) PRIMARY KEY,
  email_alumno     VARCHAR(20) NOT NULL,
  creditos          VARCHAR(10) NOT NULL,
  fecha_asignacion  DATE        NOT NULL,
  motivo            VARCHAR(50),
  CONSTRAINT fk_asignacioncredito_alumno
    FOREIGN KEY (email_alumno)
    REFERENCES alumnado(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE participacion_proyecto (
  email              VARCHAR(20) NOT NULL,
  codigo_proyecto  VARCHAR(10) NOT NULL,
  rol              VARCHAR(30),
  nivel_participacion VARCHAR(20),
  horas_dedicadas  INTEGER,
  PRIMARY KEY (email, codigo_proyecto),
  CONSTRAINT fk_participacion_alumno
    FOREIGN KEY (email)
    REFERENCES alumnado(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_participacion_proyecto
    FOREIGN KEY (codigo_proyecto)
    REFERENCES proyecto(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE inscripcion (
  email              VARCHAR(20) NOT NULL,
  codigo_evento    VARCHAR(10) NOT NULL,
  fecha_inscripcion DATE       NOT NULL,
  canal            VARCHAR(30),
  asiste           BOOLEAN     NOT NULL,
  PRIMARY KEY (email, codigo_evento),
  CONSTRAINT fk_inscripcion_alumno
    FOREIGN KEY (email)
    REFERENCES alumnado(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_inscripcion_evento
    FOREIGN KEY (codigo_evento)
    REFERENCES evento(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE participa (
  codigo_evento       VARCHAR(10) NOT NULL,
  codigo_organizacion VARCHAR(10) NOT NULL,
  PRIMARY KEY (codigo_evento, codigo_organizacion),
  CONSTRAINT fk_participa_evento
    FOREIGN KEY (codigo_evento)
    REFERENCES evento(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_participa_organizacion
    FOREIGN KEY (codigo_organizacion)
    REFERENCES organizacion(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE imparte (
  codigo_evento  VARCHAR(10) NOT NULL,
  codigo_ponente VARCHAR(10) NOT NULL,
  PRIMARY KEY (codigo_evento, codigo_ponente),
  CONSTRAINT fk_imparte_evento
    FOREIGN KEY (codigo_evento)
    REFERENCES evento(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_imparte_ponente
    FOREIGN KEY (codigo_ponente)
    REFERENCES ponente(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE promociona (
  id_pub       VARCHAR(10) NOT NULL,
  codigo_evento VARCHAR(10) NOT NULL,
  PRIMARY KEY (id_pub, codigo_evento),
  CONSTRAINT fk_promociona_publicacion
    FOREIGN KEY (id_pub)
    REFERENCES publicacion_rrss(id_pub)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_promociona_evento
    FOREIGN KEY (codigo_evento)
    REFERENCES evento(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE metrica_publicacion (
  codigo         VARCHAR(10) NOT NULL,
  fecha_medicion DATE        NOT NULL,
  likes          INTEGER,
  reposts        INTEGER,
  comentarios    INTEGER,
  visualizaciones INTEGER,
  PRIMARY KEY (codigo, fecha_medicion),
  CONSTRAINT fk_metrica_publicacion
    FOREIGN KEY (codigo)
    REFERENCES publicacion_rrss(id_pub)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

COMMIT;

-- ==========================================================================
-- ESQUEMA: DEVELOPER_01_SV
-- Tablas: ROLE, EMPLOYEE, REQUEST, REQUEST_DETAIL
-- ==========================================================================

-- ============================================================
-- TABLA: ROLE
-- ============================================================
CREATE TABLE role (
    id           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         VARCHAR2(35) NOT NULL UNIQUE,
    description  VARCHAR2(50)
);

-- ============================================================
-- TABLA: EMPLOYEE
-- ============================================================
CREATE TABLE employee (
    id                NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type_document     CHAR(3) NOT NULL 
                       CHECK (type_document IN ('DNI','CNE')),
    number_document   VARCHAR2(15) NOT NULL UNIQUE,
    names             VARCHAR2(100) NOT NULL,
    lastnames         VARCHAR2(90) NOT NULL,
    birthdate         DATE NOT NULL,
    phone             VARCHAR2(9) UNIQUE 
                       CHECK (REGEXP_LIKE(phone, '^9[0-9]{8}$')),
    email             VARCHAR2(100) UNIQUE
                       CHECK (REGEXP_LIKE(email, '.+@.+\..+')),
    address           VARCHAR2(100),
    gender            CHAR(1) CHECK (gender IN ('M','F')),
    vacation_days     NUMBER(2) DEFAULT 30 CHECK (vacation_days >= 0),
    role_id           NUMBER NOT NULL,
    area_id           NUMBER,

    CONSTRAINT ck_number_document
        CHECK (
          (type_document = 'DNI' AND REGEXP_LIKE(number_document, '^[0-9]{8}$')) OR
          (type_document = 'CNE' AND REGEXP_LIKE(number_document, '^[0-9]{12}$'))
        )
);

ALTER TABLE DEVELOPER_01_SV.EMPLOYEE ADD (STATUS VARCHAR2(1) DEFAULT 'A');
-- ============================================================
-- TABLA: REQUEST
-- ============================================================
CREATE TABLE request (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    request_date    DATE NOT NULL,
    description     VARCHAR2(2000),
    employee_id     NUMBER NOT NULL
);

-- =======================================
-- REQUEST_DETAIL
-- =======================================

CREATE TABLE request_detail (
    id               NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    start_date       DATE NOT NULL,
    end_date         DATE NOT NULL,
    days_requested   NUMBER(3,0) NOT NULL
                     CHECK (days_requested >= 1 AND days_requested <= 30),
    request_id       NUMBER NOT NULL,

    CONSTRAINT ck_valid_dates CHECK (end_date >= start_date)
);



-- ==========================================================================
-- ESQUEMA: DEVELOPER_02_SV
-- Tablas: REQUEST_STATUS, REVIEW_REQUEST, AREA
-- ==========================================================================

-- ============================================================
-- TABLA: REQUEST_STATUS
-- ============================================================
CREATE TABLE request_status (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    state_request   VARCHAR2(30) NOT NULL,
    description     VARCHAR2(50)
);

-- ============================================================
-- TABLA: AREA
-- ============================================================
CREATE TABLE area (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            VARCHAR2(50) NOT NULL,
    description     VARCHAR2(60),
    status          CHAR(1) DEFAULT 'A' CHECK (status IN ('A','I')),
    chief_area_id   NUMBER UNIQUE,
);

-- ============================================================
-- TABLA: REVIEW_REQUEST
-- ============================================================
CREATE TABLE review_request (
    id                 NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    review_date        DATE NOT NULL,
    reason_rejection   VARCHAR2(100),
    observation        VARCHAR2(260),
    reviser_id         NUMBER,
    request_id         NUMBER NOT NULL,
    request_status_id  NUMBER NOT NULL
);

-- ============================================================
-- PERMISOS ENTRE ESQUEMAS DEVELOPER_02_SV sobre las tablas del 01
-- ============================================================

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_01_SV.ROLE TO DEVELOPER_02_SV;

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_01_SV.EMPLOYEE TO DEVELOPER_02_SV;

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_01_SV.REQUEST TO DEVELOPER_02_SV;

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_01_SV.REQUEST_DETAIL TO DEVELOPER_02_SV;

-- Permitir referencias (foreign keys)
GRANT REFERENCES ON DEVELOPER_01_SV.EMPLOYEE TO DEVELOPER_02_SV;
GRANT REFERENCES ON DEVELOPER_01_SV.REQUEST TO DEVELOPER_02_SV;



-- ============================================================
-- Otorgar permisos al esquema DEVELOPER_01_SV sobre las tablas del 02
-- ============================================================ 

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_02_SV.REQUEST_STATUS TO DEVELOPER_01_SV;

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_02_SV.REVIEW_REQUEST TO DEVELOPER_01_SV;

GRANT SELECT, INSERT, UPDATE, DELETE
ON DEVELOPER_02_SV.AREA TO DEVELOPER_01_SV;

-- Permitir referencias (foreign keys)
GRANT REFERENCES ON DEVELOPER_02_SV.AREA TO DEVELOPER_01_SV;
GRANT REFERENCES ON DEVELOPER_02_SV.REQUEST_STATUS TO DEVELOPER_01_SV;





-- ============================================================
-- RELACIONES - DEVELOPER_01_SV
-- ============================================================

-- EMPLOYEE → ROLE
ALTER TABLE employee
ADD CONSTRAINT fk_employee_role
FOREIGN KEY (role_id)
REFERENCES role(id);

-- EMPLOYEE → AREA
ALTER TABLE employee
ADD CONSTRAINT fk_employee_area
FOREIGN KEY (area_id)
REFERENCES DEVELOPER_02_SV.area(id);

-- REQUEST → EMPLOYEE
ALTER TABLE request
ADD CONSTRAINT fk_request_employee
FOREIGN KEY (employee_id)
REFERENCES employee(id);

-- REQUEST_DETAIL → REQUEST
ALTER TABLE request_detail
ADD CONSTRAINT fk_requestdetail_request
FOREIGN KEY (request_id)
REFERENCES request(id);


-- ============================================================
-- RELACIONES - DEVELOPER_02_SV
-- ============================================================

-- REVIEW_REQUEST → REQUEST_STATUS
ALTER TABLE review_request
ADD CONSTRAINT fk_reviewrequest_status
FOREIGN KEY (request_status_id)
REFERENCES request_status(id);

-- REVIEW_REQUEST → REQUEST
ALTER TABLE review_request
ADD CONSTRAINT fk_reviewrequest_request
FOREIGN KEY (request_id)
REFERENCES DEVELOPER_01_SV.request(id);

-- REVIEW_REQUEST → EMPLOYEE (revisor)
ALTER TABLE review_request
ADD CONSTRAINT fk_reviewrequest_reviser
FOREIGN KEY (reviser_id)
REFERENCES DEVELOPER_01_SV.employee(id);

-- AREA → EMPLOYEE (jefe de área)
ALTER TABLE area
ADD CONSTRAINT fk_area_chief
FOREIGN KEY (chief_area_id)
REFERENCES DEVELOPER_01_SV.employee(id);

-- =======================================
-- DATOS INICIALES - TABLA ROLE
-- =======================================
INSERT INTO ROLE (name, description)
VALUES ('EMPLEADO', 'Empleado general de la organización');

INSERT INTO ROLE (name, description)
VALUES ('JEFE_AREA', 'Encargado del área, aprueba solicitudes del personal');

INSERT INTO ROLE (name, description)
VALUES ('RRHH', 'Encargado del área de Recursos Humanos, gestiona personal y jefes');


-- ======================================================
-- EMPLEADOS (Jefes de área y RRHH)
-- ======================================================

-- Gestión Agrícola – Freddy Centurión Cárdenas
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '45678912', 'Freddy', 'Centurión Cárdenas', DATE '1980-04-12', '912345678', 'freddy.centurion@vallegrande.edu.pe', 'Av. Agraria 125', 'M', 30, 2, 1);

-- Análisis de Sistema Empresarial – Luis Manzo Candela
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '45879632', 'Luis', 'Manzo Candela', DATE '1988-06-22', '913456789', 'luis.manzo@vallegrande.edu.pe', 'Av. Tecnológica 540', 'M', 30, 2, 2);

-- Dirección General – Joel Anaya Castillo
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '40123987', 'Joel', 'Anaya Castillo', DATE '1975-09-03', '914567890', 'joel.anaya@vallegrande.edu.pe', 'Calle Central 210', 'M', 30, 2, 3);

-- Administración – Yván Pajares Shiozawa
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '42345987', 'Yván', 'Pajares Shiozawa', DATE '1984-01-19', '915678901', 'yvan.pajares@vallegrande.edu.pe', 'Av. Valle Grande 450', 'M', 30, 2, 4);

-- Bienestar al Estudiante – Enzo Parra Tello Mena
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '42658975', 'Enzo', 'Parra Tello Mena', DATE '1990-03-28', '916789012', 'enzo.parra@vallegrande.edu.pe', 'Jr. Los Pinos 320', 'M', 30, 2, 5);

-- Contabilidad – Ynés Felipa Hernández
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '47896512', 'Ynés Felipa', 'Hernández', DATE '1983-08-15', '917890123', 'ynes.hernandez@vallegrande.edu.pe', 'Av. Contable 112', 'F', 30, 2, 6);

-- Laboratorio Química Agrícola – Julio Castro Lazo
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '46523987', 'Julio', 'Castro Lazo', DATE '1986-07-25', '918901234', 'julio.castro@vallegrande.edu.pe', 'Av. Química 230', 'M', 30, 2, 7);

-- Mantenimiento – Julio Vargas Solís
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '45986324', 'Julio', 'Vargas Solís', DATE '1981-02-14', '919012345', 'julio.vargas@vallegrande.edu.pe', 'Calle Talleres 500', 'M', 30, 2, 8);

-- Secretaría Académica – José Ochoa Montoya
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '47652139', 'José', 'Ochoa Montoya', DATE '1979-11-30', '920123456', 'jose.ochoa@vallegrande.edu.pe', 'Av. Académica 102', 'M', 30, 2, 9);

-- Recursos Humanos – Eva Manzo Candela (RRHH)
INSERT INTO EMPLOYEE (type_document, number_document, names, lastnames, birthdate, phone, email, address, gender, vacation_days, role_id, area_id)
VALUES ('DNI', '42369874', 'Eva', 'Manzo Candela', DATE '1987-09-14', '921234567', 'eva.manzo@vallegrande.edu.pe', 'Av. Recursos 99', 'F', 30, 3, 10);

-- =======================================
-- INSERTAR ÁREAS  DEVELOPER 02_SV
-- =======================================
INSERT INTO AREA (name, description) VALUES (
  'Gestión Agrícola',
  'Área encargada de coordinar y supervisar las actividades formativas y prácticas en el ámbito agrícola, incluyendo el manejo de cultivos y la gestión de los campos experimentales.'
);

INSERT INTO AREA (name, description) VALUES (
  'Análisis de Sistema Empresarial',
  'Área orientada a la planificación y desarrollo de proyectos tecnológicos e informáticos que apoyan la gestión académica y administrativa del instituto.'
);

INSERT INTO AREA (name, description) VALUES (
  'Dirección General',
  'Área responsable de la toma de decisiones estratégicas, supervisión institucional y coordinación general de todas las áreas académicas y administrativas.'
);

INSERT INTO AREA (name, description) VALUES (
  'Administración',
  'Área encargada de la gestión financiera, logística y administrativa del instituto, garantizando el correcto funcionamiento de los recursos y procesos.'
);

INSERT INTO AREA (name, description) VALUES (
  'Bienestar al Estudiante',
  'Área que brinda acompañamiento psicológico, social y académico a los estudiantes, fomentando su desarrollo personal y bienestar emocional.'
);

INSERT INTO AREA (name, description) VALUES (
  'Contabilidad',
  'Área responsable de la gestión contable y presupuestal del instituto, encargada del registro y control de los movimientos financieros.'
);

INSERT INTO AREA (name, description) VALUES (
  'Laboratorio Química Agrícola',
  'Área destinada a la realización de prácticas y análisis químicos de suelos, cultivos y fertilizantes, apoyando la formación técnica en el ámbito agrícola.'
);

INSERT INTO AREA (name, description) VALUES (
  'Mantenimiento',
  'Área encargada del mantenimiento preventivo y correctivo de las instalaciones, equipos y espacios del instituto Valle Grande.'
);

INSERT INTO AREA (name, description) VALUES (
  'Secretaría Académica',
  'Área que gestiona los procesos académicos, matrículas, registros y documentación de los estudiantes y docentes.'
);

INSERT INTO AREA (name, description) VALUES (
  'Recursos Humanos',
  'Área encargada de la administración del personal, reclutamiento, capacitación y gestión del clima laboral en el instituto.'
);

-- =======================================
-- ACTUALIZAR ÁREAS CON SU JEFE
-- =======================================
UPDATE AREA SET chief_area_id = 1 WHERE id = 1;
UPDATE AREA SET chief_area_id = 2 WHERE id = 2;
UPDATE AREA SET chief_area_id = 3 WHERE id = 3;
UPDATE AREA SET chief_area_id = 4 WHERE id = 4;
UPDATE AREA SET chief_area_id = 5 WHERE id = 5;
UPDATE AREA SET chief_area_id = 6 WHERE id = 6;
UPDATE AREA SET chief_area_id = 7 WHERE id = 7;
UPDATE AREA SET chief_area_id = 8 WHERE id = 8;
UPDATE AREA SET chief_area_id = 9 WHERE id = 9;
UPDATE AREA SET chief_area_id = 10 WHERE id = 10; 
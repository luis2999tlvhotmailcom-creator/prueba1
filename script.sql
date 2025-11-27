/* ============================
CREACIÓN DE TABLESPACE
============================ */
CREATE TABLESPACE INVERSIONESVICTORIA
DATAFILE 'inversionesVictoria.dbf'
SIZE 400M;

/* LISTAR TABLESPACES */
SELECT TABLESPACE_NAME, STATUS, CONTENTS FROM USER_TABLESPACES;

/* ACTIVAR ORACLE SCRIPT */
ALTER SESSION SET "_oracle_script" = TRUE;

/* ============================
CREACIÓN DE USUARIOS
============================ */
CREATE USER GestorA IDENTIFIED BY ORCL1234 DEFAULT TABLESPACE INVERSIONESVICTORIA TEMPORARY TABLESPACE TEMP QUOTA UNLIMITED ON INVERSIONESVICTORIA;

/* ============================
    ASIGNACIÓN DE PRIVILEGIOS
   ============================ */
GRANT CREATE SESSION TO GestorA;
GRANT CREATE TABLE TO GestorA;
GRANT CREATE VIEW TO GestorA;
GRANT CREATE PROCEDURE TO GestorA;
GRANT CREATE TRIGGER TO GestorA;
GRANT CREATE SEQUENCE TO GestorA;
GRANT CREATE JOB TO GestorA;
GRANT UNLIMITED TABLESPACE TO GestorA;

/* LISTADO DE USUARIOS */
SELECT * FROM DBA_USERS;












-- =============================
--  TABLAS DE APOYO (primero para FK)
-- =============================

CREATE TABLE category (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    description VARCHAR2(100),
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL
);

CREATE TABLE app_user (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    password VARCHAR2(20) NOT NULL,
    role CHAR(4) NOT NULL,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL
);

-- =============================
--  TABLAS MAESTRAS
-- =============================

CREATE TABLE product (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    brand VARCHAR2(30),
    sales_price NUMBER(6,2) CHECK (sales_price >= 0) NOT NULL,
    purchase_price NUMBER(6,2) CHECK (purchase_price >= 0) NOT NULL,
    description VARCHAR2(200),
    stock NUMBER DEFAULT 0 CHECK (stock >= 0) NOT NULL,
    expiration_date DATE,
    category_id NUMBER,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE supplier (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    ruc CHAR(11) NOT NULL UNIQUE
        CHECK (REGEXP_LIKE(ruc, '^[1-2][0-9]{10}$')),
    phone VARCHAR2(9) NOT NULL
        CHECK (REGEXP_LIKE(phone, '^9[0-9]{8}$')),
    email VARCHAR2(120) NOT NULL UNIQUE
        CHECK (REGEXP_LIKE(email, '.+@.+\..+')),
    address VARCHAR2(150),
    contact_name VARCHAR2(50),
    contact_phone VARCHAR2(9)
        CHECK (REGEXP_LIKE(contact_phone, '^9[0-9]{8}$')),
    contact_email VARCHAR2(150),
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL,
    registration_date DATE DEFAULT SYSDATE NOT NULL
);

ALTER TABLE supplier
ADD tipo_empresa VARCHAR2(30) DEFAULT 'Micro empresa'
    CHECK (tipo_empresa IN ('Micro empresa', 'Macro empresa'));


CREATE TABLE customer (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(120) NOT NULL,
    phone VARCHAR2(9)
        CHECK (REGEXP_LIKE(phone, '^9[0-9]{8}$')),
    email VARCHAR2(120) NOT NULL UNIQUE
        CHECK (REGEXP_LIKE(email, '.+@.+\..+')),
    address VARCHAR2(120) NOT NULL,
    identification_document CHAR(3) NOT NULL
        CHECK (identification_document IN ('DNI', 'CNE')),
    document_number VARCHAR2(15) NOT NULL,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')),
    registration_date DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT UQ_customer_document UNIQUE (identification_document, document_number),
    CONSTRAINT CK_customer_doc CHECK (
        (identification_document = 'DNI' AND REGEXP_LIKE(document_number, '^[0-9]{8}$')) OR
        (identification_document = 'CNE' AND REGEXP_LIKE(document_number, '^[0-9]{9}|[0-9]{11}$'))
    )
);

CREATE TABLE seller (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(150) NOT NULL,
    phone CHAR(9)
        CHECK (REGEXP_LIKE(phone, '^9[0-9]{8}$')),
    email VARCHAR2(120) NOT NULL UNIQUE
        CHECK (REGEXP_LIKE(email, '.+@.+\..+')),
    identification_document CHAR(3) NOT NULL
        CHECK (identification_document IN ('DNI', 'CNE')),
    document_number CHAR(15) NOT NULL,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')),
    registration_date DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT UQ_seller_document UNIQUE (identification_document, document_number)
);

-- =============================
--  TABLAS TRANSACCIONALES
-- =============================

CREATE TABLE sale (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    sale_date DATE DEFAULT SYSDATE NOT NULL,
    total NUMBER(6,2) CHECK (total >= 0) NOT NULL,
    payment_type CHAR(1) CHECK (payment_type IN ('E', 'T', 'Y')) NOT NULL,
    seller_id NUMBER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (seller_id) REFERENCES seller(id)
);

CREATE TABLE sale_detail (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id NUMBER NOT NULL,
    amount NUMBER CHECK (amount > 0) NOT NULL,
    unit_price NUMBER(4,2) CHECK (unit_price >= 0) NOT NULL,
    sale_id NUMBER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (sale_id) REFERENCES sale(id)
);

CREATE TABLE purchase (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id NUMBER NOT NULL,
    user_id NUMBER NOT NULL,
    purchase_date DATE DEFAULT SYSDATE NOT NULL,
    total NUMBER(6,2) CHECK (total >= 0) NOT NULL,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES supplier(id),
    FOREIGN KEY (user_id) REFERENCES app_user(id)
);

CREATE TABLE purchase_detail (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    purchase_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    amount NUMBER CHECK (amount > 0) NOT NULL,
    unit_price NUMBER(4,2) CHECK (unit_price >= 0) NOT NULL,
    subtotal NUMBER(6,2) CHECK (subtotal >= 0) NOT NULL,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchase(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);



-- =============================
--  INVENTARIO
-- =============================

CREATE TABLE inventory (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id NUMBER NOT NULL,
    quantity NUMBER CHECK (quantity >= 0) NOT NULL,
    last_update DATE DEFAULT SYSDATE NOT NULL,
    min_stock NUMBER CHECK (min_stock >= 0) NOT NULL,
    max_stock NUMBER CHECK (max_stock >= 0) NOT NULL,
    status CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I')) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- =============================
-- CATEGORÍAS
-- =============================
INSERT INTO category (name, description, status) VALUES ('Limpieza', 'Productos de limpieza para el hogar', 'A');
INSERT INTO category (name, description, status) VALUES ('Higiene Personal', 'Cuidado e higiene personal', 'A');
INSERT INTO category (name, description, status) VALUES ('Plásticos', 'Envases, botellas y otros plásticos', 'A');
INSERT INTO category (name, description, status) VALUES ('Descartables', 'Vasos, platos y utensilios descartables', 'A');

-- =============================
-- USUARIOS
-- =============================
INSERT INTO app_user (username, password, role, status) VALUES ('admin', 'admin123', 'ADMN', 'A');
INSERT INTO app_user (username, password, role, status) VALUES ('cajero1', 'cajero123', 'CAJE', 'A');
INSERT INTO app_user (username, password, role, status) VALUES ('almacen1', 'almacen123', 'ALMC', 'A');

-- =============================
-- PROVEEDORES
-- =============================
INSERT INTO supplier (name, ruc, phone, email, address, contact_name, contact_phone, contact_email, tipo_empresa) 
VALUES ('Distribuidora LimpiaMax', '10456789012', '912345678', 'ventas@limpimax.com', 'Av. Central 123, Lima', 'Juan Perez', '987654321', 'juan@limpimax.com', 'Macro empresa');

INSERT INTO supplier (name, ruc, phone, email, address, contact_name, contact_phone, contact_email, tipo_empresa) 
VALUES ('Plásticos del Sur', '20456789123', '923456789', 'contacto@plasticosur.com', 'Jr. Comercio 456, Arequipa', 'Maria Lopez', '976543210', 'maria@plasticosur.com', 'Micro empresa');

INSERT INTO supplier (name, ruc, phone, email, address, contact_name, contact_phone, contact_email, tipo_empresa) 
VALUES ('Higiene Global SAC', '10456789234', '934567890', 'info@higieneglobal.com', 'Av. Progreso 789, Trujillo', 'Carlos Medina', '965432109', 'carlos@higieneglobal.com', 'Macro empresa');

-- =============================
-- PRODUCTOS
-- =============================
INSERT INTO product (name, brand, sales_price, purchase_price, description, stock, expiration_date, category_id, status) 
VALUES ('Detergente líquido 1L', 'LimpiaMax', 12.50, 8.00, 'Detergente líquido para ropa', 100, TO_DATE('2026-12-31','YYYY-MM-DD'), 1, 'A');

INSERT INTO product (name, brand, sales_price, purchase_price, description, stock, expiration_date, category_id, status) 
VALUES ('Escoba multiusos', 'CasaPlus', 15.00, 10.00, 'Escoba para limpieza general', 50, NULL, 1, 'A');

INSERT INTO product (name, brand, sales_price, purchase_price, description, stock, expiration_date, category_id, status) 
VALUES ('Shampoo 500ml', 'HigieneGlobal', 18.00, 12.00, 'Shampoo para todo tipo de cabello', 80, TO_DATE('2025-05-20','YYYY-MM-DD'), 2, 'A');

INSERT INTO product (name, brand, sales_price, purchase_price, description, stock, expiration_date, category_id, status) 
VALUES ('Paquete de vasos descartables x50', 'PlastiSur', 6.00, 3.50, 'Vasos descartables de plástico 7oz', 200, NULL, 4, 'A');

INSERT INTO product (name, brand, sales_price, purchase_price, description, stock, expiration_date, category_id, status) 
VALUES ('Bolsa plástica x100', 'PlastiSur', 10.00, 6.50, 'Paquete de bolsas plásticas resistentes', 150, NULL, 3, 'A');

-- =============================
-- CLIENTES
-- =============================
INSERT INTO customer (name, last_name, phone, email, address, identification_document, document_number, status) 
VALUES ('Luis', 'Gonzales', '987654321', 'luisg@mail.com', 'Av. Primavera 456', 'DNI', '76543210', 'A');

INSERT INTO customer (name, last_name, phone, email, address, identification_document, document_number, status) 
VALUES ('Ana', 'Ramirez', '912345678', 'anaram@mail.com', 'Calle Los Pinos 321', 'DNI', '87654321', 'A');

-- =============================
-- VENDEDORES
-- =============================
INSERT INTO seller (name, last_name, phone, email, identification_document, document_number, status) 
VALUES ('Pedro', 'Martinez', '945678123', 'pedro.martinez@victoria.com', 'DNI', '45678912', 'A');

INSERT INTO seller (name, last_name, phone, email, identification_document, document_number, status) 
VALUES ('Rosa', 'Fernandez', '934567812', 'rosa.fernandez@victoria.com', 'DNI', '56789123', 'A');

-- =============================
-- VENTAS Y DETALLE
-- =============================
INSERT INTO sale (customer_id, sale_date, total, payment_type, seller_id) 
VALUES (1, SYSDATE, 50.00, 'E', 1);

INSERT INTO sale_detail (product_id, amount, unit_price, sale_id) 
VALUES (1, 2, 12.50, 1); -- 2 detergentes

INSERT INTO sale_detail (product_id, amount, unit_price, sale_id) 
VALUES (4, 5, 6.00, 1); -- 5 paquetes vasos

-- =============================
-- COMPRAS Y DETALLE
-- =============================
INSERT INTO purchase (supplier_id, user_id, purchase_date, total, status) 
VALUES (1, 1, SYSDATE, 800.00, 'A');

INSERT INTO purchase_detail (purchase_id, product_id, amount, unit_price, subtotal, status) 
VALUES (1, 1, 100, 8.00, 800.00, 'A');

-- =============================
-- INVENTARIO
-- =============================
INSERT INTO inventory (product_id, quantity, last_update, min_stock, max_stock, status) 
VALUES (1, 100, SYSDATE, 20, 500, 'A');

INSERT INTO inventory (product_id, quantity, last_update, min_stock, max_stock, status) 
VALUES (4, 200, SYSDATE, 50, 1000, 'A');





-- ============================
-- BOLETO DE VENTA (sale_id = 1)
-- ============================

SELECT '========================================' AS linea FROM dual
UNION ALL
SELECT '        BOLETA DE VENTA - Inversiones Victoria' FROM dual
UNION ALL
SELECT 'RUC: 10456789012   Tel: 912345678' FROM dual
UNION ALL
SELECT 'Dirección: Av. Central 123, Lima' FROM dual
UNION ALL
SELECT '========================================' FROM dual
UNION ALL
SELECT 'Boleta N°: ' || s.id || '   Fecha: ' || TO_CHAR(s.sale_date, 'DD/MM/YYYY')
FROM sale s WHERE s.id = 1
UNION ALL
SELECT 'Cliente: ' || c.name || ' ' || c.last_name 
FROM customer c JOIN sale s ON c.id = s.customer_id WHERE s.id = 1
UNION ALL
SELECT 'Vendedor: ' || v.name || ' ' || v.last_name
FROM seller v JOIN sale s ON v.id = s.seller_id WHERE s.id = 1
UNION ALL
SELECT '----------------------------------------' FROM dual
UNION ALL
SELECT 'Cant  Producto                     P.Unit   Subtotal' FROM dual
UNION ALL
SELECT LPAD(d.amount, 4) || '  ' ||
       RPAD(p.name, 25) || ' ' ||
       TO_CHAR(d.unit_price, '9990.00') || '   ' ||
       TO_CHAR(d.amount * d.unit_price, '9990.00')
FROM sale_detail d
JOIN product p ON d.product_id = p.id
WHERE d.sale_id = 1
UNION ALL
SELECT '----------------------------------------' FROM dual
UNION ALL
SELECT 'TOTAL: S/ ' || TO_CHAR(s.total, '9990.00')
FROM sale s WHERE s.id = 1
UNION ALL
SELECT 'Forma de pago: ' ||
       CASE s.payment_type
            WHEN 'E' THEN 'Efectivo'
            WHEN 'T' THEN 'Tarjeta'
            WHEN 'Y' THEN 'Yape/Plin'
       END
FROM sale s WHERE s.id = 1
UNION ALL
SELECT '========================================' FROM dual;



SELECT * FROM PURCHASE;
SELECT * FROM PURCHASE_DETAIL;
SELECT * FROM SALE;
SELECT * FROM SALE_DETAIL;

CREATE TABLE customer (
    customer_id int IDENTITY(1,1) NOT NULL,
    name varchar(50)  NOT NULL,
    last_name varchar(120)  NOT NULL,
    cellular char(9)  NOT NULL,
    email varchar(120)  NOT NULL,
    address varchar(120)  NOT NULL,
    identification_document char(3)  NOT NULL,
    document_number char(15)  NOT NULL,
    CONSTRAINT customer_pk PRIMARY KEY  (customer_id)
);

CREATE TABLE product (
    product_id INT IDENTITY(1,1) PRIMARY KEY, 
    category_id INT NOT NULL,                
    supplier_id INT NOT NULL,                
    name VARCHAR(50) NOT NULL,
    status CHAR(1) NOT NULL,                
    brand VARCHAR(20),
    sales_price DECIMAL(5,2) NOT NULL,       
    purchase_price DECIMAL(5,2) NOT NULL,
    sku VARCHAR(12),                         
    description VARCHAR(200),
    stock INT NOT NULL,
    expiration_date DATE                   

);

CREATE TABLE seller (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    identification_document CHAR(3) NOT NULL CHECK (identification_document IN ('DNI', 'CE')),
    document_number VARCHAR(20) NOT NULL UNIQUE,
    cellular VARCHAR(9) NOT NULL CHECK (cellular LIKE '9[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    status CHAR(1) NOT NULL DEFAULT 'A' CHECK (status IN ('A', 'I'))
);

CREATE TABLE supplier (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(50) NOT NULL,
    cellular VARCHAR(9) NOT NULL CHECK (cellular LIKE '9[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    ruc CHAR(11) NOT NULL UNIQUE CHECK (ruc LIKE '1__________' OR ruc LIKE '2__________'),
    status CHAR(1) NOT NULL DEFAULT 'A' CHECK (status IN ('A', 'I')),
    email VARCHAR(150)
);

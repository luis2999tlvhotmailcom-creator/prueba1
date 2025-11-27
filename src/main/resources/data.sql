-- Crear el registro si es que no se duplican datos unicos o se insertan datos nulos
INSERT INTO customer (name, last_name, cellular, email, address, identification_document, document_number)
VALUES 
('Lucía', 'Fernández', '912345678', 'lucia.fernandez@gmail.com', 'Av. Perú 123', 'DNI', '12345678'),
('Carlos', 'Ramos', '987654321', 'carlos.ramos@yahoo.com', 'Jr. Lima 456', 'CEX', '87654321'),
('María', 'Gómez', '911223344', 'maria.gomez@hotmail.com', 'Calle Real 789', 'PAS', 'A1234567');

INSERT INTO product (category_id, supplier_id, name, status, brand, sales_price, purchase_price, sku, description, stock, expiration_date)
VALUES
(1, 1, 'Vaso descartable 9oz', 'A', 'PlastiPack', 0.50, 0.30, 'VP9OZ001', 'Vasos desechables para bebidas frías', 500, '2026-12-31'),
(1, 2, 'Tenedor plástico blanco', 'A', 'EcoTable', 0.20, 0.10, 'TPBL002', 'Tenedores de plástico resistentes', 1000, '2026-11-30'),
(2, 1, 'Caja de chocolates', 'A', 'Chocology', 15.00, 10.00, 'CHC003', 'Caja con 12 bombones artesanales', 200, '2025-12-01');

INSERT INTO supplier (name, cellular, ruc, status, email)
VALUES ('Plasticos Canete', '912345678', '20123456789', 'A', 'plasticos@example.com');
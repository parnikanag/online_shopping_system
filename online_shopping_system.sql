CREATE TABLE CUSTOMER 
(
    Customer_id INT PRIMARY KEY AUTO_INCREMENT,
    Customer_name VARCHAR(100),
    Customer_address VARCHAR(255),
    Customer_contact VARCHAR(15)
);
CREATE TABLE SUPPLIER (
    Supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    Supplier_name VARCHAR(100),
    Supplier_address VARCHAR(255)
);
CREATE TABLE PRODUCT (
    Prod_id INT PRIMARY KEY AUTO_INCREMENT,
    Prod_name VARCHAR(100),
    Prod_price DECIMAL(10, 2),
    Supplier_id INT,
    FOREIGN KEY (Supplier_id) REFERENCES SUPPLIER(Supplier_id)
);
CREATE TABLE ORDERS (
    Order_no INT PRIMARY KEY AUTO_INCREMENT,
    Order_date DATE,
    Order_amount DECIMAL(10, 2),
    Customer_id INT,
    FOREIGN KEY (Customer_id) REFERENCES CUSTOMER(Customer_id)
);
CREATE TABLE TRACKING_DETAIL (
    Tracking_id INT PRIMARY KEY AUTO_INCREMENT,
    Prod_id INT,
    Prod_name VARCHAR(100),
    Prod_price DECIMAL(10, 2),
    Prod_status VARCHAR(50),
    FOREIGN KEY (Prod_id) REFERENCES PRODUCT(Prod_id)
);
CREATE TABLE ADMIN (
    Admin_id INT PRIMARY KEY AUTO_INCREMENT,
    Admin_name VARCHAR(100),
    Role VARCHAR(50)
);




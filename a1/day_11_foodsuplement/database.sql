CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    price DECIMAL(6,2)
);


CREATE TABLE sales(
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
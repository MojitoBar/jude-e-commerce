CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    country VARCHAR(100)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(20) NOT NULL UNIQUE,
    invoice_date TIMESTAMP NOT NULL,
    customer_id INT REFERENCES customers(customer_id)
);


CREATE TABLE products (
    stock_code VARCHAR(20) PRIMARY KEY,
    description TEXT
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(20) REFERENCES orders(invoice_no),
    stock_code VARCHAR(20) REFERENCES products(stock_code),
    quantity INT NOT NULL,
    unit_price NUMERIC NOT NULL
);

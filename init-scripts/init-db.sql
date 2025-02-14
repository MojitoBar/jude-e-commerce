CREATE DATABASE ecommerce;
\c ecommerce;

-- 기존 테이블이 있다면 삭제
DROP TABLE IF EXISTS sales CASCADE;
DROP TABLE IF EXISTS customer_summary CASCADE;

-- sales 테이블 생성
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50),
    stock_code VARCHAR(50),
    product_name VARCHAR(255),
    quantity INTEGER,
    date TIMESTAMP,
    price DECIMAL(10,2),
    customer_id INTEGER,
    country VARCHAR(100),
    total_amount DECIMAL(10,2)
);

-- customer_summary 테이블 생성
CREATE TABLE IF NOT EXISTS customer_summary (
    customer_id INTEGER PRIMARY KEY,
    total_purchase_amount DECIMAL(10,2),
    total_orders INTEGER,
    total_items INTEGER
);

-- airflow 사용자에게 권한 부여
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO airflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO airflow; 
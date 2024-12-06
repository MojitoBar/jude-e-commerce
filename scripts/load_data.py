import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL 연결
engine = create_engine('postgresql://postgres:1214@localhost:5432/ecommerce')

# CSV 파일 로드
data = pd.read_csv('data/data.csv', encoding='ISO-8859-1')

# 중복 제거 및 결측값 처리: customers 테이블
customers = data[['CustomerID', 'Country']].drop_duplicates()
customers.columns = ['customer_id', 'country']
customers = customers.dropna(subset=['customer_id'])
customers = customers.drop_duplicates(subset=['customer_id'])
customers.to_sql('customers', engine, if_exists='append', index=False)

# 중복 제거 및 결측값 처리: products 테이블
products = data[['StockCode', 'Description']].drop_duplicates()
products.columns = ['stock_code', 'description']
products = products.dropna(subset=['stock_code'])
products = products.drop_duplicates(subset=['stock_code'])
products.to_sql('products', engine, if_exists='append', index=False)

# 중복 제거 및 결측값 처리: orders 테이블
orders = data[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates()
orders.columns = ['invoice_no', 'invoice_date', 'customer_id']
orders = orders.dropna(subset=['invoice_no', 'invoice_date', 'customer_id'])
orders = orders.drop_duplicates(subset=['invoice_no'])
orders.to_sql('orders', engine, if_exists='append', index=False)

# 중복 제거 및 결측값 처리: order_items 테이블
order_items = data[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']]
order_items.columns = ['invoice_no', 'stock_code', 'quantity', 'unit_price']
order_items = order_items.dropna()

# 'order_items'에서 'orders'에 없는 invoice_no 필터링
orders_invoice_nos = set(orders['invoice_no'])
order_items = order_items[order_items['invoice_no'].isin(orders_invoice_nos)]

order_items.to_sql('order_items', engine, if_exists='append', index=False)

print("Data loaded successfully!")

import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL 연결 설정
DATABASE_URI = "postgresql://postgres:1214@postgres:5432/ecommerce"
engine = create_engine(DATABASE_URI)

def extract_data():
    """
    Step 1: 데이터 추출 (Extract)
    데이터베이스에서 원시 데이터를 읽어옵니다.
    """
    print("Extracting data...")
    orders_query = 'SELECT * FROM orders'
    order_items_query = "SELECT * FROM order_items"
    products_query = "SELECT * FROM products"
    customers_query = "SELECT * FROM customers"
    
    orders = pd.read_sql(orders_query, engine)
    order_items = pd.read_sql(order_items_query, engine)
    products = pd.read_sql(products_query, engine)
    customers = pd.read_sql(customers_query, engine)
    
    print("Data extracted successfully!")
    return orders, order_items, products, customers

def transform_data(orders, order_items, products, customers):
    """
    Step 2: 데이터 변환 (Transform)
    """
    print("Transforming data...")
    
    # 결측값 처리
    orders.fillna({"column_name": "default_value"}, inplace=True)  # 필요한 경우 기본값으로 대체
    order_items.dropna(subset=["invoice_no", "stock_code"], inplace=True)
    products.dropna(subset=["stock_code"], inplace=True)
    customers.dropna(subset=["customer_id"], inplace=True)
    
    # 데이터 조인
    enriched_data = (
        order_items
        .merge(orders, on="invoice_no", how="inner")
        .merge(products, on="stock_code", how="inner")
        .merge(customers, on="customer_id", how="inner")
    )
    
    # 총 주문 금액 계산
    enriched_data["total_price"] = enriched_data["quantity"].fillna(0) * enriched_data["unit_price"].fillna(0)
    
    # 데이터 요약 생성
    summarized_data = enriched_data.groupby("customer_id").agg({
        "total_price": "sum",
        "invoice_no": "count"
    }).reset_index()
    summarized_data.rename(columns={"invoice_no": "order_count"}, inplace=True)
    
    print("Data transformed successfully!")
    return enriched_data, summarized_data

def load_data(enriched_data, summarized_data):
    """
    Step 3: 데이터 적재 (Load)
    """
    print("Loading data...")
    enriched_data.to_sql("enriched_data", engine, if_exists="replace", index=False)
    summarized_data.to_sql("summarized_data", engine, if_exists="replace", index=False)
    print("Data loaded successfully!")

def run_etl_script():
    """
    ETL Pipeline 실행 함수
    """
    print("Starting ETL pipeline...")
    try:
        orders, order_items, products, customers = extract_data()
        enriched_data, summarized_data = transform_data(orders, order_items, products, customers)
        load_data(enriched_data, summarized_data)
        print("ETL pipeline completed successfully!")
    except Exception as e:
        print(f"ETL pipeline failed: {e}")

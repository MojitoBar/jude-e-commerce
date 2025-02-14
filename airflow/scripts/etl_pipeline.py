import pandas as pd
from sqlalchemy import create_engine
import chardet
import os

def detect_encoding(file_path):
    """파일의 인코딩을 감지합니다."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def extract_data():
    """
    Step 1: 데이터 추출 (Extract)
    CSV 파일에서 데이터를 읽어옵니다.
    """
    print("Extracting data...")
    try:
        file_path = '/opt/airflow/data/data.csv'
        # 파일 접근 권한 확인
        try:
            with open(file_path, 'r') as f:
                print(f"File can be opened for reading")
        except IOError as e:
            print(f"File access error: {e}")
            raise
            
        encoding = detect_encoding(file_path)
        print(f"Detected file encoding: {encoding}")
        
        df = pd.read_csv(file_path, encoding=encoding)
        
        # 데이터 구조 확인을 위한 로그 추가
        print("CSV 파일 컬럼:", df.columns.tolist())
        print("데이터 샘플:\n", df.head())
        
        print("Data extracted successfully!")
        return df
    except Exception as e:
        print(f"Data extraction failed: {e}")
        # 파일 정보 출력
        try:
            stat = os.stat(file_path)
            print(f"File permissions: {oct(stat.st_mode)}")
            print(f"File owner: {stat.st_uid}")
            print(f"File group: {stat.st_gid}")
        except Exception as e2:
            print(f"Could not get file info: {e2}")
        raise

def transform_data(df):
    """
    Step 2: 데이터 변환 (Transform)
    """
    print("Transforming data...")
    
    print("변환 전 컬럼:", df.columns.tolist())
    
    # 컬럼 이름 매핑 - Country를 소문자로 변경
    df = df.rename(columns={
        'InvoiceDate': 'date',
        'Description': 'product_name',
        'UnitPrice': 'price',
        'Quantity': 'quantity',
        'CustomerID': 'customer_id',
        'InvoiceNo': 'invoice_no',
        'StockCode': 'stock_code',
        'Country': 'country'  # 소문자로 변경
    })
    
    # 결측값 처리
    fill_values = {
        'date': pd.Timestamp.now(),
        'product_name': "Unknown Product",
        'price': 0,
        'quantity': 0,
        'customer_id': -1,
        'invoice_no': 'UNKNOWN',
        'stock_code': 'UNKNOWN'
    }
    df.fillna(fill_values, inplace=True)
    
    # 데이터 타입 변환
    df['date'] = pd.to_datetime(df['date'])  # 날짜 형식 변환
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['customer_id'] = pd.to_numeric(df['customer_id'], errors='coerce')
    
    # 총 주문 금액 계산
    df['total_amount'] = df['price'] * df['quantity']
    
    # 고객별 요약 데이터 생성
    customer_summary = df.groupby('customer_id').agg({
        'total_amount': 'sum',
        'invoice_no': 'nunique',  # 고유한 주문 수
        'stock_code': 'count'     # 총 주문 상품 수
    }).reset_index()
    
    customer_summary.rename(columns={
        'total_amount': 'total_purchase_amount',
        'invoice_no': 'total_orders',
        'stock_code': 'total_items'
    }, inplace=True)
    
    print("Data transformed successfully!")
    return df, customer_summary

def load_data(df, customer_summary, engine):
    """
    Step 3: 데이터 적재 (Load)
    """
    print("Loading data...")
    try:
        # 메인 sales 테이블에 데이터 저장
        df.to_sql('sales', engine, if_exists='append', index=False)
        
        # 고객 요약 테이블에 데이터 저장
        customer_summary.to_sql('customer_summary', engine, if_exists='replace', index=False)
        
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Data loading failed: {e}")
        raise

def run_etl_script():
    """
    ETL Pipeline 실행 함수
    """
    print("Starting ETL pipeline...")
    
    # PostgreSQL 연결 설정
    DATABASE_URL = "postgresql://airflow:airflow@postgres:5432/ecommerce"
    
    try:
        # PostgreSQL 엔진 생성
        engine = create_engine(DATABASE_URL)
        
        # ETL 프로세스 실행
        raw_data = extract_data()
        transformed_data, customer_summary = transform_data(raw_data)
        load_data(transformed_data, customer_summary, engine)
        
        print("ETL pipeline completed successfully!")
        
    except Exception as e:
        print(f"ETL pipeline failed: {str(e)}")
        raise

# 🛍 E-Commerce 데이터 파이프라인 & 분석 대시보드

## 💡 프로젝트 소개

전자상거래 거래 데이터를 ETL 파이프라인으로 처리하고 Metabase를 통해 "360° Sales & Customer Insights" 대시보드를 구축했습니다. 매출, 고객, 상품 데이터를 자동으로 처리하고 시각화하여 데이터 기반 의사결정을 지원합니다.

## 🔧 기술 스택

### Data Pipeline
- **Apache Airflow**: 워크플로우 관리 및 스케줄링
- **Python & Pandas**: 데이터 처리 및 분석
- **SQLAlchemy**: ORM을 통한 데이터베이스 연동
- **chardet**: 파일 인코딩 자동 감지

### Infrastructure
- **Docker Compose**: 컨테이너 기반 인프라 구축
- **PostgreSQL**: 데이터 저장 및 관리
- **Metabase**: 데이터 시각화 및 대시보드

## 🎯 프로젝트 구조

### 디렉토리 구조
````
project/
├── airflow/
│   ├── dags/
│   │   └── etl_pipeline_dag.py
│   └── scripts/
│       └── etl_pipeline.py
├── data/
│   └── data.csv
├── init-scripts/
│   └── init-db.sql
├── .env
├── docker-compose.yaml
└── README.md
````


### 시스템 아키텍처
````
[CSV Data] → [Airflow ETL] → [PostgreSQL] → [Metabase Dashboard]
    ↓             ↓              ↓                ↓
Raw Data    Data Processing    Storage     "360° Sales Insights"
````


## 📊 데이터베이스 스키마

### sales 테이블
````sql
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
````


### customer_summary 테이블
````sql
CREATE TABLE IF NOT EXISTS customer_summary (
    customer_id INTEGER PRIMARY KEY,
    total_purchase_amount DECIMAL(10,2),
    total_orders INTEGER,
    total_items INTEGER
);
````


## 🌟 주요 기능

### 1. ETL 파이프라인
- CSV 파일 자동 인코딩 감지 및 데이터 추출
- 데이터 정제 및 표준화
- 고객별 구매 요약 데이터 생성

### 2. "360° Sales & Customer Insights" 대시보드
- 일별 매출 추이 (라인 차트)
- 국가별 매출 분포 (지도)
- 고객 세그먼트 분포 (도넛 차트)
- 시간대별 주문 패턴 (바 차트)
- 상위 판매 제품 (수평 바 차트)
- 월별 매출 및 성장률 (복합 차트)

![Image](https://github.com/user-attachments/assets/90f6e304-55e5-493f-b2e4-f7d9f213bc9e)

## 🚀 주요 성과

- ETL 파이프라인 자동화 구현
- Docker 기반의 안정적인 실행 환경 구성
- PostgreSQL과 Metabase를 활용한 분석 환경 구축
- 데이터 파일 인코딩 문제 해결로 안정성 향상
- 실시간 데이터 모니터링 환경 구축

## 🎓 학습 내용

이 프로젝트를 통해 다음과 같은 기술을 실전에서 적용했습니다:
- ETL 파이프라인 설계 및 구현
- Docker를 활용한 컨테이너 기반 개발
- 데이터베이스 모델링 및 쿼리 작성
- 데이터 시각화 및 대시보드 구축

## 📝 회고

이 프로젝트를 통해 데이터 엔지니어링의 전체 프로세스를 경험할 수 있었습니다. 특히 파일 인코딩, 데이터베이스 연결, 권한 관리 등 실제 프로젝트에서 발생할 수 있는 다양한 문제들을 해결하면서 많은 것을 배웠습니다. 앞으로도 데이터 품질과 시스템 안정성을 고려한 데이터 파이프라인 구축에 대해 더 깊이 공부하고 싶습니다.

## ⚠️ 트러블슈팅
자세한 문제 해결 과정은 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)를 참조하세요.

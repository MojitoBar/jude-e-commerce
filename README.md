# E-Commerce Data Analysis Project

## **프로젝트 개요**

이 프로젝트는 전자상거래 데이터를 분석 가능한 형태로 정제하고 저장하기 위한 데이터 엔지니어링 파이프라인을 구축하는 것을 목표로 합니다.

Python, PostgreSQL, Docker, 그리고 Airflow를 활용하여 데이터 파이프라인을 자동화하고, 주기적으로 데이터를 가공하여 분석 테이블을 생성합니다.

---

## **폴더 구조**

```bash
ecommerce-data-analysis/
├── airflow/                 # Airflow 관련 파일 및 설정
│   ├── dags/                # Airflow DAG 파일
│   │   └── etl_pipeline_dag.py
│   ├── logs/                # Airflow 로그 파일
│   ├── airflow.cfg          # Airflow 설정 파일
│   └── scripts/             # ETL 파이프라인 스크립트
│       └── etl_pipeline.py
├── data/                    # 데이터 폴더
│   └── data.csv             # 원시 데이터
├── db_data/                 # PostgreSQL 데이터 폴더 (Docker에서 생성)
├── docker-compose.yml       # Docker 구성 파일
├── scripts/                 # Python 스크립트 폴더
│   ├── create_tables.sql    # 데이터베이스 테이블 생성 스크립트
│   └── load_data.py         # 초기 데이터 적재 스크립트
└── README.md                # 프로젝트 설명 파일
```

---

## **진행된 내용**

### 1. **프로젝트 초기 설정**

- **환경 구성**:
    - Docker를 이용해 PostgreSQL과 Airflow 컨테이너 설정.
    - Python, Pandas, SQLAlchemy 등 필수 패키지 설치 및 테스트 완료.
- **데이터셋 준비**:
    - `data.csv` 파일을 `data/` 디렉토리에 저장.
    - 이 데이터는 전자상거래의 주문 데이터를 포함합니다.
- **GitHub 레포지토리 생성**:
    - 디렉토리 구조 설정 및 `README.md`와 `requirements.txt` 파일 생성.

---

### 2. **데이터 수집 및 데이터베이스 설계**

- **테이블 설계 및 생성**:
    - `create_tables.sql` 스크립트를 통해 PostgreSQL에 테이블 생성:
        - `orders`, `order_items`, `products`, `customers`.
- **데이터 로딩**:
    - `load_data.py`를 실행하여 `data.csv` 데이터를 PostgreSQL 테이블에 적재.
- **SQL 쿼리 테스트**:
    - 데이터 조회 및 검증을 통해 적재된 데이터 확인 완료.

---

### 3. **데이터 분석 파이프라인 구축**

- **ETL 파이프라인 설계**:
    - Python 기반 `etl_pipeline.py` 스크립트를 작성:
        - **Extract**: PostgreSQL에서 원시 데이터 읽기.
        - **Transform**: Pandas로 데이터 정제 및 가공.
        - **Load**: 변환된 데이터를 PostgreSQL의 새로운 테이블로 저장.
- **Airflow DAG 생성**:
    - `etl_pipeline_dag.py`를 작성하여 ETL 작업을 Airflow에서 실행.
- **Airflow 테스트**:
    - Airflow 웹 UI에서 DAG 실행 테스트 완료.

---

## **앞으로 해야 할 일**

### 1. **분석 및 시각화**

- ETL 파이프라인으로 생성된 `enriched_data`와 `summarized_data` 테이블을 분석.
- Tableau, Power BI, 또는 Python(Matplotlib/Seaborn)을 이용해 데이터를 시각화.

### 2. **ETL 성능 최적화**

- 대규모 데이터에 대비해 ETL 성능을 점검하고 최적화.
- 필요한 경우 Airflow 작업 병렬 처리(Task Dependency) 설정.

### 3. **문서화 및 발표 준비**

- 프로젝트의 전체 과정, 구조, 문제 해결 방식을 상세히 문서화.
- 최종 결과를 발표할 때 활용할 슬라이드 준비.

---

## **사용된 기술 스택**

- **Python**: 데이터 처리 및 ETL 파이프라인 작성.
- **PostgreSQL**: 데이터베이스 설계 및 데이터 저장.
- **Airflow**: 데이터 파이프라인 스케줄링 및 자동화.
- **Docker**: 컨테이너 기반 환경 설정.
- **Pandas & SQLAlchemy**: 데이터 변환 및 데이터베이스 연결.

---

## **DAG 구성**

현재 구성된 DAG의 이름과 역할:

- **etl_pipeline_dag**:
    - 매일 한 번씩 실행되는 ETL 파이프라인.
    - PostgreSQL에서 데이터를 읽고 가공하여 분석 테이블로 저장.
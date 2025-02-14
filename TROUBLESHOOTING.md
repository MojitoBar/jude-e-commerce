## Airflow 및 관련 시스템 문제 해결 가이드

### Docker Compose 설정 관련 문제

#### 문제 1: `docker-compose.yml` 파일 설정 오류

*   **상세 내용**: `docker-compose.yml` 파일 내 설정이 최신 Airflow 버전 요구사항과 맞지 않아 발생하는 문제.
    *   `version` 속성 사용으로 인한 경고 발생 (deprecated).
    *   환경 변수 `AIRFLOW__CORE__SQL_ALCHEMY_CONN` 사용 (대신 `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` 사용해야 함).
*   **해결 방법**:
    1.  `docker-compose.yml` 파일 수정:
        *   `version` 속성 제거 (필요 X).
        *   환경 변수 이름을 최신 방식(`AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`)으로 변경.

#### 문제 2: PostgreSQL 데이터베이스 초기화 실패

*   **상세 내용**: PostgreSQL 데이터 디렉터리가 이미 초기화되어 새로운 데이터베이스 생성 건너뜀. Airflow 연결 시 필요한 `airflow` 데이터베이스가 존재하지 않아 연결 실패.
*   **해결 방법**:
    1.  PostgreSQL 컨테이너 접속 후 `airflow` 데이터베이스 수동 생성:

        ```sql
        CREATE DATABASE airflow;
        ```
    2.  기존 데이터 삭제 후 재초기화:

        ```bash
        sudo rm -rf ./db_data
        docker-compose up -d
        ```

#### 문제 3: Airflow 컨테이너 실행 시 명령 누락

*   **상세 내용**: Airflow 컨테이너 실행 시 필요한 기본 명령(`webserver`, `scheduler` 등) 누락으로 컨테이너가 즉시 종료됨. 로그에 `the following arguments are required: GROUP_OR_COMMAND` 에러 발생.
*   **해결 방법**:
    1.  `docker-compose.yml` 파일에 `command` 추가하여 Airflow 기본 명령 설정:

        ```yaml
        command: >
          bash -c "airflow db init &&
          airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com &&
          airflow webserver"
        ```

#### 문제 4: Fernet Key 설정 오류

*   **상세 내용**: `AIRFLOW__CORE__FERNET_KEY` 환경 변수에 유효하지 않은 값 설정 시, Airflow가 연결 정보를 복호화하지 못함. `ValueError: Fernet key must be 32 url-safe base64-encoded bytes` 에러 발생.
*   **해결 방법**:
    1.  Python을 사용하여 올바른 Fernet Key 생성:

        ```bash
        python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
        ```
    2.  생성된 Fernet Key를 `docker-compose.yml` 파일에 적용.

        ```yaml
        AIRFLOW__CORE__FERNET_KEY: <생성된 키>
        ```

### 데이터 관련 문제

#### 문제 1: CSV 파일 인코딩 문제

*   **상세 내용**: CSV 파일의 인코딩 문제로 인한 `UnicodeDecodeError` 발생.
*   **해결 방법**:
    1.  파일 인코딩을 `ISO-8859-1`로 설정하여 데이터 로드 시 문제 해결.
    2.  `chardet` 라이브러리를 사용하여 인코딩 자동 감지 후 적용.

        ```python
        import chardet

        def detect_encoding(file_path):
            with open(file_path, 'rb') as file:
                raw_data = file.read()
            result = chardet.detect(raw_data)
            return result['encoding']
        ```

#### 문제 2: 데이터베이스 외래 키 제약 조건 문제

*   **상세 내용**: 외래 키 제약 조건 미충족으로 데이터베이스에 데이터 삽입 실패. `order_items` 테이블이 `orders` 테이블의 `invoice_no`를 참조하지 못하는 경우 발생.
*   **해결 방법**:
    1.  데이터 로드 순서 조정: `orders` 테이블에 먼저 데이터 삽입.
    2.  데이터 검증: 누락된 외래 키 값 확인 및 수정.

#### 문제 3: 데이터베이스 중복 데이터 삽입 오류

*   **상세 내용**: 테이블에 이미 존재하는 데이터를 중복으로 삽입하려 할 때 `UniqueViolation` 오류 발생.
*   **해결 방법**:
    1.  중복 데이터 제거.
    2.  `if_exists='replace'` 옵션 사용.

#### 문제 4: 데이터베이스 테이블 컬럼 불일치

*   **상세 내용**: 테이블 컬럼의 대소문자 불일치 등으로 쿼리 실행 시 오류 발생 (`column "Country" of relation "sales" does not exist`).
*   **해결 방법**:
    1.  컬럼명을 소문자로 통일 (`df.rename(columns={'Country': 'country'})`).
    2.  테이블 스키마 수정 (`CREATE TABLE IF NOT EXISTS sales ( ... country VARCHAR(100), ... );`).

#### 문제 5: Customer Summary 데이터 적재 실패

*   **상세 내용**: `customer_summary` 테이블에 데이터가 저장되지 않는 문제 발생.
*   **해결 방법**:
    1.  `customer_id` 데이터 타입 변환 및 null 처리:

        ```python
        df['customer_id'] = pd.to_numeric(df['customer_id'], errors='coerce').astype('Int64')
        valid_customers = df[df['customer_id'].notna()]
        ```

### Airflow 설정 및 DAG 관련 문제

#### 문제 1: DAG 파일 인식 실패

*   **상세 내용**: Airflow 컨테이너에서 `DAGS_FOLDER` 설정이 올바르지 않아 DAG 파일을 찾지 못하는 문제. DAG 파일이 Airflow UI에 표시되지 않음.
*   **해결 방법**:
    1.  `DAGS_FOLDER` 설정 확인 및 수정.
    2.  DAG 파일이 올바른 위치에 있는지 확인.

#### 문제 2: Python 모듈 경로 문제

*   **상세 내용**: DAG 파일에서 다른 디렉터리의 Python 파일을 import하는 과정에서 `ModuleNotFoundError` 발생.
*   **해결 방법**:
    1.  `sys.path.append`를 사용하여 Python 경로를 동적으로 추가.

        ```python
        import sys
        sys.path.append('/path/to/your/module')
        ```

#### 문제 3: Airflow 스케줄러 문제

*   **상세 내용**: Airflow 스케줄러가 실행되지 않아 DAG 실행이 안 되는 문제 발생.
*   **해결 방법**:
    1.  스케줄러 컨테이너 로그 확인 후 오류 수정.
    2.  스케줄러와 웹 서버 컨테이너를 분리하여 실행하도록 설정.

### ETL 파이프라인 문제

#### 문제 1: SQL 쿼리 오류

*   **상세 내용**: SQL 쿼리 오타 또는 문법 오류로 인해 `psycopg2.errors.SyntaxError` 발생.
*   **해결 방법**:
    1.  쿼리 구문 재검토 및 수정 (테이블 이름, 컬럼 이름 등).

#### 문제 2: PostgreSQL 연결 오류

*   **상세 내용**: Airflow 컨테이너에서 PostgreSQL 데이터베이스 연결 실패.
*   **해결 방법**:
    1.  `localhost` 대신 `postgres`로 데이터베이스 연결 시도.
    2.  `DATABASE_URL` 수정 및 환경 변수 설정 통일.

        ```python
        DATABASE_URL = "postgresql://airflow:airflow@postgres:5432/ecommerce"
        ```

#### 문제 3: ETL 파이프라인 코드 문제

*   **상세 내용**: 데이터 정제 단계에서 결측값 처리, 중복 제거 누락 또는 잘못된 데이터 변환 로직으로 인한 데이터 품질 문제.
*   **해결 방법**:
    1.  데이터 정제 단계에서 결측값 처리 및 중복 제거 로직 추가.
    2.  데이터 변환 로직 검토 및 수정.

### 기타 문제

#### 문제 1: 포트 충돌

*   **상세 내용**: 특정 포트가 이미 사용 중이어서 서비스 실행이 불가능한 경우.
*   **해결 방법**:
    1.  충돌하는 포트 확인 후, 다른 포트로 변경. Metabase 포트 변경 예시:

        ```yaml
        ports:
          - "3001:3000"
        ```

#### 문제 2: ARM64 아키텍처 호환성 문제

*   **상세 내용**: Docker 이미지와 호스트 시스템의 아키텍처가 호환되지 않는 경우.
*   **해결 방법**:
    1.  `docker-compose.yml` 파일에 플랫폼 지정:

        ```yaml
        platform: linux/arm64
        ```

#### 문제 3: Metabase 설정 오류

*   **상세 내용**: Metabase 데이터베이스 연결 설정 오류 (`Unable to parse URL jdbc:postgresql://http://localhost:5432/ecommerce`).
*   **해결 방법**:
    1.  URL 형식 수정: `http://` 제거 후 올바른 형식(`jdbc:postgresql://postgres:5432/ecommerce`)으로 변경.

#### 문제 4: Docker 컨테이너 권한 문제

*   **상세 내용**: 컨테이너 내부에서 파일 권한 변경이 불가능한 경우.
*   **해결 방법**:
    1.  `docker-compose.yaml`에서 사용자 설정:

        ```yaml
        user: "${AIRFLOW_UID:-50000}:0"
        ```
    2.  호스트 시스템에서 권한 설정:

        ```bash
        sudo chown -R 50000:0 ./data
        ```

#### 문제 5: 데이터 파일 접근 권한 오류

*   **상세 내용**: Docker 컨테이너에서 CSV 파일 접근 권한 오류 (`FileNotFoundError: [Errno 2] No such file or directory: '/opt/airflow/data/data.csv'`).
*   **해결 방법**:
    1.  `docker-compose.yaml`에 볼륨 마운트 추가:

        ```yaml
        volumes:
          - ./data:/opt/airflow/data
        ```
    2.  파일 권한 설정:

        ```bash
        chmod -R 755 ./data
        chown -R 50000:0 ./data
        ```

#### 문제 6: 데이터베이스 연결 인증 오류

*   **상세 내용**: PostgreSQL 연결 시 인증 실패 (`FATAL: password authentication failed for user "postgres"`).
*   **해결 방법**:
    1.  `DATABASE_URL` 수정:

        ```python
        DATABASE_URL = "postgresql://airflow:airflow@postgres:5432/ecommerce"
        ```
    2.  환경 변수 설정 통일:

        ```
        AIRFLOW_UID=50000
        ```

#### 문제 7: Metabase 시각화 제한

*   **상세 내용**: Metabase에서 히트맵 등 일부 시각화 옵션이 제공되지 않는 경우.
*   **해결 방법**:
    1.  대체 시각화 방법 사용 (스택 바 차트 등).
    2.  시간대를 그룹화하여 시각화 (예: 4시간 단위로 그룹화).

        ```sql
        CASE
          WHEN EXTRACT(HOUR FROM date) BETWEEN 0 AND 3 THEN '00:00-03:59'
          ...
        END as time_range
        ```
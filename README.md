# 🛍 E-Commerce 데이터 파이프라인 구축 프로젝트

## 💡 프로젝트 소개

전자상거래 데이터를 수집하고 분석하여 비즈니스 인사이트를 도출하는 데이터 파이프라인을 구축했습니다.
매출, 고객, 상품 데이터를 자동으로 처리하고 시각화하여 데이터 기반 의사결정을 지원합니다.

> "데이터를 통해 고객의 행동을 이해하고, 비즈니스 가치를 창출하는 것이 목표입니다."

## 🔧 기술 스택

### Data Pipeline
- **Apache Airflow**: 워크플로우 관리 및 스케줄링
- **Python & Pandas**: 데이터 처리 및 분석
- **SQLAlchemy**: ORM을 통한 데이터베이스 연동

### Infrastructure
- **Docker & Docker Compose**: 컨테이너 기반 인프라 구축
- **PostgreSQL**: 데이터 저장 및 관리
- **Metabase**: 데이터 시각화 및 대시보드

## 🎯 프로젝트 구조

### **시스템 아키텍처**

```
[Data Source] → [Airflow ETL] → [PostgreSQL] → [Metabase]
     ↓              ↓              ↓              ↓
   Raw Data     Data Pipeline    Storage     Visualization
```

### ETL 파이프라인
- 일일 배치 작업으로 데이터 처리
- 데이터 정제 및 집계
- 테이블:
  - enriched_data: 상세 거래 데이터
  - summarized_data: 고객별 요약 데이터

### 데이터 분석
- 고객 세그먼테이션
- 매출 트렌드 분석
- 상품 카테고리 분석
- 구매 패턴 분석

## 📊 분석 결과

![E-Commerce 데이터 분석 대시보드](https://github.com/user-attachments/assets/b43a4aa5-14b0-4ff6-99f8-bf9d5986ca2d)

### 고객 분석
- 고객 세그먼트별 분포 (VIP, Gold, Silver, Regular)
- 일평균 주문량: 60-90건
- 주요 구매 시간대: 오전 10시 ~ 오후 2시

### 매출 분석
- 연말(10-11월) 매출 증가 추세
- 평일 vs 주말 주문 패턴 차이
- 계절성 상품의 매출 기여도

## 🌟 프로젝트 특징

### 1. 자동화된 데이터 파이프라인
- Airflow DAG를 통한 주기적 ETL 작업 실행
- orders, order_items, products, customers 테이블 데이터 통합
- enriched_data 테이블 생성 및 고객 세그먼트 분석
- try-except를 통한 기본적인 에러 처리

### 2. 컨테이너 기반 인프라
- Docker를 활용한 서비스 격리
- 환경 설정 표준화
- 배포 프로세스 단순화

### 3. 데이터 시각화
- Metabase 대시보드 구축
- 실시간 데이터 모니터링
- 직관적인 데이터 탐색 환경

## 🚀 주요 성과

- Airflow DAG를 통한 ETL 파이프라인 자동화
- Docker 기반의 안정적인 실행 환경 구성
- PostgreSQL과 Metabase를 활용한 분석 환경 구축

## 🎓 학습 내용

이 프로젝트를 통해
- ETL 파이프라인 설계 및 구현 경험
- Docker를 활용한 컨테이너 기반 개발
- 데이터베이스 모델링 및 쿼리 최적화
- 데이터 시각화 및 대시보드 구축

기술을 실전에서 적용해볼 수 있었습니다.

## 📝 회고

이 프로젝트를 통해 데이터 엔지니어링의 전체 프로세스를 경험할 수 있었습니다. 특히 Docker와 Airflow를 활용한 데이터 파이프라인 구축 과정에서 많은 것을 배웠습니다. 앞으로도 데이터 품질과 시스템 안정성을 고려한 데이터 파이프라인 구축에 대해 더 깊이 공부하고 싶습니다.

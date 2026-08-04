### Mini MES

- python, postgresql, streamlit

- Database 구조
    - product
    - material
    - production
    - product_lot
    - production_material

- 현재 구현 상태
    - 생산 제품 조회, 제품 상태 수정, 제품 추가
    - 원재료 조회, 원재료 추가 및 삭제
    - 생산 관리: 생산 조회, 생산 원재료 및 LOT 등록, 생산 등록

- 환경변수 설정
```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

- 실행
```
1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate

2. 패키지 설치
pip install -r requirements.txt
// 또는 pip install psycopg[binary] python-dotenv streamlit

3. 실행
streamlit run app.py
```

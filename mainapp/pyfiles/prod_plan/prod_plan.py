### prod_plan 데이터베이스 생성하는 코드
# - 최초 1번만 실행

### 라이브러리
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### 정규화 패키지
from sklearn.preprocessing import StandardScaler

### 모델 관련 패키지
import tensorflow as tf
tf.random.set_seed(42)
from tensorflow.keras.models import load_model
from os import listdir
from sklearn.metrics import mean_absolute_error

### mysql 패키지
import mysql.connector
from sqlalchemy import create_engine

def getData(part) :
    ### 데이터 불러오기
    data = pd.read_csv("mainapp/pyfiles/prod_plan/part_data/part{}_data.csv".format(part))
    
    data.columns= ['part_no', 'plan_0day', 'plan_1day', 'plan_2day', 'plan_3day', 'plan_4day', 'plan_5day', 
                         'plan_6day', 'plan_7day', 'plan_8day', 'plan_9day', 'plan_10day',
                         'plan_11day', 'plan_12day', 'plan_date']
    ### 안쓰는 컬럼 제거
    data = data[['part_no', 'plan_0day', 'plan_1day', 'plan_2day', 'plan_3day', 'plan_4day', 'plan_5day', 
                     'plan_6day', 'plan_7day', 'plan_8day', 'plan_9day', 'plan_date']]

    ### 날짜에서 시간 제거
    for i in range(len(data[['plan_date']])) :
        data.loc[i,'plan_date'] = data.loc[i,'plan_date'][:10]
    
    return data

def getCols(data, num) :
    ### 주요 변수 선택 및 저장
    data = data.iloc[:, [1, num+1, num+2, num+3]].reset_index(drop=True)
    return data

### 독립변수와 종속변수 만드는 함수
def to_timeseries_data(data, lookback, delay):
    # data는 원본 tabular 데이터
    # lookback: 입력으로 사용하기 위해 거슬러 올라갈 시간단위의 개수=3일전
    # delay: target으로 사용할 미래의 시점=3일후
    
    output_len = len(data)-(lookback+delay)+1 # N=total_length-(3+3)+1
    n_feature = data.shape[-1] # =4
    
    inputs = np.zeros((output_len, lookback, n_feature)) # (N,3,4)
    targets = np.zeros((output_len,)) # (N,)

    for i in range(output_len):
        inputs[i] = data.iloc[i:i+lookback, :]
        targets[i] = data.iloc[i+lookback+delay-1, 0]
        
    return inputs, targets

def getSplitData(data, num) :
    ### 사용자 정의 함수 적용
    X_part, y_part = to_timeseries_data(data, 3, num)
    
    ### 데이터 정규화
    Xscaler_part = StandardScaler()
    X_part = Xscaler_part.fit_transform(X_part.reshape(-1, X_part.shape[-1])).reshape(X_part.shape)

    yscaler_part = StandardScaler()
    y_part = yscaler_part.fit_transform(y_part.reshape(-1,1))
    
    return Xscaler_part, X_part, yscaler_part, y_part

def getModel(part, num, Xscaler_part, X_part, yscaler_part, y_part) :
    ### 모델 불러오기
    best_model = load_model('mainapp/pyfiles/prod_plan/best_model/part{}_d{}_lstm.h5'.format(part, num))
      
    ### 테스트 데이터로 예측하기
    y_pred_part = best_model.predict(X_part)
    
    ### 예측값을 기존 값 범위로 역변환
    y_pred_part_inv = yscaler_part.inverse_transform(y_pred_part)
    
    return y_pred_part_inv

# ---------------------------------------------------------------------------------------------------------
# 코드 실행


# MySQL 연결 정보 설정
db_config = {
    'user': 'root',        # MySQL 사용자 이름
    'password': '0000',    # MySQL 비밀번호
    'host': 'localhost',   # MySQL 호스트 주소
    'database': 'isix',    # MySQL 데이터베이스 이름
    'port': 3306,          # MySQL 포트 번호
}

# MySQL 서버에 연결
conn = mysql.connector.connect(**db_config)

# 커서 생성
cursor = conn.cursor()

# 테이블 존재 여부 확인 쿼리 실행
find_query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'prod_plan';"
cursor.execute(find_query)

# 생성/삭제 쿼리 지정
create_query = """CREATE TABLE prod_plan (
                    part_no VARCHAR(15),
                    plan_date VARCHAR(15),
                    plan_0day FLOAT,
                    plan_1day FLOAT,
                    plan_2day FLOAT,
                    plan_3day FLOAT,
                    plan_4day FLOAT,
                    plan_5day FLOAT,
                    plan_6day FLOAT,
                    plan_7day FLOAT
                );"""

delete_query = "DELETE FROM prod_plan;"

if cursor.fetchone():
    # 테이블 이미 존재할 경우 데이터 삭제
    print("테이블 이미 존재함")
    cursor.execute(delete_query)
    conn.commit()
else:
    # 테이블 없을 경우 테이블 생성
    print("테이블 존재하지 않음")
    cursor.execute(create_query)
    print("테이블 생성 완료")


# 파트별 데이터 저장 시작
for part in [6, 15, 16, 29, 94] :
    # 데이터 불러오기
    part_data = getData(part)

    # D+1~7 예측하기
    list_pred = []
    for num in range(1,8,1) :
        day_data = getCols(part_data, num)
        Xscaler_part, X_part, yscaler_part, y_part = getSplitData(day_data, num)
        y_pred_part_inv = getModel(part, num, Xscaler_part, X_part, yscaler_part, y_part)
        list_pred.append([y[0] for y in y_pred_part_inv])

    # 파트별 데이터프레임 생성
    part_df = pd.DataFrame(columns=['part_no', 'plan_date', 'plan_0day', 'plan_1day', 'plan_2day', 'plan_3day', 'plan_4day', 'plan_5day', 
                                     'plan_6day', 'plan_7day'])
    part_df['plan_date'] = list(part_data['plan_date'])[:30]
    part_df['plan_0day'] = list(part_data['plan_0day'])[:30]
    for i in range(0,7,1) :
        part_df['plan_{}day'.format(i+1)] = list_pred[i][:30]
    part_df['part_no'] = 'part{}'.format(part)
    
    # SQLAlchemy 엔진 생성
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # mysql에 넣기
    part_df.to_sql(name="prod_plan", con=engine, if_exists='append', index=False)
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import pickle
from datetime import datetime
from sqlalchemy import create_engine
import mysql.connector
import time

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

# 경고 메시지 무시
import warnings
warnings.filterwarnings(action='ignore')

# # Pass or Fail 모델 불러오기
# with open("./tem_model/mm.pkl", 'rb') as model_file:
#     minmax_scaler = pickle.load(model_file)

with open("./tem_model/xgb_mm_heating.pickle", 'rb') as model_file:
    xgb_mm_heating = pickle.load(model_file)

df = pd.read_csv("./data_new/tem_fi.csv").iloc[:, 1:]

data = df.iloc[:, 1:]
mms = MinMaxScaler()
tr_data = pd.DataFrame(mms.fit_transform(data), columns=data.columns)
#xgb_mm_heating.predict(mms.fit_transform(data))

# MySQL 연결 정보 설정
db_config = {
    'user': 'root',        # MySQL 사용자 이름
    'password': '1234',    # MySQL 비밀번호
    'host': 'localhost',   # MySQL 호스트 주소
    'database': 'isix',    # MySQL 데이터베이스 이름
    'port': 3306,          # MySQL 포트 번호
}
# # SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

# MySQL 서버에 연결
conn = mysql.connector.connect(**db_config)

# 커서 생성
cursor = conn.cursor()

# 테이블 존재 여부 확인 쿼리 실행
find_query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'heat_proc'"
cursor.execute(find_query)
'heat_id'
# 생성/삭제 쿼리 지정
create_query = """CREATE TABLE heat_proc (
                    heat_id VARCHAR(30) PRIMARY KEY,
                    heat_date DATE,
                    quench_temp_min FLOAT,
                    saltbelt_temp_max FLOAT,
                    saltfurnace_temp_min FLOAT,
                    heat_pred INT
                );"""

delete_query = "DELETE FROM heat_proc;"

bs = 1
i = 0
max_idx = 20 # max number of = 136 

for i in range(0, max_idx, 1) :
    if i == 0 :
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
    
    try:
        heat_pred = xgb_mm_heating.predict(mms.fit_transform(data.iloc[i:i+1, :]))

        # 컬럼명을 리스트로 감싸서 선택
        df_temp = data.iloc[i:i+bs, [5, 7, 9]].reset_index(drop=True)
        df_temp["heat_pred"] = heat_pred[0]
        df_temp0 = df.iloc[i:i+bs,0:1].reset_index(drop=True)
        df_temp0["heat_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_temp = pd.concat((df_temp0,df_temp),axis=1)
        # 컬럼 이름 변경
        df_temp = df_temp.rename(columns={"배정번호": "heat_id",
                                          "heat_date": "heat_date",
                                          "소입로 온도 1 Zone_min": "quench_temp_min",
                                          "솔트 컨베이어 온도 1 Zone_max": "saltbelt_temp_max", 
                                          "솔트조 온도 1 Zone_min": "saltfurnace_temp_min",
                                         "heat_pred": "heat_pred"})
        df_temp["heat_date"] = pd.to_datetime(df_temp["heat_date"])
        df_temp.to_sql(name="heat_proc", con=engine, if_exists='append', index=False)

        print("{}번째 데이터 삽입 완료".format(str(i)))
        i = i + bs
        time.sleep(3)

    except Exception as e:
        print(e)
        # 예외 처리 코드 추가
        break
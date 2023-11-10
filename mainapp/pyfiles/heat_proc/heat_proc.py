import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import pickle
from datetime import datetime
from sqlalchemy import create_engine
import mysql.connector
import time
import numpy as np

### 여기 추가
from tensorflow.keras.models import load_model



### 열처리 공정 모델
class Heat_Proc_Model :
    def __init__(self) :
        # 실행 플래그 초기화
        self.is_running = False
        
    def stopModel(self):
        # 실행 플래그를 False로 설정하여 코드 중지
        self.is_running = False
        
    def runModel(self) :
        # 실행 플래그를 True로 설정
        self.is_running = True
        
        with open("mainapp/pyfiles/heat_proc/tem_model/xgb_model.pkl", 'rb') as model_file:
            xgb_mm_heating = pickle.load(model_file)

#### 여기 추가함 ####
        nn_model = load_model("mainapp/pyfiles/heat_proc/tem_model/nn_model.h5")

        df = pd.read_csv("mainapp/pyfiles/heat_proc/data_new/tem_fi.csv")

        data = df.iloc[:, 1:]
        mms = MinMaxScaler()
        tr_data = pd.DataFrame(mms.fit_transform(data), columns=data.columns)

        # MySQL 연결 정보 설정
        db_config = {
            'user': 'root',        # MySQL 사용자 이름
            'password': '0000',    # MySQL 비밀번호
            'host': '127.0.0.1',   # MySQL 호스트 주소
            'database': 'isix',    # MySQL 데이터베이스 이름
            'port': 3306          # MySQL 포트 번호
        }
        
        # # SQLAlchemy 엔진 생성
        engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

        # MySQL 서버에 연결
        conn = mysql.connector.connect(**db_config)

        # 커서 생성
        cursor = conn.cursor()

        # 테이블 존재 여부 확인 쿼리 실행
        find_query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'heat_proc';"
        cursor.execute(find_query)
        
        # 생성/삭제 쿼리 지정
        create_query = """CREATE TABLE heat_proc (
                            heat_id VARCHAR(30) PRIMARY KEY,
                            heat_date DATETIME,
                            dry_temp2_min FLOAT,
                            scrubber_min FLOAT,
                            quench_cp_max FLOAT,
                            quench_temp1_min FLOAT,
                            quench_temp2_max FLOAT,
                            quench_temp3_max FLOAT,
                            heat_pred INT
                        );"""

        delete_query = "DELETE FROM heat_proc;"
        
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
            
        bs = 1
        max_idx = 60 # max number of = 136 

        for i in range(10, max_idx, 1) :
            ### 외부에서 강제 종료 시키기
            if self.is_running == False:
                break
            
#####################여기도 수정함###############################
            try:
                heat_pred = xgb_mm_heating.predict(tr_data.iloc[i:i+1, :])
                nn_pred = nn_model.predict(tr_data.iloc[i:i+1, :]).flatten()

                alpha = 0.35
                combined_pred = alpha * heat_pred + (1 - alpha) * nn_pred
                
                final_pred = np.where(combined_pred > 0.5, 1, 0)

                # 컬럼명을 리스트로 감싸서 선택
                df_temp = data.iloc[i:i+bs, [1, 2, 4, 5, 7, 8]].reset_index(drop=True)
                df_temp["heat_pred"] = final_pred[0]
                print(final_pred[0])
                df_temp0 = df.iloc[i:i+bs,0:1].reset_index(drop=True)
                df_temp0["heat_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df_temp = pd.concat((df_temp0,df_temp),axis=1)
                # 컬럼 이름 변경
                df_temp = df_temp.rename(columns={"배정번호": "heat_id",
                                                  "heat_date": "heat_date",
                                                  "건조로 온도 2 Zone_min" : "dry_temp2_min",
                                                  "세정기_min" : "scrubber_min",
                                                  "소입로 CP 값_max" : "quench_cp_max",
                                                  "소입로 온도 1 Zone_min": "quench_temp1_min",
                                                  "소입로 온도 2 Zone_max": "quench_temp2_max",
                                                  "소입로 온도 3 Zone_max": "quench_temp3_max",
                                                  "heat_pred": "heat_pred"})
                df_temp["heat_date"] = pd.to_datetime(df_temp["heat_date"])
                df_temp.to_sql(name="heat_proc", con=engine, if_exists='append', index=False)

                print("{}번째 데이터 삽입 완료".format(str(i)))
                i = i + bs
                time.sleep(2)

            except Exception as result_error:
                print(result_error)
                break
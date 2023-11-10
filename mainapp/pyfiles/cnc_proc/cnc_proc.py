### 라이브러리
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

### 학습 라이브러리
from sklearn.preprocessing import Normalizer, MinMaxScaler
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import pickle

### sql 라이브러리
from sqlalchemy import create_engine
import mysql.connector

import xgboost as xgb

### cnc 공정 모델
class Cnc_Proc_Model :
    def __init__(self) :
        # 실행 플래그 초기화
        self.is_running = False

    def stopModel(self):
        # 실행 플래그를 False로 설정하여 코드 중지
        self.is_running = False
    
    def runModel(self) :
        # 실행 플래그를 True로 설정
        self.is_running = True
        
        # Spindle Speed 모델 불러오기
        spindlespeed_md = tf.keras.models.load_model("mainapp/pyfiles/cnc_proc/cnc_model/spindlespeed.h5")

        # Spindle Load Max 모델 불러오기
        SpindleLoad_max_md = tf.keras.models.load_model("mainapp/pyfiles/cnc_proc/cnc_model/SpindleLoad_max.h5")

        # Servo Current X Mean 모델 불러오기
        ServoCurrent_X_mean = tf.keras.models.load_model("mainapp/pyfiles/cnc_proc/cnc_model/ServoCurrent_X_mean.h5")

        # Pass or Fail 모델 불러오기
        with open("mainapp/pyfiles/cnc_proc/cnc_model/xgb_model.pkl", 'rb') as model_file:
            passorfail_md = pickle.load(model_file)

        # StandardScaler 객체 불러오기
        with open("mainapp/pyfiles/cnc_proc/cnc_model/ss.pkl", 'rb') as model_file:
            ss = pickle.load(model_file)

        # 현재 날짜와 시간 가져오기
        current_datetime = datetime.now()

        # 현재 날짜만 가져오기
        current_date = current_datetime.date()
        one_day_ago = current_datetime + timedelta(days=1)
        two_day_ago = current_datetime + timedelta(days=2)

        # 날짜를 원하는 형식으로 문자열로 변환
        formatted_date = current_date.strftime("%y-%m-%d")
        one_formatted_date = one_day_ago.strftime("%y-%m-%d")
        two_formatted_date = two_day_ago.strftime("%y-%m-%d")
        
        # CSV 파일 불러오기
        csv_file = pd.read_csv("mainapp/pyfiles/cnc_proc/data_new/cnc_sql.csv")

        # 필요한 열 선택
        selected_columns = csv_file.columns
        csv_file = csv_file[selected_columns]

        list_a = []

        for idx in range(0, 337, 1):
            temp = formatted_date + csv_file["cnc_date"][idx][10:]
            datetime_obj = datetime.strptime(temp, "%y-%m-%d %H:%M:%S.%f")
            list_a.append(datetime_obj)

        for idx in range(337, 675, 1):
            temp = one_formatted_date + csv_file["cnc_date"][idx][10:]
            datetime_obj = datetime.strptime(temp, "%y-%m-%d %H:%M:%S.%f")
            list_a.append(datetime_obj)

        for idx in range(675, 1085, 1):
            temp = two_formatted_date + csv_file["cnc_date"][idx][10:]
            datetime_obj = datetime.strptime(temp, "%y-%m-%d %H:%M:%S.%f")
            list_a.append(datetime_obj)

        # 'ReceivedDateTime' 열 업데이트
        csv_file["cnc_date"] = list_a

        # MySQL 연결 정보 설정
        db_config = {
            'user': 'root',        # MySQL 사용자 이름
            'password': '0000',    # MySQL 비밀번호
            'host': '127.0.0.1',   # MySQL 호스트 주소
            'database': 'isix',    # MySQL 데이터베이스 이름
            'port': 3306          # MySQL 포트 번호
        }

        # SQLAlchemy 엔진 생성
        engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

        # MySQL 서버에 연결
        conn = mysql.connector.connect(**db_config)

        # 커서 생성
        cursor = conn.cursor()

        # 테이블 존재 여부 확인 쿼리 실행
        find_query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'cnc_proc';"
        cursor.execute(find_query)

        # 생성/삭제 쿼리 지정
        create_query = """CREATE TABLE cnc_proc (
                            cnc_id VARCHAR(30) PRIMARY KEY,
                            cnc_date DATETIME,
                            SpindleSpeed_max FLOAT,
                            Servocurrent_mean FLOAT,
                            SpindleLoad_max FLOAT,
                            SpindleSpeed_mse FLOAT,
                            SpindleLoad_mse FLOAT,
                            Servocurrent_mse FLOAT,
                            cnc_pred INT
                        );"""

        delete_query = "DELETE FROM cnc_proc;"

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
            
        # block size
        bs = 1

        # 데이터 삽입 코드
        for i in range(0, 50, 1) :
            
            ### 외부에서 강제 종료 시키기
            if self.is_running == False:
                break
            
            try:
                before = np.array(csv_file[["SpindleSpeed_max", "Servocurrent_mean", "SpindleLoad_max"]][i:i+bs])
                ss_tr = ss.transform(before)
                spindlespeed_min_max_scaled = ((csv_file["SpindleSpeed_max"][i:i+bs] - 2211.8949500000003) / (2233.11 - 2211.8949500000003))
                ServoCurrent_X_mean_min_max_scaled = ((csv_file["Servocurrent_mean"][i:i+bs] - 117.88133108108109) / (194.2170588235294 - 117.88133108108109))
                SpindleLoad_max_min_max_scaled = ((csv_file["SpindleLoad_max"][i:i+bs] - 6325.85119) / (33725.8057185 - 6325.85119))
                spindlespeed_mse = tf.losses.mean_squared_error(spindlespeed_min_max_scaled, spindlespeed_md.predict(spindlespeed_min_max_scaled))
                SpindleLoad_mse = tf.losses.mean_squared_error(SpindleLoad_max_min_max_scaled, spindlespeed_md.predict(SpindleLoad_max_min_max_scaled))
                ServoCurrent_mse = tf.losses.mean_squared_error(ServoCurrent_X_mean_min_max_scaled, ServoCurrent_X_mean.predict(ServoCurrent_X_mean_min_max_scaled))
                
                df = pd.DataFrame({'SpindleSpeed_mse': spindlespeed_mse,
                                'SpindleLoad_mse': SpindleLoad_mse,
                                'Servocurrent_mse': ServoCurrent_mse,
                                'cnc_pred': passorfail_md.predict(ss_tr)})
                
                df_temp = pd.concat((csv_file[["SpindleSpeed_max", "Servocurrent_mean", "SpindleLoad_max"]][i:i+bs].reset_index(drop=True), df), axis=1)
                
                a = datetime.now()
                
                # 날짜와 시간을 문자열로 변환
                a_str = a.strftime("%y-%m-%d %H:%M:%S.%f")
                
                # 문자열을 다시 datetime 객체로 변환
                a_parsed = datetime.strptime(a_str, "%y-%m-%d %H:%M:%S.%f")
                
                df_2 = pd.DataFrame([[csv_file["cnc_id"][i],a_parsed]],columns=["cnc_id","cnc_date"])

                df_temp = pd.concat((df_2, df_temp), axis=1)

                
                df_temp.to_sql(name="cnc_proc", con=engine, if_exists='append', index=False)
                
                print("{}번째 데이터 삽입 완료".format(str(i)))
                i = i + bs
                time.sleep(1)
            
            except Exception as result_error:
                print(result_error)
                break
        
        

                

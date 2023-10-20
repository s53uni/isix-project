import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import mysql.connector
import time
import matplotlib.pyplot as plt
import numpy as np
import xgboost
from sklearn.preprocessing import MinMaxScaler
import pickle


### 주조 공정 모델
class Cast_Proc_Model :
    def __init__(self) :
        # 실행 플래그 초기화
        self.is_running = False

    def stopModel(self):
        # 실행 플래그를 False로 설정하여 코드 중지
        self.is_running = False
        
    def runModel(self) :
        # 실행 플래그를 True로 설정
        self.is_running = True

        with open("mainapp/pyfiles/cast_proc/pkl/xgb_casting.pickle", 'rb') as model_file:
            xgb_mm_casting = pickle.load(model_file)
        
        df = pd.read_csv("mainapp/pyfiles/cast_proc/data_new/cast_fi.csv")
        
        data = df.iloc[:, 2:]
        
        mms = MinMaxScaler()
        tr_data = mms.fit_transform(data)  
       
        
        # 원래 컬럼 이름과 새로운 컬럼 이름을 매핑하는 딕셔너리 생성
        column_mapping = {
            'datetime': 'cast_date',
            'lower_mold_temp2': 'lower_mold_temp',
            'upper_mold_temp1': 'upper_mold_temp',
            'sleeve_temperature': 'sleeve_temp'
            # 다른 컬럼도 필요한 만큼 추가 가능
        }
        
        # CSV 파일 불러오기
        csv_file = pd.read_csv('mainapp/pyfiles/cast_proc/data_new/cast_fi.csv')
        
        # 컬럼 이름 변경
        csv_file.rename(columns=column_mapping, inplace=True)
        
        # 필요한 열 선택
        selected_columns = ["cast_id", "cast_date", "cast_pressure", "lower_mold_temp", "upper_mold_temp", "sleeve_temp"]
        csv_file = csv_file[selected_columns]
        
        # 일별로 데이터를 나누기 위한 딕셔너리
        daily_data = {}
        
        list_temp = []
        
        # 데이터를 날자별로 분리
        for item in csv_file['cast_date']:
            # 날짜 형식으로 변환
            date_obj = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
        
            # 날짜만 추출
            date = date_obj.date()
        
            # 날짜별로 리스트 생성 또는 추가
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)
        
        # 결과 출력
        for date, items in daily_data.items():
            for item in items:
                list_temp.append(item)
        
        list_time = []
        
        # 더할 날 수
        days_to_add = 1654
        
        # 결과를 저장할 리스트
        new_date_time_list = []
        
        # 각 날짜 및 시간에 대해 1655일을 더한 값을 계산하여 저장
        for date_time_str in list_temp:
            # 문자열을 datetime 객체로 변환
            date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        
            # 날짜에 1655일을 더함
            new_date_time_obj = date_time_obj + timedelta(days=days_to_add)
        
            # 결과를 리스트에 추가
            new_date_time_list.append(new_date_time_obj)
        
        # 결과 출력
        for new_date_time_obj in new_date_time_list:
            new_date_time_str = new_date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
            list_time.append(new_date_time_str)
        
        # 열 업데이트
        csv_file["cast_date"] = list_time
        
        csv_file['cast_date'] = pd.to_datetime(csv_file['cast_date'], format="%Y-%m-%d %H:%M:%S")
        
        # MySQL 연결 정보 설정
        db_config = {
            'user': 'isix',        # MySQL 사용자 이름
            'password': 'dnqnsxn1',    # MySQL 비밀번호
            'host': '43.202.171.200',   # MySQL 호스트 주소
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
        find_query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'cast_proc';"
        cursor.execute(find_query)
        
        # 생성/삭제 쿼리 지정
        create_query = """CREATE TABLE cast_proc (
                            cast_id VARCHAR(30) PRIMARY KEY,
                            cast_date DATETIME,
                            cast_pressure FLOAT,
                            lower_mold_temp FLOAT,
                            upper_mold_temp FLOAT,
                            sleeve_temp FLOAT,
                            cast_pred INT
                        );"""
        
        delete_query = "DELETE FROM cast_proc;"
        
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
        max_idx = 15 # max index = 92014
        
        for i in range(0, max_idx, 1) : 
        
            ### 외부에서 강제 종료 시키기
            if self.is_running == False:
                break
        
            try:         
                a = datetime.now()
                # 날짜와 시간을 문자열로 변환
                a_str = a.strftime("%y-%m-%d %H:%M:%S.%f")
            
                # 문자열을 다시 datetime 객체로 변환
                a_parsed = datetime.strptime(a_str, "%y-%m-%d %H:%M:%S.%f")
            
                df_2 = pd.DataFrame([[csv_file["cast_id"][i],a_parsed]],columns=["cast_id","cast_date"])
            
                cast_pred = xgb_mm_casting.predict(mms.fit_transform(data.iloc[i:i+1]))
        
                df_temp = data.iloc[i:i+bs, :].reset_index(drop=True)
                df_temp["cast_pred"] = xgb_mm_casting.predict(np.array([tr_data[i]]))
                df_temp = pd.concat((df_2, df_temp), axis=1)
                
                df_temp.to_sql(name="cast_proc", con=engine, if_exists='append', index=False)
        
                print("{}번째 데이터 삽입 완료".format(str(i)))
                i = i + bs
                time.sleep(2)
        
            except Exception as result_error:
                print(result_error)
                break